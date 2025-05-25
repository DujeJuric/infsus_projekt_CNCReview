from fastapi import APIRouter
from schemas.ocjena import OcjenaBase
from dependencies import db_dependency
from models.ocjena import Ocjene as ocjena_model

router = APIRouter(prefix="/ocjena", tags=["ocjena"])

@router.post("/createOcjena")
async def create_ocjena(ocjena: OcjenaBase, db: db_dependency):
    db_ocjena = ocjena_model(
        ocjena=ocjena.ocjena
    )
    db.add(db_ocjena)
    db.commit()
    db.refresh(db_ocjena)
    return db_ocjena

@router.get("/getAllOcjena")
async def get_all_ocjena(db: db_dependency):
    return db.query(ocjena_model).all()

@router.post("/editOcjena/{ocjena_id}")
async def edit_ocjena(ocjena_id: int, ocjena: OcjenaBase, db: db_dependency):
    db_ocjena = db.query(ocjena_model).filter(ocjena_model.ocjena_id == ocjena_id).first()
    if not db_ocjena:
        return {"error": "Ocjena not found"}
    db_ocjena.ocjena = ocjena.ocjena
    db.commit()
    db.refresh(db_ocjena)
    return db_ocjena

@router.delete("/deleteOcjena/{ocjena_id}")
async def delete_ocjena(ocjena_id: int, db: db_dependency):
    db_ocjena = db.query(ocjena_model).filter(ocjena_model.ocjena_id == ocjena_id).first()
    if not db_ocjena:
        return {"error": "Ocjena not found"}
    db.delete(db_ocjena)
    db.commit()
    return {"message": "Ocjena deleted successfully"}