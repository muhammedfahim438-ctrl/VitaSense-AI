from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ══════════════════════════════════════════════════════════════
# TABLE 1 — PREDICTIONS
# Stores every diabetes prediction made by users
# ══════════════════════════════════════════════════════════════
class Prediction(db.Model):
    __tablename__ = 'predictions'

    id              = db.Column(db.Integer, primary_key=True)

    # Input features
    pregnancies     = db.Column(db.Float, nullable=False)
    glucose         = db.Column(db.Float, nullable=False)
    blood_pressure  = db.Column(db.Float, nullable=False)
    skin_thickness  = db.Column(db.Float, nullable=False)
    insulin         = db.Column(db.Float, nullable=False)
    bmi             = db.Column(db.Float, nullable=False)
    dpf             = db.Column(db.Float, nullable=False)
    age             = db.Column(db.Float, nullable=False)

    # Prediction results
    result          = db.Column(db.String(20),  nullable=False)  # Diabetic / Not Diabetic
    risk_percent    = db.Column(db.Float,        nullable=False)  # 0 - 100
    risk_category   = db.Column(db.String(20),  nullable=False)  # Normal / Prediabetes / Diabetes
    hba1c_estimate  = db.Column(db.Float,        nullable=True)   # Estimated HbA1c

    # Timestamp
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':             self.id,
            'pregnancies':    self.pregnancies,
            'glucose':        self.glucose,
            'blood_pressure': self.blood_pressure,
            'skin_thickness': self.skin_thickness,
            'insulin':        self.insulin,
            'bmi':            self.bmi,
            'dpf':            self.dpf,
            'age':            self.age,
            'result':         self.result,
            'risk_percent':   self.risk_percent,
            'risk_category':  self.risk_category,
            'hba1c_estimate': self.hba1c_estimate,
            'created_at':     self.created_at.strftime('%Y-%m-%d %H:%M')
        }

# ══════════════════════════════════════════════════════════════
# TABLE 2 — CALENDAR ENTRIES
# Stores daily blood sugar logs from the Sugar Tracker
# ══════════════════════════════════════════════════════════════
class CalendarEntry(db.Model):
    __tablename__ = 'calendar_entries'

    id              = db.Column(db.Integer, primary_key=True)
    date            = db.Column(db.String(20),  nullable=False)   # YYYY-MM-DD
    sugar_level     = db.Column(db.Float,        nullable=False)   # mg/dL
    sugar_status    = db.Column(db.String(20),  nullable=False)   # Normal/Prediabetes/High/Low
    notes           = db.Column(db.String(200), nullable=True)    # Optional notes
    created_at      = db.Column(db.DateTime,    default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':           self.id,
            'date':         self.date,
            'sugar_level':  self.sugar_level,
            'sugar_status': self.sugar_status,
            'notes':        self.notes,
            'created_at':   self.created_at.strftime('%Y-%m-%d %H:%M')
        }

# ══════════════════════════════════════════════════════════════
# TABLE 3 — CHAT HISTORY
# Stores chatbot conversations
# ══════════════════════════════════════════════════════════════
class ChatHistory(db.Model):
    __tablename__ = 'chat_history'

    id           = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(500), nullable=False)
    bot_reply    = db.Column(db.String(2000), nullable=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':           self.id,
            'user_message': self.user_message,
            'bot_reply':    self.bot_reply,
            'created_at':   self.created_at.strftime('%Y-%m-%d %H:%M')
        }