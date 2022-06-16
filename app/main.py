from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from . import schemas, models
from .database import engine, get_db
from .routers import post, user, article

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(article.router)

@app.get("/")
def root():
    return {"message": "Welcome my app"}

