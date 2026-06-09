from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime




class Base(DeclarativeBase):
    pass


# a voir pour gerer -> table role avec les 3 possiblités pour limiter la selection
ROLES = ["commercial", "support", "gestion"]


# table des collaborateurs
class Collaborateur(Base):
    __tablename__ = "collaborateur"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    mot_de_passe = Column(String(255), nullable=False)
    telephone = Column(String(20))
    role = Column(String(20), nullable=False)  # "commercial", "support", "gestion"
    date_creation = Column(DateTime, default=datetime.now)

    clients = relationship("Client", back_populates="commercial")


# table des clients
class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    telephone = Column(String(20))
    nom_entreprise = Column(String(150))
    date_creation = Column(DateTime, default=datetime.now)
    date_dernier_contact = Column(DateTime)
    commercial_id = Column(Integer, ForeignKey("collaborateur.id"))

    commercial = relationship("Collaborateur", back_populates="clients")
    contrats = relationship("Contrat", back_populates="client")
    evenements = relationship("Evenement", back_populates="client")


# table des contrats
class Contrat(Base):
    __tablename__ = "contrat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client.id"))
    commercial_id = Column(Integer, ForeignKey("collaborateur.id"))
    montant_total = Column(Float)
    montant_a_payer = Column(Float)
    date_creation = Column(DateTime)
    signe = Column(Boolean)

    client = relationship("Client", back_populates="contrats")
    commercial = relationship("Collaborateur", foreign_keys=[commercial_id])
    evenement = relationship("Evenement", back_populates="contrat", uselist=False)


# table des évenements
class Evenement(Base):
    __tablename__ = "evenement"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    contrat_id = Column(Integer, ForeignKey("contrat.id"))
    client_id = Column(Integer, ForeignKey("client.id"))
    support_id = Column(Integer, ForeignKey("collaborateur.id"))
    date_debut = Column(DateTime)
    date_fin = Column(DateTime)
    adresse = Column(String(150))
    participants = Column(Integer)
    notes = Column(String(1000))

    contrat = relationship("Contrat", back_populates="evenement")
    client = relationship("Client", back_populates="evenements")
    support = relationship("Collaborateur", foreign_keys=[support_id])






