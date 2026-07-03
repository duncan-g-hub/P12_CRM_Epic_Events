import jwt
import bcrypt
import time
import os
from dotenv import load_dotenv

from models.models import Collaborator
import database

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_EXPIRATION_HOURS = 8


def login(email, password):
    """
    Authenticate a collaborator and return a JWT token.

    Raises:
        ValueError: If email not found or password is incorrect.
    """
    session = database.get_session()
    collaborator = session.query(Collaborator).filter(Collaborator.email == email).first()

    if not collaborator:
        raise ValueError("Email introuvable.")

    if not bcrypt.checkpw(password.encode("utf-8"), collaborator.password.encode("utf-8")):
        raise ValueError("Mot de passe incorrect.")

    token = jwt.encode(
        {
            "id": collaborator.id,
            "role": collaborator.role.name,
            "exp": int(time.time()) + (TOKEN_EXPIRATION_HOURS * 3600)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token, collaborator


def decode_token(token: str) -> dict:
    """
    Decode and validate a JWT token.

    Raises:
        PermissionError: If token is expired or invalid.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise PermissionError("Token expiré.")
    except jwt.InvalidTokenError:
        raise PermissionError("Token invalide.")
