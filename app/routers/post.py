from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import engine, get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
def posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    
    return posts

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} has not been found.")

    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
    
    post = models.Post(**post.dict())

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post id {id} has not been found.")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == post_id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post id {post_id} has not been found.")
    
    post.delete(synchronize_session=False)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

