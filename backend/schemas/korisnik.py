from pydantic import BaseModel

class KorisnikBase(BaseModel):

    ime : str
    prezime : str
    lozinka : str
    email : str