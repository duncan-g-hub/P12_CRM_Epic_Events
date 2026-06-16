def view_display_collaborator(c, c_role):
        print("----------------------------------\n"
              f"Collaborateur : \nid : {c.id} - Nom : {c.name} "
              f"\nemail : {c.email} - téléphone : {c.phone} \nrole : {c_role}"
              "\n----------------------------------")
