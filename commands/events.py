import click

from controllers.events import create_event
from controllers.contracts import get_contracts
from controllers.customers import get_customers
from controllers.collaborators import get_supports


@click.group("events")
def events_group():
    """Gestion des événements"""
    pass


contracts, contract_ids = get_contracts()
customers, customer_ids = get_customers()
supports, support_ids = get_supports()

@events_group.command("create")
@click.option("--name", prompt="Nom")
@click.option(
    "--contract-id",
    prompt= f"\nContrats disponibles :\n{contracts}\n\nN° id du contrat",
    type=click.Choice(contract_ids),
)
@click.option(
    "--customer-id",
    prompt= f"\nClients disponibles :\n{customers}\n\nN° id du client",
    type=click.Choice(customer_ids),
)
@click.option(
    "--support-id",
    prompt= f"\nSupports disponibles :\n{supports}\n\nN° id du support",
    type=click.Choice(support_ids),
)
@click.option("--date-start", prompt="Date de départ (JJ/MM/AAAA)", type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option("--date-end",  prompt="Date de fin (JJ/MM/AAAA)", type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option("--location",  prompt="Adresse")
@click.option("--attendees",  prompt="Nombre de participants", type=int)
@click.option("--notes", prompt="Commentaires")


@click.pass_context
def create(ctx, name, contract_id, customer_id, support_id, date_start, date_end, location, attendees, notes):
    """Créer un événement"""
    token = ctx.obj["token"]
    try:
        event = create_event(token, name, contract_id, customer_id, support_id, date_start, date_end, location, attendees, notes)

        click.echo(click.style(f"Événement {event.name} créé.", fg="green"))

    except PermissionError as e:
        click.echo(click.style(f"{e}", fg="red"))