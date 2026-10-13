"""Curriculum OpenAPI specifications."""

from src.domains.curriculum.routes.v1.openapi.chapter_openapi import (
    COMPONENTS as CHAPTER_COMPONENTS,
)
from src.domains.curriculum.routes.v1.openapi.chapter_openapi import (
    PATHS as CHAPTER_PATHS,
)
from src.domains.curriculum.routes.v1.openapi.chapter_openapi import (
    TAGS as CHAPTER_TAGS,
)
from src.domains.curriculum.routes.v1.openapi.lesson_openapi import (
    COMPONENTS as LESSON_COMPONENTS,
)
from src.domains.curriculum.routes.v1.openapi.lesson_openapi import (
    PATHS as LESSON_PATHS,
)
from src.domains.curriculum.routes.v1.openapi.lesson_openapi import (
    TAGS as LESSON_TAGS,
)
from src.domains.curriculum.routes.v1.openapi.subject_openapi import (
    COMPONENTS as SUBJECT_COMPONENTS,
)
from src.domains.curriculum.routes.v1.openapi.subject_openapi import (
    PATHS as SUBJECT_PATHS,
)
from src.domains.curriculum.routes.v1.openapi.subject_openapi import (
    TAGS as SUBJECT_TAGS,
)

TAGS = SUBJECT_TAGS + CHAPTER_TAGS + LESSON_TAGS
PATHS = {**SUBJECT_PATHS, **CHAPTER_PATHS, **LESSON_PATHS}
COMPONENTS = {
    "schemas": {
        **SUBJECT_COMPONENTS.get("schemas", {}),
        **CHAPTER_COMPONENTS.get("schemas", {}),
        **LESSON_COMPONENTS.get("schemas", {}),
    }
}

__all__ = ["COMPONENTS", "PATHS", "TAGS"]
