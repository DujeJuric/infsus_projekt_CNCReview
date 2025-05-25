from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


URL_DATABASE = 'postgresql://postgres:duje@localhost:5432/CNCReviewDB'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)
