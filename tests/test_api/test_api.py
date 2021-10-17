from app.schemas.item import Item, ItemWithPagination, ItemCreate
from app.schemas.user import User
from app.schemas.response import StandardResponse
from flask.testing import FlaskClient

ITEM_ID = ""


def test_create_item(
    client: FlaskClient,
    item_create_dict: dict,
    item_create: ItemCreate,
    user: User,
    headers_with_authorization: dict,
):
    r = client.post("/api/items", json=item_create_dict, headers=headers_with_authorization)
    print(r.get_json())
    item = Item(**r.get_json()["response"])
    global ITEM_ID
    ITEM_ID = item.id
    assert item.name == item_create.name
    assert item.created_by_name == user.name


def test_get_item(
    client: FlaskClient,
    item_create: ItemCreate,
    user: User,
    headers_with_authorization: dict,
):
    r = client.get(f"/api/items/{ITEM_ID}", headers=headers_with_authorization)
    item = Item(**r.get_json()["response"])
    assert item.name == item_create.name
    assert item.created_by_name == user.name


def test_get_item_with_wrong_id(
    client: FlaskClient,
    item_create: ItemCreate,
    user: User,
    headers_with_authorization: dict,
):
    r = client.get(f"/api/items/wrong_id", headers=headers_with_authorization)
    print(r.get_json())
    standard_response = StandardResponse(**r.get_json())
    assert standard_response.success == False


def test_delete_item(client: FlaskClient, headers_with_authorization: dict):
    r = client.delete(f"/api/items/{ITEM_ID}", headers=headers_with_authorization)
    standard_response = StandardResponse(**r.get_json())
    assert standard_response.message == "item deleted"
