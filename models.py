from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# DB nesnesini burada başlatıyoruz
db = SQLAlchemy()

# Ülke modeli
class Country(db.Model):
    __tablename__ = 'countries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    flag_url = db.Column(db.String(200)) # Bayrak
    
    # İstatistikler (0-100 arası)
    economy = db.Column(db.Integer, default=50)
    military = db.Column(db.Integer, default=50)
    stability = db.Column(db.Integer, default=50)
    
    def to_dict(self):
        """Objeyi JSON formatına çevirmek için yardımcı fonksiyon"""
        return {
            'id': self.id,
            'name': self.name,
            'stats': {
                'economy': self.economy,
                'military': self.military,
                'stability': self.stability
            }
        }
# Ekstra: Olay günlüğü modeli
class EventLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    # Yardımcı fonksiyon
    def to_dict(self):
        return {
            'message': self.message,
            'time': self.timestamp.strftime("%H:%M")
        }