import click
from controllers.customers import create_customer, display_customer, get_customers, update_customer, \
    update_customer_commercial
from controllers.collaborators import get_commercials
from auth.auth import decode_token


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


@customers_group.command("update")
@click.pass_context
def update(ctx):
    """Modifier un client"""
    token = ctx.obj["token"]
    payload = decode_token(token)
    collaborator_role = payload.get("role")

    customers, customer_ids = get_customers()
    customer_id = click.prompt(f"\nListe des Clients :\n{customers}\n\n"
                               "N° id du client à modifier", type=click.Choice(customer_ids))

    if collaborator_role == "commercial":
        name = click.prompt("Nouveau nom du client (Entrée pour ignorer)", default="", show_default=False
                            ).strip() or None
        email = click.prompt("Adresse email (Entrée pour ignorer)", default="", show_default=False
                             ).strip() or None
        phone = click.prompt("Numéro de téléphone (Entrée pour ignorer)", default="", show_default=False
                             ).strip() or None
        company_name = click.prompt("Nom de l'entreprise (Entrée pour ignorer)", default="", show_default=False
                                    ).strip() or None
        try:
            customer = update_customer(token, customer_id, name, email, phone, company_name)
            click.echo(click.style(f"Client '{customer.name}' mis à jour.", fg="green"))
        except PermissionError as e:
            click.echo(click.style(f"{e}", fg="red"))

    if collaborator_role == "gestion":
        commercials, commercial_ids = get_commercials()
        commercial_id = click.prompt(f"\nCommerciaux disponibles :\n{commercials}\n\n"
                                     "N° id du nouveau commercial (Entrée pour ignorer)",
                                     default="", show_default=False, type=click.Choice(commercial_ids)) or None
        try:
            customer = update_customer_commercial(token, customer_id, commercial_id)
            click.echo(click.style(f"Client '{customer.name}' mis à jour.", fg="green"))
        except PermissionError as e:
            click.echo(click.style(f"{e}", fg="red"))


@customers_group.command("display")
@click.pass_context
def display(ctx):
    token = ctx.obj["token"]
    customers, customer_ids = get_customers()
    customer_id = click.prompt(f"\nListe de des clients :\n{customers}\n\n"
                               "N° id du client à afficher", type=click.Choice(customer_ids))
    display_customer(token, customer_id)
