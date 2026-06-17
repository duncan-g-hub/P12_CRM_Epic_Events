import click
from controllers.customers import create_customer, display_customer, get_customers
from controllers.collaborators import get_commercials

@click.group("customers")
def customers_group():
    """Gestion des clients"""
    pass




@customers_group.command("create")
@click.pass_context
def create(ctx):
    """Créer un client"""

    token = ctx.obj["token"]

    name = click.prompt("Nom complet du client")
    email = click.prompt("Adresse email")
    phone = click.prompt("Numéro de téléphone")
    company_name = click.prompt("Nom de l'entreprise")

    commercials, commercial_ids = get_commercials()
    commercial_id = click.prompt(f"\nCommerciaux disponibles :\n{commercials}\n\nN° id du commercial",
                  type=click.Choice(commercial_ids))

    try:
        customer = create_customer(token, name, email, phone, company_name, commercial_id)
        click.echo(click.style(f"Client '{customer.name}' créé.", fg="green"))
    except PermissionError as e:
        click.echo(click.style(f"{e}", fg="red"))




@customers_group.command("display")
@click.pass_context
def display(ctx):
    token = ctx.obj["token"]
    customers, customer_ids = get_customers()
    customer_id = click.prompt(f"\nListe de des clients :\n{customers}\n\nN° id du client à afficher",
                 type=click.Choice(customer_ids))
    display_customer(token, customer_id)