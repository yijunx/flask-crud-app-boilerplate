from typing import Dict
import pytest
from app.schemas.item import ItemCreate
from app.schemas.user import User


@pytest.fixture
def item_create_dict():
    return {
        "name": "test",
        "description": "desc"
    }


@pytest.fixture
def item_create(item_create_dict: Dict):
    return ItemCreate(**item_create_dict)


@pytest.fixture
def user_dict():
    return {
        "id": "test-user-id",
        "name": "test",
        "email": "test@test.com"
    }


@pytest.fixture
def user(user_dict: Dict):
    return User(**user_dict)

