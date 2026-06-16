from models.models import Contract
from database import session

from permissions import require_role

@require_role("gestion")
def create_contract(token, customer_id, commercial_id, total_amount, amount_to_pay, signed):
    contract = Contract(customer_id=int(customer_id),
                        commercial_id=int(commercial_id),
                        total_amount=float(total_amount),
                        amount_to_pay=float(amount_to_pay),
                        signed=signed
                        )
    session.add(contract)
    session.commit()
    return contract

def get_contracts():
    contracts = session.query(Contract).all()
    return contracts


if __name__ == '__main__':
    create_contract()