from src.domains.curriculum.entities import Subject, Chapter, Lesson
from src.core.entities import generate_id

def test_subject_create():
    subject = Subject.create(name="Maths", code="MATH")
    assert subject.id is not None
    assert subject.name == "Maths"
    assert subject.code == "MATH"
    assert subject.is_active is True
    assert not subject.collect_events()

def test_chapter_create():
    subject_id = generate_id()
    chapter = Chapter.create(subject_id=subject_id, title="Algèbre", order=1, description="Bases")
    assert chapter.id is not None
    assert chapter.subject_id == subject_id
    assert chapter.title == "Algèbre"
    assert chapter.order == 1
    assert chapter.description == "Bases"

def test_lesson_create():
    chapter_id = generate_id()
    lesson = Lesson.create(chapter_id=chapter_id, title="Polynômes", content="Contenu ici", order=1)
    assert lesson.id is not None
    assert lesson.chapter_id == chapter_id
    assert lesson.title == "Polynômes"
    assert lesson.content == "Contenu ici"
    assert lesson.order == 1
