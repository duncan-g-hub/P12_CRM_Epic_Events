import bcrypt

from models.models import Collaborator, Role
from database import session
from auth.permissions import require_role
from views.views import view_display_collaborator


@require_role("gestion")
def create_collaborator(token, name, email, password, phone, role_id):
    # hachage du mdp :
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    existing = session.query(Collaborator).filter(Collaborator.email == email).first()
    if existing:
        raise ValueError(f"L'email '{email}' est déjà utilisé.")
    collaborator = Collaborator(name=name,
                                email=email,
                                password=hashed_password.decode("utf-8"),
                                phone=phone,
                                role_id=int(role_id))

    session.add(collaborator)
    session.commit()
    return collaborator


@require_role("gestion")
def update_collaborator(token, collaborator_id, name, email, password, phone, role_id):
    collaborator = session.query(Collaborator).filter(Collaborator.id == collaborator_id).first()

    if name:
        collaborator.name = name
    if email:
        existing = session.query(Collaborator).filter(
            Collaborator.email == email,
            Collaborator.id != collaborator_id
        ).first()
        if existing:
            raise ValueError(f"L'email '{email}' est déjà utilisé.")
        collaborator.email = email
    if password:
        # hachage du mdp :
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        collaborator.password = hashed_password.decode("utf-8")
    if phone:
        collaborator.phone = phone
    if role_id:
        collaborator.role_id = int(role_id)

    session.commit()
    return collaborator


@require_role("gestion", "commercial", "support")
def display_collaborator(token, collaborator_id):
    collaborator = session.get(Collaborator, collaborator_id)
    view_display_collaborator(collaborator, collaborator.role.name)


def get_commercials():
    commercials = session.query(Collaborator).join(Collaborator.role).filter(Role.name == "commercial").all()
    liste = "\n".join(
        f" id : {c.id} - Nom : {c.name}" for c in commercials)
    valid_ids = [str(c.id) for c in commercials]
    return liste, valid_ids


def get_supports():
    supports = session.query(Collaborator).join(Collaborator.role).filter(Role.name == "support").all()
    liste = "\n".join(
        f" id : {s.id} - Nom : {s.name}" for s in supports)
    valid_ids = [str(s.id) for s in supports]
    return liste, valid_ids


def get_collaborators():
    collaborators = session.query(Collaborator).all()
    liste = "\n".join(
        f" nom : {c.name} (id : {c.id})" for c in collaborators)
    valid_ids = [str(c.id) for c in collaborators]
    return liste, valid_ids
