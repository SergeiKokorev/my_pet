from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import engine, get_db


router = APIRouter(
    prefix="/articles",
    tags=['Articles']
)
