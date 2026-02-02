import uuid
import enum
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    ForeignKey,
    String,
    Float,
    DateTime,
    func,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .ai_audit import AiAudit


class Source(str, enum.Enum):
    WEB = "WEB"
    TELEGRAM = "TELEGRAM"


class FoodLog(Base):
    __tablename__ = "food_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    food_name: Mapped[str] = mapped_column(String, nullable=False)
    calories: Mapped[float] = mapped_column(Float, default=0.0)
    proteins: Mapped[float] = mapped_column(Float, default=0.0)
    carbs: Mapped[float] = mapped_column(Float, default=0.0)
    fats: Mapped[float] = mapped_column(Float, default=0.0)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    source: Mapped[Source] = mapped_column(
        Enum(Source, name="source_type", create_type=False),
        default=Source.WEB,
        server_default=Source.WEB.value,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, onupdate=func.now(), nullable=True
    )

    user: Mapped["User"] = relationship("User", back_populates="food_logs")
    ai_audits: Mapped["AiAudit | None"] = relationship(
        "AiAudit",
        back_populates="food_log",
        cascade="all, delete-orphan",
        uselist=False,
    )
