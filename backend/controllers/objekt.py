from fastapi import APIRouter
from schemas.objekt import ObjektBase
from dependencies import db_dependency
from models.objekt import Objekti as objekt_model
from models.kafic import Kafici as kafic_model
from models.nocni_klub import Nocni_klubovi as nocni_klub_model
from models.grad import Gradovi as grad_model
from models.vlasnistvo import Vlasnistvo as vlasnistvo_model
from fastapi import HTTPException
from sqlalchemy.orm import Session


router = APIRouter(prefix="/objekt", tags=["objekt"])

def get_objekt_with_details(objekt_id, db: Session = None):
    objekt = db.query(objekt_model).filter(objekt_model.objekt_id == objekt_id).first()
    
    if not objekt:
        raise HTTPException(status_code=404, detail="Objekt not found")

    response = {
        "objekt_id": objekt.objekt_id,
        "naziv": objekt.naziv,
        "adresa": objekt.adresa,
        "opis": objekt.opis,
        "radno_vrijeme": objekt.radno_vrijeme,
        "radni_dani": objekt.radni_dani,
        "mobilni_broj": objekt.mobilni_broj,
        "vlasnistvo_id": objekt.vlasnistvo_id,
        "grad_id": objekt.grad_id
    }

    nocni_klub = db.query(nocni_klub_model).filter(nocni_klub_model.objekt_id == objekt_id).first()
    if nocni_klub:
        response.update({
            "tip": "nocni_klub",
            "stil_glazbe": nocni_klub.stil_glazbe,
            "cijena_ulaza": nocni_klub.cijena_ulaza
        })
        return response

    kafic = db.query(kafic_model).filter(kafic_model.objekt_id == objekt_id).first()
    if kafic:
        response.update({
            "tip": "kafic",
            "dozvoljeno_pusenje": kafic.dozvoljeno_pusenje,
            "ponuda_hrane": kafic.ponuda_hrane
        })
    
    return response

@router.get("/getObjektById/{id}")
async def get_objekt_by_id(id: int, db: db_dependency):
    objekt = get_objekt_with_details(id, db)
    if not objekt:
        raise HTTPException(status_code=404, detail="Objekt not found")
    return objekt

@router.post("/createObjekt")
async def create_objekt(objekt: ObjektBase, db: db_dependency):

    if not db.query(grad_model).filter(grad_model.grad_id == objekt.grad_id).first():
        raise HTTPException(status_code=404, detail="Grad not found")
    if not db.query(vlasnistvo_model).filter(vlasnistvo_model.vlasnistvo_id == objekt.vlasnistvo_id).first():
        raise HTTPException(status_code=404, detail="Vlasnistvo not found")
    
    db_objekt = objekt_model(
        naziv=objekt.naziv,
        adresa=objekt.adresa,
        opis=objekt.opis,
        radno_vrijeme=objekt.radno_vrijeme,
        radni_dani=objekt.radni_dani,
        mobilni_broj=objekt.mobilni_broj,
        vlasnistvo_id=objekt.vlasnistvo_id,
        grad_id=objekt.grad_id
    )
    db.add(db_objekt)
    db.commit()
    db.refresh(db_objekt)
    return db_objekt

@router.get("/getAllObjekt")
async def gett_all_objekt(db: db_dependency):
    db_objekti = db.query(objekt_model).all()
    response = []
    for objekt in db_objekti:
        objekt_details = get_objekt_with_details(objekt.objekt_id, db)
        if objekt_details:
            response.append(objekt_details)
    return response

@router.post("/editObjekt/{objekt_id}")
async def edit_objekt(objekt_id: int, objekt: ObjektBase, db: db_dependency):

    if not db.query(grad_model).filter(grad_model.grad_id == objekt.grad_id).first():
        raise HTTPException(status_code=404, detail="Grad not found")
    if not db.query(vlasnistvo_model).filter(vlasnistvo_model.vlasnistvo_id == objekt.vlasnistvo_id).first():
        raise HTTPException(status_code=404, detail="Vlasnistvo not found")
    
    db_objekt = db.query(objekt_model).filter(objekt_model.objekt_id == objekt_id).first()
    db_objekt.naziv = objekt.naziv
    db_objekt.adresa = objekt.adresa
    db_objekt.opis = objekt.opis
    db_objekt.radno_vrijeme = objekt.radno_vrijeme
    db_objekt.radni_dani = objekt.radni_dani
    db_objekt.mobilni_broj = objekt.mobilni_broj
    db_objekt.vlasnistvo_id = objekt.vlasnistvo_id
    db_objekt.grad_id = objekt.grad_id
    db.commit()
    db.refresh(db_objekt)
    return get_objekt_with_details(db_objekt.objekt_id, db)

@router.delete("/deleteObjekt/{objekt_id}")
async def delete_objekt(objekt_id: int, db: db_dependency):
    db_objekt = db.query(objekt_model).filter(objekt_model.objekt_id == objekt_id).first()
    if not db_objekt:
        raise HTTPException(status_code=404, detail="Objekt not found")
    db.delete(db_objekt)
    db.commit()
    return {"message": "Objekt deleted successfully"}


# @router.get("/getObjektByGradId/{grad_id}")
# async def get_objekt_by_grad_id(grad_id: int, db: db_dependency):
#     objekti = db.query(objekt_model).filter(objekt_model.grad_id == grad_id).all()
#     if not objekti:
#         raise HTTPException(status_code=404, detail="No objekti found for this grad")
    
#     response = []
#     for objekt in objekti:
#         objekt_details = get_objekt_with_details(objekt.objekt_id)
#         if objekt_details:
#             response.append(objekt_details)
    
#         return response
    

# @router.get("/getAllNocniKlubObjekt")
# async def get_all_nocni_klub_objekt(db: db_dependency):
#     db_objekti = db.query(objekt_model).all()
#     response = []

#     for objekt in db_objekti:
#         objekt_details = get_objekt_with_details(objekt.objekt_id)
#         if objekt_details and objekt_details.get("tip") == "nocni_klub":
#             response.append(objekt_details)

#     return response


# @router.get("/getAllKaficObjekt")
# async def get_all_kafic_objekt(db: db_dependency):
#     db_objekti = db.query(objekt_model).all()
#     response = []

#     for objekt in db_objekti:
#         objekt_details = get_objekt_with_details(objekt.objekt_id)
#         if objekt_details and objekt_details.get("tip") == "kafic":
#             response.append(objekt_details)

#     return response
    







   

    
