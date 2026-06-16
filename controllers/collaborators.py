import bcrypt

from models.models import Collaborator, Role
from database import session
from permissions import require_role
from views.collaborators import view_display_collaborator

@require_role("gestion")
def create_collaborator(token, name, email, password, phone, role_id):

    # hachage du mdp :
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    collaborator = Collaborator(name=name,
                           email=email,
                           password=hashed_password.decode("utf-8"),
                           phone=phone,
                           role_id=int(role_id))

    # gestion d'erreur à gerer (adresse email unique etc)
    session.add(collaborator)
    session.commit()
    return collaborator



def get_collaborator_name(collaborator_id):
    collaborator_name = session.query(Collaborator.name).filter(Collaborator.id == collaborator_id).scalar()
    return collaborator_name

def get_collaborator_role(collaborator_role_id):
    collaborator_role = session.query(Role.name).filter(collaborator_role_id == Role.id).scalar()
    return collaborator_role


def get_commercials():
    commercials = session.query(Collaborator).join(Collaborator.role).filter(Role.name == "commercial").all()
    liste = "\n\n".join(
        f"id : {c.id} - Nom : {c.name} \nemail : {c.email} - téléphone : {c.phone}" for c in commercials)
    valid_ids = [str(c.id) for c in commercials]
    return liste, valid_ids

def get_supports():
    supports = session.query(Collaborator).join(Collaborator.role).filter(Role.name == "support").all()
    liste = "\n\n".join(
        f"id : {s.id} - Nom : {s.name} \nemail : {s.email} - téléphone : {s.phone}" for s in supports)
    valid_ids = [str(s.id) for s in supports]
    return liste, valid_ids

def get_managers():
    managers = session.query(Collaborator).join(Collaborator.role).filter(Role.name == "gestion").all()
    liste = "\n\n".join(
        f"id : {m.id} - Nom : {m.name} \nemail : {m.email} - téléphone : {m.phone}" for m in managers)
    valid_ids = [str(m.id) for m in managers]
    return liste, valid_ids


def get_collaborators():
    collaborators = session.query(Collaborator).all()
    liste = "\n\n".join(
        f"id : {c.id} - Nom : {c.name} \nemail : {c.email} - téléphone : {c.phone}"
        f"\nrole : {get_collaborator_role(c.role_id)}" for c in collaborators)
    valid_ids = [str(c.id) for c in collaborators]
    return liste, valid_ids



@require_role("gestion", "commercial", "support")
def display_collaborator(token, collaborator_id):
    collaborator = session.query(Collaborator).get(collaborator_id)
    view_display_collaborator(collaborator, get_collaborator_role(collaborator.role_id))


if __name__ == '__main__':
    liste, valid_ids = get_collaborators()
    print(liste)

    # from views.collaborators import display_collaborators
    # display_collaborators(get_commercials())
