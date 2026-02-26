from app.extensions import db
from datetime import datetime

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(100))  # Tipo de actividad (taller, club de lectura, etc.)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(10))  # Hora (formato HH:MM)
    duration = db.Column(db.Integer)  # Duración en minutos
    max_slots = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="borrador")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to enrollments
    enrollments = db.relationship('Enrollment', backref='activity', lazy=True, cascade='all, delete-orphan')
