import functools
from sys import path
import jwt
import os
from app.schemas.user import User
from flask import Request, abort
from datetime import datetime, timedelta, timezone
from typing import List
from flask import Request, request
from app.casbin.rbac import casbin_enforcer, is_admin
from app.util.response_util import create_response


# def authorize_specific_resource(func):
#     @functools.wraps(func)
#     def wrapper_func(*args, **kwargs):
#         path_components = request.path.split("/")
#         # this is also not good
#         # coz some function will need to get user again
#         user = get_user_info_from_request(request=request)
#         # this is bad design..
#         # path must be /api/resource_name/resource_id/verb
#         # but the normal get /api/resource_name/resource_id .. no verb..
#         item_id = path_components[-1]
#         action = path_components[-2]

#         # check if it admin, if its admin, no need enforce!!!
#         # well we can run without it...

#         if casbin_enforcer.enforce(user.id, item_id, action):
#             # now it means all endpoints requires user must be authorized
#             # get items/ will also need to be authrized
#             # which means there need to be a user role id required
#             # all users will be added to this group
#             return func(*args, **kwargs, user=user)
#         else:
#             return create_response(
#                 status_code=403,
#                 message=f"User {user.id} has no right to {action} item {item_id}",
#                 success=False,
#             )
#     return wrapper_func


def decode_token(token: str):
    # [if RS256]
    # pub = _read_pem(file_location=PUBLIC_KEY_LOCATION)
    # data = jwt.decode(jwt=token, key=pub, algorithms=["RS256"])
    data = jwt.decode(jwt=token, options={"verify_signature": False})
    return data


def get_token_from_cookie(request: Request) -> str:
    token: str = request.cookies.get("token", None)
    return token


def get_token_from_authorization_header(request: Request) -> str:
    bearer_auth: str = request.headers.get("Authorization", None)
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
    token = get_token_from_cookie(request)
    if token is None:
        abort(status=401)
    else:
        user = User(**decode_token(token=token))
        user.is_admin = is_admin(user)
        return user
