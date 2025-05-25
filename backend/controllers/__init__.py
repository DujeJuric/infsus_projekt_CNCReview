from .korisnik import router as korisnik_router
from .recenzija import router as recenzija_router
from .grad import router as grad_router
from .ocjena import router as ocjena_router
from .objekt import router as objekt_router
from .vlasnik import router as vlasnik_router
from .admin import router as admin_router
from .vlasnistvo import router as vlasnistvo_router


routers = [
    korisnik_router,
    recenzija_router,
    grad_router,
    ocjena_router,
    objekt_router,
    vlasnik_router,
    admin_router,
    vlasnistvo_router
    
]