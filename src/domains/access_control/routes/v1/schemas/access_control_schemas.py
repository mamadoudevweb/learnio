from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RoleCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    permission_ids: list[UUID] | None = None


class RoleResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None = None
    permission_ids: list[UUID] = []
    created_at: datetime
    updated_at: datetime


class PermissionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    domain: str
    resource: str
    action: str
    created_at: datetime
    updated_at: datetime
