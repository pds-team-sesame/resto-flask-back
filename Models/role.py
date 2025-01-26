from sqlalchemy import Enum
import enum

class Role(enum.Enum):
    ADMIN = "admin"
    GERANT = "gerant"
    CLIENT = "client"
    LIVREUR = "livreur"

