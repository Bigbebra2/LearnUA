from flask import Blueprint, jsonify
from ..models import Lesson


lesson_bp = Blueprint('lesson', __name__)

@lesson_bp.route('/<int:lesson_id>')
def get_lesson_info(lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id).one_or_none()
    if not lesson:
        return jsonify(msg='Lesson not found')

    return jsonify(
        section_id=lesson.section_id,
        title=lesson.title,
        place=lesson.place,
        steps=[
            {'content_type': s.content_type, 'place': s.place}
            for s in lesson.steps
        ]
    )