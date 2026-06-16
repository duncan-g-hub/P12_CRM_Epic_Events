from views.collaborators import display_collaborators

def display_customer_form(commercials):
    name = input("Veuillez saisir le nom complet du client : ")
    email = input("Veuillez saisir l'adresse email du client : ")
    phone = input("Veuillez saisir le n° de telephone du client : ")
    company_name = input("Veuillez saisir le nom de l'entreprise du client : ")


    ids=[]
    for c in commercials:
        ids.append(str(c.id))
    display_collaborators(commercials)
    commercial_id = input("Veuillez saisir l'id du commercial à associé au client : ")
    while commercial_id not in ids:
        display_collaborators(commercials)
        commercial_id = input("Veuillez saisir l'id d'un commercial valide à associé au client : ")

    return name, email, phone, company_name, commercial_id




def view_display_customer(c):
        print("----------------------------------\n"
              f"Client : \nid : {c.id} - Nom : {c.name} \nemail : {c.email} - téléphone : {c.phone}"
              f"\nentreprise : {c.company_name} - id commercial : {c.commercial_id}"
              "\n----------------------------------")