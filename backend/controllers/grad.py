from fastapi import APIRouter
from schemas.grad import GradBase
from dependencies import db_dependency
from models.grad import Gradovi as grad_model

router = APIRouter(prefix="/grad", tags=["grad"])

@router.post("/createGrad")
async def create_grad(grad: GradBase, db: db_dependency):
    db_grad = grad_model(
        naziv=grad.naziv
    )
    db.add(db_grad)
    db.commit()
    db.refresh(db_grad)
    return db_grad

@router.get("/getAllGradovi")
async def get_all_gradovi(db: db_dependency):
    return db.query(grad_model).all()

@router.post("/editGrad/{grad_id}")
async def edit_grad(grad_id: int, grad: GradBase, db: db_dependency):
    db_grad = db.query(grad_model).filter(grad_model.grad_id == grad_id).first()
    if not db_grad:
        return {"error": "Grad not found"}
    db_grad.naziv = grad.naziv
    db.commit()
    db.refresh(db_grad)
    return db_grad

@router.delete("/deleteGrad/{grad_id}")
async def delete_grad(grad_id: int, db: db_dependency):
    db_grad = db.query(grad_model).filter(grad_model.grad_id == grad_id).first()
    if not db_grad:
        return {"error": "Grad not found"}
    db.delete(db_grad)
    db.commit()
    return {"message": "Grad deleted successfully"}