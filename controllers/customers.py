from models.models import Customer
from database import session
from auth.permissions import require_role
from views.views import view_display_customer
from auth.auth import decode_token

@require_role("commercial")
def create_customer(token, name, email, phone, company_name, commercial_id):

    customer = Customer(name=name,
                    email=email,
                    phone=phone,
                    company_name=company_name,
                    commercial_id=int(commercial_id)
                    )

    #gestion d'erreur à gerer (adresse email unique etc)

    session.add(customer)
    session.commit()
    return customer


@require_role("commercial")
def update_customer(token, customer_id, name, email, phone, company_name, commercial_id):
    # Récupération de l'id collab depuis le token
    payload = decode_token(token)
    collaborator_id = payload.get("id")

    customer = session.query(Customer).filter(Customer.id == customer_id).first()

    #uniquement les clients dont ils sont responsables
    if customer.commercial_id != collaborator_id:
        raise PermissionError("Vous ne pouvez modifier que les clients dont vous êtes responsable.")

    if name:
        customer.name = name
    if email:
        customer.email = email
    if phone:
        customer.phone = phone
    if company_name:
        customer.company_name = company_name
    if commercial_id:
        customer.commercial_id = commercial_id

    session.commit()
    return customer


@require_role("gestion")
def update_customer_commercial(token, customer_id, commercial_id):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if commercial_id:
        customer.commercial_id = commercial_id

    session.commit()
    return customer

@require_role("gestion", "commercial", "support")
def display_customer(token, customer_id):
    customer = session.query(Customer).get(customer_id)
    view_display_customer(customer)


def get_customers():
    customers = session.query(Customer).all()
    liste = "\n".join(
        f" id : {c.id} - Nom : {c.name}" for c in customers)
    valid_ids = [str(c.id) for c in customers]
    return liste, valid_ids


def get_customer_name(customer_id):
    customer_name = session.query(Customer.name).filter(Customer.id == customer_id).scalar()
    return customer_name





if __name__ == "__main__":
    display_customer(1)
    # from views.customers import display_customers
    # display_customers(get_customers())