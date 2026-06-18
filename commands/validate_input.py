from datetime import datetime
import re


def validate_date(prompt: str) -> datetime:
    format = "%d/%m/%Y"
    while True:
        saisie = input(prompt).strip()
        try:
            return datetime.strptime(saisie, format)
        except ValueError:
            print(f"Format invalide, veuillez saisir une date au format JJ/MM/AAAA")


def validate_phone(phone):
    if not re.match(r"^\+?[\d\s\-]{10,15}$", phone):
        raise ValueError("Format invalide (ex: 0612345678)")


def validate_password(password):
    if len(password) < 8:
        raise ValueError("8 caractères minimum")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Au moins une majuscule requise")
