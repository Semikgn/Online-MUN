from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, Country, EventLog, User
from game_engine import GameEngine
from werkzeug.security import generate_password_hash # Admin oluşturma garantisi için
import os

app = Flask(__name__)

# --- AYARLAR ---
app.secret_key = 'cok_gizli_bir_anahtar_kelime_mun_2026'
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'instance', 'mun_game.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- LOGIN SETUP ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- YARDIMCI FONKSİYON: BAŞLANGIÇ VERİLERİ ---
# seed_data mantığını buraya taşıdık ki hata vermesin.
def get_initial_countries():
    return [
        Country(name="Almanya", budget=4200, military=60, oil=20, food=60, tech=95, happiness=85, inflation=5),
        Country(name="Türkiye", budget=900, military=85, oil=15, food=95, tech=60, happiness=60, inflation=45),
        Country(name="İtalya", budget=2100, military=50, oil=20, food=90, tech=75, happiness=70, inflation=8),
        Country(name="Birleşik Krallık", budget=3100, military=80, oil=50, food=40, tech=85, happiness=75, inflation=7),
        Country(name="Fransa", budget=2900, military=85, oil=30, food=80, tech=85, happiness=70, inflation=6),
        Country(name="Avusturya", budget=500, military=30, oil=20, food=70, tech=70, happiness=90, inflation=4),
        Country(name="İspanya", budget=1400, military=45, oil=10, food=85, tech=65, happiness=75, inflation=9),
        Country(name="İsviçre", budget=800, military=25, oil=5, food=50, tech=90, happiness=98, inflation=2),
        Country(name="Polonya", budget=700, military=75, oil=40, food=70, tech=55, happiness=65, inflation=12),
        Country(name="ABD", budget=23000, military=100, oil=90, food=90, tech=100, happiness=75, inflation=6),
        Country(name="Rusya", budget=1700, military=95, oil=100, food=80, tech=65, happiness=55, inflation=15),
        Country(name="Hollanda", budget=1000, military=40, oil=30, food=75, tech=92, happiness=88, inflation=4),
        Country(name="Belçika", budget=600, military=35, oil=10, food=60, tech=85, happiness=82, inflation=5),
        Country(name="Danimarka", budget=400, military=30, oil=40, food=65, tech=90, happiness=96, inflation=3),
        Country(name="Portekiz", budget=280, military=30, oil=10, food=70, tech=60, happiness=72, inflation=8),
    ]

# --- ROTALAR (ROUTES) ---

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = Country.query.all()
    return jsonify([country.to_dict() for country in countries])

@app.route('/api/news', methods=['GET'])
def get_news():
    logs = EventLog.query.order_by(EventLog.timestamp.desc()).limit(10).all()
    return jsonify([log.to_dict() for log in logs])

# --- GÜVENLİK VE ADMİN ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin_panel'))
        else:
            flash('Hatalı kullanıcı adı veya şifre!')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET'])
@login_required
def admin_panel():
    all_countries = Country.query.all()
    return render_template('admin.html', countries=all_countries)

@app.route('/api/execute_action', methods=['POST'])
@login_required
def execute_action():
    source_id = request.form.get('source_id')
    target_id = request.form.get('target_id')
    action_type = request.form.get('action_type')
    intensity = request.form.get('intensity')
    justification = request.form.get('justification')
    
    engine = GameEngine()
    result_message = engine.execute_action(source_id, target_id, action_type, intensity, justification)
    
    flash(result_message, 'success')
    return redirect(url_for('admin_panel'))

# --- OYUNU SIFIRLAMA ROTASI (DÜZELTİLDİ) ---
@app.route('/api/reset_game', methods=['POST'])
@login_required
def reset_game():
    try:
        # 1. Tabloları temizle
        db.session.query(EventLog).delete()
        db.session.query(Country).delete()
        
        # 2. Başlangıç verilerini al ve ekle
        initial_data = get_initial_countries()
        db.session.add_all(initial_data)
        
        # 3. Kaydet
        db.session.commit()
        
        flash('⚠️ OYUN BAŞARIYLA SIFIRLANDI! Tüm veriler başlangıç durumuna döndü.', 'info')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Hata oluştu: {str(e)}', 'danger')
        
    return redirect(url_for('admin_panel'))

# --- BAŞLATMA ---
if __name__ == '__main__':
    # Veritabanı tablolarını otomatik oluştur (İlk kurulum kolaylığı)
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)