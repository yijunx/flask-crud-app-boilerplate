from typing import List, Tuple
from sqlalchemy.sql.expression import and_, or_
from app.schemas.pagination import QueryPagination, ResponsePagination
from app.db.models import models
from sqlalchemy.orm import Session
from app.schemas.casbin_rule import CasbinPolicy, PolicyTypeEnum
from app.schemas.user import UsersItemRight, UsersItemRightWithPaging
from app.schemas.item import ItemsUserRight
from datetime import datetime, timezone
from app.repo.util import translate_query_pagination
from app.exceptions.item import ItemDoesNotExist, ItemNameIsAlreadyThere
from sqlalchemy.exc import IntegrityError


def create(db: Session, casbin_policy: CasbinPolicy) -> models.Item:
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
    return db_item


def get_all_given_user(
    db: Session,
    users_item_right: UsersItemRight,
    query_pagination: QueryPagination,
    is_admin: bool,
) -> Tuple[List[models.CasbinRule], ResponsePagination]:
    """
    Given a user (user_id + optional right),
    return what resource he/she operator at what right
    """

    query = db.query(models.CasbinRule).filter(
        models.CasbinRule.ptype == PolicyTypeEnum.p
    )
    if users_item_right.right:
        query = query.filter(models.CasbinRule.v2 == users_item_right.right)
    if not is_admin:
        query = query.filter(models.CasbinRule.v0 == users_item_right.user_id)
    total = query.count()
    limit, offset, paging = translate_query_pagination(
        query_pagination=query_pagination, total=total
    )
    db_items = (
        query.order_by(models.Item.created_at.desc()).limit(limit).offset(offset).all()
    )
    paging.page_size = len(db_items)

    return db_items, paging
    return


def get_all_given_item(
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
            models.CasbinRule.ptype == PolicyTypeEnum.p.name,
        )
    )
    total = query.count()
    limit, offset, paging = translate_query_pagination(
        query_pagination=query_pagination, total=total
    )
    db_items = (
        query.order_by(models.Item.created_at.desc()).limit(limit).offset(offset).all()
    )
    paging.page_size = len(db_items)

    return db_items, paging


def get_role(db: Session, user_id: str):
    return
