from contextlib import contextmanager

from casbin import enforcer
from app.db.database import SessionLocal
from app.schemas.item import Item, ItemCreate, ItemWithPagination, ItemPatch
from app.schemas.pagination import QueryPagination
from app.schemas.user import User
import app.repo.item as itemRepo
from app.casbin.rbac import create_casbin_enforcer
from app.casbin.role_definition import SpecificResourceRightsEnum, SpecificResourceActionsEnum


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

        # the owner can do anything to the resource
        casbin_enforcer.add_policy(
            user.id, item.id, SpecificResourceRightsEnum.own.name
        )
    return item


def get_item(item_id: str, user: User) -> Item:
    if casbin_enforcer.enforce(user.id, item_id, SpecificResourceActionsEnum.get.name):
        with get_db() as db:
            db_item = itemRepo.get(db=db, item_id=item_id)
            item = Item.from_orm(db_item)
        return item
    else:
        return {"no access": "bro"}


def list_items(query_pagination: QueryPagination) -> ItemWithPagination:
    with get_db() as db:
        db_items, paging = itemRepo.get_all(db=db, query_pagination=query_pagination)
        items = [Item.from_orm(x) for x in db_items]
    return ItemWithPagination(data=items, paging=paging)


def delete_item(item_id: str, user: User) -> None:
    if casbin_enforcer.enforce(user.id, item_id, SpecificResourceActionsEnum.get.name):
        with get_db() as db:
            itemRepo.delete(db=db, item_id=item_id)
        
    else:
        return {"no access": "bro"}


def clean_up() -> None:
    with get_db() as db:
        itemRepo.delete_all(db=db)
