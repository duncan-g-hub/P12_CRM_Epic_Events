from models.models import Contract, Customer
from database import session
from views.views import view_display_contract
from auth.permissions import require_role
from auth.auth import decode_token
from validators import validate_amount_to_pay


@require_role("gestion")
def create_contract(token, customer_id, total_amount, amount_to_pay, signed):
    validate_amount_to_pay(amount_to_pay, total_amount)
    contract = Contract(customer_id=int(customer_id),
                        total_amount=float(total_amount),
                        amount_to_pay=float(amount_to_pay),
                        signed=signed
                        )
    session.add(contract)
    session.commit()
    return contract


@require_role("gestion", "commercial")
def update_contract(token, contract_id, customer_id, total_amount, amount_to_pay, signed):
    payload = decode_token(token)
    collaborator_role = payload.get("role")
    collaborator_id = payload.get("id")

    contract = session.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise ValueError(f"Contract introuvable.")

    if collaborator_role == "commercial":
        customer = session.query(Customer).filter(Customer.id == contract.customer_id).first()
        if customer.commercial_id != collaborator_id:
            raise PermissionError("Vous ne pouvez modifier que les contrats de vos propres clients.")

    if customer_id:
        contract.customer_id = int(customer_id)
    if total_amount is not None:
        contract.total_amount = float(total_amount)
    if amount_to_pay is not None:
        total_amount_reference = total_amount if total_amount is not None else contract.total_amount
        validate_amount_to_pay(amount_to_pay, total_amount_reference)
        contract.amount_to_pay = float(amount_to_pay)
    if signed is not None:
        if contract.signed and not signed:
            raise ValueError("Un contrat déjà signé ne peut pas être repassé à non signé.")
        contract.signed = signed

    session.commit()
    return contract


@require_role("gestion", "commercial", "support")
def display_contract(token, contract_id):
    contract = session.get(Contract, contract_id)
    view_display_contract(contract)


def get_contracts(commercial_id=None, filter_by_commercial=False, filter_by_amount_to_pay=False,
                  filter_by_signed=False):
    query = session.query(Contract)
    if filter_by_commercial and commercial_id:
        query = query.filter(Contract.customer.commercial_id == commercial_id)
    if filter_by_amount_to_pay:
        query = query.filter(Contract.amount_to_pay > 0)
    if filter_by_signed:
        query = query.filter(Contract.signed == False)
    contracts = query.all()
    if not contracts:
        raise ValueError("Contrats introuvables.")
    liste = "\n\n".join(
        f" id : {c.id} "
        f"\n client : {c.customer.name} (id : {c.customer_id})"
        f"\n commercial : {c.customer.commercial.name} (id : {c.customer.commercial_id})" for c in contracts)
    valid_ids = [str(c.id) for c in contracts]
    return liste, valid_ids


def get_contract(contract_id):
    contract = session.query(Contract).filter(Contract.id == contract_id).first()
    return contract