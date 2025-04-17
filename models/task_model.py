from app import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=True)
    days_remaining = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'is_completed': self.is_completed,
            'date_created': self.date_created,
            'due_date': self.due_date,
            'days_remaining': self.days_remaining
        }
    


