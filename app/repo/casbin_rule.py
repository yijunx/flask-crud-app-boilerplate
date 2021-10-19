from typing import List, Tuple
from sqlalchemy.sql.expression import and_, or_
from app.schemas.pagination import QueryPagination, ResponsePagination
from app.db.models import models
from sqlalchemy.orm import Session
from app.schemas.casbin_rule import CasbinPolicy
from app.schemas.user import UserRight
from app.schemas.item import Item, ItemRight
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


def get_item_for_user_right(db: Session, user_right: UserRight):
    """Given a user (user_id + optional right), return what resource he/she operator at what right"""
    return


def get_users_who_have_access_item(
    db: Session,
    user_right: UserRight,
    is_admin: bool,
    query_pagination: QueryPagination,  # yes we need to make it paginated
) -> List[ItemRight]:
    """Given an item (resource_id + optional right), return who has what rights (user_id + optional right)"""
    query = db.query(models.CasbinRule).filter(models.CasbinRule.v1 == user_right.resource_id)

    if is_admin:
        # takes all the owns...
        total = query.count()
        limit, offset, paging = translate_query_pagination(
            query_pagination=query_pagination, total=total
        )

    return


def get_role(db: Session, user_id: str):
    return
