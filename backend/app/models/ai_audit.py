from __future__ import annotations
import uuid
from datetime import datetime
from typing import Dict, TYPE_CHECKING, Any
from sqlalchemy import DateTime, String, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import Base

if TYPE_CHECKING:
    from .food_log import FoodLog


class AiAudit(Base):
    __tablename__ = "ai_audits"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    food_log_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("food_logs.id"), nullable=False, unique=True
    )
    prompt_used: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_response: Mapped[Dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    model_version: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    food_log: Mapped["FoodLog"] = relationship("FoodLog", back_populates="ai_audits")
