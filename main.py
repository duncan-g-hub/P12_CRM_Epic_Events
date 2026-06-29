"""Entry point of the Epic Events CRM application."""

import click
import os
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import logging
import bcrypt

from database import engine, session
from models.models import Base, Role, Collaborator
from commands.auth import login_command, logout_command
from commands.collaborators import collaborators_group
from commands.customers import customers_group
from commands.contracts import contracts_group
from commands.events import events_group
from token_storage import load_token, delete_token

load_dotenv()

logging.basicConfig(level=logging.INFO)
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Enable sending logs to Sentry
    enable_logs=True,
    integrations=[
        LoggingIntegration(
            level=logging.INFO,
            event_level=logging.ERROR
        )
    ]
)

# Base.metadata.drop_all(engine)   # supprime toutes les tables
Base.metadata.create_all(engine)  # Créer les tables

# Alimenter les rôles si la table est vide
if not session.query(Role).first():
    session.add_all([
        Role(name="commercial"),
        Role(name="support"),
        Role(name="gestion"),
    ])
    session.commit()

# créer un admin si aucun n'existe
if not session.query(Collaborator).filter(Collaborator.email == "admin@crm.com").first():
    role = session.query(Role).filter(Role.name == "gestion").first()
    hashed = bcrypt.hashpw("Admin12345".encode(), bcrypt.gensalt())
    admin = Collaborator(
        name="Admin",
        email="admin@crm.com",
        password=hashed.decode("utf-8"),
        phone="0600000000",
        role_id=role.id
    )
    session.add(admin)
    session.commit()
    print("Admin créé : "
          "\nemail = admin@crm.com"
          "\nmot de passe = Admin12345"
          "\nPensez à modifier le mot de passe !")

@click.group()
@click.pass_context
def cli(ctx):
    """Epic Events CRM"""
    ctx.ensure_object(dict)
    token = load_token()
    ctx.obj["token"] = token
    if token:
        from auth.auth import decode_token
        payload = decode_token(token)
        sentry_sdk.set_user({"id": payload.get("id"), "role": payload.get("role")})


cli.add_command(login_command)
cli.add_command(logout_command)
cli.add_command(collaborators_group)
cli.add_command(customers_group)
cli.add_command(contracts_group)
cli.add_command(events_group)

if __name__ == "__main__":
    try:
        cli(standalone_mode=False)
    except click.exceptions.Abort:
        pass
    except click.exceptions.Exit:
        pass
    except click.exceptions.UsageError as e:
        click.echo(click.style(str(e), fg="yellow"))
    except PermissionError as e:
        click.echo(click.style(str(e), fg="red"))
        if "expiré" in str(e):
            delete_token()
            click.echo(click.style("Veuillez vous reconnecter.", fg="yellow"))
    except Exception as e:
        sentry_sdk.capture_exception(e)  # toute erreur inattendue -> Sentry
        logging.error(f"Une erreur est survenue : {e}")
        click.echo(click.style("Une erreur inattendue est survenue.", fg="red"))
