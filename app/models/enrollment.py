from app.extensions import db
from datetime import datetime

class Enrollment(db.Model):
    __table_args__ = (
        db.UniqueConstraint('email', 'activity_id', name='unique_enrollment'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))  # Teléfono del participante
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)  # Link to user account if logged in
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="confirmada")  # confirmada, cancelada
    attended = db.Column(db.Boolean, default=None, nullable=True)  # None=pendiente, True=asistió, False=no asistió
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
