from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Enum
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime




class Base(DeclarativeBase):
    pass



# table des Collaborators
class Collaborator(Base):
    __tablename__ = "Collaborator"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone = Column(String(20))
    role = Column(Enum("commercial", "support", "gestion", name="role"), nullable=False)
    date_creation = Column(DateTime, default=datetime.now)

    customers = relationship("Customer", back_populates="commercial", foreign_keys="Customer.commercial_id")
    contracts = relationship("Contract", back_populates="commercial", foreign_keys="Contract.commercial_id")
    events_support = relationship("Event", back_populates="support", foreign_keys="Event.support_id")


# table des Customers
class Customer(Base):
    __tablename__ = "Customer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    telephone = Column(String(20))
    company_name = Column(String(150))
    date_creation = Column(DateTime, default=datetime.now)
    date_last_contact = Column(DateTime, default=datetime.now)
    commercial_id = Column(Integer, ForeignKey("Collaborator.id"))

    commercial = relationship("Collaborator", back_populates="customers")
    contracts = relationship("Contract", back_populates="customer")
    events = relationship("Event", back_populates="customer")


# table des Contracts
class Contract(Base):
    __tablename__ = "Contract"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("Customer.id"))
    commercial_id = Column(Integer, ForeignKey("Collaborator.id"))
    total_amount = Column(Float)
    amount_to_pay = Column(Float)
    date_creation = Column(DateTime)
    signed = Column(Boolean)

    customer = relationship("Customer", back_populates="contracts")
    commercial = relationship("Collaborator", back_populates="contracts" ,foreign_keys="Contract.commercial_id")
    event = relationship("Event", back_populates="contract", uselist=False)


# table des évenements
class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    contract_id = Column(Integer, ForeignKey("Contract.id"))
    customer_id = Column(Integer, ForeignKey("Customer.id"))
    support_id = Column(Integer, ForeignKey("Collaborator.id"))
    date_debut = Column(DateTime)
    date_fin = Column(DateTime)
    adresse = Column(String(150))
    participants = Column(Integer)
    notes = Column(String(1000))

    contract = relationship("Contract", back_populates="event")
    customer = relationship("Customer", back_populates="events")
    support = relationship("Collaborator", back_populates="events_support", foreign_keys="Event.support_id")






