from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class LegalEntity(Base):
    __tablename__ = 'legal_entities'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    applications = relationship('Application', back_populates='legal_entity')

class Credit(Base):
    __tablename__ = 'credits'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    interest_rate = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    repayment_term = Column(Integer, nullable=False)
    credit_applications = relationship('CreditsInApplication', back_populates='credit')

class Application(Base):
    __tablename__ = 'applications'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    legal_entity_id = Column(UUID(as_uuid=True), ForeignKey('legal_entities.id'), nullable=False)
    submission_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    legal_entity = relationship('LegalEntity', back_populates='applications')
    credit_applications = relationship('CreditsInApplication', back_populates='application')

class CreditsInApplication(Base):
    __tablename__ = 'credits_in_application'
    application_id = Column(UUID(as_uuid=True), ForeignKey('applications.id'), primary_key=True)
    credit_id = Column(UUID(as_uuid=True), ForeignKey('credits.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    application = relationship('Application', back_populates='credit_applications')
    credit = relationship('Credit', back_populates='credit_applications')