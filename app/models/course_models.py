from sqlalchemy import ForeignKey, String, DateTime, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.user_models import Progress
from ..extensions import db
from datetime import datetime, timezone


class Course(db.Model):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    title: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(String(1800))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    rating: Mapped[float] = mapped_column(Numeric(2, 1), default=0.0)

    enrolls: Mapped[list['Progress']] = relationship('Progress',
                                                     back_populates='course'
                                                     )
    author: Mapped['User'] = relationship('User',
                                          back_populates='courses'
                                          )
    sections: Mapped[list['Section']] = relationship('Section', back_populates='course')
    reviews: Mapped[list["Review"]] = relationship('Review',
                                                   back_populates='course'
                                                   )

class Section(db.Model):
    __tablename__ = 'sections'

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'), index=True)
    title: Mapped[str] = mapped_column(String(80))
    place: Mapped[int] = mapped_column(Integer)

    course: Mapped['Course'] = relationship('Course', back_populates='sections')
    lessons: Mapped[list['Lesson']] = relationship('Lesson', back_populates='section')


class Lesson(db.Model):
    __tablename__ = 'lessons'

    id: Mapped[int] = mapped_column(primary_key=True)
    section_id: Mapped[int] = mapped_column(ForeignKey('sections.id'), index=True)
    title: Mapped[str] = mapped_column(String(80))
    place: Mapped[int] = mapped_column(Integer)

    section: Mapped['Section'] = relationship('Section', back_populates='lessons')
    steps: Mapped[list['Step']] = relationship('Step', back_populates='lesson')


class Step(db.Model):
    __tablename__ = 'steps'

    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey('lessons.id'), index=True)
    place: Mapped[int] = mapped_column(Integer)
    content_type: Mapped[str] = mapped_column(String(64))
    content_path: Mapped[str] = mapped_column(String(256))

    lesson: Mapped['Lesson'] = relationship('Lesson', back_populates='steps')


class Review(db.Model):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True,)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'), index=True)
    text: Mapped[str] = mapped_column(String(2048))
    score: Mapped[int] = mapped_column(Integer)
    review_datetime: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    user: Mapped['User'] = relationship('User',
                                        back_populates='reviews'
                                        )
    course: Mapped['Course'] = relationship('Course',
                                            back_populates='reviews'
                                            )
