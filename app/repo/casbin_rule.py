from typing import List, Tuple
from sqlalchemy.sql.expression import and_, or_
from app.schemas.pagination import QueryPagination, ResponsePagination
from app.db.models import models
from sqlalchemy.orm import Session
from app.schemas.casbin_rule import CasbinPolicy
from app.schemas.user import User
from datetime import datetime, timezone
from app.repo.util import translate_query_pagination
from app.exceptions.item import ItemDoesNotExist, ItemNameIsAlreadyThere
from sqlalchemy.exc import IntegrityError


def create(db: Session, casbin_policy: CasbinPolicy) -> models.Item:
    db_item = models.CasbinRule(
        
    )
    db.add(db_item)
    return db_item


def get_all():
    return
