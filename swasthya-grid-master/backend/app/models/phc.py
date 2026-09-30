import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Numeric, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class PHC(Base):
    __tablename__ = "phcs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    district_id = Column(UUID(as_uuid=True), ForeignKey("districts.id", ondelete="RESTRICT"), nullable=False)
    name = Column(String(150), nullable=False)
    code = Column(String(30), nullable=False, unique=True)
    address = Column(Text, nullable=True)
    latitude = Column(Numeric(9, 6), nullable=False)
    longitude = Column(Numeric(9, 6), nullable=False)
    total_beds = Column(Integer, default=0, nullable=False)
    active_doctors = Column(Integer, default=0, nullable=False)
    active_nurses = Column(Integer, default=0, nullable=False)
    status = Column(String(20), default="healthy", nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    district = relationship("District", back_populates="phcs", lazy="selectin")
    inventory = relationship("Inventory", back_populates="phc", cascade="all, delete-orphan", lazy="selectin")
    beds = relationship("Bed", back_populates="phc", uselist=False, cascade="all, delete-orphan", lazy="selectin")
    staff = relationship("Staff", back_populates="phc", cascade="all, delete-orphan", lazy="selectin")
    patient_visits = relationship("PatientVisit", back_populates="phc", cascade="all, delete-orphan", lazy="selectin")
    medicine_consumption = relationship("MedicineConsumption", back_populates="phc", cascade="all, delete-orphan", lazy="selectin")
    forecasts = relationship("Forecast", back_populates="phc", cascade="all, delete-orphan", lazy="selectin")
    risk_alerts = relationship("RiskAlert", back_populates="phc", cascade="all, delete-orphan", lazy="selectin")
    outgoing_transfers = relationship(
        "ResourceTransfer",
        foreign_keys="ResourceTransfer.source_phc_id",
        back_populates="source_phc",
        lazy="selectin"
    )
    incoming_transfers = relationship(
        "ResourceTransfer",
        foreign_keys="ResourceTransfer.destination_phc_id",
        back_populates="destination_phc",
        lazy="selectin"
    )
