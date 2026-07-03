import pytest
from controllers.customers import (
    create_customer,
    update_customer,
    update_customer_commercial,
    display_customer,
    get_customers,
)


# create
def test_create_customer(db_session, commercial_token, commercial):
    customer = create_customer(
        token=commercial_token,
        name="test client",
        email="client@test.com",
        phone="0123456789",
        company_name="entreprise",
        commercial_id=commercial.id
    )

    assert customer.id is not None
    assert customer.email == "client@test.com"


def test_create_customer_duplicate_email(db_session, commercial_token, commercial):
    create_customer(
        token=commercial_token,
        name="test client",
        email="client@test.com",
        phone="0123456789",
        company_name="entreprise",
        commercial_id=commercial.id
    )

    with pytest.raises(ValueError, match="déjà utilisé"):
        create_customer(
            token=commercial_token,
            name="test client",
            email="client@test.com",
            phone="0123456789",
            company_name="entreprise",
            commercial_id=commercial.id
        )


# update
def test_update_customer(db_session, commercial_token, customer):
    updated = update_customer(
        token=commercial_token,
        customer_id=customer.id,
        name="test client 2",
        email=None,
        phone=None,
        company_name=None
    )

    assert updated.name == "test client 2"


def test_update_customer_permission_error(db_session, support_token, customer):
    with pytest.raises(PermissionError):
        update_customer(
            token=support_token,
            customer_id=customer.id,
            name="test client",
            email=None,
            phone=None,
            company_name=None
        )


def test_update_customer_commercial(db_session, gestion_token, customer, commercial):
    updated = update_customer_commercial(
        token=gestion_token,
        customer_id=customer.id,
        commercial_id=commercial.id
    )

    assert updated.commercial_id == commercial.id


# display
def test_display_customer(db_session, commercial_token, customer, capsys):
    display_customer(commercial_token, customer.id)

    out = capsys.readouterr().out
    assert customer.name in out or customer.email in out


# get
def test_get_customers(db_session, customer):
    result, ids = get_customers()

    assert customer.name in result
    assert str(customer.id) in ids
