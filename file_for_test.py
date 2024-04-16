from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import text

from pydantic import BaseModel, EmailStr

import datetime
from typing import List, Optional


SQLALCHEMY_DATABASE_URL = ('postgresql://jimmylevesque'
                           '@localhost'
                           ':5432'
                           '/school')


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

class Base(DeclarativeBase):
    pass

db = SessionLocal()





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






stmt_course = select(Course).where(Course.id==1)
course = db.scalar(stmt_course)
course_output = course.__dict__.copy()

students_list = []
stmt_students = select(Student).where(Student.course_id==course_output['id'])
for student in db.scalars(stmt_students):
    student_dict = student.__dict__.copy()

    emails_list = []
    stmt_emails = select(Email).where(Email.email_owner_id==student_dict['id'])
    for email in db.scalars(stmt_emails):
        emails_list.append(email.__dict__.copy())
    
    student_dict['emails'] = emails_list

    students_list.append(student_dict)

course_output['students'] = students_list
    


class PydEmail(BaseModel):
    id: int
    email: EmailStr


class PydStudent(BaseModel):
    id: int
    firstname: str
    lastname: str
    emails: Optional[List[PydEmail]] 
    

class PydCourseGetOneFull(BaseModel):
    id: int
    course_name: str
    teacher: str
    students: Optional[List[PydStudent]]



