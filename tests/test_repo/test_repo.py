import pytest
import app.repo.item as itemRepo
from app.schemas.item import ItemCreate
from app.schemas.user import User
from sqlalchemy.orm import Session
from app.exceptions.item import ItemNameIsAlreadyThere, ItemDoesNotExist


ITEM_ID = ""


def test_create_item(db: Session, item_create: ItemCreate, user: User):
    db_item = itemRepo.create(db=db, item_create=item_create, creator=user)
    global ITEM_ID
    ITEM_ID = db_item.id
    assert db_item.created_by == user.id
    assert db_item.name == item_create.name


def test_get_item(db: Session, item_create: ItemCreate, user: User):
    db_item = itemRepo.get(db=db, item_id=ITEM_ID)
    assert db_item.created_by == user.id
    assert db_item.name == item_create.name


def test_cannot_get_item(db: Session):
    with pytest.raises(ItemDoesNotExist):
        _ = itemRepo.get(db=db, item_id="wrong id")


def test_cannot_create_item_with_used_name(
    db: Session, item_create: ItemCreate, user: User
):
    with pytest.raises(ItemNameIsAlreadyThere):
        _ = itemRepo.create(db=db, item_create=item_create, creator=user)


def test_list_items(db: Session, item_create: ItemCreate, user: User):
    pass


def test_delete_item(db: Session):
    itemRepo.delete(db=db, item_id=ITEM_ID)


def test_delete_item_again(db: Session):
    with pytest.raises(ItemDoesNotExist):
        itemRepo.delete(db=db, item_id=ITEM_ID)
