import click
from controllers.collaborators import create_collaborator

@click.group("collaborators")
def collaborators_group():
    """Gestion des collaborateurs"""
    pass



@collaborators_group.command("create")
@click.option("--name",     prompt="Nom complet")
@click.option("--email",    prompt="Adresse email")
@click.option("--password", prompt="Mot de passe",          hide_input=True)
@click.option("--confirm",  prompt="Confirmer mot de passe", hide_input=True)
@click.option("--phone",    prompt="Numéro de téléphone")
@click.option(
    "--role-id",
    prompt="Rôle (1:commercial / 2:support / 3:gestion)",
    type=click.Choice(["1", "2", "3"]),
)
@click.pass_context
def create(ctx, name, email, password, confirm, phone, role_id):
    """Créer un collaborateur (gestion uniquement)"""

    # Vérification confirmation mot de passe
    while password != confirm:
        click.echo(click.style("✗ Les mots de passe ne correspondent pas.", fg="red"))
        password = click.prompt("Mot de passe",           hide_input=True)
        confirm  = click.prompt("Confirmer mot de passe", hide_input=True)

    token = ctx.obj["token"]
    try:
        collaborator = create_collaborator(token, name, email, password, phone, role_id)
        click.echo(click.style(f"Collaborateur '{collaborator.name}' créé.", fg="green"))
    except PermissionError as e:
        click.echo(click.style(f"{e}", fg="red"))