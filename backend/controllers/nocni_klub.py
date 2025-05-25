from fastapi import APIRouter
from schemas.nocni_klub import Nocni_klubBase
from dependencies import db_dependency
from models.nocni_klub import Nocni_klubovi as nocni_klub_model

router = APIRouter(prefix="/nocni_klub", tags=["nocni_klub"])