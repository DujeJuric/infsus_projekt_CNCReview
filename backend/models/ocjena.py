from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from . import Base

class Ocjene(Base):
    __tablename__ = 'Ocjena'

    ocjena_id = Column(Integer, primary_key=True, index=True)
    ocjena = Column(Text, index=True)
 