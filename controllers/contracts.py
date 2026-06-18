from models.models import Contract, Customer
from database import session
from views.views import view_display_contract
from auth.permissions import require_role
from auth.auth import decode_token

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


@require_role("gestion", "commercial")
def update_contract(token, contract_id, customer_id, commercial_id, total_amount, amount_to_pay, signed):

    # Récupération du rôle et id collab depuis le token
    payload = decode_token(token)
    collaborator_role = payload.get("role")
    collaborator_id = payload.get("id")

    contract = session.query(Contract).filter(Contract.id == contract_id).first()

    # Vérification si commercial : doit être rattaché au client du contrat
    if collaborator_role == "commercial":
        customer = session.query(Customer).filter(Customer.id == contract.customer_id).first()
        if customer.commercial_id != collaborator_id:
            raise PermissionError("Vous ne pouvez modifier que les contrats de vos propres clients.")

    if customer_id :
        contract.customer_id = customer_id
    if commercial_id :
        contract.commercial_id = int(commercial_id)
    if total_amount :
        contract.total_amount = float(total_amount)
    if amount_to_pay :
        contract.amount_to_pay = float(amount_to_pay)
    if signed is not None :
        contract.signed = signed

    session.commit()
    return contract


@require_role("gestion", "commercial", "support")
def display_contract(token, contract_id):
    contract = session.query(Contract).get(contract_id)
    view_display_contract(contract)


def get_contracts(commercial_id=False, filter_by_commercial=False, filter_by_amount_to_pay=False, filter_by_signed=False):
    query = session.query(Contract)
    if filter_by_commercial and commercial_id:
        query = query.filter(Contract.commercial_id == commercial_id)
    if filter_by_amount_to_pay:
        query = query.filter(Contract.amount_to_pay > 0)
    if filter_by_signed:
        query = query.filter(Contract.signed == False)
    contracts = query.all()

    liste = "\n".join(
        f" id : {c.id} - id client : {c.customer_id} - id commercial : {c.commercial_id}" for c in contracts)
    valid_ids = [str(c.id) for c in contracts]
    return liste, valid_ids






if __name__ == '__main__':
    display_contract(1)