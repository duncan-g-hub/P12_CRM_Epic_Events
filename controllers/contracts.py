from models.models import Contract
from database import session
from views.contracts import view_display_contract
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
    liste = "\n\n".join(
        f" id : {c.id} - id client : {c.customer_id} - id commercial : {c.commercial_id}" for c in contracts)
    valid_ids = [str(c.id) for c in contracts]
    return liste, valid_ids


@require_role("gestion", "commercial", "support")
def display_contract(token, contract_id):
    contract = session.query(Contract).get(contract_id)
    view_display_contract(contract)



if __name__ == '__main__':
    display_contract(1)