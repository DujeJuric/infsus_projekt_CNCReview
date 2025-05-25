from fastapi import APIRouter
from schemas.recenzija import RecenzijaBase
from dependencies import db_dependency
from models.recenzija import Recenzije as recenzija_model
from models.korisnik import Korisnici as korisnik_model
from models.objekt import Objekti as objekt_model
from models.ocjena import Ocjene as ocjena_model
from fastapi import HTTPException


router = APIRouter(prefix="/recenzija", tags=["recenzija"])

@router.post("/createRecenzija")
async def create_recenzija(recenzija: RecenzijaBase, db: db_dependency):
    if not db.query(korisnik_model).filter(korisnik_model.korisnik_id == recenzija.korisnik_id).first():
        raise HTTPException(status_code=404, detail="Korisnik not found")
    if not db.query(objekt_model).filter(objekt_model.objekt_id == recenzija.objekt_id).first():
        raise HTTPException(status_code=404, detail="Objekt not found")
    if not db.query(ocjena_model).filter(ocjena_model.ocjena_id == recenzija.ocjena_id).first():
        raise HTTPException(status_code=404, detail="Ocjena not found")

    db_recenzija = recenzija_model(
        korisnik_id=recenzija.korisnik_id,
        objekt_id=recenzija.objekt_id,
        ocjena_id=recenzija.ocjena_id,
        naslov=recenzija.naslov,
        sadrzaj=recenzija.sadrzaj,
    )

    db.add(db_recenzija)
    db.commit()
    db.refresh(db_recenzija)
    return db_recenzija

@router.get("/getRecenzijeByObjekt/{objekt_id}")
async def get_recenzije_by_objekt(objekt_id: int, db: db_dependency):
    recenzije = db.query(recenzija_model).filter(recenzija_model.objekt_id == objekt_id).all()
    if not recenzije:
        raise HTTPException(status_code=404, detail="No reviews found for this object")
    return recenzije

@router.delete("/deleteRecenzija/{id}")
async def delete_recenzija(id: int, db: db_dependency):
    db_recenzija = db.query(recenzija_model).filter(recenzija_model.recenzija_id == id).first()
    if not db_recenzija:
        raise HTTPException(status_code=404, detail="Recenzija not found")
    
    db.delete(db_recenzija)
    db.commit()
    return {"detail": "Recenzija deleted successfully"}

@router.post("/updateRecenzija/{id}")
async def update_recenzija(id: int, recenzija: RecenzijaBase, db: db_dependency):
    db_recenzija = db.query(recenzija_model).filter(recenzija_model.recenzija_id == id).first()
    if not db_recenzija:
        raise HTTPException(status_code=404, detail="Recenzija not found")

    if recenzija.korisnik_id:
        if not db.query(korisnik_model).filter(korisnik_model.korisnik_id == recenzija.korisnik_id).first():
            raise HTTPException(status_code=404, detail="Korisnik not found")
        db_recenzija.korisnik_id = recenzija.korisnik_id

    if recenzija.objekt_id:
        if not db.query(objekt_model).filter(objekt_model.objekt_id == recenzija.objekt_id).first():
            raise HTTPException(status_code=404, detail="Objekt not found")
        db_recenzija.objekt_id = recenzija.objekt_id

    if recenzija.ocjena_id:
        if not db.query(ocjena_model).filter(ocjena_model.ocjena_id == recenzija.ocjena_id).first():
            raise HTTPException(status_code=404, detail="Ocjena not found")
        db_recenzija.ocjena_id = recenzija.ocjena_id

    db_recenzija.naslov = recenzija.naslov
    db_recenzija.sadrzaj = recenzija.sadrzaj

    db.commit()
    db.refresh(db_recenzija)
    return db_recenzija
