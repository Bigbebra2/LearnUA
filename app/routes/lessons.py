from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import select
from ..models import Course, Lesson, Section
from ..extensions import db
from ..schemas import LessonIn, LessonQuery
from pydantic import ValidationError


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

@lesson_bp.route('/', methods=['POST'])
@jwt_required()
def add_lesson():
    course_id, section_place = request.args.get('course_id'), request.args.get('section_place')
    if not (course_id and section_place):
        print(course_id, section_place)
        return jsonify(msg='Missing query-parameter \'course_id\' or \'section_place\''), 400
    try:
        lesson_model = LessonQuery(course_id=course_id, section_place=section_place)

    except ValidationError as e:
        return jsonify(msg=f'Incorrect value of query-parameters: {e}'), 400

    if not request.is_json:
        return jsonify(msg='Expected json format'), 415
    course_id, section_place = lesson_model.course_id, lesson_model.section_place

    sub_query = select(Course.id).where(Course.author_id == current_user.id).scalar_subquery()
    section_query = select(Section).where(
        Section.course_id.in_(sub_query),
        Section.course_id == course_id,
        Section.place == section_place
    )
    section = db.session.execute(section_query).scalars().one_or_none()
    if not section:
        return jsonify(msg='You can\'t modify this section'), 403
    lesson_place = len(section.lessons) + 1

    try:
        lesson_model = LessonIn.model_validate(request.get_json())
        existing_lesson = db.session.execute(
            select(Lesson).where(
                Lesson.section_id == section.id,
                Lesson.title == lesson_model.title
            )
        ).scalar_one_or_none()

        if existing_lesson:
            return jsonify(msg='Title must be unique'), 400

        lesson = Lesson(
            title=lesson_model.title,
            section_id=section.id,
            place=lesson_place
        )
        db.session.add(lesson)

    except ValidationError as e:
        return jsonify(
            msg=str(e),
            example_json=LessonIn.model_json_schema().get('examples')
        ), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f'Server error, please report: {e}'), 500

    db.session.commit()
    return jsonify(msg='Lesson created successfully'), 201