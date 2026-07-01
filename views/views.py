def view_display_collaborator(c, c_role):
    """Print collaborator details."""
    print("\n----------------------------------\n"
          f"Collaborateur sélectionné : "
          f"\n nom : {c.name} (id : {c.id}) "
          f"\n email : {c.email} - téléphone : {c.phone} "
          f"\n role : {c_role}"
          f"\n date de création : {c.date_creation}"
          "\n----------------------------------\n")


def view_display_contract(c):
    """Print contract details."""
    signed = "Oui" if c.signed else "Non"
    print("\n----------------------------------\n"
          f"Contrat sélectionné : "
          f"\n id : {c.id}"
          f"\n commercial : {c.customer.commercial.name} (id : {c.customer.commercial_id})"
          f"\n client : {c.customer.name} (id : {c.customer_id})"
          f"\n montant total : {c.total_amount}€ - montant à payer : {c.amount_to_pay}€ - signé : {signed}"
          f"\n date de création : {c.date_creation}"
          "\n----------------------------------\n")


def view_display_customer(c):
    """Print customer details."""
    print("\n----------------------------------\n"
          f"Client sélectionné : "
          f"\n nom : {c.name} (id : {c.id}) "
          f"\n email : {c.email} - téléphone : {c.phone}"
          f"\n entreprise : {c.company_name} "
          f"\n commercial : {c.commercial.name} (id : {c.commercial_id})"
          f"\n date de création : {c.date_creation}"
          f"\n date de dernière mise à jour : {c.date_last_contact}"
          "\n----------------------------------\n")


def view_display_event(e):
    """Print event details."""
    support_name = e.support.name if e.support else "Aucun"
    print("\n----------------------------------\n"
          f"Événement sélectionné : "
          f"\n id : {e.id} - nom : {e.name}"
          f"\n support : {support_name} (id : {e.support_id})"
          f"\n client : {e.contract.customer.name} (id : {e.contract.customer_id} - "
          f"email : {e.contract.customer.email} - tel : {e.contract.customer.phone})"
          f"\n contrat id : {e.contract_id}"
          f"\n date de début : {e.date_start} - date de fin : {e.date_end}"
          f"\n adresse : {e.location}"
          f"\n nombre participants : {e.attendees}"
          f"\n commentaire : {e.notes}"
          "\n----------------------------------\n")
