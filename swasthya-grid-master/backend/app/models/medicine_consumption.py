import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class MedicineConsumption(Base):
    __tablename__ = "medicine_consumption"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phc_id = Column(UUID(as_uuid=True), ForeignKey("phcs.id", ondelete="CASCADE"), nullable=False)
    medicine_id = Column(UUID(as_uuid=True), ForeignKey("medicines.id", ondelete="RESTRICT"), nullable=False)
    consumption_date = Column(Date, nullable=False)
    quantity_consumed = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    phc = relationship("PHC", back_populates="medicine_consumption", lazy="selectin")
    medicine = relationship("Medicine", back_populates="consumption_records", lazy="selectin")

    __table_args__ = (
        UniqueConstraint("phc_id", "medicine_id", "consumption_date", name="uq_medicine_consumption_phc_med_date"),
    )
