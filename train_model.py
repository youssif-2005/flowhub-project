import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

# 1. تحميل الداتا الجديدة اللي لسه عاملين لها Generate
df = pd.read_csv("production_data_no_cotton_44.csv")

# 2. تحويل النصوص لأرقام عشان الموديل يفهمها (Label Encoding)
# لازم نثبت الترتيب ده عشان task.py يقرأ صح
df['product_code'] = df['product_type'].astype('category').cat.codes
df['fabric_code'] = df['fabric_type'].astype('category').cat.codes

# 3. تحديد المدخلات (Features) والمخرجات (Targets)
# المخرجات اللي بنوقعها هي الأيام والجودة
X = df[['product_code', 'fabric_code', 'quantity', 'gsm', 'current_load']]
y_days = df['actual_days']
y_quality = df['fabric_quality_score']

print("🔄 Training Models... Please wait.")

# 4. تدريب موديل الأيام
model_days = RandomForestRegressor(n_estimators=100, random_state=42)
model_days.fit(X, y_days)

# 5. تدريب موديل الجودة
model_quality = RandomForestRegressor(n_estimators=100, random_state=42)
model_quality.fit(X, y_quality)

# 6. حفظ الموديلات الجديدة (هتمسح القديمة تلقائياً)
joblib.dump(model_days, "model_days.pkl")
joblib.dump(model_quality, "model_quality.pkl")

print("✅ Success! model_days.pkl and model_quality.pkl are updated.")
print("🚀 Now you are ready to Deploy!")