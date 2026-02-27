import pytest
from datetime import date
from app.models.enrollment import Enrollment
from app.models.activity import Activity


@pytest.mark.unit
class TestEnrollmentModel:
    
    def test_enrollment_creation(self, db, activity):
        """RF08: Crear inscripción"""
        enrollment = Enrollment(
            user_name='Juan Pérez',
            email='juan@test.com',
            activity_id=activity.id
        )
        
        db.session.add(enrollment)
        db.session.commit()
        
        assert enrollment.id is not None
        assert enrollment.activity_id == activity.id
        assert enrollment.user_name == 'Juan Pérez'
    
    def test_enrollment_email(self, db, activity):
        """Verificar almacenamiento de email"""
        enrollment = Enrollment(
            user_name='Test User',
            email='test@example.com',
            activity_id=activity.id
        )
        
        db.session.add(enrollment)
        db.session.commit()
        
        saved_enrollment = Enrollment.query.filter_by(
            email='test@example.com'
        ).first()
        assert saved_enrollment is not None
        assert saved_enrollment.email == 'test@example.com'
    
    def test_enrollment_activity_relationship(self, db, activity):
        """Verificar relación con actividad"""
        enrollment = Enrollment(
            user_name='Test',
            email='test@test.com',
            activity_id=activity.id
        )
        
        db.session.add(enrollment)
        db.session.commit()
        
        # Verificar que se puede acceder a la actividad desde la inscripción
        assert enrollment.activity is not None
        assert enrollment.activity.id == activity.id
    
    def test_enrollment_representation(self, db, activity):
        """Test string representation"""
        enrollment = Enrollment(
            user_name='María García',
            email='maria@test.com',
            activity_id=activity.id
        )
        db.session.add(enrollment)
        db.session.commit()
        
        assert 'María García' in str(enrollment)
    
    def test_multiple_enrollments_same_activity(self, db, activity):
        """Múltiples inscripciones en misma actividad"""
        enrollment1 = Enrollment(
            user_name='Usuario 1',
            email='user1@test.com',
            activity_id=activity.id
        )
        enrollment2 = Enrollment(
            user_name='Usuario 2',
            email='user2@test.com',
            activity_id=activity.id
        )
        
        db.session.add(enrollment1)
        db.session.add(enrollment2)
        db.session.commit()
        
        enrollments = Enrollment.query.filter_by(activity_id=activity.id).all()
        assert len(enrollments) == 2
