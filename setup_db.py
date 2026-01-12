from app import app
from models import db, Country

def seed_data():
    """15 Ülkeyi Yeni Stratejik Verilerle Oluşturur"""
    
    countries = [

        Country(name="Almanya", budget=4200, military=60, oil=20, food=60, tech=95, happiness=85, inflation=5),
        Country(name="Türkiye", budget=900, military=85, oil=15, food=95, tech=60, happiness=60, inflation=45),
        Country(name="İtalya", budget=2100, military=50, oil=20, food=90, tech=75, happiness=70, inflation=8),
        Country(name="Birleşik Krallık", budget=3100, military=80, oil=50, food=40, tech=85, happiness=75, inflation=7),
        Country(name="Fransa", budget=2900, military=85, oil=30, food=80, tech=85, happiness=70, inflation=6),
        Country(name="Avusturya", budget=500, military=30, oil=20, food=70, tech=70, happiness=90, inflation=4),
        Country(name="İspanya", budget=1400, military=45, oil=10, food=85, tech=65, happiness=75, inflation=9),
        Country(name="İsviçre", budget=800, military=25, oil=5, food=50, tech=90, happiness=98, inflation=2),
        Country(name="Polonya", budget=700, military=75, oil=40, food=70, tech=55, happiness=65, inflation=12),
        # ABD: Süper güç. Her şeyi yüksek ama enflasyon riski var.
        Country(name="ABD", budget=23000, military=100, oil=90, food=90, tech=100, happiness=75, inflation=6),
        # Rusya: Enerji (Petrol) ve Askeri devi. Teknoloji ve Ekonomi yaptırımlardan dolayı biraz düşük.
        Country(name="Rusya", budget=1700, military=95, oil=100, food=80, tech=65, happiness=55, inflation=15),
        # Hollanda: Ticaret ve Lojistik merkezi. Teknoloji çok yüksek.
        Country(name="Hollanda", budget=1000, military=40, oil=30, food=75, tech=92, happiness=88, inflation=4),

        # Belçika: Diplomasi merkezi (AB/NATO). Dengeli, istikrarlı.
        Country(name="Belçika", budget=600, military=35, oil=10, food=60, tech=85, happiness=82, inflation=5),

        # Danimarka: Mutluluk ve Refah tavan. Yeşil enerji (Tech) yüksek.
        Country(name="Danimarka", budget=400, military=30, oil=40, food=65, tech=90, happiness=96, inflation=3),

        # Portekiz: Daha mütevazı bütçe ama sosyal açıdan (Mutluluk) güçlü.
        Country(name="Portekiz", budget=280, military=30, oil=10, food=70, tech=60, happiness=72, inflation=8),
    ]

    for country in countries:
        db.session.add(country)

    db.session.commit()
    print("Veritabanı 15 ülke ile güncellendi.")

if __name__ == '__main__':
    with app.app_context():
        # Veritabanını tamamen silip baştan kuruyoruz
        db.drop_all()
        db.create_all()
        seed_data()