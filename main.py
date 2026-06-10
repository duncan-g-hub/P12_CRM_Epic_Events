from database import engine

from models.models import Base, Collaborator, Customer, Contract, Event



# Créer les tables
# Base.metadata.drop_all(engine)   # supprime toutes les tables
Base.metadata.create_all(engine)
