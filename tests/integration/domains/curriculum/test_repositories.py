from src.domains.curriculum.entities import Subject, Chapter, Lesson
from src.domains.curriculum.repositories.filters import SubjectFilter, ChapterFilter, LessonFilter
from src.domains.curriculum.repositories.sql import SubjectRepository, ChapterRepository, LessonRepository


def test_subject_repository_filters(uow_factory):
    with uow_factory() as uow:
        repo = uow.get_repository(SubjectRepository)
        
        s1 = Subject.create(name="Subject 1", code="S1")
        s2 = Subject.create(name="Subject 2", code="S2")
        s2.is_active = False
        
        repo.add(s1)
        repo.add(s2)
        
        # Test code filter
        res = repo.list(SubjectFilter(code="S1"))
        assert len(res) == 1
        assert res[0].name == "Subject 1"
        
        # Test is_active filter
        res = repo.list(SubjectFilter(is_active=False))
        assert len(res) == 1
        assert res[0].name == "Subject 2"
        



def test_chapter_repository_filters(uow_factory):
    with uow_factory() as uow:
        repo = uow.get_repository(ChapterRepository)
        
        import uuid
        sid1 = uuid.uuid4()
        sid2 = uuid.uuid4()
        
        c1 = Chapter.create(subject_id=sid1, title="C1", order=1)
        c2 = Chapter.create(subject_id=sid2, title="C2", order=2)
        
        repo.add(c1)
        repo.add(c2)
        
        res = repo.list(ChapterFilter(subject_id=sid1))
        assert len(res) == 1
        assert res[0].title == "C1"
        



def test_lesson_repository_filters(uow_factory):
    with uow_factory() as uow:
        repo = uow.get_repository(LessonRepository)
        
        import uuid
        cid1 = uuid.uuid4()
        cid2 = uuid.uuid4()
        
        l1 = Lesson.create(chapter_id=cid1, title="L1", content="X", order=1)
        l2 = Lesson.create(chapter_id=cid2, title="L2", content="Y", order=2)
        
        repo.add(l1)
        repo.add(l2)
        
        res = repo.list(LessonFilter(chapter_id=cid2))
        assert len(res) == 1
        assert res[0].title == "L2"
        

