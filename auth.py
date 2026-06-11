import jwt
import bcrypt
import time
from models.models import Collaborator
from database import session

SECRET_KEY = "secret"  # à mettre dans une variable d'environnement
ALGORITHM = "HS256"
TOKEN_EXPIRATION_HOURS = 8


def login():
    email = input("Saisir votre adresse email : ")

    collaborator = session.query(Collaborator).filter(Collaborator.email == email).first()
    # verif email
    if not collaborator:
        print("Email introuvable.")
        return None


    password = input("Saisir votre mot de passe :")

    # verif mdp
    if not bcrypt.checkpw(password.encode("utf-8"), collaborator.password.encode("utf-8")):
        print("Mot de passe incorrect.")
        return None

    # Génération du token
    payload = {
        "collaborator_id": collaborator.id,
        "role": collaborator.role.name,
        "expiration": int(time.time()) + (TOKEN_EXPIRATION_HOURS * 3600)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Connecté en tant que {collaborator.name} ({collaborator.role.name})")
    return token


if __name__ == "__main__":
    login()