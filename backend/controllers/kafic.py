from fastapi import APIRouter
from schemas.kafic import KaficBase
from dependencies import db_dependency
from models.kafic import kafici as kafic_model

router = APIRouter(prefix="/kafic", tags=["kafic"])