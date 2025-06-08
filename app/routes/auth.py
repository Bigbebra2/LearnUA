import pydantic
from flask import Blueprint, request, jsonify
from ..schemas import RegisterModel, LoginModel
from ..models import User, Profile
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                set_access_cookies, set_refresh_cookies,
                                jwt_required, unset_jwt_cookies, current_user)
from datetime import timedelta
from ..services import logout_cookies


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/is-authorized')
@jwt_required()
def my_profile():
    return jsonify(msg='User is authorized'), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify(msg='Expected json format'), 415

    try:
        reg_model = RegisterModel.model_validate(request.get_json())
        user = User.query.filter_by(email=reg_model.email).one_or_none()
        if user:
            return jsonify(msg='This email is already registered'), 409
        elif reg_model.password != reg_model.password_again:
            return jsonify(msg='Passwords do not match'), 422

        psw_hash = generate_password_hash(reg_model.password)
        user = User(email=reg_model.email, password=psw_hash)
        db.session.add(user)
        db.session.flush()

        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.flush()

    except pydantic.ValidationError as e:
        return jsonify(
            msg=str(e),
            example_json=RegisterModel.model_json_schema().get('examples')
        ), 422
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f'Server error, please report: {e}'), 500

    db.session.commit()
    return jsonify(msg='User is successfully registered')


@auth_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify(msg='Expected json format'), 415

    try:
        login_model = LoginModel.model_validate(request.get_json())
        user = User.query.filter_by(email=login_model.email).one_or_none()

        if (not user) or (not check_password_hash(user.password, login_model.password)):
            return jsonify(msg='Wrong email or password'), 401
        else:
            access_token = create_access_token(identity=str(user.id), fresh=True, expires_delta=timedelta(minutes=30))
            refresh_token = create_refresh_token(identity=str(user.id), expires_delta=timedelta(days=7))

    except pydantic.ValidationError as e:
        return jsonify(
            msg=str(e),
            example_json=LoginModel.model_json_schema().get('examples')
        )
    except Exception as e:
        return jsonify(msg=f'Server error, please report: {e}'), 500

    response = jsonify({"msg": "login successful"})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    access_token = create_access_token(identity=str(current_user.id))
    response = jsonify(msg='Access token created successfully')
    set_access_cookies(response, access_token)
    return response

@auth_bp.route('/logout', methods=['DELETE'])
@jwt_required(verify_type=False)
def logout():
    result = logout_cookies()

    response = jsonify(
        errrors=result.get('errors'),
        revoked_tokens=result.get('revoked_tokens')
    )
    unset_jwt_cookies(response)
    return response







