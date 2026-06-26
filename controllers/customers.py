from models.models import Customer
from database import session
from auth.permissions import require_role
from views.views import view_display_customer
from auth.auth import decode_token
from validators import validate_email, validate_phone


@require_role("commercial")
def create_customer(token, name, email, phone, company_name, commercial_id):
    validate_email(email)
    validate_phone(phone)
    existing = session.query(Customer).filter(Customer.email == email).first()
    if existing:
        raise ValueError(f"L'email '{email}' est déjà utilisé.")

    customer = Customer(name=name,
                        email=email,
                        phone=phone,
                        company_name=company_name,
                        commercial_id=int(commercial_id)
                        )
    # gestion d'erreur à gerer (adresse email unique)
    session.add(customer)
    session.commit()
    return customer


@require_role("commercial")
def update_customer(token, customer_id, name, email, phone, company_name):
    payload = decode_token(token)
    collaborator_id = payload.get("id")

    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise ValueError("Client introuvable.")

    if customer.commercial_id != collaborator_id:
        raise PermissionError("Vous ne pouvez modifier que les clients dont vous êtes responsable.")
    if name:
        customer.name = name
    if email:
        validate_email(email)
        customer.email = email
    if phone:
        validate_phone(phone)
        customer.phone = phone
    if company_name:
        customer.company_name = company_name

    session.commit()
    return customer


@require_role("gestion")
def update_customer_commercial(token, customer_id, commercial_id):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise ValueError("Client introuvable.")

    if commercial_id:
        customer.commercial_id = commercial_id

    session.commit()
    return customer


@require_role("gestion", "commercial", "support")
def display_customer(token, customer_id):
    customer = session.get(Customer, customer_id)
    view_display_customer(customer)


def get_customers():
    customers = session.query(Customer).all()
    if not customers:
        raise ValueError("Clients introuvables.")
    liste = "\n".join(
        f" nom : {c.name} (id : {c.id})" for c in customers)
    valid_ids = [str(c.id) for c in customers]
    return liste, valid_ids
