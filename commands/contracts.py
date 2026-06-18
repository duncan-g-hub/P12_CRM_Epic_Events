import click

from controllers.contracts import create_contract, get_contracts, display_contract, update_contract
from controllers.customers import get_customers, get_customer_name
from controllers.collaborators import get_commercials
from auth.auth import decode_token


@click.group("contracts")
def contracts_group():
    """Gestion des contrats"""
    pass


@contracts_group.command("create")
@click.pass_context
def create(ctx):
    """Créer un contrat"""
    token = ctx.obj["token"]

    customers, customer_ids = get_customers()
    customer_id = click.prompt(f"\nClients disponibles :\n{customers}\n\n"
                               "N° id du client", type=click.Choice(customer_ids))

    commercials, commercial_ids = get_commercials()
    commercial_id = click.prompt(f"\nCommerciaux disponibles :\n{commercials}\n\n"
                                 "N° id du commercial", type=click.Choice(commercial_ids))

    total_amount = click.prompt("Montant total", type=float)
    amount_to_pay = click.prompt("Reste à payer", type=float)
    signed = click.prompt("Contrat signé ?", type=click.BOOL)

    try:
        contract = create_contract(token, customer_id, commercial_id, total_amount, amount_to_pay, signed)
        customer_name = get_customer_name(contract.customer_id)
        click.echo(click.style(f"Contrat pour le client {customer_name} créé.", fg="green"))

    except PermissionError as e:
        click.echo(click.style(f"{e}", fg="red"))


@contracts_group.command("update")
@click.pass_context
def update(ctx):
    token = ctx.obj["token"]

    contracts, contract_ids = get_contracts()
    contract_id = click.prompt(
        f"\nListe des contrats :\n{contracts}\n\n"
        "N° id du contrat à modifier", type=click.Choice(contract_ids))

    customers, customer_ids = get_customers()
    customer_id = click.prompt(f"\nClients disponibles :\n{customers}\n\n"
                               "N° id du nouveau client (Entrée pour ignorer)",
                               default="", show_default=False, type=click.Choice(customer_ids)) or None

    commercials, commercial_ids = get_commercials()
    commercial_id = click.prompt(f"\nCommerciaux disponibles :\n{commercials}\n\n"
                                 "N° id du nouveau commercial (Entrée pour ignorer)",
                                 default="", show_default=False, type=click.Choice(commercial_ids)) or None

    total_amount = click.prompt("Nouveau montant total (Entrée pour ignorer)",
                                type=float, default="", show_default=False) or None
    amount_to_pay = click.prompt("Nouveau reste à payer (Entrée pour ignorer)",
                                 type=float, default="", show_default=False) or None
    signed = click.prompt("Contrat signé ? (Entrée pour ignorer)",
                          type=click.BOOL, default="", show_default=False) or None

    try:
        contract = update_contract(token, contract_id, customer_id, commercial_id, total_amount, amount_to_pay, signed)
        customer_name = get_customer_name(contract.customer_id)
        click.echo(click.style(f"Contrat pour le client {customer_name} mis à jour.", fg="green"))
    except PermissionError as e:
        click.echo(click.style(str(e), fg="red"))


@contracts_group.command("display")
@click.pass_context
def display(ctx):
    token = ctx.obj["token"]

    commercial_id = None
    filter_by_commercial = False
    filter_by_amount_to_pay = False
    filter_by_signed = False

    payload = decode_token(token)
    collaborator_role = payload.get("role")
    collaborator_id = payload.get("id")

    if collaborator_role == "commercial":
        filter_by_commercial = click.prompt(
            "Voulez-vous ajouter le filtre pour afficher les contrats qui vous sont attribués ? (Entrée pour ignorer)",
            type=click.BOOL, default="", show_default=False)
        if filter_by_commercial:
            commercial_id = collaborator_id

        filter_by_amount_to_pay = click.prompt(
            "Voulez-vous ajouter le filtre pour afficher les contrats pas entièrement payés ? (Entrée pour ignorer)",
            type=click.BOOL, default="", show_default=False)

        filter_by_signed = click.prompt(
            "Voulez-vous ajouter le filtre pour afficher les contrats non signés ? (Entrée pour ignorer)",
            type=click.BOOL, default="", show_default=False)

    contracts, contract_ids = get_contracts(commercial_id, filter_by_commercial, filter_by_amount_to_pay,
                                            filter_by_signed)

    contract_id = click.prompt(f"\nListe des contrats :\n{contracts}\n\n"
                               "N° id du contrat à afficher", type=click.Choice(contract_ids))
    display_contract(token, contract_id)
