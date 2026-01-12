from flask import Flask, jsonify, render_template, request
from models import db, Country, EventLog
from game_engine import GameEngine
import os


app = Flask(__name__)
# Veritabanı yapılandırması
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'instance', 'mun_game.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanını app ile bağla
db.init_app(app)

# Routes
@app.route('/dashboard')
def home():
    return render_template('dashboard.html')

@app.route('/api/countries', methods=['GET'])
def get_countries():
    # Tüm ülkeleri veritabanından al
    countries = Country.query.all()
    # Tüm ülkeleri JSON formatında döndür
    return jsonify([country.to_dict() for country in countries])

@app.route('/admin', methods=['GET'])
def admin_panel():
    # Ülkeleri çekip HTML'e gönderiyoruz ki listeden seçebilelim
    all_countries = Country.query.all()
    return render_template('admin.html', countries=all_countries)

@app.route('/api/execute_action', methods=['POST'])
def execute_action():
    # Formdan gelen verileri al
    source_id = request.form.get('source_id')
    target_id = request.form.get('target_id')
    action_type = request.form.get('action_type')

    # Motoru çalıştır
    engine = GameEngine()
    result_message = engine.execute_action(source_id, target_id, action_type)

    # Admin sayfasına geri dön ve mesajı göster
    all_countries = Country.query.all()
    return render_template('admin.html', countries=all_countries, message=result_message)

@app.route('/api/news', methods=['GET'])
def get_news():
    # En son eklenen 5 haberi çek (Ters tarih sırasına göre)
    logs = EventLog.query.order_by(EventLog.timestamp.desc()).limit(5).all()
    return jsonify([log.to_dict() for log in logs])

if __name__ == '__main__':
    app.run(debug=True, port=5000)