from sqlalchemy.orm import declarative_base

Base = declarative_base()

from . import korisnik
from . import recenzija
from . import objekt
from . import kafic
from . import nocni_klub
from . import grad
from . import vlasnistvo
from . import vlasnik
from . import admin
from . import ocjena