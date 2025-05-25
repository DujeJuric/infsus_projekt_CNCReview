from fastapi import APIRouter
from schemas.admin import AdminBase
from dependencies import db_dependency
from models.admin import Admin as admin_model

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/createAdmin")
async def create_admin(admin: AdminBase, db: db_dependency):
    db_admin = admin_model(
        lozinka=admin.lozinka,
        email=admin.email
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

@router.get("/getAllAdmin")
async def get_all_admin(db: db_dependency):
    return db.query(admin_model).all()

@router.delete("/deleteAdmin/{id}")
async def delete_admin(id: int, db: db_dependency):
    db_admin = db.query(admin_model).filter(admin_model.admin_id == id).first()
    if not db_admin:
        return {"message": "Admin not found"}
    
    db.delete(db_admin)
    db.commit()
    return {"message": "Admin deleted successfully"}