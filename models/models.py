from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass


# table des Roles
class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)  # "commercial", "support", "gestion"

    collaborators = relationship("Collaborator", back_populates="role")


# table des Collaborators
class Collaborator(Base):
    __tablename__ = "collaborator"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone = Column(String(20))
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    date_creation = Column(DateTime, default=datetime.now)

    customers = relationship("Customer", back_populates="commercial", foreign_keys="Customer.commercial_id")
    events_support = relationship("Event", back_populates="support", foreign_keys="Event.support_id")
    role = relationship("Role", back_populates="collaborators")


# table des Customers
class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    phone = Column(String(20))
    company_name = Column(String(150))
    date_creation = Column(DateTime, default=datetime.now)
    date_last_contact = Column(DateTime, default=datetime.now)
    commercial_id = Column(Integer, ForeignKey("collaborator.id"))

    commercial = relationship("Collaborator", back_populates="customers")
    contracts = relationship("Contract", back_populates="customer")


# table des Contracts
class Contract(Base):
    __tablename__ = "contract"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    total_amount = Column(Float)
    amount_to_pay = Column(Float)
    date_creation = Column(DateTime, default=datetime.now)
    signed = Column(Boolean)

    customer = relationship("Customer", back_populates="contracts")
    event = relationship("Event", back_populates="contract", uselist=False)


# table des évenements
class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    contract_id = Column(Integer, ForeignKey("contract.id"))
    support_id = Column(Integer, ForeignKey("collaborator.id"))
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    location = Column(String(150))
    attendees = Column(Integer)
    notes = Column(String(1000))

    contract = relationship("Contract", back_populates="event")
    support = relationship("Collaborator", back_populates="events_support", foreign_keys="Event.support_id")
