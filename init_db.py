from database import engine, session
from models.models import Base, Role, Collaborator
import bcrypt

def init_db():
    """Initialize the database: create tables, seed roles, and create default admin if needed."""
    # Base.metadata.drop_all(engine)   # supprime toutes les tables (à supprimer lors du passage en prod)
    Base.metadata.create_all(engine)  # Créer les tables

    if not session.query(Role).first():
        session.add_all([
            Role(name="commercial"),
            Role(name="support"),
            Role(name="gestion"),
        ])
        session.commit()

    if not session.query(Collaborator).filter(Collaborator.email == "admin@crm.com").first():
        role = session.query(Role).filter(Role.name == "gestion").first()
        hashed = bcrypt.hashpw("Admin12345".encode(), bcrypt.gensalt())
        session.add(Collaborator(
            name="Admin",
            email="admin@crm.com",
            password=hashed.decode("utf-8"),
            phone="0600000000",
            role_id=role.id
        ))
        session.commit()
        print("Admin créé - pensez à changer le mot de passe !")

if __name__ == "__main__":
    init_db()