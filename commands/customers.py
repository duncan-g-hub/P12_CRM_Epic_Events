import click
from controllers.customers import create_customer, display_customer, get_customers, update_customer, \
    update_customer_commercial
from controllers.collaborators import get_commercials
from auth.auth import decode_token
from validators import validate_email, validate_phone
from commands.utils import validate_prompt, require_cli_role


@click.group("customers")
def customers_group():
    """Manage customers."""
    pass


@customers_group.command("create")
@click.pass_context
@require_cli_role("commercial")
def create(ctx):
    """Create a new customer (commercial only)."""

    token = ctx.obj["token"]
    click.echo("Création d'un client:\n")
    name = click.prompt("Nom complet du client")
    email = validate_prompt("Adresse email", validate_email)
    phone = validate_prompt("Numéro de téléphone", validate_phone)
    company_name = click.prompt("Nom de l'entreprise")

    commercial_id = decode_token(token).get("id")

    try:
        customer = create_customer(token, name, email, phone, company_name, commercial_id)
        click.echo(click.style(f"Client '{customer.name}' créé.", fg="green"))
    except PermissionError as e:
        click.echo(click.style(f"{e}", fg="red"))


@customers_group.command("update")
@click.pass_context
@require_cli_role("commercial", "gestion")
def update(ctx):
    """Update an existing customer (commercial and gestion only)."""
    token = ctx.obj["token"]
    payload = decode_token(token)
    collaborator_role = payload.get("role")
    click.echo("Modification d'un client:\n")
    try:
        customers, customer_ids = get_customers()
    except ValueError as e:
        click.echo(click.style(str(e), fg="red"))
        return
    customer_id = click.prompt(f"\nListe des Clients :\n{customers}\n\n"
                               "N° id du client à modifier", type=click.Choice(customer_ids))

    if collaborator_role == "commercial":
        name = click.prompt("Nouveau nom du client (Entrée pour ignorer)", default="", show_default=False
                            ).strip() or None

        email = validate_prompt("Adresse email (Entrée pour ignorer)", validate_email, optional=True,
                                default="", show_default=False)

        phone = validate_prompt("Numéro de téléphone (Entrée pour ignorer)", validate_phone, optional=True,
                                default="", show_default=False)

        company_name = click.prompt("Nom de l'entreprise (Entrée pour ignorer)", default="", show_default=False
                                    ).strip() or None
        try:
            customer = update_customer(token, customer_id, name, email, phone, company_name)
            click.echo(click.style(f"Client '{customer.name}' mis à jour.", fg="green"))
        except (PermissionError, ValueError) as e:
            click.echo(click.style(f"{e}", fg="red"))

    if collaborator_role == "gestion":
        try:
            commercials, commercial_ids = get_commercials()
        except ValueError as e:
            click.echo(click.style(str(e), fg="red"))
            return
        commercial_id = click.prompt(f"\nCommerciaux disponibles :\n{commercials}\n\n"
                                     "N° id du nouveau commercial (Entrée pour ignorer)",
                                     default="", show_default=False, type=click.Choice([*commercial_ids, ""])) or None
        try:
            customer = update_customer_commercial(token, customer_id, commercial_id)
            click.echo(click.style(f"Client '{customer.name}' mis à jour.", fg="green"))
        except (PermissionError, ValueError) as e:
            click.echo(click.style(f"{e}", fg="red"))


@customers_group.command("display")
@click.pass_context
@require_cli_role("commercial", "gestion", "support")
def display(ctx):
    """Display customer details."""
    token = ctx.obj["token"]
    click.echo("Affichage des détails d'un client:\n")
    try:
        customers, customer_ids = get_customers()
    except ValueError as e:
        click.echo(click.style(str(e), fg="red"))
        return
    customer_id = click.prompt(f"\nListe de des clients :\n{customers}\n\n"
                               "N° id du client à afficher", type=click.Choice(customer_ids))
    display_customer(token, customer_id)
