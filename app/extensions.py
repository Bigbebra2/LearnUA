from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from flask_jwt_extended import JWTManager
from redis import Redis
from flask_cors import CORS


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()
jwt_redis_blocklist = Redis('127.0.0.1', port=6379, db=0)
cors = CORS()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    from .models import User
    identity = jwt_data["sub"]
    return User.query.filter_by(id=int(identity)).one_or_none()