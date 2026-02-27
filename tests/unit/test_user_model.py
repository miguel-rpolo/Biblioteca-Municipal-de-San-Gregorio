import pytest
from app.models.user import User


@pytest.mark.unit
class TestUserModel:
    
    def test_password_hashing(self):
        """RF14: Contraseñas deben hashearse"""
        user = User(username='test', role='admin')
        user.set_password('password123')
        
        assert user.password_hash != 'password123'
        assert len(user.password_hash) > 20
    
    def test_password_verification(self):
        """RF14: Verificación de contraseña"""
        user = User(username='test', role='admin')
        user.set_password('correct_password')
        
        assert user.check_password('correct_password') is True
        assert user.check_password('wrong_password') is False
    
    def test_user_creation(self, db):
        """Crear usuario correctamente"""
        user = User(username='admin@test.com', role='admin')
        user.set_password('pass123')
        
        db.session.add(user)
        db.session.commit()
        
        saved_user = User.query.filter_by(username='admin@test.com').first()
        assert saved_user is not None
        assert saved_user.role == 'admin'
    
    def test_user_representation(self):
        """Test string representation"""
        user = User(username='test@test.com', role='admin')
        assert 'test@test.com' in str(user)
    
    def test_user_role_assignment(self, db):
        """Verificar asignación de rol"""
        user = User(username='user@test.com', role='user')
        user.set_password('pass123')
        
        db.session.add(user)
        db.session.commit()
        
        assert user.role == 'user'
