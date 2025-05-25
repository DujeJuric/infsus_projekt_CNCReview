from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from . import Base

class Korisnici(Base):
    __tablename__ = 'Korisnik'

    korisnik_id = Column(Integer, primary_key = True, index = True)
    ime = Column(Text, index = True)
    prezime = Column(Text, index = True)
    lozinka = Column(Text, index = True)
    email = Column(Text, index = True)