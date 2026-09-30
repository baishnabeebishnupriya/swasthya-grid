import uuid
from datetime import date
from sqlalchemy import Column, String, Boolean, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Staff(Base):
    __tablename__ = "staff"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phc_id = Column(UUID(as_uuid=True), ForeignKey("phcs.id", ondelete="CASCADE"), nullable=False)
    employee_code = Column(String(30), nullable=False, unique=True)
    name = Column(String(120), nullable=False)
    role = Column(String(30), nullable=False)  # doctor, nurse, pharmacist, lab_technician, administrative, other
    specialization = Column(String(100), nullable=True)
    employment_type = Column(String(30), default="permanent", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    joined_at = Column(Date, default=date.today, nullable=False)

    # Relationships
    phc = relationship("PHC", back_populates="staff", lazy="selectin")
    attendance_records = relationship("Attendance", back_populates="staff_member", cascade="all, delete-orphan", lazy="selectin")
