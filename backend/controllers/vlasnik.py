from fastapi import APIRouter
from schemas.vlasnik import VlasnikBase
from dependencies import db_dependency
from models.vlasnik import Vlasnik as vlasnik_model

router = APIRouter(prefix="/vlasnik", tags=["vlasnik"])

@router.post("/createVlasnik")
async def create_vlasnik(vlasnik: VlasnikBase, db: db_dependency):
    db_vlasnik = vlasnik_model(
        naziv=vlasnik.naziv,
        lozinka=vlasnik.lozinka,
        email=vlasnik.email
    )
    db.add(db_vlasnik)
    db.commit()
    db.refresh(db_vlasnik)
    return db_vlasnik

@router.get("/getAllVlasnik")
async def get_all_vlasnik(db: db_dependency):
    return db.query(vlasnik_model).all()

@router.delete("/deleteVlasnik/{id}")
async def delete_vlasnik(id: int, db: db_dependency):
    db_vlasnik = db.query(vlasnik_model).filter(vlasnik_model.vlasnik_id == id).first()
    if not db_vlasnik:
        return {"message": "Vlasnik not found"}
    
    db.delete(db_vlasnik)
    db.commit()
    return {"message": "Vlasnik deleted successfully"}

