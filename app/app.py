from flask import Flask
from flask.json import JSONEncoder
from flask_request_id_header.middleware import RequestID
from flask_cors import CORS
from app.util.app_logging import get_logger, init_logger
from app.blueprints.item import bp as itemBp
from app.blueprints.internal import bp as internalBp
from app.blueprints.rbac import bp as rbacBp
from app.config.app_config import conf
from datetime import datetime


logger = get_logger(__name__)

app = Flask(__name__)
init_logger(app=app)
# app.json_encoder = some custom json encoder... (to deal with some datetime issues)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app.config["REQUEST_ID_UNIQUE_VALUE_PREFIX"] = ""
RequestID(app)
CORS(app, resources={r"/api/*": {"origins": conf.CORS_ALLOWED_ORIGINS}})

app.json_encoder = CustomJSONEncoder

app.register_blueprint(itemBp)
app.register_blueprint(internalBp)
app.register_blueprint(rbacBp)


# @app.after_request
# def modify_flask_pydantic_response(response: Response):
#     if (
#         response.status_code == 400
#         and response.is_json
#         and "validation_error" in response.json
#     ):
#         logger.info(response.json)
#         message = "The problem is in the validation"
#         return create_response(message=message, status_code=400)
#     return response
