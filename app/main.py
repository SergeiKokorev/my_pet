import psycopg

from fastapi import (
    FastAPI, Response, status,
    HTTPException, Depends
)
from typing import List, Tuple
from sqlalchemy.orm import Session

from . import schemas, models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Greatings!"}


@app.get("/posts", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
def posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    
    return posts

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {post_id} has not been found.")

    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
    
    post = models.Post(**post.dict())

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@app.put("/posts/{post_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def update_post(post_id: int, post: schemas.CreatePost, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    updated_post = post_query.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post id {post_id} has not been found.")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == post_id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post id {post_id} has not been found.")
    
    post.delete(synchronize_session=False)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
