from models.models import Customer
from database import session
from permissions import require_role

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


def get_customers():
    customers = session.query(Customer).all()
    liste = "\n".join(
        f" id : {c.id} - Nom : {c.name} - email : {c.email} - téléphone : {c.phone}" for c in customers)
    valid_ids = [str(c.id) for c in customers]
    return liste, valid_ids

def get_customer_name(customer_id):
    customer_name = session.query(Customer.name).filter(Customer.id == customer_id).scalar()
    return customer_name



if __name__ == "__main__":
    get_customer_name(1)
    # from views.customers import display_customers
    # display_customers(get_customers())