import pytest
from datetime import date
from app.models.activity import Activity
from app.extensions import db


@pytest.mark.unit
class TestActivityModel:
    
    def test_activity_creation(self, db):
        """RF01: Crear actividad"""
        activity = Activity(
            title='Taller Test',
            description='Descripción test',
            date=date(2026, 4, 1),
            max_slots=20,
            status='borrador'
        )
        
        db.session.add(activity)
        db.session.commit()
        
        assert activity.id is not None
        assert activity.status == 'borrador'
        assert activity.title == 'Taller Test'
    
    def test_default_status(self, db):
        """RF02: Estado por defecto es 'borrador'"""
        activity = Activity(
            title='Test',
            description='Test desc',
            date=date(2026, 4, 1),
            max_slots=10
        )
        
        db.session.add(activity)
        db.session.commit()
        
        assert activity.status == 'borrador'
    
    def test_activity_dates(self, db):
        """Verificar manejo de fechas"""
        test_date = date(2026, 6, 15)
        activity = Activity(
            title='Test Fecha',
            description='Test',
            date=test_date,
            max_slots=10
        )
        
        db.session.add(activity)
        db.session.commit()
        
        assert activity.date == test_date
    
    def test_activity_representation(self):
        """Test string representation"""
        activity = Activity(
            title='Taller Representación',
            description='Test',
            date=date(2026, 4, 1),
            max_slots=10
        )
        assert 'Taller Representación' in str(activity)
    
    def test_activity_max_slots(self, db):
        """Verificar límite de plazas"""
        activity = Activity(
            title='Test Plazas',
            description='Test',
            date=date(2026, 4, 1),
            max_slots=25
        )
        
        db.session.add(activity)
        db.session.commit()
        
        assert activity.max_slots == 25
