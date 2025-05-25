from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from . import Base

class Vlasnistvo(Base):
    __tablename__ = 'Vlasnistvo'

    vlasnistvo_id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("Admin.admin_id"))
    vlasnik_id = Column(Integer, ForeignKey("Vlasnik.vlasnik_id"))