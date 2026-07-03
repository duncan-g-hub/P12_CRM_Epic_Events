import os
import bcrypt
import pytest

from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

from models.models import (
    Base,
    Role,
    Collaborator,
    Customer,
    Contract,
    Event,
)

from auth.auth import login


load_dotenv()
DATABASE_URL = os.getenv("TEST_DB_URL")

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture()
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.expunge_all()
    session.close()

    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True)
def override_get_session(monkeypatch, db_session):
    import database

    monkeypatch.setattr(database, "get_session", lambda: db_session)

    import sys
    sys.modules["database"].get_session = lambda: db_session


@pytest.fixture(autouse=True)
def clean_db(db_session):
    yield

    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())

    db_session.commit()


@pytest.fixture()
def roles(db_session):
    commercial = Role(name="commercial")
    support = Role(name="support")
    gestion = Role(name="gestion")

    db_session.add_all([commercial, support, gestion])
    db_session.commit()

    return {
        "commercial": commercial,
        "support": support,
        "gestion": gestion,
    }


@pytest.fixture()
def gestion(db_session, roles):
    obj = Collaborator(
        name="gestion",
        email="gestion@crm.com",
        password=bcrypt.hashpw(b"Mdp12345", bcrypt.gensalt()).decode(),
        phone="0123456789",
        role_id=roles["gestion"].id,
    )
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    return obj


@pytest.fixture()
def commercial(db_session, roles):
    obj = Collaborator(
        name="commercial",
        email="commercial@crm.com",
        password=bcrypt.hashpw(b"Mdp12345", bcrypt.gensalt()).decode(),
        phone="0123456789",
        role_id=roles["commercial"].id,
    )
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    return obj


@pytest.fixture()
def support(db_session, roles):
    obj = Collaborator(
        name="support",
        email="support@crm.com",
        password=bcrypt.hashpw(b"Mdp12345", bcrypt.gensalt()).decode(),
        phone="0123456789",
        role_id=roles["support"].id,
    )
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    return obj


@pytest.fixture()
def gestion_token(gestion):
    token, _ = login("gestion@crm.com", "Mdp12345")
    return token


@pytest.fixture()
def commercial_token(commercial):
    token, _ = login("commercial@crm.com", "Mdp12345")
    return token


@pytest.fixture()
def support_token(support):
    token, _ = login("support@crm.com", "Mdp12345")
    return token


@pytest.fixture()
def tokens(gestion_token, commercial_token, support_token):
    return {
        "gestion": gestion_token,
        "commercial": commercial_token,
        "support": support_token,
    }


@pytest.fixture()
def customer(db_session, commercial):
    obj = Customer(
        name="client",
        email="client@crm.com",
        phone="0123456789",
        company_name="Entreprise",
        commercial_id=commercial.id,
    )
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    return obj


@pytest.fixture()
def signed_contract(db_session, customer):
    obj = Contract(
        customer_id=customer.id,
        total_amount=1000,
        amount_to_pay=300,
        signed=True,
    )
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    return obj


@pytest.fixture()
def unsigned_contract(db_session, customer):
    obj = Contract(
        customer_id=customer.id,
        total_amount=1000,
        amount_to_pay=300,
        signed=False,
    )
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    return obj


@pytest.fixture()
def event(db_session, signed_contract, support):
    obj = Event(
        name="Evénement",
        contract_id=signed_contract.id,
        support_id=support.id,
        date_start=datetime.now() + timedelta(days=5),
        date_end=datetime.now() + timedelta(days=6),
        location="Paris",
        attendees=50,
        notes="RAS",
    )
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    return obj
