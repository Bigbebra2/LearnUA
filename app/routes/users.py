import pydantic
from flask import Blueprint, jsonify, request
from ..models import Profile
from flask_jwt_extended import jwt_required, current_user
from ..schemas import ProfileModel
from ..extensions import db


user_pb = Blueprint('user', __name__)

@user_pb.route('/<int:user_id>/profile')
def user_profile(user_id):
    profile = Profile.query.filter_by(user_id=user_id).one_or_none()
    if not profile:
        jsonify(msg='Profile not found'), 404

    return jsonify(
        id=profile.id,
        user_id=profile.user_id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        age=profile.age,
        bio=profile.bio,
        contacts=profile.contacts,
        reg_datetime=profile.user.reg_datetime
    ), 200


@user_pb.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    if not request.is_json:
        return jsonify(msg='Expected json format'), 415

    try:
        profile_model = ProfileModel.model_validate(request.get_json())
        profile = current_user.profile
        for k, v in profile_model.model_dump().items():
            if k != 'contacts':
                setattr(profile, k, v)
            else:
                setattr(profile, k, '\n'.join(f'{soc}: {link}' for dct in v for soc, link in dct.items()))

    except pydantic.ValidationError as e:
            return jsonify(
                msg=str(e),
                example_json=ProfileModel.model_json_schema().get('examples')
            )
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f'Server error, please report: {e}'), 500

    db.session.commit()
    return jsonify(msg='Profile updated successfully'), 200






