import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, Time, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    attendance_date = Column(Date, nullable=False)
    status = Column(String(20), default="present", nullable=False)  # present, absent, leave, on_duty
    check_in = Column(Time, nullable=True)
    check_out = Column(Time, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    staff_member = relationship("Staff", back_populates="attendance_records", lazy="selectin")

    __table_args__ = (
        UniqueConstraint("staff_id", "attendance_date", name="uq_attendance_staff_date"),
    )
