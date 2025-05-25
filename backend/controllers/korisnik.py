from fastapi import APIRouter
from schemas.korisnik import KorisnikBase
from dependencies import db_dependency
from models.korisnik import Korisnici as korisnik_model

router = APIRouter(prefix="/korisnik", tags=["korisnik"])

@router.post("/createKorisnik")
async def create_korisnik(korisnik: KorisnikBase, db: db_dependency):
    db_korisnik = korisnik_model(
        ime = korisnik.ime,
        prezime = korisnik.prezime,
        lozinka = korisnik.lozinka,
        email = korisnik.email
    )
    db.add(db_korisnik)
    db.commit()
    db.refresh(db_korisnik)
    return db_korisnik

@router.get("/getAllKorisnik")
async def get_all_korisnik(db: db_dependency):
    return db.query(korisnik_model).all()

@router.delete("/deleteKorisnik/{id}")
async def delete_korisnik(id: int, db: db_dependency):
    db_korisnik = db.query(korisnik_model).filter(korisnik_model.korisnik_id == id).first()
    if not db_korisnik:
        return {"message": "Korisnik not found"}
    
    db.delete(db_korisnik)
    db.commit()
    return {"message": "Korisnik deleted successfully"}


    