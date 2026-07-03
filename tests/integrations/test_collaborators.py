import pytest

from controllers.collaborators import (
    create_collaborator,
    update_collaborator,
    display_collaborator,
    get_collaborators
)

from models.models import Collaborator


# =========================================================
# CREATE
# =========================================================

def test_create_collaborator(db_session, tokens):
    token = tokens["gestion"]

    collaborator = create_collaborator(
        token=token,
        name="John Doe",
        email="john@test.com",
        password="PasswordA1",
        phone="0612345678",
        role_id=1
    )

    assert collaborator.id is not None
    assert collaborator.email == "john@test.com"


def test_create_collaborator_duplicate_email(db_session, tokens):
    token = tokens["gestion"]

    create_collaborator(
        token=token,
        name="John Doe",
        email="dup@test.com",
        password="PasswordA1",
        phone="0612345678",
        role_id=1
    )

    with pytest.raises(ValueError, match="déjà utilisé"):
        create_collaborator(
            token=token,
            name="Jane",
            email="dup@test.com",
            password="PasswordA1",
            phone="0612345678",
            role_id=1
        )


def test_create_collaborator_permission_error(tokens):
    token = tokens["support"]

    with pytest.raises(PermissionError):
        create_collaborator(
            token=token,
            name="Hack",
            email="hack@test.com",
            password="PasswordA1",
            phone="0612345678",
            role_id=1
        )


# =========================================================
# UPDATE
# =========================================================

def test_update_collaborator(db_session, tokens):
    token = tokens["gestion"]

    collab = create_collaborator(
        token=token,
        name="Old Name",
        email="old@test.com",
        password="PasswordA1",
        phone="0612345678",
        role_id=1
    )

    updated = update_collaborator(
        token=token,
        collaborator_id=collab.id,
        name="New Name",
        email=None,
        password=None,
        phone=None,
        role_id=None
    )

    assert updated.name == "New Name"


def test_update_collaborator_not_found(tokens):
    token = tokens["gestion"]

    with pytest.raises(ValueError, match="introuvable"):
        update_collaborator(
            token=token,
            collaborator_id=9999,
            name="X",
            email=None,
            password=None,
            phone=None,
            role_id=None
        )


# =========================================================
# DISPLAY
# =========================================================

def test_display_collaborator(db_session, tokens, capsys):
    token = tokens["gestion"]

    collab = create_collaborator(
        token=token,
        name="Display Test",
        email="display@test.com",
        password="PasswordA1",
        phone="0612345678",
        role_id=1
    )

    display_collaborator(token, collab.id)

    captured = capsys.readouterr()
    assert "Display Test" in captured.out


# =========================================================
# GET LIST
# =========================================================

def test_get_collaborators(db_session, tokens):
    token = tokens["gestion"]

    create_collaborator(
        token=token,
        name="List Test",
        email="list@test.com",
        password="PasswordA1",
        phone="0612345678",
        role_id=1
    )

    result, ids = get_collaborators()

    assert "List Test" in result
    assert len(ids) > 0