# ══════════════════════════════════════════════════════════════
# VitaSense AI - Main Flask Application
# Catalyst Crew | Nehru Arts and Science College, Coimbatore
# ══════════════════════════════════════════════════════════════

from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from routes.predict  import predict_bp
from routes.food     import food_bp
from routes.chatbot  import chatbot_bp
from routes.calendar import calendar_bp
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.config['SECRET_KEY']                  = 'vitasense-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI']     = f'sqlite:///{os.path.join(BASE_DIR, "vitasense.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db.init_app(app)

app.register_blueprint(predict_bp)
app.register_blueprint(food_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(calendar_bp)

with app.app_context():
    db.create_all()
    print("Database tables created!")

@app.route('/')
def index():
    return jsonify({
        'status':  'success',
        'message': 'VitaSense AI Backend is running!',
    })

if __name__ == '__main__':
    print("=" * 55)
    print("  VitaSense AI - Starting Server...")
    print("=" * 55)
    app.run(debug=True, port=5000)
