from views.collaborators import display_collaborators
from views.customers import display_customers
from views.contracts import display_contracts
from views.input_format import input_date

def display_event_form(supports, customers, contracts):

    name = input("Veuillez saisir le nom de l'événement : ")

    ids = []
    for c in contracts:
        ids.append(str(c.id))
    display_contracts(contracts)
    contract_id = input("Veuillez saisir l'id du contrat à associé à l'événement : ")
    while contract_id not in ids:
        display_contracts(contracts)
        contract_id = input("Veuillez saisir l'id d'un contrat valide à associé à l'événement : ")

    ids = []
    for c in customers:
        ids.append(str(c.id))
    display_customers(customers)
    customer_id = input("Veuillez saisir l'id du client à associé à l'événement : ")
    while customer_id not in ids:
        display_customers(customers)
        customer_id = input("Veuillez saisir l'id d'un client valide à associé à l'événement : ")

    ids = []
    for s in supports:
        ids.append(str(s.id))
    display_collaborators(supports)
    support_id = input("Veuillez saisir l'id du support à associé à l'événement : ")
    while support_id not in ids:
        display_collaborators(supports)
        support_id = input("Veuillez saisir l'id d'un support valide à associé à l'événement : ")


    date_start = input_date("Veuillez saisir la date de début de l'événement (JJ/MM/AAAA) : ")

    date_end = input_date("Veuillez saisir la date de fin de l'événement (JJ/MM/AAAA) : ")

    location = input("Veuillez saisir l'adresse de l'événement : ")

    attendees = input("Veuillez saisir une estimation du nombre de participants : ")

    notes = input("Veuillez saisir un commentaire concernant l'événement : ")


    return name, contract_id, customer_id, support_id, date_start, date_end, location, attendees, notes



def display_events(events):
    for e in events:
        print(f"id : {e.id} - nom : {e.name} - id support : {e.support_id} - id client : {e.customer_id} - "
              f"id contrat : {e.contract_id} - date de début : {e.date_start}€ - date de fin : {e.date_end} - "
              f"adresse : {e.location} - nombre participants : {e.attendees} - commentaire : {e.notes}")