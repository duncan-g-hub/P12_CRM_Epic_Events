"""
One-time script to create the default admin collaborator.
Run once after initial database setup.
"""

import bcrypt
from database import session
from models.models import Collaborator, Role
try:
    existing = session.query(Collaborator).filter(Collaborator.email == "admin@crm.com").first()
    if existing:
        raise ValueError(f"L'utilisateur admin existe déja.")
    role = session.query(Role).filter(Role.name == "gestion").first()
    hashed = bcrypt.hashpw("Admin12345".encode(), bcrypt.gensalt())
    admin = Collaborator(
        name="Admin",
        email="admin@crm.com",
        password=hashed.decode("utf-8"),
        phone="0600000000",
        role_id=role.id
    )
    session.add(admin)
    session.commit()
    print("Admin créé.")
except ValueError as e:
    print(e)