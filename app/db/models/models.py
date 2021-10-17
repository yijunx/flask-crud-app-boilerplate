from sqlalchemy import Column, String, DateTime
from .base import Base


class Item(Base):
    __tablename__ = "test_items"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(String, nullable=False)
    created_by_name = Column(String, nullable=False)
