import click
from functools import partial

from controllers.events import create_event, get_events, display_event, update_event, update_event_support, get_event
from controllers.contracts import get_contracts
from controllers.collaborators import get_supports
from auth.auth import decode_token
from validators import validate_future_date, validate_date_end, validate_integer
from commands.utils import validate_prompt, require_cli_role


@click.group("events")
def events_group():
    """Gestion des événements"""
    pass


@events_group.command("create")
@click.pass_context
@require_cli_role("commercial")
def create(ctx):
    """Créer un événement"""
    token = ctx.obj["token"]
    payload = decode_token(token)
    collaborator_id = payload.get("id")

    click.echo("Création d'un événement:\n")
    name = click.prompt("Nom de l'événement")
    try:
        contracts, contract_ids = get_contracts(commercial_id=collaborator_id, filter_by_commercial=True)
    except ValueError as e:
        click.echo(click.style(str(e), fg="red"))
        return
    contract_id = click.prompt(f"\nContrats disponibles :\n{contracts}\n\n"
                               "N° id du contrat", type=click.Choice(contract_ids))

    date_start = validate_prompt("Date de départ (JJ/MM/AAAA)",validate_future_date)
    validate_fn = partial(validate_date_end, date_start)
    date_end = validate_prompt("Date de fin (JJ/MM/AAAA)", validate_fn)

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
@require_cli_role("gestion", "support")
def update(ctx):
    token = ctx.obj["token"]
    payload = decode_token(token)
    collaborator_role = payload.get("role")
    click.echo("Modification d'un événement:\n")

    if collaborator_role == "support":
        try:
            events, event_ids = get_events(support_id=payload.get("id"), filter_by_support=True)
        except ValueError as e:
            click.echo(click.style(str(e), fg="red"))
            return
        event_id = click.prompt(f"\nListe des événements :\n{events}\n\n"
                                "N° id de l'événement à modifier", type=click.Choice(event_ids))

        name = click.prompt("Nom de l'événement (Entrée pour ignorer)", default="", show_default=False
                            ).strip() or None

        try:
            contracts, contract_ids = get_contracts()
        except ValueError as e:
            click.echo(click.style(str(e), fg="red"))
            return
        contract_id = click.prompt(f"\nListe des contrats :\n{contracts}\n\n"
                                   "N° id du contrat (Entrée pour ignorer)", default="", show_default=False,
                                   type=click.Choice([*contract_ids, ""])) or None


        date_start = validate_prompt("Date de départ (JJ/MM/AAAA) (Entrée pour ignorer)", validate_future_date,
                                     optional=True, default="", show_default=False)

        reference_date_start = date_start if date_start else get_event(event_id).date_start
        validate_fn = partial(validate_date_end,reference_date_start)
        date_end = validate_prompt("Date de fin (JJ/MM/AAAA) (Entrée pour ignorer)", validate_fn, optional=True,
                                   default="", show_default=False)

        location = click.prompt("Adresse (Entrée pour ignorer)", default="", show_default=False).strip() or None

        attendees = validate_prompt("Nombre de participants (Entrée pour ignorer)", validate_integer,
                                    optional=True, default="", show_default=False)

        notes = click.prompt("Commentaires (Entrée pour ignorer)", default="", show_default=False).strip() or None

        try:
            event = update_event(token, event_id, name, contract_id, date_start, date_end, location, attendees, notes)
            click.echo(click.style(f"Événement '{event.name}' mis à jour.", fg="green"))
        except (PermissionError, ValueError) as e:
            click.echo(click.style(f"{e}", fg="red"))


    if collaborator_role == "gestion":
        try:
            events, event_ids = get_events()
        except ValueError as e:
            click.echo(click.style(str(e), fg="red"))
            return
        event_id = click.prompt(f"\nListe des événements :\n{events}\n\n"
                                "N° id de l'événement à modifier", type=click.Choice(event_ids))
        try:
            supports, support_ids = get_supports()
        except ValueError as e:
            click.echo(click.style(str(e), fg="red"))
            return
        support_id = click.prompt(f"\nListe des supports :\n{supports}\n\n"
                                  "N° id du support à associer à l'événement (Entrée pour ignorer)",
                                  default="", show_default=False, type=click.Choice([*support_ids, ""])) or None
        try:
            event = update_event_support(token, event_id, support_id)
            click.echo(click.style(f"Événement '{event.name}' mis à jour.", fg="green"))
        except (PermissionError, ValueError) as e:
            click.echo(click.style(f"{e}", fg="red"))


@events_group.command("display")
@click.pass_context
@require_cli_role("commercial", "gestion", "support")
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
    try:
        events, event_ids = get_events(support_id, filter_by_support, filter_by_empty_support)
    except ValueError as e:
        click.echo(click.style(str(e), fg="red"))
        return
    event_id = click.prompt(f"\nListe des événements :\n{events}\n\n"
                            "N° id de l'événnement à afficher", type=click.Choice(event_ids))
    display_event(token, event_id)
