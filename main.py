from database import engine, session

from models.models import Base, Role, Collaborator, Customer, Contract, Event



# Créer les tables
# Base.metadata.drop_all(engine)   # supprime toutes les tables
Base.metadata.create_all(engine)

# Alimenter les rôles si la table est vide
if not session.query(Role).first():
    session.add_all([
        Role(name="commercial"),
        Role(name="support"),
        Role(name="gestion"),
    ])
    session.commit()