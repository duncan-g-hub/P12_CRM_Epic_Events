from models.models import Contract
from views.contracts import display_contract_form
from database import session
from controllers.collaborators import get_commercials
from controllers.customers import get_customers

def create_contract():
    commercials = get_commercials()
    customers = get_customers()
    customer_id, commercial_id, total_amount, amount_to_pay, signed = display_contract_form(commercials, customers)

    contract = Contract(customer_id=int(customer_id),
                        commercial_id=int(commercial_id),
                        total_amount=float(total_amount),
                        amount_to_pay=float(amount_to_pay),
                        signed=signed
                        )
    session.add(contract)
    session.commit()


def get_contracts():
    contracts = session.query(Contract).all()
    return contracts


if __name__ == '__main__':
    create_contract()