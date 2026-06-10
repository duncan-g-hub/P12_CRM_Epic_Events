import bcrypt

from models.models import Collaborator, Role
from views.collaborators import display_collaborator_form
from database import session


def create_collaborator():
    name, email, password, phone, role_id = display_collaborator_form()
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







def get_commercials():
    commercials = session.query(Collaborator).join(Collaborator.role).filter(Role.name == "commercial").all()
    return commercials

def get_supports():
    supports = session.query(Collaborator).join(Collaborator.role).filter(Role.name == "support").all()
    return supports

def get_managers():
    managers = session.query(Collaborator).join(Collaborator.role).filter(Role.name == "gestion").all()
    return managers








# # controler le mdp :
# import bcrypt
#
# mot_de_passe_saisi = "monMotDePasse123"
# hashed_en_base = b'$2b$12$...'  # récupéré depuis la DB
#
# if bcrypt.checkpw(mot_de_passe_saisi.encode("utf-8"), hashed_en_base):
#     print("Mot de passe correct")
# else:
#     print("Mot de passe incorrect")


if __name__ == '__main__':
    create_collaborator()

    # from views.collaborators import display_collaborators
    # display_collaborators(get_commercials())
