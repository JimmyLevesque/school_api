from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import text

import datetime
from typing import List

from .database import Base


class Course(Base):
    __tablename__ = "course"
    
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    course_name: Mapped[str] = mapped_column(nullable=False)
    teacher: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default=text('now()'))

    students: Mapped[List["Student"]] = relationship(back_populates="registered_course", 
                                                     cascade="all, delete-orphan")
    

class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default=text('now()'))
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))

    registered_course: Mapped[Course] = relationship(back_populates="students")
    emails: Mapped[List["Email"]] = relationship(back_populates="email_owner",
                                                 cascade="all, delete-orphan")


class Email(Base):
    __tablename__ = "email"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    email_owner_id: Mapped[int] = mapped_column(ForeignKey("student.id"))

    email_owner: Mapped[Student] = relationship(back_populates="emails")

