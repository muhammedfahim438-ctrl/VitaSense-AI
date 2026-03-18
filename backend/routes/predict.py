# ══════════════════════════════════════════════════════════════
# VitaSense AI - Prediction API Route
# Catalyst Crew | Nehru Arts and Science College, Coimbatore
# POST /api/predict  → Returns diabetes prediction result
# GET  /api/predictions → Returns last 10 predictions
# ══════════════════════════════════════════════════════════════

from flask import Blueprint, request, jsonify
from models import db, Prediction
from ai_model import predict_diabetes

predict_bp = Blueprint('predict', __name__)

# ══════════════════════════════════════════════════════════════
# POST /api/predict
# Accepts health data → returns prediction result
# ══════════════════════════════════════════════════════════════
@predict_bp.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'status':  'error',
                'message': 'No data received'
            }), 400

        # ── VALIDATE REQUIRED FIELDS ────────────────────────
        required = ['pregnancies','glucose','blood_pressure',
                    'skin_thickness','insulin','bmi','dpf','age']

        for field in required:
            if field not in data:
                return jsonify({
                    'status':  'error',
                    'message': f'Missing field: {field}'
                }), 400

        # ── VALIDATE RANGES ─────────────────────────────────
        try:
            pregnancies    = float(data['pregnancies'])
            glucose        = float(data['glucose'])
            blood_pressure = float(data['blood_pressure'])
            skin_thickness = float(data['skin_thickness'])
            insulin        = float(data['insulin'])
            bmi            = float(data['bmi'])
            dpf            = float(data['dpf'])
            age            = float(data['age'])
        except (ValueError, TypeError):
            return jsonify({
                'status':  'error',
                'message': 'All fields must be valid numbers'
            }), 400

        # ── RANGE CHECKS ────────────────────────────────────
        if not (0  <= pregnancies <= 20):
            return jsonify({'status':'error','message':'Pregnancies must be 0-20'}), 400
        if not (50 <= glucose     <= 300):
            return jsonify({'status':'error','message':'Glucose must be 50-300 mg/dL'}), 400
        if not (40 <= blood_pressure <= 180):
            return jsonify({'status':'error','message':'Blood pressure must be 40-180 mmHg'}), 400
        if not (0  <= skin_thickness <= 100):
            return jsonify({'status':'error','message':'Skin thickness must be 0-100 mm'}), 400
        if not (0  <= insulin     <= 900):
            return jsonify({'status':'error','message':'Insulin must be 0-900'}), 400
        if not (10 <= bmi         <= 70):
            return jsonify({'status':'error','message':'BMI must be 10-70'}), 400
        if not (0.05 <= dpf      <= 3.0):
            return jsonify({'status':'error','message':'DPF must be 0.05-3.0'}), 400
        if not (1  <= age        <= 120):
            return jsonify({'status':'error','message':'Age must be 1-120 years'}), 400

        # ── RUN AI PREDICTION ────────────────────────────────
        result = predict_diabetes(data)

        if result['status'] == 'error':
            return jsonify(result), 500

        # ── SAVE TO DATABASE ─────────────────────────────────
        prediction = Prediction(
            pregnancies    = pregnancies,
            glucose        = glucose,
            blood_pressure = blood_pressure,
            skin_thickness = skin_thickness,
            insulin        = insulin,
            bmi            = bmi,
            dpf            = dpf,
            age            = age,
            result         = result['result'],
            risk_percent   = result['risk_percent'],
            risk_category  = result['risk_category'],
            hba1c_estimate = result['hba1c_estimate'],
        )
        db.session.add(prediction)
        db.session.commit()

        # ── RETURN RESULT ────────────────────────────────────
        return jsonify({
            'status':         'success',
            'prediction_id':  prediction.id,
            'result':         result['result'],
            'risk_percent':   result['risk_percent'],
            'risk_level':     result['risk_level'],
            'risk_category':  result['risk_category'],
            'hba1c_estimate': result['hba1c_estimate'],
            'tips':           result['tips'],
            'input_summary':  result['input_summary'],
            'saved':          True
        }), 200

    except Exception as e:
        return jsonify({
            'status':  'error',
            'message': f'Prediction failed: {str(e)}'
        }), 500


# ══════════════════════════════════════════════════════════════
# GET /api/predictions
# Returns last 10 predictions from database
# ══════════════════════════════════════════════════════════════
@predict_bp.route('/api/predictions', methods=['GET'])
def get_predictions():
    try:
        predictions = Prediction.query\
            .order_by(Prediction.created_at.desc())\
            .limit(10).all()

        return jsonify({
            'status':      'success',
            'count':        len(predictions),
            'predictions': [p.to_dict() for p in predictions]
        }), 200

    except Exception as e:
        return jsonify({
            'status':  'error',
            'message': str(e)
        }), 500


# ══════════════════════════════════════════════════════════════
# GET /api/dashboard/stats
# Returns stats for dashboard charts
# ══════════════════════════════════════════════════════════════
@predict_bp.route('/api/dashboard/stats', methods=['GET'])
def dashboard_stats():
    try:
        predictions = Prediction.query.all()
        total       = len(predictions)

        if total == 0:
            return jsonify({
                'status': 'success',
                'total':   0,
                'message': 'No predictions yet'
            }), 200

        diabetic     = sum(1 for p in predictions if p.result == 'Diabetic')
        not_diabetic = total - diabetic

        # Risk level counts
        high_risk = sum(1 for p in predictions if p.risk_percent >= 70)
        mod_risk  = sum(1 for p in predictions if 40 <= p.risk_percent < 70)
        low_risk  = sum(1 for p in predictions if p.risk_percent < 40)

        # Average values
        avg_glucose = round(sum(p.glucose for p in predictions) / total, 1)
        avg_bmi     = round(sum(p.bmi     for p in predictions) / total, 1)
        avg_age     = round(sum(p.age     for p in predictions) / total, 1)
        avg_risk    = round(sum(p.risk_percent for p in predictions) / total, 1)

        # BMI categories
        underweight = sum(1 for p in predictions if p.bmi < 18.5)
        normal      = sum(1 for p in predictions if 18.5 <= p.bmi < 25)
        overweight  = sum(1 for p in predictions if 25   <= p.bmi < 30)
        obese       = sum(1 for p in predictions if p.bmi >= 30)

        # Age groups
        young  = sum(1 for p in predictions if p.age < 30)
        middle = sum(1 for p in predictions if 30 <= p.age < 45)
        senior = sum(1 for p in predictions if p.age >= 45)

        # Last 7 predictions for timeline
        recent = Prediction.query\
            .order_by(Prediction.created_at.desc())\
            .limit(7).all()
        timeline = [{
            'date':    p.created_at.strftime('%d %b'),
            'risk':    p.risk_percent,
            'result':  p.result
        } for p in reversed(recent)]

        return jsonify({
            'status':         'success',
            'total':           total,
            'diabetic':        diabetic,
            'not_diabetic':    not_diabetic,
            'high_risk':       high_risk,
            'moderate_risk':   mod_risk,
            'low_risk':        low_risk,
            'avg_glucose':     avg_glucose,
            'avg_bmi':         avg_bmi,
            'avg_age':         avg_age,
            'avg_risk':        avg_risk,
            'bmi_categories': {
                'underweight': underweight,
                'normal':      normal,
                'overweight':  overweight,
                'obese':       obese
            },
            'age_groups': {
                'young':  young,
                'middle': middle,
                'senior': senior
            },
            'timeline': timeline
        }), 200

    except Exception as e:
        return jsonify({
            'status':  'error',
            'message': str(e)
        }), 500