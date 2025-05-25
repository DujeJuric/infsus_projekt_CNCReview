from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from . import Base

class Admin(Base):
    __tablename__ = 'Admin'

    admin_id = Column(Integer, primary_key=True, index=True)
    email = Column(Text, index=True)
    lozinka = Column(Text, index=True)