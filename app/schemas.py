from pydantic import BaseModel, EmailStr

from typing import List, Optional


class Email(BaseModel):
    id: int
    email: EmailStr


class EmailCreate(BaseModel):
    email: EmailStr

    # class Config:
    #     orm_mode = True


class Student(BaseModel):
    id: int
    firstname: str
    lastname: str
    emails: Optional[List[Email]] 


class StudentCreate(BaseModel):
    course_id: int
    firstname: str
    lastname: str
    emails: Optional[List[EmailCreate]] 

    # class Config:
    #     orm_mode = True


class CourseCreate(BaseModel):
    course_name: str
    teacher: str

    # class Config:
    #     orm_mode = True


class CourseGetAll(BaseModel):
    id: int
    course_name: str
    teacher: str
    

class CourseGetOneFull(BaseModel):
    id: int
    course_name: str
    teacher: str
    students: Optional[List[Student]]
