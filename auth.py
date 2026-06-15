import jwt
import bcrypt
import time
from models.models import Collaborator
from database import session

SECRET_KEY = "secret"  # à mettre dans une variable d'environnement
ALGORITHM = "HS256"
TOKEN_EXPIRATION_HOURS = 8


def login(email: str, password: str) -> str | None:
    collaborator = session.query(Collaborator).filter(Collaborator.email == email).first()

    if not collaborator:
        raise ValueError("Email introuvable.")

    if not bcrypt.checkpw(password.encode("utf-8"), collaborator.password.encode("utf-8")):
        raise ValueError("Mot de passe incorrect.")

    token = jwt.encode(
        {
            "collaborator_id": collaborator.id,
            "role": collaborator.role.name,
            "exp": int(time.time()) + (TOKEN_EXPIRATION_HOURS * 3600)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token, collaborator


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise PermissionError("Token expiré.")
    except jwt.InvalidTokenError:
        raise PermissionError("Token invalide.")


if __name__ == "__main__":
    login()