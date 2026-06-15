import bcrypt

from models.models import Collaborator, Role
from views.collaborators import display_collaborator_form
from database import session

from permissions import require_role

@require_role("gestion")
def create_collaborator(token, name, email, password, phone, role_id):
    # name, email, password, phone, role_id = display_collaborator_form()
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







def get_commercials():
    commercials = session.query(Collaborator).join(Collaborator.role).filter(Role.name == "commercial").all()
    liste = "\n".join(
        f" id : {c.id} - Nom : {c.name} - email : {c.email} - téléphone : {c.phone}" for c in commercials)
    valid_ids = [str(c.id) for c in commercials]
    return liste, valid_ids

def get_supports():
    supports = session.query(Collaborator).join(Collaborator.role).filter(Role.name == "support").all()
    return supports

def get_managers():
    managers = session.query(Collaborator).join(Collaborator.role).filter(Role.name == "gestion").all()
    return managers




if __name__ == '__main__':
    create_collaborator()

    # from views.collaborators import display_collaborators
    # display_collaborators(get_commercials())
