from flask import Blueprint, jsonify, request
from ..models import Section
from flask_jwt_extended import jwt_required, current_user
from ..schemas import SectionIn
from ..extensions import db
from pydantic import ValidationError
from ..schemas import SectionQuery


section_bp = Blueprint('section', __name__)

# Get info about a section by its ID
@section_bp.route('/<int:section_id>')
def get_section_data(section_id):
    section = Section.query.filter_by(id=section_id).one_or_none()
    if not section:
        return jsonify(msg='Section not found'), 404

    return jsonify(
        course_id=section.course_id,
        title=section.title,
        place=section.place,
        lessons=[
            {'place': les.place, 'title': les.title} for les in section.lessons
        ]
    )

# Create a new section
@section_bp.route('/', methods=['POST'])
@jwt_required()
def create_section():
    q = request.args.get('course_id')
    if not q:
        return jsonify(msg='Query-parameter \'course_id\' is required'), 400

    try:
        course_id = SectionQuery(course_id=request.args.get('course_id')).course_id
    except ValidationError as e:
        return jsonify(msg=f'Incorrect value of query-parameter \'course_id\': {e}'), 400

    if not request.is_json:
        return jsonify(msg='Expected json format'), 415
    if course_id not in (c.id for c in current_user.courses):
        return jsonify(msg='Can\'t edit this course'), 403

    try:
        section_model = SectionIn.model_validate(request.get_json())
        sections = Section.query.filter_by(course_id=course_id)

        if section_model.title in [s.title for s in sections]:
            return jsonify(msg='Title must be unique'), 400

        place = sections.count() + 1
        section = Section(
            course_id=course_id,
            title=section_model.title,
            place=place
        )
        db.session.add(section)

    except ValidationError as e:
        return jsonify(
            msg=str(e),
            example_json=SectionIn.model_json_schema().get('examples')
        ), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f'Server error, please report: {e}'), 500

    db.session.commit()
    return jsonify(msg='Section successfully added', section_id=section.id), 201