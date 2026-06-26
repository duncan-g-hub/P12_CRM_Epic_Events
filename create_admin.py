import bcrypt
from database import session
from models.models import Collaborator, Role

role = session.query(Role).filter(Role.name == "gestion").first()
hashed = bcrypt.hashpw("Admin1234".encode(), bcrypt.gensalt())
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
