import click
from controllers.customers import create_customer
from controllers.collaborators import get_commercials

@click.group("customers")
def customers_group():
    """Gestion des clients"""
    pass


liste, valid_ids = get_commercials()

@customers_group.command("create")
@click.option("--name",     prompt="Nom complet")
@click.option("--email",    prompt="Adresse email")
@click.option("--phone",    prompt="Numéro de téléphone")
@click.option("--company-name",    prompt="Nom de l'entreprise")
@click.option(
    "--commercial-id",
    prompt= f"\nCommerciaux disponibles :\n{liste}\n\nN° id du commercial",
    type=click.Choice(valid_ids),
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