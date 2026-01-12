from app import app
from models import db, User

# --- AYARLAR ---
ADMIN_USER = "admin"
ADMIN_PASS = "12345"

def create_admin():
    with app.app_context():
        # Veritabanında tabloların güncel olduğundan emin ol
        db.create_all()
        
        # Eğer admin zaten varsa silip tekrar oluşturalım (Şifre yenilemek için)
        existing_user = User.query.filter_by(username=ADMIN_USER).first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
            print("Eski admin silindi.")
            
        # Yeni Admin Ekle
        new_admin = User(username=ADMIN_USER)
        new_admin.set_password(ADMIN_PASS)
        
        db.session.add(new_admin)
        db.session.commit()
        print(f"Admin kullanıcısı oluşturuldu! Kullanıcı: {ADMIN_USER} / Şifre: {ADMIN_PASS}")

if __name__ == '__main__':
    create_admin()