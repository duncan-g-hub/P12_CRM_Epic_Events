from models.models import Event
from views.events import display_event_form
from database import session
from controllers.collaborators import get_supports
from controllers.customers import get_customers
from controllers.contracts import get_contracts

def create_event():
    supports = get_supports()
    customers = get_customers()
    contracts = get_contracts()
    name, contract_id, customer_id, support_id, date_start, date_end, location, attendees, notes = (
        display_event_form(supports, customers, contracts))



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
    session.add(event)
    session.commit()


def get_events():
    events = session.query(Event).all()
    return events



if __name__ == '__main__':
    create_event()