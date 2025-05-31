from ..extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Integer
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String(512))
    reg_datetime: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    enrolls: Mapped[list["Progress"]] = relationship(
        "Progress",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select"
    )
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    courses: Mapped[list['Course']] = relationship('Course',
                                                   back_populates='author'
                                                   )
    reviews: Mapped[list["Review"]] = relationship('Review',
                                                   back_populates='user'
                                                   )


class Progress(db.Model):
    __tablename__ = 'progresses'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'), index=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    enroll_datetime: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    user: Mapped['User'] = relationship('User', back_populates='enrolls')
    course: Mapped['Course'] = relationship('Course', back_populates='enrolls')


class Profile(db.Model):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    first_name: Mapped[str | None] = mapped_column(String(35), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(35), nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0)
    bio: Mapped[str | None] = mapped_column(String(256), nullable=True, default='no bio')
    contacts: Mapped[str | None] = mapped_column(String(126), nullable=True)

    user: Mapped["User"] = relationship("User",
                                        back_populates="profile"
                                        )






