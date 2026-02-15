import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# 1. تحميل الداتا
try:
    df = pd.read_csv("production_data_no_cotton_44.csv")
    print("✅ CSV loaded successfully!")
except:
    print("❌ Error: production_data_no_cotton_44.csv not found!")
    exit()

# 2. تجهيز البيانات
df['product_n'] = df['product_type'].astype('category').cat.codes
df['fabric_n'] = df['fabric_type'].astype('category').cat.codes
gsm_map = {'Low': 0, 'Medium': 1, 'High': 2}
df['gsm_n'] = df['fabric_category'].map(gsm_map)

# 3. تدريب الموديلات
features = ['product_n', 'fabric_n', 'quantity', 'gsm_n', 'current_load']
X = df[features]

model_days = RandomForestRegressor(n_estimators=100, random_state=42)
model_days.fit(X, df['actual_days'])

model_quality = RandomForestRegressor(n_estimators=100, random_state=42)
model_quality.fit(X, df['defect_rate'])

# 4. حفظ
joblib.dump(model_days, "model_days.pkl")
joblib.dump(model_quality, "model_quality.pkl")
print("✅ AI Brains Ready!")