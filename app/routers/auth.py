from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from .. import schemas, models, database, utils, oath2


router = APIRouter(tags=['Authentification'])

@router.post("/login")
def login(user_credential: schemas.UserLogin, db: Session = Depends(database.get_db)):

    user = db.query(models.BaseUser).filter(models.BaseUser.email==user_credential.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credential")

    if not utils.verify_password(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credential")

    access_token = oath2.create_access_token(data={"user_id": user.id})

    return access_token
