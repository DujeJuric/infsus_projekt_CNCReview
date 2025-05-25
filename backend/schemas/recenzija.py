from pydantic import BaseModel

class RecenzijaBase(BaseModel):

    sadrzaj : str
    naslov : str
    ocjena_id : int
    objekt_id : int
    korisnik_id : int
