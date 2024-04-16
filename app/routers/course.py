from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

# from sqlalchemy.sql.functions import func
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/course", tags=["Course"])


@router.post(
    "/create_course/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CourseGetOneFull,
)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    new_course = models.Course(**course.model_dump())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


@router.get("/get_all_courses/", response_model=List[schemas.CourseGetAll])
def get_all_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses


@router.get("/get_course/{id}", response_model=schemas.CourseGetOneFull)
def get_course(id: int, db: Session = Depends(get_db)):

    stmt_course = select(models.Course).where(models.Course.id==id)
    course = db.scalar(stmt_course)
    course_output = course.__dict__.copy()

    students_list = []
    stmt_students = select(models.Student).where(models.Student.course_id==course_output['id'])

    for student in db.scalars(stmt_students):
        student_dict = student.__dict__.copy()

        emails_list = []
        stmt_emails = select(models.Email).where(models.Email.email_owner_id==student_dict['id'])
        for email in db.scalars(stmt_emails):
            emails_list.append(email.__dict__.copy())
        
        student_dict['emails'] = emails_list

        students_list.append(student_dict)

    course_output['students'] = students_list

    return course_output

