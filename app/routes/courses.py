from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from ..schemas import CourseIn, SectionIn, LessonIn
import pydantic
from ..models import Course, Section, Lesson
from ..extensions import db
from sqlalchemy import select


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
        ), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f'Server error, please report: {e}'), 500

    db.session.commit()

    return jsonify(msg='Course created successfully'), 201

@courses_bp.route('/<int:course_id>/add-section', methods=['POST'])
@jwt_required()
def add_section(course_id):
    if not request.is_json:
        return jsonify(msg='Expected json format'), 415
    if course_id not in tuple(c.id for c in current_user.courses):
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

    except pydantic.ValidationError as e:
        return jsonify(
            msg=str(e),
            example_json=SectionIn.model_json_schema().get('examples')
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f'Server error, please report: {e}'), 500

    db.session.commit()
    return jsonify(msg='Section successfully added'), 201

@courses_bp.route('/<int:course_id>/<int:place>/add-lesson', methods=['POST'])
@jwt_required()
def add_lesson(course_id, place):
    if not request.is_json:
        return jsonify(msg='Expected json format'), 415

    sub_query = select(Course.id).where(Course.author_id == current_user.id).scalar_subquery()
    section_query = select(Section).where(
        Section.course_id.in_(sub_query),
        Section.course_id == course_id,
        Section.place == place
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

    except pydantic.ValidationError as e:
        return jsonify(
            msg=str(e),
            example_json=LessonIn.model_json_schema().get('examples')
        ), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f'Server error, please report: {e}'), 500

    db.session.commit()
    return jsonify(msg='Lesson created successfully'), 201












