from pydantic import BaseModel

class Nocni_klubBase(BaseModel):
    stil_glazbe: str
    cijena_ulaza: int