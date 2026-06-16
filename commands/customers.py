import click
from controllers.customers import create_customer, display_customer, get_customers
from controllers.collaborators import get_commercials

@click.group("customers")
def customers_group():
    """Gestion des clients"""
    pass


commercials, commercial_ids = get_commercials()

@customers_group.command("create")
@click.option("--name",     prompt="Nom complet")
@click.option("--email",    prompt="Adresse email")
@click.option("--phone",    prompt="Numéro de téléphone")
@click.option("--company-name",    prompt="Nom de l'entreprise")
@click.option(
    "--commercial-id",
    prompt= f"\nCommerciaux disponibles :\n{commercials}\n\nN° id du commercial",
    type=click.Choice(commercial_ids),
)
@click.pass_context
def create(ctx, name, email, phone, company_name, commercial_id):
    """Créer un client"""

    token = ctx.obj["token"]
    try:
        customer = create_customer(token, name, email, phone, company_name, commercial_id)
        click.echo(click.style(f"Client '{customer.name}' créé.", fg="green"))
    except PermissionError as e:
        click.echo(click.style(f"{e}", fg="red"))



customers, customer_id = get_customers()
@customers_group.command("display")
@click.option(
    "--customers-id",
    prompt= f"\nListe de des clients :\n{customers}\n\nN° id du client à afficher",
    type=click.Choice(customer_id),
)
@click.pass_context
def display(ctx, customers_id):
    token = ctx.obj["token"]
    display_customer(token, customers_id)