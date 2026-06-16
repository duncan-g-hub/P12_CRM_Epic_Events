def view_display_customer(c):
        print("\n----------------------------------\n"
              f"Client : \nid : {c.id} - Nom : {c.name} \nemail : {c.email} - téléphone : {c.phone}"
              f"\nentreprise : {c.company_name} - id commercial : {c.commercial_id}"
              "\n----------------------------------\n")