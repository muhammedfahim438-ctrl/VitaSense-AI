import joblib
import pandas as pd
import numpy as np
import os

# ══════════════════════════════════════════════════════════════
# LOAD MODEL
# ══════════════════════════════════════════════════════════════
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'diabetes_model.pkl')
FEAT_PATH  = os.path.join(BASE_DIR, 'models', 'diabetes_features.pkl')

model        = joblib.load(MODEL_PATH)
feature_cols = joblib.load(FEAT_PATH)

print("✅ Diabetes AI model loaded successfully!")

# ══════════════════════════════════════════════════════════════
# HELPER — ADD ENGINEERED FEATURES
# ══════════════════════════════════════════════════════════════
def add_features(d):
    d['glucose_bmi']      = d['glucose'] * d['bmi']
    d['age_glucose']      = d['age']     * d['glucose']
    d['insulin_glucose']  = d['insulin'] / (d['glucose'] + 1)
    d['bmi_age']          = d['bmi']     * d['age']
    d['glucose_category'] = pd.cut(
        d['glucose'], bins=[0,99,125,300],
        labels=[0,1,2]).astype(int)
    d['bmi_category']     = pd.cut(
        d['bmi'], bins=[0,18.5,24.9,29.9,100],
        labels=[0,1,2,3]).astype(int)
    d['age_group']        = pd.cut(
        d['age'], bins=[0,30,45,60,100],
        labels=[0,1,2,3]).astype(int)
    d['high_risk_combo']  = (
        (d['glucose'] > 140).astype(int) +
        (d['bmi']     >  30).astype(int) +
        (d['age']     >  45).astype(int) +
        (d['dpf']     > 0.5).astype(int)
    )
    return d

# ══════════════════════════════════════════════════════════════
# HELPER — ESTIMATE HbA1c FROM GLUCOSE
# ══════════════════════════════════════════════════════════════
def estimate_hba1c(glucose):
    # Formula: HbA1c = (glucose + 46.7) / 28.7
    return round((glucose + 46.7) / 28.7, 1)

# ══════════════════════════════════════════════════════════════
# HELPER — GET RISK CATEGORY
# ══════════════════════════════════════════════════════════════
def get_risk_category(glucose, risk_percent):
    if glucose < 100 and risk_percent < 30:
        return 'Normal'
    elif glucose < 126 or risk_percent < 50:
        return 'Prediabetes'
    else:
        return 'Diabetes'

# ══════════════════════════════════════════════════════════════
# HELPER — GET HEALTH TIPS
# ══════════════════════════════════════════════════════════════
def get_health_tips(result, risk_percent, bmi, glucose, age):
    tips = []

    if result == 'Diabetic':
        tips.append("Consult a doctor immediately for proper medical evaluation and guidance.")
        tips.append("Monitor your blood sugar levels daily and keep a log.")
        tips.append("Follow a low glycemic index diet — avoid white rice, sugar and refined carbs.")
        tips.append("Exercise at least 30 minutes daily — walking, cycling or swimming.")
        tips.append("Stay hydrated — drink at least 8 glasses of water daily.")

    else:
        if risk_percent >= 30:
            tips.append("You are at moderate risk. Regular checkups every 6 months are recommended.")
            tips.append("Reduce sugar and processed food intake to lower your risk.")
            tips.append("Exercise at least 30 minutes daily to maintain healthy blood sugar.")
        else:
            tips.append("Great! Your diabetes risk is low. Keep maintaining a healthy lifestyle.")
            tips.append("Continue with regular physical activity and balanced diet.")
            tips.append("Get a diabetes screening test once a year as a precaution.")

        if bmi > 25:
            tips.append("Your BMI is above normal. Losing 5-10% body weight can significantly reduce diabetes risk.")

        if glucose > 100:
            tips.append("Your glucose is slightly elevated. Reduce sugar intake and exercise regularly.")

        if age > 45:
            tips.append("Age is a risk factor. Regular blood sugar monitoring is advised after 45.")

    tips.append("⚠️ This is an AI prediction only. Always consult a qualified doctor for medical advice.")

    return tips

# ══════════════════════════════════════════════════════════════
# MAIN PREDICTION FUNCTION
# ══════════════════════════════════════════════════════════════
def predict_diabetes(data):
    """
    Takes a dictionary of health inputs and returns prediction.

    Input:
        data = {
            'pregnancies': float,
            'glucose': float,
            'blood_pressure': float,
            'skin_thickness': float,
            'insulin': float,
            'bmi': float,
            'dpf': float,
            'age': float
        }

    Returns:
        dict with result, risk_percent, category, hba1c, tips
    """
    try:
        # ── BUILD DATAFRAME ─────────────────────────────────
        df = pd.DataFrame([{
            'pregnancies':    float(data.get('pregnancies',    0)),
            'glucose':        float(data.get('glucose',       120)),
            'blood_pressure': float(data.get('blood_pressure', 70)),
            'skin_thickness': float(data.get('skin_thickness', 20)),
            'insulin':        float(data.get('insulin',        80)),
            'bmi':            float(data.get('bmi',           25.0)),
            'dpf':            float(data.get('dpf',          0.350)),
            'age':            float(data.get('age',            30)),
        }])

        # ── ADD ENGINEERED FEATURES ─────────────────────────
        df = add_features(df)

        # ── PREDICT ─────────────────────────────────────────
        prediction   = model.predict(df[feature_cols])[0]
        probability  = model.predict_proba(df[feature_cols])[0][1]
        risk_percent = round(probability * 100, 1)

        # ── BUILD RESULT ────────────────────────────────────
        result       = 'Diabetic' if prediction == 1 else 'Not Diabetic'
        glucose      = float(data.get('glucose', 120))
        bmi          = float(data.get('bmi', 25.0))
        age          = float(data.get('age', 30))
        hba1c        = estimate_hba1c(glucose)
        category     = get_risk_category(glucose, risk_percent)
        tips         = get_health_tips(result, risk_percent, bmi, glucose, age)

        # ── RISK LEVEL LABEL ────────────────────────────────
        if risk_percent >= 70:
            risk_level = 'High'
        elif risk_percent >= 40:
            risk_level = 'Moderate'
        else:
            risk_level = 'Low'

        return {
            'status':        'success',
            'result':         result,
            'risk_percent':   risk_percent,
            'risk_level':     risk_level,
            'risk_category':  category,
            'hba1c_estimate': hba1c,
            'tips':           tips,
            'input_summary': {
                'glucose':        glucose,
                'bmi':            bmi,
                'age':            age,
                'blood_pressure': float(data.get('blood_pressure', 70)),
            }
        }

    except Exception as e:
        return {
            'status':  'error',
            'message': str(e)
        }


# ══════════════════════════════════════════════════════════════
# TEST (run this file directly to test)
# ══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("\n Testing ai_model.py...\n")

    test_cases = [
        {
            'name': 'High Risk Patient',
            'data': {'pregnancies':6,'glucose':148,'blood_pressure':72,
                     'skin_thickness':35,'insulin':200,'bmi':33.6,'dpf':0.627,'age':50}
        },
        {
            'name': 'Low Risk Patient',
            'data': {'pregnancies':1,'glucose':85,'blood_pressure':66,
                     'skin_thickness':29,'insulin':0,'bmi':26.6,'dpf':0.351,'age':31}
        },
        {
            'name': 'Moderate Risk Patient',
            'data': {'pregnancies':3,'glucose':120,'blood_pressure':70,
                     'skin_thickness':25,'insulin':100,'bmi':29.0,'dpf':0.400,'age':40}
        },
    ]

    for tc in test_cases:
        result = predict_diabetes(tc['data'])
        print(f"  Patient  : {tc['name']}")
        print(f"  Result   : {result['result']}")
        print(f"  Risk     : {result['risk_percent']}% ({result['risk_level']})")
        print(f"  Category : {result['risk_category']}")
        print(f"  HbA1c    : {result['hba1c_estimate']}%")
        print(f"  Tips     : {len(result['tips'])} tips generated")
        print()