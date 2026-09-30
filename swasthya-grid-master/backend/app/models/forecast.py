import uuid
from datetime import datetime
from sqlalchemy import Column, String, Numeric, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phc_id = Column(UUID(as_uuid=True), ForeignKey("phcs.id", ondelete="CASCADE"), nullable=False)
    medicine_id = Column(UUID(as_uuid=True), ForeignKey("medicines.id", ondelete="RESTRICT"), nullable=False)
    forecast_date = Column(Date, nullable=False)
    predicted_demand = Column(Numeric(10, 2), nullable=False)
    lower_bound = Column(Numeric(10, 2), nullable=False)
    upper_bound = Column(Numeric(10, 2), nullable=False)
    confidence_score = Column(Numeric(5, 4), nullable=False)
    model_version = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    phc = relationship("PHC", back_populates="forecasts", lazy="selectin")
    medicine = relationship("Medicine", back_populates="forecasts", lazy="selectin")

    __table_args__ = (
        UniqueConstraint("phc_id", "medicine_id", "forecast_date", "model_version", name="uq_forecasts_phc_med_date_version"),
    )
