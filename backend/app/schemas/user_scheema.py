from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str
    daily_calory_goal: float = 2000.0


class UserCreate(UserBase):
    password: str


class UserCreateTelegram(UserBase):
    telegram_id: int
    first_name: str
    username: str | None = None


class UserInDB(UserBase):
    id: UUID
    password: str


class UserResponse(UserBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
