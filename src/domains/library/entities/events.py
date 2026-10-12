from dataclasses import dataclass
from uuid import UUID

from src.core.entities import DomainEvent


@dataclass(frozen=True)
class DocumentCreated(DomainEvent):
    document_id: UUID
    title: str


@dataclass(frozen=True)
class DocumentUpdated(DomainEvent):
    document_id: UUID


@dataclass(frozen=True)
class DocumentDeleted(DomainEvent):
    document_id: UUID
