from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base, Collaborator, Customer, Contract, Event




engine = create_engine(
    "mysql+mysqlconnector://admin:admin@localhost/epic_events_CRM",
    echo=True
)

# Session
Session = sessionmaker(bind=engine)
session = Session()


# Créer les tables
# Base.metadata.drop_all(engine)   # supprime toutes les tables
Base.metadata.create_all(engine)
