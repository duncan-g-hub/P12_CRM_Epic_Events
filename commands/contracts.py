import click
from functools import partial
from controllers.contracts import create_contract, get_contracts, display_contract, update_contract, get_contract
from controllers.customers import get_customers
from controllers.collaborators import get_commercials
from auth.auth import decode_token
from utils import validate_prompt
from validators import validate_amount_to_pay

@click.group("contracts")
def contracts_group():
    """Gestion des contrats"""
    pass


@contracts_group.command("create")
@click.pass_context
def create(ctx):
    """Créer un contrat"""
    token = ctx.obj["token"]
    click.echo("Création d'un contrat:\n")
    customers, customer_ids = get_customers()
    customer_id = click.prompt(f"\nClients disponibles :\n{customers}\n\n"
                               "N° id du client", type=click.Choice(customer_ids))

    commercials, commercial_ids = get_commercials()
    commercial_id = click.prompt(f"\nCommerciaux disponibles :\n{commercials}\n\n"
                                 "N° id du commercial", type=click.Choice(commercial_ids))

    total_amount = click.prompt("Montant total €", type=float)

    validate_function = partial(validate_amount_to_pay, total_amount=total_amount)
    amount_to_pay = validate_prompt("Reste à payer €", validate_function, type=float)

    signed = click.prompt("Contrat signé ?", type=click.BOOL)

    try:
        contract = create_contract(token, customer_id, commercial_id, total_amount, amount_to_pay, signed)
        click.echo(click.style(f"Contrat pour le client {contract.customer.name} créé.", fg="green"))

    except PermissionError as e:
        click.echo(click.style(f"{e}", fg="red"))


@contracts_group.command("update")
@click.pass_context
def update(ctx):
    token = ctx.obj["token"]
    click.echo("Modification d'un contrat:\n")
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



    contract = get_contract(contract_id)
    total_amount = click.prompt("Nouveau montant total € (Entrée pour ignorer)",
                                type=float, default="", show_default=False) or None

    reference_total = total_amount if total_amount is not None else contract.total_amount
    validate_fn = partial(validate_amount_to_pay, total_amount=reference_total)
    amount_to_pay = validate_prompt("Nouveau reste à payer € (Entrée pour ignorer)",
                                    validate_fn, optional=True,
                                    type=float, default="", show_default=False)


    signed = click.prompt("Contrat signé ? (Entrée pour ignorer)",
                          type=click.BOOL, default="", show_default=False) or None

    try:
        contract = update_contract(token, contract_id, customer_id, commercial_id, total_amount, amount_to_pay, signed)
        click.echo(click.style(f"Contrat pour le client {contract.customer.name} mis à jour.", fg="green"))
    except PermissionError as e:
        click.echo(click.style(str(e), fg="red"))


@contracts_group.command("display")
@click.pass_context
def display(ctx):
    token = ctx.obj["token"]
    click.echo("Affichage des détails d'un contrat:\n")
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
