import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class PatientVisit(Base):
    __tablename__ = "patient_visits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phc_id = Column(UUID(as_uuid=True), ForeignKey("phcs.id", ondelete="CASCADE"), nullable=False)
    visit_date = Column(Date, nullable=False)
    disease_category = Column(String(50), nullable=False)  # general, fever, dengue, malaria, respiratory, diarrhea, dehydration, injury, other
    patient_count = Column(Integer, default=0, nullable=False)
    emergency_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    phc = relationship("PHC", back_populates="patient_visits", lazy="selectin")

    __table_args__ = (
        UniqueConstraint("phc_id", "visit_date", "disease_category", name="uq_patient_visits_phc_date_category"),
    )
