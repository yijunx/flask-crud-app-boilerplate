import jwt
import os
from app.schemas.user import User
from flask import Request, abort
from datetime import datetime, timedelta, timezone
from typing import List


def decode_token(token: str):
    # [if RS256]
    # pub = _read_pem(file_location=PUBLIC_KEY_LOCATION)
    # data = jwt.decode(jwt=token, key=pub, algorithms=["RS256"])
    data = jwt.decode(jwt=token, options={"verify_signature": False})
    return data


def get_token_from_cookie(headers: dict) -> str:
    cookie: str = headers.get("Cookie", None)
    if cookie is None:
        return None
    raisins: List[str] = cookie.split("; ")
    token = None
    for r in raisins:
        if r.startswith("token="):
            token = r.split("=")[1]
    return token


def get_token_from_authorization_header(headers: dict) -> str:
    bearer_auth: str = headers.get("Authorization", None)
    if bearer_auth is None:
        return None
    token = bearer_auth.split(" ")[1]
    return token


def get_user_info_from_request(request: Request) -> User:
    """
    As the user-management will only issue httpOnly token,
    react frontend cannot get it. and chrome will only add the token
    in the cookie accompanying the request sent to the server.
    """
    token = get_token_from_cookie(request.headers)
    if token is None:
        print("TOKEN IS NONE")
        abort(status=401)
    else:
        user = User(**decode_token(token=token))
        return user
