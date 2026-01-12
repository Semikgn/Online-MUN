from app import app
from models import db, Country

def seed_data():
    with app.app_context():
        # Örnek ülkeler ekle
        countries = [
            Country(name='Country A', flag_url='http://example.com/flag_a.png', economy=70, military=60, stability=80),
            Country(name='Country B', flag_url='http://example.com/flag_b.png', economy=50, military=70, stability=60),
            Country(name='Country C', flag_url='http://example.com/flag_c.png', economy=90, military=40, stability=70),
        ]
        
        db.session.bulk_save_objects(countries)
        db.session.commit()
        print("Veritabanı örnek verilerle dolduruldu.")

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # Mevcut tabloları sil
        db.create_all()  # Tabloları oluştur
        seed_data()      # Örnek verileri ekle