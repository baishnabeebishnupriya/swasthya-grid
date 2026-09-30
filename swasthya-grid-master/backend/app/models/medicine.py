import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    generic_name = Column(String(150), nullable=False)
    category = Column(String(60), nullable=False)
    unit = Column(String(30), nullable=False)
    minimum_stock_level = Column(Integer, default=100, nullable=False)
    reorder_level = Column(Integer, default=200, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    inventory_items = relationship("Inventory", back_populates="medicine", lazy="selectin")
    consumption_records = relationship("MedicineConsumption", back_populates="medicine", lazy="selectin")
    forecasts = relationship("Forecast", back_populates="medicine", lazy="selectin")
    risk_alerts = relationship("RiskAlert", back_populates="medicine", lazy="selectin")
    transfers = relationship("ResourceTransfer", back_populates="medicine", lazy="selectin")
