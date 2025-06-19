from flask import Blueprint, jsonify
from ..models import Section


section_bp = Blueprint('section', __name__)

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