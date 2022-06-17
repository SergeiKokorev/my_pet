from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional
from sqlalchemy.orm import Session

from .. import schemas, models, utils
from ..database import engine, get_db


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserBack)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.get_hash_password(user.password)
    user = models.BaseUser(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    profile = models.UserProfile(user_idx=user.id)
    db.add(profile)
    db.commit()
    db.refresh(profile)

    return user

@router.post("/{id}")
def profile_create():
    pass

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.GetUser)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.BaseUser).filter(models.BaseUser.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} doesn\'t exist.")
    
    profile = db.query(models.UserProfile).filter(models.UserProfile.user_idx==user.id).first()
    print(profile)

    return {"user": user, "profile": profile}
