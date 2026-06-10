import bcrypt
from getpass import getpass

from models.models import Collaborator
from views.collaborators import get_collaborators_data_from_form
from main import session


def create_collaborator():
    name, email, password, phone, role = get_collaborators_data_from_form()
    # hachage du mdp :
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # penser au hachage / salage mdp
    collaborator = Collaborator(name=name,
                           email=email,
                           password=hashed_password.decode("utf-8"),
                           phone=phone,
                           role=role)
    session.add(collaborator)
    session.commit()







def get_commercials():
    commercials = session.query(Collaborator).filter(Collaborator.role == "commercial").all()
    return commercials

def get_supports():
    supports = session.query(Collaborator).filter(Collaborator.role == "support").all()
    return supports

def get_managers():
    managers = session.query(Collaborator).filter(Collaborator.role == "gestion").all()
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
    # creer_collaborateur()
    get_commercials()