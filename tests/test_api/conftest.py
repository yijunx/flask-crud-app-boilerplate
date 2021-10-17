import pytest
from app.app import app
import jwt
from flask.testing import FlaskClient


@pytest.fixture
def client(user_dict) -> FlaskClient:
    token = jwt.encode(payload=user_dict, key="secret")
    with app.test_client() as c:
        c.set_cookie("localhost", "token", token)
        yield c


@pytest.fixture
def headers_with_cookie(user_dict) -> dict:
    token = jwt.encode(payload=user_dict, key="secret")
    headers = {"Cookie": f"token={token}"}
    return headers


@pytest.fixture
def headers_with_authorization(user_dict) -> dict:
    token = jwt.encode(payload=user_dict, key="secret")
    headers = {"Authorization": f"Bearer {token}"}
    return headers
