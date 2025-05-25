from pydantic import BaseModel

class VlasnikBase(BaseModel):
    naziv: str
    email: str
    lozinka: str