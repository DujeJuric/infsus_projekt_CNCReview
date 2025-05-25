from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from . import Base

class Gradovi(Base):
    __tablename__ = 'Grad'

    grad_id = Column(Integer, primary_key=True, index=True)
    naziv = Column(Text, index=True)
 