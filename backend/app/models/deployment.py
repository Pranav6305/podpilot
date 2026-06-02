from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
# Database Table
from app.database.base import Base


class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True, index=True)
    app_name = Column(String, nullable=False)
    image_name = Column(String, nullable=False)
    replicas = Column(Integer, nullable=False)
    container_port = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
