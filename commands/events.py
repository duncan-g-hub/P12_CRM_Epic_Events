import click

from controllers.events import create_event, get_events, display_event, update_event, update_event_support
from controllers.contracts import get_contracts
from controllers.collaborators import get_supports
from auth.auth import decode_token


@click.group("events")
def events_group():
    """Gestion des événements"""
    pass


@events_group.command("create")
@click.pass_context
def create(ctx):
    """Créer un événement"""
    token = ctx.obj["token"]

    click.echo("Création d'un événement:\n")
    name = click.prompt("Nom de l'événement")

    contracts, contract_ids = get_contracts()
    contract_id = click.prompt(f"\nContrats disponibles :\n{contracts}\n\n"
                               "N° id du contrat", type=click.Choice(contract_ids))

    date_start = click.prompt("Date de départ (JJ/MM/AAAA)", type=click.DateTime(formats=["%d/%m/%Y"]))
    date_end = click.prompt("Date de fin (JJ/MM/AAAA)", type=click.DateTime(formats=["%d/%m/%Y"]))
    location = click.prompt("Adresse")
    attendees = click.prompt("Nombre de participants", type=int)
    notes = click.prompt("Commentaires")

    try:
        event = create_event(token, name, contract_id, date_start, date_end, location, attendees, notes)

        click.echo(click.style(f"Événement {event.name} créé.", fg="green"))

    except PermissionError as e:
        click.echo(click.style(f"{e}", fg="red"))


@events_group.command("update")
@click.pass_context
def update(ctx):
    token = ctx.obj["token"]
    payload = decode_token(token)
    collaborator_role = payload.get("role")
    click.echo("Modification d'un événement:\n")
    events, event_ids = get_events()
    event_id = click.prompt(f"\nListe des événements :\n{events}\n\n"
                            "N° id de l'événement à modifier", type=click.Choice(event_ids))

    if collaborator_role == "support":
        name = click.prompt("Nom de l'événement (Entrée pour ignorer)", default="", show_default=False
                            ).strip() or None

        contracts, contract_ids = get_contracts()
        contract_id = click.prompt(f"\nListe des contrts :\n{contracts}\n\n"
                                   "N° id du contrat", default="", show_default=False,
                                   type=click.Choice(contract_ids)) or None

        date_start = click.prompt("Date de départ (JJ/MM/AAAA) (Entrée pour ignorer)",
                                  type=click.DateTime(formats=["%d/%m/%Y"]), default=None, show_default=False) or None
        date_end = click.prompt("Date de fin (JJ/MM/AAAA) (Entrée pour ignorer)",
                                type=click.DateTime(formats=["%d/%m/%Y"]), default=None, show_default=False) or None

        location = click.prompt("Adresse (Entrée pour ignorer)", default="", show_default=False).strip() or None

        attendees = click.prompt("Nombre de participants (Entrée pour ignorer)",
                                 type=int, default=None, show_default=False) or None

        notes = click.prompt("Commentaires (Entrée pour ignorer)", default="", show_default=False).strip() or None

        try:
            event = update_event(token, event_id, name, contract_id, date_start, date_end, location, attendees, notes)
            click.echo(click.style(f"Événement '{event.name}' mis à jour.", fg="green"))
        except PermissionError as e:
            click.echo(click.style(f"{e}", fg="red"))

    if collaborator_role == "gestion":
        supports, support_ids = get_supports()
        support_id = click.prompt(f"\nListe des supports :\n{supports}\n\n"
                                  "N° id du support à associer à l'événement (Entrée pour ignorer)",
                                  default="", show_default=False, type=click.Choice(support_ids)) or None
        try:
            event = update_event_support(token, event_id, support_id)
            click.echo(click.style(f"Événement '{event.name}' mis à jour.", fg="green"))
        except PermissionError as e:
            click.echo(click.style(f"{e}", fg="red"))


@events_group.command("display")
@click.pass_context
def display(ctx):
    token = ctx.obj["token"]

    support_id = None
    filter_by_support = False
    filter_by_empty_support = False

    payload = decode_token(token)
    collaborator_role = payload.get("role")
    collaborator_id = payload.get("id")

    click.echo("Affichage des détails d'un événement:\n")
    if collaborator_role == "gestion":
        filter_by_empty_support = click.prompt(
            "Voulez-vous ajouter le filtre pour afficher les événements sans supports associés ? "
            "(Entrée pour ignorer)", type=click.BOOL, default="", show_default=False)

    if collaborator_role == "support":
        filter_by_support = click.prompt(
            "Voulez-vous ajouter le filtre pour afficher les événements qui vous sont attribués ? "
            "(Entrée pour ignorer)", type=click.BOOL, default="", show_default=False)
        if filter_by_support:
            support_id = collaborator_id

    events, event_ids = get_events(support_id, filter_by_support, filter_by_empty_support)

    event_id = click.prompt(f"\nListe des événements :\n{events}\n\n"
                            "N° id de l'événnement à afficher", type=click.Choice(event_ids))
    display_event(token, event_id)
