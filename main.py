import click


from database import engine, session
from models.models import Base, Role, Collaborator, Customer, Contract, Event
from commands.auth import login_command, logout_command
from commands.collaborators import collaborators_group
from commands.customers import customers_group
from commands.contracts import contracts_group
from token_storage import load_token


# Créer les tables
# Base.metadata.drop_all(engine)   # supprime toutes les tables
Base.metadata.create_all(engine)

# Alimenter les rôles si la table est vide
if not session.query(Role).first():
    session.add_all([
        Role(name="commercial"),
        Role(name="support"),
        Role(name="gestion"),
    ])
    session.commit()



@click.group()
@click.pass_context
def cli(ctx):
    """Epic Events CRM"""
    ctx.ensure_object(dict)
    ctx.obj["token"] = load_token()

cli.add_command(login_command)
cli.add_command(logout_command)
cli.add_command(collaborators_group)
cli.add_command(customers_group)
cli.add_command(contracts_group)

if __name__ == "__main__":
    cli()