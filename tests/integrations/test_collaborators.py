import pytest

from controllers.collaborators import (
    create_collaborator,
    update_collaborator,
    display_collaborator,
    get_collaborators
)


# create
def test_create_collaborator(db_session, tokens, roles):
    token = tokens["gestion"]

    collaborator = create_collaborator(
        token=token,
        name="test collaborator",
        email="collaborator@test.com",
        password="Mdp12345",
        phone="0123456789",
        role_id=roles["commercial"].id
    )

    assert collaborator.id is not None
    assert collaborator.email == "collaborator@test.com"


def test_create_collaborator_duplicate_email(db_session, tokens, roles):
    token = tokens["gestion"]

    create_collaborator(
        token=token,
        name="test collaborator",
        email="collaborator@test.com",
        password="Mdp12345",
        phone="0123456789",
        role_id=roles["commercial"].id
    )

    with pytest.raises(ValueError, match="déjà utilisé"):
        create_collaborator(
            token=token,
            name="test collaborator",
            email="collaborator@test.com",
            password="Mdp12345",
            phone="0123456789",
            role_id=roles["commercial"].id
        )


def test_create_collaborator_permission_error(tokens, roles):
    token = tokens["support"]

    with pytest.raises(PermissionError):
        create_collaborator(
            token=token,
            name="test collaborator",
            email="collaborator@test.com",
            password="Mdp12345",
            phone="0123456789",
            role_id=roles["commercial"].id
        )


# update
def test_update_collaborator(db_session, tokens, roles):
    token = tokens["gestion"]

    collab = create_collaborator(
        token=token,
        name="test collaborator",
        email="collaborator@test.com",
        password="Mdp12345",
        phone="0123456789",
        role_id=roles["commercial"].id
    )

    updated = update_collaborator(
        token=token,
        collaborator_id=collab.id,
        name="test collaborator new",
        email=None,
        password=None,
        phone=None,
        role_id=None
    )

    assert updated.name == "test collaborator new"


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


# display
def test_display_collaborator(db_session, tokens, capsys, roles):
    token = tokens["gestion"]

    collab = create_collaborator(
        token=token,
        name="test collaborator",
        email="collaborator@test.com",
        password="Mdp12345",
        phone="0123456789",
        role_id=roles["commercial"].id
    )

    display_collaborator(token, collab.id)

    captured = capsys.readouterr()
    assert "test collaborator" in captured.out


# get
def test_get_collaborators(db_session, tokens, roles):
    token = tokens["gestion"]

    create_collaborator(
        token=token,
        name="test collaborator",
        email="collaborator@test.com",
        password="Mdp12345",
        phone="0123456789",
        role_id=roles["commercial"].id
    )

    result, ids = get_collaborators()

    assert "test collaborator" in result
    assert len(ids) > 0
