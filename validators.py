from datetime import datetime
import re


def validate_date(date: str) -> datetime:
    format = "%d/%m/%Y"
    try:
        datetime.strptime(date, format)
    except ValueError:
        print(f"Format de date invalide, veuillez saisir une date au format JJ/MM/AAAA")
    return date

def validate_phone(phone):
    if not re.fullmatch(r"^(0|\+33)\d{9}$", phone):
        raise ValueError("Format de n° de téléphone invalide (ex: 0612345678)")
    return phone

def validate_email(email):
    pattern = "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]"
    if not re.fullmatch(pattern, email):
        raise ValueError("Format d'email invalide (ex: mon-email@email.com)")
    return email


def validate_password(password):
    if len(password) < 8:
        raise ValueError("Mot de passe invalide : 8 caractères minimum")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Mot de passe invalide : Au moins une majuscule requise")
    return password