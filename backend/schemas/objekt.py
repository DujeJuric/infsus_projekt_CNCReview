from pydantic import BaseModel

class ObjektBase(BaseModel):
    naziv: str
    adresa: str
    opis: str
    radno_vrijeme: str
    radni_dani: str
    mobilni_broj: str
    vlasnistvo_id: int
    grad_id: int
    
    