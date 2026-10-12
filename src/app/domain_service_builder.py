"""Constructeur des services de domaine.

Instancie chaque service de domaine avec la fabrique d'unités de travail.
Sera enrichi à chaque nouveau domaine.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.domains.curriculum.services.chapter_service import ChapterService
from src.domains.curriculum.services import CurriculumDomainService
from src.domains.curriculum.services.lesson_service import LessonService
from src.domains.curriculum.services.subject_service import SubjectService
from src.domains.library.services import DocumentService, LibraryDomainService


@dataclass
class DomainServices:
    """Conteneur de tous les services de domaine de l'application."""

    curriculum: CurriculumDomainService
    library: LibraryDomainService


def build_domain_services(uow_factory: Any) -> DomainServices:
    """Construit et retourne le conteneur de services de domaine."""
    curriculum = CurriculumDomainService(
        subject_service=SubjectService(uow_factory),
        chapter_service=ChapterService(uow_factory),
        lesson_service=LessonService(uow_factory),
    )
    library = LibraryDomainService(
        document_service=DocumentService(uow_factory),
    )
    return DomainServices(curriculum=curriculum, library=library)
