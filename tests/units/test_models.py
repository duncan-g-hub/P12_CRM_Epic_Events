from sqlalchemy import Integer, String, Float, Boolean, DateTime, inspect

from models.models import Role, Collaborator, Customer, Contract, Event

# Fields
def get_column(model, field_name):
    return model.__table__.columns[field_name]



# Role
def test_role_id():
    col = get_column(Role, "id")
    assert isinstance(col.type, Integer)
    assert col.primary_key is True


def test_role_name():
    col = get_column(Role, "name")
    assert isinstance(col.type, String)
    assert col.type.length == 50
    assert col.nullable is False
    assert col.unique is True



# Collaborator
def test_collaborator_id():
    col = get_column(Collaborator, "id")
    assert isinstance(col.type, Integer)
    assert col.primary_key is True


def test_collaborator_name():
    col = get_column(Collaborator, "name")
    assert isinstance(col.type, String)
    assert col.type.length == 100
    assert col.nullable is False


def test_collaborator_email():
    col = get_column(Collaborator, "email")
    assert isinstance(col.type, String)
    assert col.type.length == 150
    assert col.nullable is False
    assert col.unique is True


def test_collaborator_password():
    col = get_column(Collaborator, "password")
    assert isinstance(col.type, String)
    assert col.type.length == 255
    assert col.nullable is False


def test_collaborator_phone():
    col = get_column(Collaborator, "phone")
    assert isinstance(col.type, String)
    assert col.type.length == 20
    assert col.nullable is True


def test_collaborator_role():
    col = get_column(Collaborator, "role_id")
    assert isinstance(col.type, Integer)
    assert col.nullable is False
    assert {fk.target_fullname for fk in col.foreign_keys} == {"role.id"}


def test_collaborator_date_creation():
    col = get_column(Collaborator, "date_creation")
    assert isinstance(col.type, DateTime)
    assert col.default is not None



# Customer
def test_customer_id():
    col = get_column(Customer, "id")
    assert isinstance(col.type, Integer)
    assert col.primary_key is True


def test_customer_name():
    col = get_column(Customer, "name")
    assert isinstance(col.type, String)
    assert col.type.length == 100
    assert col.nullable is False


def test_customer_email():
    col = get_column(Customer, "email")
    assert isinstance(col.type, String)
    assert col.type.length == 150
    assert col.nullable is False
    assert col.unique is True


def test_customer_phone():
    col = get_column(Customer, "phone")
    assert isinstance(col.type, String)
    assert col.type.length == 20
    assert col.nullable is True


def test_customer_company_name():
    col = get_column(Customer, "company_name")
    assert isinstance(col.type, String)
    assert col.type.length == 150
    assert col.nullable is True


def test_customer_date_creation():
    col = get_column(Customer, "date_creation")
    assert isinstance(col.type, DateTime)
    assert col.default is not None


def test_customer_date_last_contact():
    col = get_column(Customer, "date_last_contact")
    assert isinstance(col.type, DateTime)
    assert col.default is not None


def test_customer_commercial_id():
    col = get_column(Customer, "commercial_id")
    assert isinstance(col.type, Integer)
    assert col.nullable is True
    assert {fk.target_fullname for fk in col.foreign_keys} == {"collaborator.id"}



# Contract
def test_contract_id():
    col = get_column(Contract, "id")
    assert isinstance(col.type, Integer)
    assert col.primary_key is True


def test_contract_customer_id():
    col = get_column(Contract, "customer_id")
    assert isinstance(col.type, Integer)
    assert {fk.target_fullname for fk in col.foreign_keys} == {"customer.id"}


def test_contract_total_amount():
    col = get_column(Contract, "total_amount")
    assert isinstance(col.type, Float)


def test_contract_amount_to_pay():
    col = get_column(Contract, "amount_to_pay")
    assert isinstance(col.type, Float)


def test_contract_date_creation():
    col = get_column(Contract, "date_creation")
    assert isinstance(col.type, DateTime)
    assert col.default is not None


def test_contract_signed():
    col = get_column(Contract, "signed")
    assert isinstance(col.type, Boolean)



# Event
def test_event_id():
    col = get_column(Event, "id")
    assert isinstance(col.type, Integer)
    assert col.primary_key is True


def test_event_name():
    col = get_column(Event, "name")
    assert isinstance(col.type, String)
    assert col.type.length == 100
    assert col.nullable is False


def test_event_contract_id():
    col = get_column(Event, "contract_id")
    assert isinstance(col.type, Integer)
    assert {fk.target_fullname for fk in col.foreign_keys} == {"contract.id"}


def test_event_support_id():
    col = get_column(Event, "support_id")
    assert isinstance(col.type, Integer)
    assert {fk.target_fullname for fk in col.foreign_keys} == {"collaborator.id"}


def test_event_date_start():
    col = get_column(Event, "date_start")
    assert isinstance(col.type, DateTime)


def test_event_date_end():
    col = get_column(Event, "date_end")
    assert isinstance(col.type, DateTime)


def test_event_location():
    col = get_column(Event, "location")
    assert isinstance(col.type, String)
    assert col.type.length == 150
    assert col.nullable is True


def test_event_attendees():
    col = get_column(Event, "attendees")
    assert isinstance(col.type, Integer)


def test_event_notes():
    col = get_column(Event, "notes")
    assert isinstance(col.type, String)
    assert col.type.length == 1000
    assert col.nullable is True



# Relationship
def get_relationship(model, field_name):
    return inspect(model).relationships[field_name]


def test_role_collaborators_relationship():
    rel = get_relationship(Role, "collaborators")
    assert rel.mapper.class_ is Collaborator
    assert rel.back_populates == "role"
    assert rel.uselist is True


def test_collaborator_role_relationship():
    rel = get_relationship(Collaborator, "role")
    assert rel.mapper.class_ is Role
    assert rel.back_populates == "collaborators"
    assert rel.uselist is False


def test_collaborator_customers_relationship():
    rel = get_relationship(Collaborator, "customers")
    assert rel.mapper.class_ is Customer
    assert rel.back_populates == "commercial"
    assert rel.uselist is True


def test_collaborator_events_support_relationship():
    rel = get_relationship(Collaborator, "events_support")
    assert rel.mapper.class_ is Event
    assert rel.back_populates == "support"
    assert rel.uselist is True


def test_customer_commercial_relationship():
    rel = get_relationship(Customer, "commercial")
    assert rel.mapper.class_ is Collaborator
    assert rel.back_populates == "customers"
    assert rel.uselist is False


def test_customer_contracts_relationship():
    rel = get_relationship(Customer, "contracts")
    assert rel.mapper.class_ is Contract
    assert rel.back_populates == "customer"
    assert rel.uselist is True


def test_contract_customer_relationship():
    rel = get_relationship(Contract, "customer")
    assert rel.mapper.class_ is Customer
    assert rel.back_populates == "contracts"
    assert rel.uselist is False


def test_contract_event_relationship():
    rel = get_relationship(Contract, "event")
    assert rel.mapper.class_ is Event
    assert rel.back_populates == "contract"
    assert rel.uselist is False


def test_event_contract_relationship():
    rel = get_relationship(Event, "contract")
    assert rel.mapper.class_ is Contract
    assert rel.back_populates == "event"
    assert rel.uselist is False


def test_event_support_relationship():
    rel = get_relationship(Event, "support")
    assert rel.mapper.class_ is Collaborator
    assert rel.back_populates == "events_support"
    assert rel.uselist is False