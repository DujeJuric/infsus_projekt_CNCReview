from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from . import Base


class Nocni_klubovi(Base):
    __tablename__ = 'Nocni_klub'

    objekt_id = Column(Integer, ForeignKey("Objekt.objekt_id"), primary_key=True)
    stil_glazbe = Column(Text, index=True)
    cijena_ulaza = Column(Integer, index=True)
    