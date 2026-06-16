def view_display_contract(c):
        if c.signed:
            signed = "Oui"
        else:
            signed = "Non"
        print("\n----------------------------------\n"
              f"Contrat : \nid : {c.id} - id commercial : {c.commercial_id} - id client : {c.customer_id} \n"
              f"montant total : {c.total_amount}€ - montant à payer : {c.amount_to_pay}€ - signé : {signed}"
              "\n----------------------------------\n")