from enum import StrEnum


class DocumentType(StrEnum):
    COURSE = "course"           # cours
    EXAM_PAPER = "exam_paper"   # sujet d'examen
    EXERCISE = "exercise"       # exercice
    CORRECTION = "correction"   # corrigé
    OTHER = "other"             # autre


class DocumentSource(StrEnum):
    USER = "user"               # document importé par l'élève
    EXTERNAL = "external"       # source externe vérifiée
    AI_GENERATED = "ai_generated" # contenu généré par l'IA
