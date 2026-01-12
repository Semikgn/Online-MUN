from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, Country, EventLog, User
from game_engine import GameEngine
import os


app = Flask(__name__)
app.secret_key = '0anahtar_kelime_mun_2026' # Session güvenliği için şart!
# Veritabanı yapılandırması
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'instance', 'mun_game.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Veritabanını app ile bağla
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)    
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
@app.route('/dashboard') #Herkese açık ana sayfa
def home():
    return render_template('dashboard.html')

@app.route('/api/countries', methods=['GET'])
def get_countries():
    # Tüm ülkeleri veritabanından al
    countries = Country.query.all()
    # Tüm ülkeleri JSON formatında döndür
    return jsonify([country.to_dict() for country in countries])

@app.route('/api/news', methods=['GET'])
def get_news():
    # En son eklenen 5 haberi çek (Ters tarih sırasına göre)
    logs = EventLog.query.order_by(EventLog.timestamp.desc()).limit(5).all()
    return jsonify([log.to_dict() for log in logs])

# Güvenlik için admin paneli korumalı kısım
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

@app.route('/help')
def help_page():
    return render_template('help.html')

# --------------------------------------------------------------
#Admin Paneli ve Eylem Gerçekleştirme
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
    
    # Motoru çalıştır (Yeni parametrelerle)
    engine = GameEngine()
    result_message = engine.execute_action(source_id, target_id, action_type, intensity, justification)
    
    flash(result_message, 'success')
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)