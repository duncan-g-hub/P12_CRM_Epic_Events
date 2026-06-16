def view_display_event(e):
        print("----------------------------------\n"
              f"Événement : \nid : {e.id} - nom : {e.name} \nid support : {e.support_id} - id client : {e.customer_id} - "
              f"id contrat : {e.contract_id} \ndate de début : {e.date_start} - date de fin : {e.date_end} \n"
              f"adresse : {e.location} - nombre participants : {e.attendees} \ncommentaire : {e.notes}"
              "\n----------------------------------")