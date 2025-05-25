from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from . import Base


class Recenzije(Base):
    __tablename__ = 'Recenzija'

    recenzija_id = Column(Integer, primary_key = True, index = True)
    sadrzaj = Column(Text, index = True)
    naslov = Column(Text, index = True)
    korisnik_id = Column(Integer, ForeignKey("Korisnik.korisnik_id"))
    objekt_id = Column(Integer, ForeignKey("Objekt.objekt_id"))
    ocjena_id = Column(Integer, ForeignKey("Ocjena.ocjena_id"))