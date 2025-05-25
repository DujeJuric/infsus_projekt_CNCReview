from pydantic import BaseModel

class KaficBase(BaseModel):
    dozoljeno_pusenje: bool
    ponuda_hrane: bool