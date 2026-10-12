from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AccountCreateSchema(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=25)
    last_name: str = Field(..., min_length=1, max_length=25)
    birth_date: date | None = None
    active: bool = True
    role_ids: list[UUID] | None = None


class AccountUpdateSchema(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=25)
    last_name: str | None = Field(default=None, min_length=1, max_length=25)
    birth_date: date | None = None
    active: bool | None = None


class AccountResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
    birth_date: date | None = None
    active: bool = True
    role_ids: list[UUID] = []
    created_at: datetime
    updated_at: datetime
