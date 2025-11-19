# app/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from .database import Base

class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    machine_name = Column(String, index=True)
    status = Column(String, default="inactive")
    model_id = Column(Integer, unique=True, index=True)
    metrics = Column(JSONB, nullable=True)
