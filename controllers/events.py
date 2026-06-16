from models.models import Event
from database import session
from permissions import require_role
from views.events import view_display_event

@require_role("gestion")
def create_event(token, name, contract_id, customer_id, support_id, date_start, date_end, location, attendees, notes):

    event = Event(name=name,
                  contract_id=int(contract_id),
                  customer_id=int(customer_id),
                  support_id=int(support_id),
                  date_start=date_start,
                  date_end=date_end,
                  location=location,
                  attendees=int(attendees),
                  notes=notes
                 )

    # Gerer les formats et gestion erreur sur les dates

    session.add(event)
    session.commit()
    return event


@require_role("gestion", "commercial", "support")
def get_events(token):
    events = session.query(Event).all()
    liste = "\n".join(
        f" id : {e.id} - nom : {e.name} - date de départ : {e.date_start}"
        f" - date de fin : {e.date_end} - adresse : {e.location}" for e in events)
    valid_ids = [str(e.id) for e in events]
    return liste, valid_ids


@require_role("gestion", "commercial", "support")
def display_event(token, event_id):
    event = session.query(Event).get(event_id)
    view_display_event(event)



# @require_role("gestion", "support")
# def update_event(token, event_id):
#     pass



if __name__ == '__main__':
    display_event(3)