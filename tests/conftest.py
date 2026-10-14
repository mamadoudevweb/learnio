import pytest
from flask_jwt_extended import create_access_token
from sqlalchemy.orm import sessionmaker

from src.app.domain_service_builder import build_domain_services
from src.app.factory import create_app
from src.app.uow import REPOSITORY_CLASSES
from src.core.unit_of_work.sql_uow import SqlUnitOfWork


@pytest.fixture(scope="session")
def app():
    """Application Flask pour les tests."""
    app = create_app("testing")
    with app.app_context():
        yield app


@pytest.fixture(autouse=True)
def clear_email_outbox(app):
    """Vide la boîte d'envoi d'emails avant et après chaque test."""
    if "email_sender" in app.extensions:
        app.extensions["email_sender"].clear()
    yield
    if "email_sender" in app.extensions:
        app.extensions["email_sender"].clear()


@pytest.fixture
def client(app):
    """Client de test Flask."""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """Fournit une session de base de données isolée par test."""
    engine = app.extensions["engine"]
    connection = engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection, join_transaction_mode="create_savepoint")
    session = Session()

    yield session

    session.close()
    if transaction.is_active:
        transaction.rollback()
    connection.close()


@pytest.fixture
def uow_factory(db_session):
    """Fabrique d'UnitOfWork qui utilise la session de test isolée."""

    # Au lieu de créer une nouvelle session avec session_factory,
    # on passe directement la session isolée.
    def factory():
        uow = SqlUnitOfWork(
            session_factory=lambda: db_session,
            repository_classes=REPOSITORY_CLASSES,
        )
        return uow

    return factory


@pytest.fixture
def domain_service(uow_factory, app):
    """Service de domaine pointant vers la db_session de test."""
    email_sender = app.extensions.get("email_sender")
    return build_domain_services(uow_factory, email_sender=email_sender)


@pytest.fixture
def auth_headers(app):
    """Headers avec un faux token pour passer jwt_required."""
    with app.app_context():
        token = create_access_token(identity="test-user")
    return {"Authorization": f"Bearer {token}"}
