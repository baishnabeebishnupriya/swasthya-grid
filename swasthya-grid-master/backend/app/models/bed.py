import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Bed(Base):
    __tablename__ = "beds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phc_id = Column(UUID(as_uuid=True), ForeignKey("phcs.id", ondelete="CASCADE"), nullable=False, unique=True)
    total_beds = Column(Integer, default=0, nullable=False)
    occupied_beds = Column(Integer, default=0, nullable=False)
    reserved_beds = Column(Integer, default=0, nullable=False)
    available_beds = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    phc = relationship("PHC", back_populates="beds", lazy="selectin")
