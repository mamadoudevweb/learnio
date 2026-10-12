from dataclasses import dataclass

from src.core.repositories.filters import EntityFilter


@dataclass(kw_only=True)
class AccountFilter(EntityFilter):
    active: bool | None = None
    search: str | None = None
