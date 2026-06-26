import click
import sentry_sdk

from auth.auth import login
from token_storage import save_token, delete_token


@click.command("login")
@click.pass_context
def login_command(ctx):
    """Log in to the CRM."""
    click.echo("Connexion:\n")
    email = click.prompt("Adresse email")
    password = click.prompt("Mot de passe", hide_input=True)

    try:
        token, collaborator = login(email, password)
        save_token(token)

        # contexte utilisateur envoyé à Sentry
        sentry_sdk.set_user({
            "id": collaborator.id,
        })

        click.echo(click.style(
            f"Connecté en tant que {collaborator.name} ({collaborator.role.name})",
            fg="green"
        ))
    except ValueError as e:
        click.echo(click.style(f"✗ {e}", fg="red"))
        raise click.Abort()


@click.command("logout")
def logout_command():
    """Log out of the CRM."""
    delete_token()
    click.echo("Déconnecté.")
