import pydantic
from flask import Blueprint, jsonify, request, current_app, send_from_directory
from ..models import Profile
from flask_jwt_extended import jwt_required, current_user
from ..schemas import ProfileModel
from ..extensions import db
import os
from werkzeug.utils import secure_filename
from ..utils import delete_all_files


user_pb = Blueprint('user', __name__)

@user_pb.route('/my-profile')
@jwt_required()
def my_profile():
    profile = current_user.profile
    contacts = profile.contacts

    try:
        return jsonify(
            user_data = {
                'id': current_user.id,
                'reg_datetime': current_user.reg_datetime,
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'age': profile.age,
                'bio': profile.bio,
                'contacts': [{cont.split(': ')[0]: cont.split(': ')[1]} for cont in contacts.split('\n')] \
                    if contacts else []
            }
        )
    except Exception as e:
        return jsonify(msg=f'Server error, report please: {e}'), 500


@user_pb.route('/<int:user_id>/profile')
def user_profile(user_id):
    profile = Profile.query.filter_by(user_id=user_id).one_or_none()

    if not profile:
        jsonify(msg='Profile not found'), 404

    try:
        contacts = profile.contacts

        return jsonify(
            id=profile.id,
            user_id=profile.user_id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            age=profile.age,
            bio=profile.bio,
            contacts=[{cont.split(': ')[0]: cont.split(': ')[1]} for cont in contacts.split('\n')] if contacts else [],
            reg_datetime=profile.user.reg_datetime
        ), 200
    except Exception as e:
        return jsonify(msg=f'Server error, report please: {e}'), 500


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

@user_pb.route('/upload-ava', methods=['PUT'])
@jwt_required()
def upload_ava():
   file = request.files.get('ava')
   if not file or file.filename == '':
       return jsonify(msg='File not uploaded or has empty name'), 400

   ext = os.path.splitext(file.filename)[1]
   if ext not in current_app.config['ALLOWED_IMAGE_EXTENSIONS']:
       return jsonify(msg='File has not allowed extension'), 400

   max_size = current_app.config['MAX_AVA_SIZE']

   file.seek(0, 2)
   size = file.tell()
   file.seek(0)
   if size > max_size:
       return jsonify(msg=f'File too large, max size: {max_size}'), 400

   try:
       filename = secure_filename(f'{current_user.id}_ava{ext}')
       path = os.path.join(os.getcwd(), 'uploads', f'user_{current_user.id}', 'ava')

       if os.path.isdir(path) and os.listdir(path):
           delete_all_files(path)

       os.makedirs(path, exist_ok=True)
       file.save(os.path.join(path, filename))
   except Exception as e:
       return jsonify(msg=f'File uploading error: {e}'), 500

   return jsonify(msg='Profile ava updated successfully')


@user_pb.route('/ava/<int:user_id>')
def get_avatar(user_id):
    try:
        path = os.path.join(os.path.split(current_app.root_path)[0], 'uploads', f'user_{user_id}', 'ava')
        if os.path.isdir(path):
            files = os.listdir(path)
            if files and os.path.splitext(files[0])[1] in current_app.config['ALLOWED_IMAGE_EXTENSIONS']:
                return send_from_directory(path, files[0], mimetype='image/jpeg')
    except Exception as e:
        return jsonify(msg=f'File defining error: {e}'), 500

    return jsonify(msg='No ava'), 404
