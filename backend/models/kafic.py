from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from . import Base


class Kafici(Base):
    __tablename__ = 'Kafic'

    objekt_id = Column(Integer, ForeignKey("Objekt.objekt_id"), primary_key=True)
    dozvoljeno_pusenje = Column(Boolean, index=True)
    ponuda_hrane = Column(Boolean, index=True)