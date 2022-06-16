from pydantic import BaseModel, EmailStr
from typing import Optional, Tuple, List
from datetime import datetime


class BaseUser(BaseModel):

    id: int
    email: EmailStr
    password: str
    created_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserBack(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class GetBaseUser(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class GetUserProfile(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        orm_mode = True


class GetUser(BaseModel):
    
    user: GetBaseUser
    profile: Optional[GetUserProfile] = None

    class Config:
        orm_mode = True


class PostBase(BaseModel):

    title: str
    content: str
    user_idx: int


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CreatePost(PostBase):
    pass


class Article(BaseModel):

    title: str
    template: str
    user_idx: int
    created_at: datetime



