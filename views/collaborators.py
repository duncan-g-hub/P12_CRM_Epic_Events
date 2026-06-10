from getpass import getpass


def get_collaborators_data_from_form():
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

    role = input("Veuillez saisir le rôle du collaborateur (commercial/support/gestion) : ")
    while role not in ["commercial", "support", "gestion"]:
        role = input("Veuillez saisir un rôle valide (commercial/support/gestion) :")

    return name, email, password, phone, role




def display_collaborators(collaborators):
    for c in collaborators:
        print(f"id : {c.id} - Nom : {c.name} - email : {c.email} - téléphone : {c.phone}")