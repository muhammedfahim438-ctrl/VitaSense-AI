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

# ══════════════════════════════════════════════════════════════
# CREATE FLASK APP
# ══════════════════════════════════════════════════════════════
app = Flask(__name__)

# ── CONFIGURATION ────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.config['SECRET_KEY']                  = 'vitasense-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI']     = f'sqlite:///{os.path.join(BASE_DIR, "vitasense.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ── CORS — Allow frontend to connect ─────────────────────────
CORS(app, resources={r"/api/*": {
    "origins": [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "null"
    ],
    "supports_credentials": True
}})

# ── DATABASE ─────────────────────────────────────────────────
db.init_app(app)

# ── REGISTER BLUEPRINTS ──────────────────────────────────────
app.register_blueprint(predict_bp)
app.register_blueprint(food_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(calendar_bp)

# ── CREATE TABLES ────────────────────────────────────────────
with app.app_context():
    db.create_all()
    print("✅ Database tables created!")

# ══════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════

# Health check
@app.route('/')
def index():
    return jsonify({
        'status':  'success',
        'message': '🏥 VitaSense AI Backend is Running!',
        'version': '1.0.0',
        'team':    'Catalyst Crew',
        'college': 'Nehru Arts and Science College, Coimbatore',
        'endpoints': {
            'predict':          'POST /api/predict',
            'predictions':      'GET  /api/predictions',
            'dashboard_stats':  'GET  /api/dashboard/stats',
            'food_check':       'POST /api/food',
            'food_list':        'GET  /api/food/list',
            'chatbot':          'POST /api/chatbot',
            'chat_history':     'GET  /api/chatbot/history',
            'quick_replies':    'GET  /api/chatbot/replies',
            'calendar_add':     'POST /api/calendar/add',
            'calendar_all':     'GET  /api/calendar',
            'calendar_month':   'GET  /api/calendar/month',
            'calendar_stats':   'GET  /api/calendar/stats',
            'calendar_delete':  'DELETE /api/calendar/delete/<id>',
        }
    })

# ══════════════════════════════════════════════════════════════
# RUN SERVER
# ══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("=" * 55)
    print("  🏥 VitaSense AI - Starting Server...")
    print("  Catalyst Crew | Nehru Arts and Science College")
    print("=" * 55)
    print("  Backend  : http://127.0.0.1:5000")
    print("  Frontend : Open vitasense.html with Live Server")
    print("=" * 55)
    app.run(debug=True, port=5000)