from app.extensions import db

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    max_slots = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="borrador")
