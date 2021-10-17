from contextlib import contextmanager
from app.db.database import SessionLocal
from app.schemas.item import Item, ItemCreate, ItemWithPagination, ItemPatch
from app.schemas.pagination import QueryPagination
from app.schemas.user import User
import app.repo.item as itemRepo


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
    with get_db() as db:
        db_item = itemRepo.create(db=db, item_create=item_create, creator=user)
        item = Item.from_orm(db_item)
    return item


def get_item(item_id: str) -> Item:
    with get_db() as db:
        db_item = itemRepo.get(db=db, item_id=item_id)
        item = Item.from_orm(db_item)
    return item


def list_items(query_pagination: QueryPagination) -> ItemWithPagination:
    with get_db() as db:
        db_items, paging = itemRepo.get_all(db=db, query_pagination=query_pagination)
        items = [Item.from_orm(x) for x in db_items]
    return ItemWithPagination(data=items, paging=paging)


def delete_item(item_id: str) -> None:
    with get_db() as db:
        itemRepo.delete(db=db, item_id=item_id)


def clean_up() -> None:
    with get_db() as db:
        itemRepo.delete_all(db=db)
