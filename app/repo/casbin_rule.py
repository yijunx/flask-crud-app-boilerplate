from typing import List, Tuple
from casbin_sqlalchemy_adapter.adapter import CasbinRule
from sqlalchemy.sql.expression import and_
from app.schemas.pagination import QueryPagination, ResponsePagination
from app.db.models import models
from sqlalchemy.orm import Session
from app.casbin.role_definition import SpecificResourceRightsEnum
from app.schemas.casbin_rule import CasbinPolicy, PolicyTypeEnum
from app.schemas.user import UsersItemRight
from app.schemas.item import ItemsUserRight
from app.repo.util import translate_query_pagination
from sqlalchemy.exc import IntegrityError
from app.exceptions.casbin_rule import PolicyDoesNotExist, PolicyIsAlreadyThere


def create(db: Session, casbin_policy: CasbinPolicy) -> models.Item:
    """Create both g type and p type here"""
    db_item = models.CasbinRule(
        ptype=casbin_policy.ptype,
        v0=casbin_policy.v0,
        v1=casbin_policy.v1,
        v2=casbin_policy.v2,
        v3=casbin_policy.v3,
        v4=casbin_policy.v4,
        v5=casbin_policy.v5,
        created_at=casbin_policy.created_at,
        created_by=casbin_policy.created_by,
    )
    db.add(db_item)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise PolicyIsAlreadyThere(casbin_policy=casbin_policy)
    return db_item


def get_all_policies_given_user(
    db: Session,
    users_item_right: UsersItemRight,
    query_pagination: QueryPagination,
    resource_name: str = None,
    is_admin: bool = False,
) -> Tuple[List[models.CasbinRule], ResponsePagination]:
    """
    Given a user (user_id + optional right),
    return what resource he/she operator at what right
    """
    # also need to filter by the resource id (need to include the resource name)
    # because there can be 2 kind of resources...

    query = db.query(models.CasbinRule).filter(
        models.CasbinRule.ptype == PolicyTypeEnum.p
    )
    if resource_name:
        query = query.filter(models.CasbinRule.v1.ilike(f"%{resource_name}%"))

    if is_admin:
        # admin in fact owns everything
        query = query.filter(models.CasbinRule.v2 == SpecificResourceRightsEnum.own)
    else:
        if users_item_right.right:
            # for a user only wants to pull his/her own/edit/view
            query = query.filter(models.CasbinRule.v2 == users_item_right.right)
        # match the user id
        query = query.filter(models.CasbinRule.v0 == users_item_right.user_id)

    total = query.count()
    limit, offset, paging = translate_query_pagination(
        query_pagination=query_pagination, total=total
    )
    db_items = (
        query.order_by(models.CasbinRule.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    paging.page_size = len(db_items)
    return db_items, paging


def get_all_policies_given_item(
    db: Session,
    items_user_right: ItemsUserRight,
    query_pagination: QueryPagination,  # yes we need to make it paginated
) -> Tuple[List[models.CasbinRule], ResponsePagination]:
    """
    Given an item (resource_id + optional right),
    return who has what rights (user_id + optional right)
    """
    query = db.query(models.CasbinRule).filter(
        and_(
            models.CasbinRule.v1 == items_user_right.resource_id,
            models.CasbinRule.ptype == PolicyTypeEnum.p,
        )
    )
    total = query.count()
    limit, offset, paging = translate_query_pagination(
        query_pagination=query_pagination, total=total
    )
    db_items = (
        query.order_by(models.CasbinRule.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    paging.page_size = len(db_items)
    return db_items, paging


def get_role_ids_of_user(db: Session, user_id: str):
    db_items = (
        db.query(models.CasbinRule)
        .filter(
            and_(
                models.CasbinRule.ptype == PolicyTypeEnum.g,
                models.CasbinRule.v0 == user_id,
            )
        )
        .all()
    )
    return db_items


def delete_policies_by_resource_id(
    db: Session, items_user_right: ItemsUserRight
) -> None:
    """used when deleting item"""
    query = db.query(models.CasbinRule).filter(
        and_(
            models.CasbinRule.ptype == PolicyTypeEnum.p,
            models.CasbinRule.v1 == items_user_right.resource_id,
        )
    )
    if items_user_right.right:
        print("got right here")
        query.filter(models.CasbinRule.v2 == items_user_right.right)
    query.delete()
    # db.delete(db_items)


def delete_specific_policy(db: Session, user_id: str, resource_id: str) -> None:
    """called when unshare"""
    query = db.query(models.CasbinRule).filter(
        and_(
            models.CasbinRule.ptype == PolicyTypeEnum.p,
            models.CasbinRule.v0 == user_id,
            models.CasbinRule.v1 == resource_id,
        )
    )
    db_items = query.all()
    if db_items:
        query.delete()
    else:
        raise PolicyDoesNotExist(user_id=user_id, resource_id=resource_id)


def update_specific_policy(
    db: Session,
    user_id: str,
    resource_id: str,
    right_to_update: SpecificResourceRightsEnum,
) -> None:
    """called when update another user's states"""
    query = db.query(models.CasbinRule).filter(
        and_(
            models.CasbinRule.ptype == PolicyTypeEnum.p,
            models.CasbinRule.v0 == user_id,
            models.CasbinRule.v1 == resource_id,
        )
    )
    db_item = query.first()
    if db_item:
        db_item.v2 = right_to_update
    else:
        raise PolicyDoesNotExist(user_id=user_id, resource_id=resource_id)
