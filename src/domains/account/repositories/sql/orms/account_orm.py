"""Account ORM models.

These are the same physical tables as before (accounts, account_roles).
We import the tables from the access_control ORM so the FK relationships
are declared in one place (access_control keeps role/permission tables).
"""
from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

# Association table lives here since Account owns the relationship
account_roles = Table(
    "account_roles",
    Base.metadata,
    Column("account_id", ForeignKey("accounts.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    extend_existing=True,
)


class AccountOrm(Base):
    __tablename__ = "accounts"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(25), nullable=False)
    last_name: Mapped[str] = mapped_column(String(25), nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    roles = relationship("RoleOrm", secondary=account_roles, lazy="joined")
