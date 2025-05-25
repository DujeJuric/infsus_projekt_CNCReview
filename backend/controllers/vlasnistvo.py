from fastapi import APIRouter
from schemas.vlasnistvo import VlasnistvoBase
from dependencies import db_dependency
from models.vlasnistvo import Vlasnistvo as vlasnistvo_model
from models.admin import Admin as admin_model
from models.vlasnik import Vlasnik as vlasnik_model
from fastapi import HTTPException

router = APIRouter(prefix="/vlasnistvo", tags=["vlasnistvo"])

@router.post("/createVlasnistvo")
async def create_vlasnistvo(vlasnistvo: VlasnistvoBase, db: db_dependency):

    if not db.query(admin_model).filter(admin_model.admin_id == vlasnistvo.admin_id).first():
        raise HTTPException(status_code=404, detail="Admin not found")
    if not db.query(vlasnik_model).filter(vlasnik_model.vlasnik_id == vlasnistvo.vlasnik_id).first():
        raise HTTPException(status_code=404, detail="Vlasnik not found")

    db_vlasnistvo = vlasnistvo_model(
        admin_id=vlasnistvo.admin_id,
        vlasnik_id=vlasnistvo.vlasnik_id,
    )

    db.add(db_vlasnistvo)
    db.commit()
    db.refresh(db_vlasnistvo)
    return db_vlasnistvo

@router.get("/getAllVlasnistvo")
async def get_all_vlasnistvo(db: db_dependency):
    return db.query(vlasnistvo_model).all()

@router.delete("/deleteVlasnistvo/{id}")
async def delete_vlasnistvo(id: int, db: db_dependency):
    db_vlasnistvo = db.query(vlasnistvo_model).filter(vlasnistvo_model.vlasnistvo_id == id).first()
    if not db_vlasnistvo:
        return HTTPException(status_code=404, detail="Vlasnistvo not found")
    
    db.delete(db_vlasnistvo)
    db.commit()
    return {"detail": "Vlasnistvo deleted successfully"}