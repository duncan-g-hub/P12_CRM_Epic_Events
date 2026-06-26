from datetime import datetime
import re


def validate_date(date):
    """Parse and return a date. Accepts datetime or DD/MM/YYYY string."""
    if isinstance(date, datetime):
        return date
    try:
        return datetime.strptime(date, "%d/%m/%Y")
    except ValueError:
        raise ValueError("Format de date invalide, veuillez saisir une date au format JJ/MM/AAAA")


def validate_future_date(date):
    """Validate that a date is not in the past."""
    date = validate_date(date)
    if date < datetime.now():
        raise ValueError("La date ne peut pas être dans le passé")
    return date


def validate_date_end(date_start, date_end):
    """Validate that end date is not before start date."""
    date_end = validate_date(date_end)
    if date_start > date_end:
        raise ValueError("La date de fin ne peut pas etre antérieur à la date de départ")
    return date_end


def validate_phone(phone):
    """Validate French phone number format."""
    if not re.match(r"^(0|\+33)\d{9}$", phone):
        raise ValueError("Format de n° de téléphone invalide (ex: 0612345678)")
    return phone


def validate_email(email):
    """Validate email format."""
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]"
    if not re.match(pattern, email):
        raise ValueError("Format d'email invalide (ex: mon-email@email.com)")
    return email


def validate_password(password):
    """Validate password: min 8 chars and at least one uppercase letter."""
    if len(password) < 8:
        raise ValueError("Mot de passe invalide : 8 caractères minimum")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Mot de passe invalide : Au moins une majuscule requise")
    return password


def validate_amount_to_pay(amount, total_amount):
    """Validate that amount to pay does not exceed total amount."""
    amount = validate_float(amount)
    if amount > total_amount:
        raise ValueError("Le montant restant à payer ne peut pas être supérieur au montant total.")
    return amount


def validate_float(value):
    """Parse and return a float value."""
    try:
        return float(value)
    except ValueError:
        raise ValueError("Format de valeur invalide (ex: 3.14)")


def validate_integer(value):
    """Parse and return an integer value."""
    try:
        return int(value)
    except ValueError:
        raise ValueError("Format de valeur invalide (ex: 31)")
