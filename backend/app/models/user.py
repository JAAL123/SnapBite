from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, BigInteger, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

if TYPE_CHECKING:
    from .food_log import FoodLog


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    telegram_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True, unique=True, index=True
    )
    daily_calory_goal: Mapped[float] = mapped_column(Float, default=2000.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    food_logs: Mapped[List["FoodLog"]] = relationship(
        "FoodLog", back_populates="user", cascade="all, delete-orphan"
    )
