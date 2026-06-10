from models.models import Customer
from main import session

from views.customers import get_customers_data_from_form

def create_customer():

    name, email, phone, company_name, commercial_id = get_customers_data_from_form()

    customer = Customer(name=name,
                    email=email,
                    phone=phone,
                    company_name=company_name,
                    commercial_id=commercial_id
                    )
    session.add(customer)
    session.commit()


def get_customers():
    clients = session.query(Customer).all()
    return clients




if __name__ == "__main__":
    # create_customer()
    from views.customers import display_customers
    display_customers(get_customers())