from datetime import datetime, timedelta

from models.models import Collaborator, Role, Customer, Contract, Event

import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()



# Contextes / tokens par rôle
@pytest.fixture
def fake_token():
    return "fake-jwt-token"


@pytest.fixture
def gestion_ctx(fake_token):
    return {"token": fake_token}


@pytest.fixture
def commercial_ctx(fake_token):
    return {"token": fake_token}


@pytest.fixture
def support_ctx(fake_token):
    return {"token": fake_token}


@pytest.fixture
def no_auth_ctx():
    return {"token": None}


@pytest.fixture
def payload_commercial():
    return {"id": 1, "role": "commercial"}

@pytest.fixture
def payload_gestion():
    return {"id": 2, "role": "gestion"}

@pytest.fixture
def payload_support():
    return {"id": 3, "role": "support"}



# Objets fake
@pytest.fixture
def fake_commercial():
    role = Role(id=1, name="commercial")
    collaborator = Collaborator(
        id=1,
        name="commercial",
        email="commercial@crm.com",
        password="Mdp12345",
        phone="0123456789",
        role_id=role.id,
    )
    collaborator.role = role
    return collaborator

@pytest.fixture
def fake_gestion():
    role = Role(id=2, name="gestion")

    collaborator = Collaborator(
        id=2,
        name="gestion",
        email="gestion@crm.com",
        password="Mdp12345",
        phone="0123456789",
        role_id=role.id,
    )
    collaborator.role = role
    return collaborator

@pytest.fixture
def fake_support():
    role = Role(id=3, name="support")
    collaborator = Collaborator(
        id=3,
        name="support",
        email="support@crm.com",
        password="Mdp12345",
        phone="0123456789",
        role_id=role.id,
    )
    collaborator.role = role
    return collaborator



@pytest.fixture
def fake_customer(fake_commercial):
    customer = Customer(
        id=1,
        name="client",
        email="client@crm.com",
        phone="0123456789",
        company_name="entreprise",
        commercial_id=fake_commercial.id,
        date_creation=datetime.now(),
        date_last_contact=datetime.now(),
    )
    customer.commercial = fake_commercial
    return customer


@pytest.fixture
def fake_contract(fake_customer):
    contract = Contract(
        id=1,
        customer_id=fake_customer.id,
        total_amount=1000.0,
        amount_to_pay=500.0,
        signed=True,
    )
    contract.customer = fake_customer
    return contract


@pytest.fixture
def fake_event(fake_contract):
    event = Event(
        id=1,
        name="événement",
        contract_id=fake_contract.id,
        support_id=None,
        date_start=datetime.now(),
        date_end=datetime.now() + timedelta(days=1),
        location="Paris",
        attendees=100,
        notes="RAS",
    )
    event.contract = fake_contract
    return event



# Listes formatées
@pytest.fixture
def fake_collaborators_list():
    return (("\n nom : commercial (id : 1)"
            "\n nom : gestion (id : 2)"
            "\n nom : support (id : 3)"),
            ["1","2","3"])


@pytest.fixture
def fake_customers_list():
    return " nom : client (id : 1)", ["1"]


@pytest.fixture
def fake_contracts_list():
    return ((" id : 1 "
             "\n client : client (id : 1)"
             "\n commercial : commercial (id : 1)"),
            ["1"])


@pytest.fixture
def fake_events_list():
    return ((" nom : événement (id : 1) "
             "\n date de départ : 01/09/2056 - date de fin : 02/09/2056 "
             "\n adresse : Paris"),
            ["1"])