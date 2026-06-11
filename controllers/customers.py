from models.models import Customer
from database import session
from controllers.collaborators import get_commercials
from views.customers import display_customer_form

def create_customer():
    commercials = get_commercials()
    name, email, phone, company_name, commercial_id = display_customer_form(commercials)
    customer = Customer(name=name,
                    email=email,
                    phone=phone,
                    company_name=company_name,
                    commercial_id=int(commercial_id)
                    )
    #gestion d'erreur à gerer (adresse email unique etc)
    session.add(customer)
    session.commit()


def get_customers():
    customers = session.query(Customer).all()
    return customers




if __name__ == "__main__":
    create_customer()
    # from views.customers import display_customers
    # display_customers(get_customers())