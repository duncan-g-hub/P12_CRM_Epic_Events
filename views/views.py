def view_display_collaborator(c, c_role):
    print("\n----------------------------------\n"
          f"Collaborateur sélectionné : "
          f"\n id : {c.id} - Nom : {c.name} "
          f"\n email : {c.email} - téléphone : {c.phone} "
          f"\n role : {c_role}"
          "\n----------------------------------\n")


def view_display_contract(c):
    if c.signed:
        signed = "Oui"
    else:
        signed = "Non"
    print("\n----------------------------------\n"
          f"Contrat sélectionné : "
          f"\n id : {c.id} - id commercial : {c.commercial_id} - id client : {c.customer_id} "
          f"\n montant total : {c.total_amount}€ - montant à payer : {c.amount_to_pay}€ - signé : {signed}"
          "\n----------------------------------\n")


def view_display_customer(c):
    print("\n----------------------------------\n"
          f"Client sélectionné : "
          f"\n id : {c.id} - Nom : {c.name} "
          f"\n email : {c.email} - téléphone : {c.phone}"
          f"\n entreprise : {c.company_name} - id commercial : {c.commercial_id}"
          "\n----------------------------------\n")


def view_display_event(e):
    print("\n----------------------------------\n"
          f"Événement sélectionné : "
          f"\n id : {e.id} - nom : {e.name} "
          f"\n id support : {e.support_id} - id client : {e.customer_id} - id contrat : {e.contract_id} "
          f"\n date de début : {e.date_start} - date de fin : {e.date_end}"
          f"\n adresse : {e.location} "
          f"\n nombre participants : {e.attendees} "
          f"\n commentaire : {e.notes}"
          "\n----------------------------------\n")
