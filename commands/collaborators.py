import click
from controllers.collaborators import create_collaborator, get_collaborators, display_collaborator, update_collaborator
from commands.utils import validate_prompt
from validators import validate_email, validate_phone, validate_password

@click.group("collaborators")
def collaborators_group():
    """Gestion des collaborateurs"""
    pass


@collaborators_group.command("create")
@click.pass_context
def create(ctx, ):
    """Créer un collaborateur (gestion uniquement)"""
    token = ctx.obj["token"]
    click.echo("Création d'un collaborateur:\n")
    name = click.prompt("Nom complet du collaborateur")
    email = validate_prompt("Adresse email", validate_email)

    password = validate_prompt("Mot de passe", validate_password, hide_input=True)
    confirm = click.prompt("Confirmer mot de passe", hide_input=True)

    while password != confirm:
        click.echo(click.style("Les mots de passe ne correspondent pas.", fg="red"))
        password = validate_prompt("Mot de passe", validate_password, hide_input=True)
        confirm = click.prompt("Confirmer mot de passe", hide_input=True)

    phone = validate_prompt("Numéro de téléphone", validate_phone)
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
    click.echo("Modification d'un collaborateur:\n")
    try:
        collaborators, collaborator_ids = get_collaborators()
    except ValueError as e:
        click.echo(click.style(str(e), fg="red"))
        return
    collaborator_id = click.prompt(
        f"\nListe des collaborateurs :\n{collaborators}\n\nN° id du collaborateur à modifier",
        type=click.Choice(collaborator_ids))

    name = click.prompt("Nouveau nom (Entrée pour ignorer)", default="", show_default=False).strip() or None
    email = validate_prompt("Nouvel email (Entrée pour ignorer)", validate_email, optional=True, default="",
                            show_default=False)
    password = validate_prompt("Nouveau mot de passe (Entrée pour ignorer)", validate_password, optional=True,
                               default="", hide_input=True, show_default=False)
    if password:
        confirm = click.prompt("Confirmer mot de passe", hide_input=True)
        while password != confirm:
            click.echo(click.style("Les mots de passe ne correspondent pas.", fg="red"))
            password = validate_prompt("Nouveau mot de passe", validate_password, hide_input=True)
            confirm = click.prompt("Confirmer mot de passe", hide_input=True)

    phone = validate_prompt("Nouveau téléphone (Entrée pour ignorer)", validate_phone, optional=True,
                            default="", show_default=False)

    role_id = click.prompt(
        "Nouveau rôle (1:commercial / 2:support / 3:gestion) (Entrée pour ignorer)",
        default="", show_default=False,
        type=click.Choice(["", "1", "2", "3"])
    ) or None

    try:
        collaborator = update_collaborator(token, collaborator_id, name, email, password, phone, role_id)
        click.echo(click.style(f"Collaborateur '{collaborator.name}' mis à jour.", fg="green"))
    except (PermissionError, ValueError) as e:
        click.echo(click.style(str(e), fg="red"))


@collaborators_group.command("display")
@click.pass_context
def display(ctx):
    token = ctx.obj["token"]
    click.echo("Affichage des détails d'un collaborateur:\n")

    try:
        collaborators, collaborator_ids = get_collaborators()
    except ValueError as e:
        click.echo(click.style(str(e), fg="red"))
        return

    collaborator_id = click.prompt(f"\nListe des collaborateurs :\n{collaborators}\n\n"
                                   "N° id du collaborateur à afficher", type=click.Choice(collaborator_ids))
    display_collaborator(token, collaborator_id)
