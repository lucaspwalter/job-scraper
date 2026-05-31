import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id"), nullable=False)
    title = Column(String, nullable=False)
    company = Column(String, nullable=True)
    url = Column(String, nullable=False, unique=True, index=True)
    found_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    notified = Column(Boolean, nullable=False, default=False)

    source = relationship("Source", back_populates="jobs")
