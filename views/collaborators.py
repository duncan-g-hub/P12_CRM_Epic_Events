from getpass import getpass


def display_collaborator_form():
    # ajouter des controles (email + tel + securité mdp)
    name = input("Veuillez saisir le nom complet du collaborateur : ")
    email = input("Veuillez saisir l'adresse email du collaborateur : ")

    password_1 = getpass("Veuillez saisir le mot de passe du collaborateur : ")
    password_2 = getpass("Veuillez confirmer le mot de passe du collaborateur : ")
    while password_1 != password_2:
        print("Les mots de passe ne correspondent pas")
        password_1 = getpass("Veuillez saisir le mot de passe du collaborateur : ")
        password_2 = getpass("Veuillez confirmer le mot de passe du collaborateur : ")
    password = password_1

    phone = input("Veuillez saisir le n° de telephone du collaborateur : ")

    role_id = input("Veuillez saisir le n° correspondant au rôle du collaborateur "
                    "(1:commercial / 2:support / 3:gestion) : ")
    while role_id not in ["1", "2", "3"]:
        role_id = input("Veuillez saisir un n° valide correspondant au rôle du collaborateur "
                    "(1:commercial / 2:support / 3:gestion) : ")

    return name, email, password, phone, role_id




def display_collaborators(collaborators):
    for c in collaborators:
        print(f"id : {c.id} - Nom : {c.name} - email : {c.email} - téléphone : {c.phone}")