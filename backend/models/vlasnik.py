from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from . import Base

class Vlasnik(Base):
    __tablename__ = 'Vlasnik'

    vlasnik_id = Column(Integer, primary_key=True, index=True)
    naziv = Column(Text, index=True)
    email = Column(Text, index=True)
    lozinka = Column(Text, index=True)
    