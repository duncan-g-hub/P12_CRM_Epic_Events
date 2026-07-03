import pytest
from controllers.events import (
    create_event,
    update_event,
    update_event_support,
    display_event,
    get_events,
)


# create
def test_create_event(db_session, commercial_token, signed_contract, commercial):
    event = create_event(
        token=commercial_token,
        name="event",
        contract_id=signed_contract.id,
        date_start="01/01/2050",
        date_end="02/01/2050",
        location="Paris",
        attendees=50,
        notes="RAS"
    )

    assert event.id is not None
    assert event.name == "event"


def test_create_event_unsigned_contract(db_session, commercial_token, unsigned_contract):
    with pytest.raises(PermissionError):
        create_event(
            token=commercial_token,
            name="event",
            contract_id=unsigned_contract.id,
            date_start="01/01/2050",
            date_end="02/01/2050",
            location="Paris",
            attendees=50,
            notes="RAS"
        )


def test_create_event_not_owner(db_session, support_token, signed_contract):
    with pytest.raises(PermissionError):
        create_event(
            token=support_token,
            name="event",
            contract_id=signed_contract.id,
            date_start="01/01/2050",
            date_end="02/01/2050",
            location="Paris",
            attendees=50,
            notes="RAS"
        )


def test_update_event(db_session, support_token, event):
    updated = update_event(
        token=support_token,
        event_id=event.id,
        name="event 2",
        contract_id=None,
        date_start=None,
        date_end=None,
        location=None,
        attendees=None,
        notes=None
    )

    assert updated.name == "event 2"


def test_update_event_wrong_support(db_session, commercial_token, event):
    with pytest.raises(PermissionError):
        update_event(
            token=commercial_token,
            event_id=event.id,
            name="event",
            contract_id=None,
            date_start=None,
            date_end=None,
            location=None,
            attendees=None,
            notes=None
        )


def test_update_event_support(db_session, gestion_token, event, support):
    updated = update_event_support(
        token=gestion_token,
        event_id=event.id,
        support_id=support.id
    )

    assert updated.support_id == support.id


# display
def test_display_event(db_session, support_token, event, capsys):
    display_event(support_token, event.id)

    out = capsys.readouterr().out
    assert event.name in out or str(event.id) in out


# get
def test_get_events(db_session, event):
    result, ids = get_events()

    assert str(event.id) in ids
