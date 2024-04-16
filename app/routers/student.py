from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db


router = APIRouter(
    prefix="/student",
    tags=['students']
)


@router.post("/create_student/",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.Student)
def create_course(student: schemas.StudentCreate, 
                  db: Session = Depends(get_db)):
    
    new_student = models.Student(firstname=student.firstname,
                                 lastname=student.lastname,
                                 course_id=student.course_id)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    final_output = new_student.__dict__.copy()

    student_id = new_student.id

    email_dicts = []

    if student.emails:
        for email in student.emails:
            print(f'{email=}')
            new_email = models.Email(email=email.email,
                                     email_owner_id=student_id)
            db.add(new_email)
            db.commit()
            db.refresh(new_email)

            email_dicts.append(new_email.__dict__)

    final_output.update({'emails': email_dicts})

    return final_output

