import click
from auth import login
from token_storage import save_token, delete_token


@click.command("login")
@click.option("--email",    prompt="Email",           help="Adresse email")
@click.option("--password", prompt="Mot de passe",    hide_input=True, help="Mot de passe")
@click.pass_context
def login_command(ctx, email, password):
    """Se connecter au CRM"""
    try:
        token, collaborator = login(email, password)
        save_token(token)
        click.echo(click.style(
            f"Connecté en tant que {collaborator.name} ({collaborator.role.name})",
            fg="green"
        ))
    except ValueError as e:
        click.echo(click.style(f"✗ {e}", fg="red"))
        raise click.Abort()

@click.command("logout")
def logout_command():
    delete_token()
    click.echo("Déconnecté.")