from models.models import Event, Customer, Contract
from database import session
from auth.permissions import require_role
from views.views import view_display_event
from auth.auth import decode_token
from validators import validate_date, validate_future_date, validate_date_end


@require_role("commercial")
def create_event(token, name, contract_id, date_start, date_end, location, attendees, notes):
    payload = decode_token(token)
    collaborator_id = payload.get("id")

    contract = session.query(Contract).filter(Contract.id == contract_id).first()
    customer = session.query(Customer).filter(Customer.id == contract.customer_id).first()

    if customer.commercial_id != collaborator_id:
        raise PermissionError("Vous ne pouvez créer un évennement que pour les clients dont vous êtes responsable.")

    if not contract.signed:
        raise PermissionError("Vous ne pouvez pas créer un évennement sans que le contrat ne soit signé")

    date_start = validate_future_date(date_start)
    date_end = validate_date_end(date_start, date_end)

    event = Event(name=name,
                  contract_id=int(contract_id),
                  date_start=date_start,
                  date_end=date_end,
                  location=location,
                  attendees=int(attendees),
                  notes=notes
                  )

    session.add(event)
    session.commit()
    return event


@require_role("support")
def update_event(token, event_id, name, contract_id, date_start, date_end, location, attendees, notes):
    payload = decode_token(token)
    collaborator_id = payload.get("id")

    event = session.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise ValueError("Événement introuvable.")

    if event.support_id != collaborator_id:
        raise PermissionError("Vous ne pouvez modifier que les événements dont vous êtes responsable.")

    if name:
        event.name = name
    if contract_id:
        contract = session.query(Contract).filter(Contract.id == contract_id).first()
        if not contract.signed:
            raise PermissionError("Vous ne pouvez pas créer un évennement sans que le contrat ne soit signé")
        event.contract_id = int(contract_id)
    if date_start:
        date_start = validate_future_date(date_start)
        event.date_start = date_start
    if date_end:
        date_start_reference = date_start if date_start is not None else event.date_start
        date_end = validate_date_end(date_start_reference, date_end)
        event.date_end = date_end
    if location:
        event.location = location
    if attendees is not None:
        event.attendees = int(attendees)
    if notes:
        event.notes = notes
    session.commit()
    return event


@require_role("gestion")
def update_event_support(token, event_id, support_id):
    event = session.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise ValueError("Événement introuvable.")
    if support_id:
        event.support_id = int(support_id)
    session.commit()
    return event


@require_role("gestion", "commercial", "support")
def display_event(token, event_id):
    event = session.get(Event, event_id)
    view_display_event(event)


def get_events(support_id=None, filter_by_support=False, filter_by_empty_support=False):
    query = session.query(Event)
    if filter_by_support and support_id:
        query = query.filter(Event.support_id == support_id)
    if filter_by_empty_support:
        query = query.filter(Event.support_id.is_(None))

    events = query.all()
    if not events:
        raise ValueError("Événnements introuvables.")
    liste = "\n\n".join(
        f" nom : {e.name} (id : {e.id}) "
        f"\n date de départ : {e.date_start} - date de fin : {e.date_end} "
        f"\n adresse : {e.location}" for e in events)
    valid_ids = [str(e.id) for e in events]
    return liste, valid_ids


def get_event(event_id):
    event = session.query(Event).filter(Event.id == event_id).first()
    return event