import pandas as pd
import numpy as np
import random

n_rows = 1000
factories = ['F1', 'F2', 'F3']
products = ['T-shirt', 'Pants', 'Jacket', 'Hoodie', 'Sweater', 'Dress', 'Skirt', 'Shorts']
fabrics = ['Cotton', 'Polyester', 'Wool', 'Silk', 'Blend', 'Leather']

data = []
for i in range(n_rows):
    f_id = random.choice(factories)
    product = random.choice(products)
    fabric = random.choice(fabrics)
    qty = np.random.randint(100, 5000)
    load = np.round(np.random.uniform(0.1, 0.9), 2)
    
    # 1. منطق الأيام (الإنتاجية): الجاكيت بياخد وقت أكتر من التيشرت
    base_days_per_unit = 0.002 # التيشرت كبداية
    if product in ['Jacket', 'Sweater']: base_days_per_unit = 0.005
    if fabric == 'Leather': base_days_per_unit *= 1.5
    
    # الأيام = (الكمية * الوقت) + وقت ثابت للتجهيز + تأخير بسبب الزحمة (Load)
    actual_days = (qty * base_days_per_unit) + 2 + (load * 5)
    actual_days += np.random.normal(0, 0.5) # شوية عشوائية واقعية
    
    # 2. منطق الجودة: كل ما المصنع كان مضغوط (Load عالي) العيوب بتزيد
    # العيوب (Defect Rate) بتزيد مع الزحمة وصعوبة الخامة
    base_defect = 0.02
    if load > 0.7: base_defect += 0.03
    if fabric == 'Silk' or fabric == 'Leather': base_defect += 0.02
    defect_rate = base_defect + np.random.uniform(0, 0.01)
    
    # الجودة (Score من 10) = عكس العيوب
    quality_score = 10 - (defect_rate * 50) 

    data.append({
        'order_id': i + 1,
        'product_type': product,
        'fabric_type': fabric,
        'quantity': qty,
        'gsm': np.random.randint(150, 400),
        'factory_id': f_id,
        'current_load': load,
        'brand_rating': np.random.uniform(3.5, 5.0),
        'defect_rate': np.round(defect_rate, 4),
        'actual_days': np.round(actual_days, 1),
        'fabric_quality_score': np.round(max(1, quality_score), 1)
    })

df = pd.DataFrame(data)
df.to_csv("production_data_no_cotton_44.csv", index=False)
print("✅ Logic Implemented! Data is now realistic and AI-ready.")