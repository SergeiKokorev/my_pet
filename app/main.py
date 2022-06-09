import psycopg2

from sqlalchemy import MetaData, select, insert
from sqlalchemy.orm import registry, Session
from fastapi import (
    FastAPI, Response, status, 
    HTTPException, Depends
    )
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

from . import models
from .database import engine, Base, get_db

app = FastAPI()
Base.metadata.create_all(bind=engine)
oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Article(BaseModel):
    title: str
    template: str


class User(BaseModel):
    email: str


class Profile(BaseModel):
    name: str
    fulname: str


class Post(BaseModel):
    title: str
    content: str


def fake_decode_token(token):
    return models.User(
        email=token + "fakedecode"
    )


async def get_current_user(token: str = Depends(oath2_scheme)):
    user = fake_decode_token(token)
    return user


@app.get("/")
def root():
    return {"message": "Hello word"}


@app.get("/articles")
def articles(response: Response, db: Session = Depends(get_db)):

    with db as session:
        with session.begin():
            articles = db.query(models.Article).all()
    
    if not articles:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "No articles were found"}

    return {"content": articles}


@app.post("/articles", status_code=status.HTTP_201_CREATED)
def create_article(
    article: Article, 
    response: Response, 
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
    ):
    new_article = models.Article(**article.dict())
    
    print(user)

    with db as session:
        with session.begin():
            session.add(new_article)

    return {"content": new_article}


