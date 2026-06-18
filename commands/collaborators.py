import click
from controllers.collaborators import create_collaborator, get_collaborators, display_collaborator, update_collaborator

@click.group("collaborators")
def collaborators_group():
    """Gestion des collaborateurs"""
    pass


@collaborators_group.command("create")
@click.pass_context
def create(ctx,):
    """Créer un collaborateur (gestion uniquement)"""
    token = ctx.obj["token"]

    name = click.prompt("Nom complet du collaborateur")
    email = click.prompt("Adresse email")

    password = click.prompt("Mot de passe", hide_input=True)
    confirm = click.prompt("Confirmer mot de passe", hide_input=True)

    while password != confirm:
        click.echo(click.style("Les mots de passe ne correspondent pas.", fg="red"))
        password = click.prompt("Mot de passe", hide_input=True)
        confirm = click.prompt("Confirmer mot de passe", hide_input=True)

    phone = click.prompt("Numéro de téléphone")
    role_id = click.prompt("Rôle (1:commercial / 2:support / 3:gestion)",
                           type=click.Choice(["1", "2", "3"]))

    try:
        collaborator = create_collaborator(token, name, email, password, phone, role_id)
        click.echo(click.style(f"Collaborateur '{collaborator.name}' créé.", fg="green"))
    except PermissionError as e:
        click.echo(click.style(f"{e}", fg="red"))


@collaborators_group.command("update")
@click.pass_context
def update(ctx):
    token = ctx.obj["token"]

    collaborators, collaborator_ids = get_collaborators()
    collaborator_id = click.prompt(
        f"\nListe des collaborateurs :\n{collaborators}\n\nN° id du collaborateur à modifier",
        type=click.Choice(collaborator_ids))

    name = click.prompt("Nouveau nom (Entrée pour ignorer)", default="", show_default=False).strip() or None
    email = click.prompt("Nouvel email (Entrée pour ignorer)", default="", show_default=False).strip() or None
    password = click.prompt("Nouveau mot de passe (Entrée pour ignorer)", default="", hide_input=True,
                            show_default=False).strip() or None
    if password:
        confirm = click.prompt("Confirmer mot de passe", hide_input=True)
        while password != confirm:
            click.echo(click.style("Les mots de passe ne correspondent pas.", fg="red"))
            password = click.prompt("Nouveau mot de passe", hide_input=True)
            confirm = click.prompt("Confirmer mot de passe", hide_input=True)

    phone = click.prompt("Nouveau téléphone (Entrée pour ignorer)",
                         default="", show_default=False).strip() or None

    role_id = click.prompt(
        "Nouveau rôle (1:commercial / 2:support / 3:gestion) (Entrée pour ignorer)",
        default="", show_default=False,
        type=click.Choice(["", "1", "2", "3"])
    ) or None

    try:
        collaborator = update_collaborator(token, collaborator_id, name, email, password, phone, role_id)
        click.echo(click.style(f"Collaborateur '{collaborator.name}' mis à jour.", fg="green"))
    except PermissionError as e:
        click.echo(click.style(str(e), fg="red"))


@collaborators_group.command("display")
@click.pass_context
def display(ctx):
    token = ctx.obj["token"]
    collaborators, collaborator_ids = get_collaborators()
    collaborator_id = click.prompt(f"\nListe des collaborateurs :\n{collaborators}\n\n"
                                   "N° id du collaborateur à afficher", type=click.Choice(collaborator_ids))
    display_collaborator(token, collaborator_id)