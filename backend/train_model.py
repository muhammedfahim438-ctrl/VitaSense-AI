import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score
from imblearn.over_sampling import SMOTE
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs('models', exist_ok=True)

print("=" * 60)
print("  VitaSense AI - Diabetes Prediction Model Trainer")
print("  Catalyst Crew | Nehru Arts and Science College")
print("=" * 60)

# ══════════════════════════════════════════════════════════════
# STEP 1 - LOAD OR GENERATE DATASET
# ══════════════════════════════════════════════════════════════
print("\n Step 1: Loading diabetes dataset...")

PIMA_PATH = 'models/diabetes.csv'

if os.path.exists(PIMA_PATH):
    print("   Real PIMA dataset found!")
    df_real = pd.read_csv(PIMA_PATH)
    df_real.columns = [
        'pregnancies','glucose','blood_pressure',
        'skin_thickness','insulin','bmi','dpf','age','outcome'
    ]
    cols_with_zeros = ['glucose','blood_pressure','skin_thickness','insulin','bmi']
    for col in cols_with_zeros:
        df_real[col] = df_real[col].replace(0, df_real[col].median())
    print(f"   Real PIMA records : {len(df_real)}")
    use_real = True
else:
    print("   Generating realistic dataset based on PIMA statistics...")
    use_real = False

np.random.seed(42)
n_extra = 4232 if use_real else 5000
n_neg   = int(n_extra * 0.60)
n_pos   = n_extra - n_neg

neg = {
    'pregnancies':    np.random.choice([0,1,2,3,4], n_neg, p=[0.35,0.25,0.20,0.12,0.08]),
    'glucose':        np.clip(np.random.normal(109,18,n_neg), 70,140).astype(int),
    'blood_pressure': np.clip(np.random.normal(68,10,n_neg),  50, 90).astype(int),
    'skin_thickness': np.clip(np.random.normal(20, 8,n_neg),  10, 40).astype(int),
    'insulin':        np.clip(np.random.normal(68,50,n_neg),  10,200).astype(int),
    'bmi':            np.round(np.clip(np.random.normal(27,5,n_neg), 18,38),1),
    'dpf':            np.round(np.clip(np.random.normal(0.30,0.15,n_neg),0.08,0.80),3),
    'age':            np.clip(np.random.normal(31,9,n_neg), 18,55).astype(int),
    'outcome':        np.zeros(n_neg, dtype=int)
}
pos = {
    'pregnancies':    np.random.choice([0,1,2,3,4,5,6,7,8], n_pos,
                      p=[0.10,0.12,0.13,0.13,0.12,0.12,0.10,0.09,0.09]),
    'glucose':        np.clip(np.random.normal(141,28,n_pos),100,250).astype(int),
    'blood_pressure': np.clip(np.random.normal(75,12,n_pos),  55,110).astype(int),
    'skin_thickness': np.clip(np.random.normal(33,10,n_pos),  15, 60).astype(int),
    'insulin':        np.clip(np.random.normal(180,90,n_pos), 50,400).astype(int),
    'bmi':            np.round(np.clip(np.random.normal(35,6,n_pos), 24,50),1),
    'dpf':            np.round(np.clip(np.random.normal(0.55,0.25,n_pos),0.10,2.40),3),
    'age':            np.clip(np.random.normal(37,10,n_pos), 21,70).astype(int),
    'outcome':        np.ones(n_pos, dtype=int)
}

df_gen = pd.concat([pd.DataFrame(neg), pd.DataFrame(pos)], ignore_index=True)
df     = pd.concat([df_real, df_gen], ignore_index=True) if use_real else df_gen
df     = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv('models/diabetes_dataset.csv', index=False)

print(f"   Total records  : {len(df)}")
print(f"   Non-Diabetic   : {(df['outcome']==0).sum()}")
print(f"   Diabetic       : {(df['outcome']==1).sum()}")
print(f"   Saved          : models/diabetes_dataset.csv")

# ══════════════════════════════════════════════════════════════
# STEP 2 - FEATURE ENGINEERING
# ══════════════════════════════════════════════════════════════
print("\n Step 2: Engineering smart features...")

df['glucose_bmi']      = df['glucose'] * df['bmi']
df['age_glucose']      = df['age']     * df['glucose']
df['insulin_glucose']  = df['insulin'] / (df['glucose'] + 1)
df['bmi_age']          = df['bmi']     * df['age']
df['glucose_category'] = pd.cut(df['glucose'],
                           bins=[0,99,125,300], labels=[0,1,2]).astype(int)
df['bmi_category']     = pd.cut(df['bmi'],
                           bins=[0,18.5,24.9,29.9,100], labels=[0,1,2,3]).astype(int)
df['age_group']        = pd.cut(df['age'],
                           bins=[0,30,45,60,100], labels=[0,1,2,3]).astype(int)
df['high_risk_combo']  = (
    (df['glucose'] > 140).astype(int) +
    (df['bmi']     >  30).astype(int) +
    (df['age']     >  45).astype(int) +
    (df['dpf']     > 0.5).astype(int)
)

feature_cols = [
    'pregnancies','glucose','blood_pressure','skin_thickness',
    'insulin','bmi','dpf','age',
    'glucose_bmi','age_glucose','insulin_glucose','bmi_age',
    'glucose_category','bmi_category','age_group','high_risk_combo'
]
X = df[feature_cols]
y = df['outcome']
print(f"   Features : {len(feature_cols)} (8 original + 8 engineered)")

# ══════════════════════════════════════════════════════════════
# STEP 3 - SPLIT + BALANCE + SCALE
# ══════════════════════════════════════════════════════════════
print("\n Step 3: Splitting and balancing data...")

X_tr_raw, X_te, y_tr_raw, y_te = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y)
X_tr, y_tr = SMOTE(random_state=42).fit_resample(X_tr_raw, y_tr_raw)
scaler      = StandardScaler()
scaler.fit(X_tr)

print(f"   Training : {len(X_tr)} samples")
print(f"   Testing  : {len(X_te)} samples")

# ══════════════════════════════════════════════════════════════
# STEP 4 - TRAIN MODELS
# ══════════════════════════════════════════════════════════════
print("\n Step 4: Training models...")

rf = RandomForestClassifier(
    n_estimators=300, max_depth=14,
    min_samples_split=3, min_samples_leaf=1,
    max_features='sqrt', class_weight='balanced',
    random_state=42, n_jobs=-1)
rf.fit(X_tr, y_tr)
print(f"   Random Forest     : {accuracy_score(y_te, rf.predict(X_te))*100:.2f}%")

gb = GradientBoostingClassifier(
    n_estimators=300, max_depth=6,
    learning_rate=0.08, subsample=0.85, random_state=42)
gb.fit(X_tr, y_tr)
print(f"   Gradient Boosting : {accuracy_score(y_te, gb.predict(X_te))*100:.2f}%")

# ══════════════════════════════════════════════════════════════
# STEP 5 - VOTING ENSEMBLE
# ══════════════════════════════════════════════════════════════
print("\n Step 5: Building Voting Ensemble...")

ensemble = VotingClassifier(
    estimators=[('rf',rf),('gb',gb)], voting='soft', weights=[1,1])
ensemble.fit(X_tr, y_tr)

acc = accuracy_score(y_te, ensemble.predict(X_te))
cv  = cross_val_score(ensemble, X, y,
      cv=StratifiedKFold(n_splits=5,shuffle=True,random_state=42),
      scoring='accuracy')
roc = roc_auc_score(y_te, ensemble.predict_proba(X_te)[:,1])

print(f"   Voting Ensemble   : {acc*100:.2f}%")
print(f"   Cross Val Mean    : {cv.mean()*100:.2f}%")
print(f"   ROC-AUC Score     : {roc:.4f}")

# ══════════════════════════════════════════════════════════════
# STEP 6 - SAVE
# ══════════════════════════════════════════════════════════════
print("\n Step 6: Saving models...")

joblib.dump(ensemble,     'models/diabetes_model.pkl')
joblib.dump(scaler,       'models/diabetes_scaler.pkl')
joblib.dump(feature_cols, 'models/diabetes_features.pkl')

print("   diabetes_model.pkl    saved")
print("   diabetes_scaler.pkl   saved")
print("   diabetes_features.pkl saved")

# ══════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("  VitaSense AI - TRAINING COMPLETE!")
print("=" * 60)
print(f"  Voting Ensemble   : {acc*100:.2f}%  SAVED")
print(f"  Cross Val Mean    : {cv.mean()*100:.2f}%")
print(f"  ROC-AUC Score     : {roc:.4f}")
print(f"  Total Records     : {len(df)}")
print(f"  Features          : {len(feature_cols)}")
print(f"\n  Final Accuracy    : {acc*100:.2f}%")
print("=" * 60)
print("  VitaSense AI Diabetes model is READY!")
print("=" * 60)

# ══════════════════════════════════════════════════════════════
# QUICK TEST
# ══════════════════════════════════════════════════════════════
print("\n Quick Test - Sample Predictions:")

def prepare(row):
    d = pd.DataFrame([row], columns=[
        'pregnancies','glucose','blood_pressure','skin_thickness',
        'insulin','bmi','dpf','age'])
    d['glucose_bmi']      = d['glucose'] * d['bmi']
    d['age_glucose']      = d['age']     * d['glucose']
    d['insulin_glucose']  = d['insulin'] / (d['glucose'] + 1)
    d['bmi_age']          = d['bmi']     * d['age']
    d['glucose_category'] = pd.cut(d['glucose'],bins=[0,99,125,300],labels=[0,1,2]).astype(int)
    d['bmi_category']     = pd.cut(d['bmi'],bins=[0,18.5,24.9,29.9,100],labels=[0,1,2,3]).astype(int)
    d['age_group']        = pd.cut(d['age'],bins=[0,30,45,60,100],labels=[0,1,2,3]).astype(int)
    d['high_risk_combo']  = (
        (d['glucose']>140).astype(int) + (d['bmi']>30).astype(int) +
        (d['age']>45).astype(int)      + (d['dpf']>0.5).astype(int))
    return d[feature_cols]

tests = [
    ([6,148,72,35,200,33.6,0.627,50], 'Diabetic'),
    ([1, 85,66,29,  0,26.6,0.351,31], 'Not Diabetic'),
    ([8,183,64, 0,  0,23.3,0.672,32], 'Diabetic'),
    ([0,137,40,35,168,43.1,2.288,33], 'Diabetic'),
]

print(f"\n  Case  Expected        Predicted       Risk%   Result")
print(f"  {'-'*55}")
for i,(row,expected) in enumerate(tests):
    data   = prepare(row)
    pred   = ensemble.predict(data)[0]
    prob   = ensemble.predict_proba(data)[0][1]
    result = 'Diabetic' if pred==1 else 'Not Diabetic'
    status = 'CORRECT' if result==expected else 'WRONG'
    print(f"  {i+1}     {expected:<15} {result:<15} {prob*100:.1f}%  {status}")

print("\n  Model ready for VitaSense AI website!")