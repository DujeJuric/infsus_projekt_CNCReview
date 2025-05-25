from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from models import Base
from schemas import korisnik, recenzija
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from controllers import routers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

for router in routers:
    app.include_router(router)

