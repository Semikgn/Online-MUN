from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Country(db.Model):
    __tablename__ = 'countries'
    
    # Temel Bilgiler
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # 1. Finansal & Askeri
    budget = db.Column(db.Integer, default=1000) # Milyar $ cinsinden bütçe
    military = db.Column(db.Integer, default=50) # Askeri Güç (0-100)
    
    # 2. Kaynaklar (0-100)
    oil = db.Column(db.Integer, default=50)      # Enerji/Petrol stoğu
    food = db.Column(db.Integer, default=50)     # Gıda stoğu
    tech = db.Column(db.Integer, default=50)     # Teknoloji seviyesi
    
    # 3. Sosyal Göstergeler
    happiness = db.Column(db.Integer, default=50) # Halk Mutluluğu (0-100)
    inflation = db.Column(db.Integer, default=10) # Enflasyon Oranı (%)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'stats': {
                'budget': self.budget,
                'military': self.military,
                'oil': self.oil,
                'food': self.food,
                'tech': self.tech,
                'happiness': self.happiness,
                'inflation': self.inflation
            }
        }

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    

class EventLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'message': self.message,
            'time': self.timestamp.strftime("%H:%M")
        }