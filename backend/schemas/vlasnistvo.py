
from pydantic import BaseModel

class VlasnistvoBase(BaseModel):
    admin_id: int
    vlasnik_id: int
    