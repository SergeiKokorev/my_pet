from pydantic import BaseModel, EmailStr
from typing import List, Tuple
from datetime import datetime


class BaseUser(BaseModel):

    email: EmailStr
    password: str
    created_at: datetime


class UserProfile(BaseModel):
    
    user_first_name: str
    user_last_name: str
    user_idx: int


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
