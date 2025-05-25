from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from . import Base

class Objekti(Base):
    __tablename__ = 'Objekt'

    objekt_id = Column(Integer, primary_key = True, index = True)
    naziv = Column(Text, index = True)
    adresa = Column(Text, index = True)
    opis = Column(Text, index = True)
    radno_vrijeme = Column(Text, index = True)
    radni_dani = Column(Text, index = True)
    mobilni_broj = Column(Text, index = True)
    vlasnistvo_id = Column(Integer, ForeignKey("Vlasnistvo.vlasnistvo_id"))
    grad_id = Column(Integer, ForeignKey("Grad.grad_id"))