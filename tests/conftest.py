import pytest
from app import create_app
from app.extensions import db as _db
from app.models.user import User
from app.models.activity import Activity
from app.models.enrollment import Enrollment
from datetime import date


@pytest.fixture(scope='session')
def app():
    """Create application for the tests."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    ctx = app.app_context()
    ctx.push()
    
    yield app
    
    ctx.pop()


@pytest.fixture(scope='function')
def db(app):
    """Create database for the tests."""
    _db.create_all()
    
    yield _db
    
    _db.session.remove()
    _db.drop_all()


@pytest.fixture(scope='function')
def client(app, db):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def admin_user(db):
    """Create admin user."""
    user = User(username='admin@biblioteca.com', role='admin')
    user.set_password('admin123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def auth_admin(client, admin_user):
    """Authenticated admin client."""
    with client.session_transaction() as session:
        session['_user_id'] = str(admin_user.id)
    return client


@pytest.fixture
def activity(db):
    """Create a test activity."""
    activity = Activity(
        title='Taller Test',
        description='Descripción de prueba',
        date=date(2026, 5, 1),
        max_slots=10,
        status='borrador'
    )
    db.session.add(activity)
    db.session.commit()
    return activity


@pytest.fixture
def open_activity(db):
    """Create an open activity with available slots."""
    activity = Activity(
        title='Taller Abierto',
        description='Actividad abierta para inscripciones',
        date=date(2026, 5, 15),
        max_slots=10,
        status='abierta'
    )
    db.session.add(activity)
    db.session.commit()
    return activity


@pytest.fixture
def full_activity(db):
    """Create a full activity with no available slots."""
    activity = Activity(
        title='Taller Lleno',
        description='Sin plazas disponibles',
        date=date(2026, 5, 20),
        max_slots=2,
        status='abierta'
    )
    db.session.add(activity)
    db.session.commit()
    
    # Fill activity
    for i in range(2):
        enrollment = Enrollment(
            user_name=f'Usuario {i}',
            email=f'user{i}@test.com',
            activity_id=activity.id
        )
        db.session.add(enrollment)
    
    db.session.commit()
    return activity


@pytest.fixture
def activity_with_enrollments(db):
    """Create activity with some enrollments."""
    activity = Activity(
        title='Taller con Inscritos',
        description='Actividad con inscripciones',
        date=date(2026, 6, 1),
        max_slots=10,
        status='abierta'
    )
    db.session.add(activity)
    db.session.commit()
    
    # Add enrollments
    for i in range(3):
        enrollment = Enrollment(
            user_name=f'Participante {i+1}',
            email=f'participante{i+1}@test.com',
            activity_id=activity.id
        )
        db.session.add(enrollment)
    
    db.session.commit()
    return activity
