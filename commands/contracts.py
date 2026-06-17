import click

from controllers.contracts import create_contract, get_contracts, display_contract
from controllers.customers import get_customers, get_customer_name
from controllers.collaborators import get_commercials


@click.group("contracts")
def contracts_group():
    """Gestion des contrats"""
    pass


customers, customer_ids = get_customers()
commercials, commercial_ids = get_commercials()
@contracts_group.command("create")
@click.option(
    "--customer-id",
    prompt= f"\nClients disponibles :\n{customers}\n\nN° id du client",
    type=click.Choice(customer_ids),
)
@click.option(
    "--commercial-id",
    prompt= f"\nCommerciaux disponibles :\n{commercials}\n\nN° id du commercial",
    type=click.Choice(commercial_ids),
)
@click.option("--total-amount", prompt="Montant total", type=float)
@click.option("--ammount-to-pay",  prompt="Reste à payer", type=float)
@click.option("--signed",  prompt="Contrat signé ?", type=click.BOOL)
@click.pass_context
def create(ctx, customer_id, commercial_id, total_amount, amount_to_pay, signed):
    """Créer un contrat"""
    token = ctx.obj["token"]
    try:
        contract = create_contract(token, customer_id, commercial_id, total_amount, amount_to_pay, signed)
        customer_name = get_customer_name(contract.customer_id)
        click.echo(click.style(f"Contrat pour le client {customer_name} créé.", fg="green"))

    except PermissionError as e:
        click.echo(click.style(f"{e}", fg="red"))



@contracts_group.command("display")
@click.pass_context
def display(ctx):
    token = ctx.obj["token"]
    contracts, contract_ids = get_contracts()
    contract_id = click.prompt(f"\nListe de des contrats :\n{contracts}\n\nN° id du contrat à afficher",
        type=click.Choice(contract_ids))
    display_contract(token, contract_id)