import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Numeric, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class ResourceTransfer(Base):
    __tablename__ = "resource_transfers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_phc_id = Column(UUID(as_uuid=True), ForeignKey("phcs.id", ondelete="RESTRICT"), nullable=False)
    destination_phc_id = Column(UUID(as_uuid=True), ForeignKey("phcs.id", ondelete="RESTRICT"), nullable=False)
    resource_type = Column(String(30), nullable=False)  # medicine, equipment, staff, other
    medicine_id = Column(UUID(as_uuid=True), ForeignKey("medicines.id", ondelete="SET NULL"), nullable=True)
    quantity = Column(Integer, nullable=False)
    requested_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(30), default="recommended", nullable=False)  # recommended, pending_approval, approved, in_transit, completed, cancelled
    distance_km = Column(Numeric(8, 2), nullable=True)
    estimated_arrival_minutes = Column(Integer, nullable=True)
    reason = Column(Text, nullable=False)
    approved_by = Column(String(100), nullable=True)

    # Relationships
    source_phc = relationship(
        "PHC",
        foreign_keys=[source_phc_id],
        back_populates="outgoing_transfers",
        lazy="selectin"
    )
    destination_phc = relationship(
        "PHC",
        foreign_keys=[destination_phc_id],
        back_populates="incoming_transfers",
        lazy="selectin"
    )
    medicine = relationship("Medicine", back_populates="transfers", lazy="selectin")
