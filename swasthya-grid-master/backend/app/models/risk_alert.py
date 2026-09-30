import uuid
from datetime import datetime
from sqlalchemy import Column, String, Numeric, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class RiskAlert(Base):
    __tablename__ = "risk_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phc_id = Column(UUID(as_uuid=True), ForeignKey("phcs.id", ondelete="CASCADE"), nullable=False)
    medicine_id = Column(UUID(as_uuid=True), ForeignKey("medicines.id", ondelete="SET NULL"), nullable=True)
    alert_type = Column(String(40), nullable=False)  # stockout, bed_shortage, staff_shortage, demand_surge, emergency
    severity = Column(String(20), nullable=False)    # low, medium, high, critical
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    risk_score = Column(Numeric(5, 2), nullable=False)
    recommended_action = Column(Text, nullable=True)
    status = Column(String(20), default="open", nullable=False)  # open, acknowledged, resolved
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    phc = relationship("PHC", back_populates="risk_alerts", lazy="selectin")
    medicine = relationship("Medicine", back_populates="risk_alerts", lazy="selectin")
