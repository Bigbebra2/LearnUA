from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from ..schemas import CourseIn
import pydantic
from ..models import Course
from ..extensions import db


courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/create-course', methods=['POST'])
@jwt_required()
def create_course():
    if not request.is_json:
        return jsonify(msg='Expected json format'), 415

    try:
        course_model = CourseIn.model_validate(request.get_json())
        course = Course(title=course_model.title,
                        description=course_model.description,
                        author_id=current_user.id
                )
        if Course.query.filter_by(author_id=current_user.id, title=course_model.title).all():
            return jsonify(msg='Course title must be unique'), 400

        db.session.add(course)
    except pydantic.ValidationError as e:
        return jsonify(
            msg=str(e),
            example_json=CourseIn.model_json_schema().get('examples')
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f'Server error, please report: {e}'), 500

    db.session.commit()

    return jsonify(msg='Course created successfully'), 201







