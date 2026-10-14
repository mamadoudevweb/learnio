from datetime import date

from pydantic import BaseModel, Field

from src.domains.account.routes.v1.schemas.account_schemas import AccountResponseSchema


class RegisterRequestSchema(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=25)
    last_name: str = Field(..., min_length=1, max_length=25)
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=6)
    birth_date: date | None = None


class LoginRequestSchema(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=1)


class PasswordResetRequestSchema(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)


class PasswordResetConfirmSchema(BaseModel):
    token: str | None = None
    new_password: str = Field(..., min_length=6)


class LoginResponseSchema(BaseModel):
    token: str
    account: AccountResponseSchema
    permissions: list[str] = []
