from views.collaborators import display_collaborators
from views.customers import display_customers


def display_contract_form(commercials, customers):
    ids = []
    for c in commercials:
        ids.append(str(c.id))
    display_collaborators(commercials)
    commercial_id = input("Veuillez saisir l'id du commercial à associé au contrat : ")
    while commercial_id not in ids:
        display_collaborators(commercials)
        commercial_id = input("Veuillez saisir l'id d'un commercial valide à associé au contrat : ")

    ids = []
    for c in customers:
        ids.append(str(c.id))
    display_customers(customers)
    customer_id = input("Veuillez saisir l'id du client à associé au contrat : ")
    while customer_id not in ids:
        display_customers(customers)
        customer_id = input("Veuillez saisir l'id d'un client valide à associé au contrat : ")

    total_amount = input("Veuillez saisir le montant total à payer (€) : ")

    amount_to_pay = input("Veuillez saisir le montant restant à payer (€) : ")

    response = input("Le contrat est-il signé ? (o/n) : ").strip().lower()
    signed = response in ("o", "oui", "y", "yes")

    return commercial_id, customer_id, total_amount, amount_to_pay, signed


def display_contracts(contracts):
    for c in contracts:
        print (c.signed)
        if c.signed:
            signed = "Oui"
        else:
            signed = "Non"
        print(f"id : {c.id} - id commercial : {c.commercial_id} - id client : {c.customer_id} - "
              f"montant total : {c.total_amount}€ - montant à payer : {c.amount_to_pay}€ - signé : {signed}")