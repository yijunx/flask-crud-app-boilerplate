from contextlib import contextmanager
from datetime import datetime, timezone
from app.db.database import SessionLocal
from app.schemas.item import Item, ItemCreate, ItemWithPaging, ItemPatch, ItemsUserRight
from app.schemas.pagination import QueryPagination
from app.schemas.user import User, UsersItemRight
from app.schemas.casbin_rule import CasbinPolicy
import app.repo.item as itemRepo
import app.repo.casbin_rule as casbinruleRepo
from app.casbin.rbac import create_casbin_enforcer
from app.casbin.role_definition import (
    SpecificResourceRightsEnum,
    SpecificResourceActionsEnum,
    PolicyTypeEnum,
)
from app.service.util import get_resource_id, get_item_id
from app.config.app_config import conf


casbin_enforcer = create_casbin_enforcer()


@contextmanager
def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        # can roll other things back here
        raise
    finally:
        session.close()


def create_item(item_create: ItemCreate, user: User) -> Item:
    # here it means every body can post
    with get_db() as db:
        db_item = itemRepo.create(db=db, item_create=item_create, creator=user)
        item = Item.from_orm(db_item)
        casbin_policy = CasbinPolicy(
            ptype=PolicyTypeEnum.p,
            v0=user.id,
            v1=item.id,
            v2=SpecificResourceRightsEnum.own,
            created_at=datetime.now(timezone.utc),
            created_by=user.id,
        )
        casbinruleRepo.create(db=db, casbin_policy=casbin_policy)
    return item


def get_item(item_id: str, user: User) -> Item:
    if casbin_enforcer.enforce(user.id, item_id, SpecificResourceActionsEnum.get):
        with get_db() as db:
            db_item = itemRepo.get(db=db, item_id=item_id)
            item = Item.from_orm(db_item)
        return item
    else:
        # well here need to raise something
        return {"no access": "bro"}


def list_items(query_pagination: QueryPagination, user: User) -> ItemWithPaging:
    with get_db() as db:
        is_admin = any(
            x
            for x in casbinruleRepo.get_role_ids_of_user(db=db, user_id=user.id)
            if x.v1 == conf.ADMIN_ROLE_ID
        )
        if not is_admin:
            policies, _ = casbinruleRepo.get_all_policies_given_user(
                db=db,
                users_item_right=UsersItemRight(user_id=user.id),
                query_pagination=QueryPagination(size=-1),
                is_admin=False,
            )
            item_ids = [p.v1 for p in policies]
            db_items, paging = itemRepo.get_all(
                db=db, query_pagination=query_pagination, item_ids=item_ids
            )
        else:
            db_items, paging = itemRepo.get_all(
                db=db, query_pagination=query_pagination
            )
        items = [Item.from_orm(x) for x in db_items]
    return ItemWithPaging(data=items, paging=paging)


def delete_item(item_id: str, user: User) -> None:
    if casbin_enforcer.enforce(user.id, item_id, SpecificResourceActionsEnum.delete):
        with get_db() as db:
            itemRepo.delete(db=db, item_id=item_id)
            casbinruleRepo.delete_resource(
                db=db, items_user_right=ItemsUserRight(resource_id=item_id)
            )
    else:
        return {"no access": "bro"}


def share_item(item_id: str, user: User) -> None:
    if casbin_enforcer.enforce(user.id, item_id, SpecificResourceActionsEnum.share):
        with get_db() as db:
            itemRepo.delete(db=db, item_id=item_id)
            casbinruleRepo.delete_resource(
                db=db, items_user_right=ItemsUserRight(resource_id=item_id)
            )
    else:
        return {"no access": "bro"}
    return


def clean_up() -> None:
    with get_db() as db:
        itemRepo.delete_all(db=db)
