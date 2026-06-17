import click
from controllers.collaborators import create_collaborator, get_collaborators, display_collaborator

@click.group("collaborators")
def collaborators_group():
    """Gestion des collaborateurs"""
    pass



@collaborators_group.command("create")
@click.pass_context
def create(ctx,):
    """Créer un collaborateur (gestion uniquement)"""

    name = click.prompt("Nom complet du collaborateur")
    email = click.prompt("Adresse email")
    password = click.prompt("Mot de passe", hide_input=True)
    confirm = click.prompt("Confirmer mot de passe", hide_input=True)
    phone = click.prompt("Numéro de téléphone")
    role_id = click.prompt("Rôle (1:commercial / 2:support / 3:gestion)",
                           type=click.Choice(["1", "2", "3"]))

    # Vérification confirmation mot de passe
    while password != confirm:
        click.echo(click.style("Les mots de passe ne correspondent pas.", fg="red"))
        password = click.prompt("Mot de passe",           hide_input=True)
        confirm  = click.prompt("Confirmer mot de passe", hide_input=True)

    token = ctx.obj["token"]
    try:
        collaborator = create_collaborator(token, name, email, password, phone, role_id)
        click.echo(click.style(f"Collaborateur '{collaborator.name}' créé.", fg="green"))
    except PermissionError as e:
        click.echo(click.style(f"{e}", fg="red"))




@collaborators_group.command("display")
@click.pass_context
def display(ctx):
    token = ctx.obj["token"]
    collaborators, collaborator_ids = get_collaborators()
    collaborator_id = click.prompt(
        "\nListe des collaborateurs :\n\n{collaborators}\n\nN° id du collaborateur à afficher",
        type=click.Choice(collaborator_ids))
    display_collaborator(token, collaborator_id)