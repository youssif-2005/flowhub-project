import pandas as pd
import joblib
import numpy as np
import random
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# تأكد أن مجلد templates موجود في نفس المسار
templates = Jinja2Templates(directory="templates")

# تحميل الداتا والموديلات
try:
    df = pd.read_csv("production_data_no_cotton_44.csv")
    model_days = joblib.load("model_days.pkl")
    model_quality = joblib.load("model_quality.pkl")
except Exception as e:
    print(f"⚠️ Warning: Check files! Error: {e}")

# قوائم الاختيار
PRODUCT_OPTIONS = list(df['product_type'].unique()) if 'df' in locals() else []
FABRIC_OPTIONS = list(df['fabric_type'].unique()) if 'df' in locals() else []
FACTORY_OPTIONS = list(df['factory_id'].unique()) if 'df' in locals() else []

USER_ORDERS = []

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "mode": "home"})

@app.get("/recommendations_menu", response_class=HTMLResponse)
async def recommendations_menu(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "mode": "reco_menu"})

@app.get("/orders", response_class=HTMLResponse)
async def manage_orders(request: Request):
    simulated_orders = []
    if not USER_ORDERS: 
        sample_df = df.sample(3)
        for _, row in sample_df.iterrows():
            simulated_orders.append({
                "id": f"#SYS-{random.randint(100,999)}",
                "product": row['product_type'],
                "fabric": row['fabric_type'],
                "quantity": row['quantity'],
                "factory": row['factory_id'],
                "status": "In Production",
                "color": "text-yellow-400",
                "progress": random.randint(40, 80),
                "is_new": False
            })
    all_orders = USER_ORDERS + simulated_orders
    return templates.TemplateResponse("index.html", {"request": request, "mode": "orders_dashboard", "orders": all_orders})

@app.get("/create_order", response_class=HTMLResponse)
async def create_order_form(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "mode": "create_order",
        "products": PRODUCT_OPTIONS,
        "fabrics": FABRIC_OPTIONS,
        "factories": FACTORY_OPTIONS
    })

@app.post("/submit_order", response_class=HTMLResponse)
async def submit_order(request: Request, product_type: str = Form(...), fabric_type: str = Form(...), factory_id: str = Form(...), quantity: int = Form(...)):
    new_order = {
        "id": f"#NEW-{random.randint(1000,9999)}",
        "product": product_type,
        "fabric": fabric_type,
        "quantity": quantity,
        "factory": factory_id,
        "status": "Initiated",
        "color": "text-neon",
        "progress": 5,
        "is_new": True
    }
    USER_ORDERS.insert(0, new_order)
    return await manage_orders(request)

@app.get("/form/materials", response_class=HTMLResponse)
async def material_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "mode": "mat_form", "products": PRODUCT_OPTIONS})

@app.post("/process_materials", response_class=HTMLResponse)
async def process_materials(request: Request, product_type: str = Form(...)):
    relevant_df = df[df['product_type'] == product_type]
    stats = relevant_df.groupby('fabric_type').agg({'defect_rate': 'mean', 'gsm': 'mean'}).reset_index()
    materials = []
    for _, row in stats.iterrows():
        score = int((1 - row['defect_rate']) * 100)
        materials.append({"name": row['fabric_type'], "price": f"${int(row['gsm'] * 0.05)}-${int(row['gsm'] * 0.08)}", "durability": f"{score}/100", "why": f"Top match", "glow": score > 95})
    return templates.TemplateResponse("index.html", {"request": request, "mode": "mat_result", "materials": materials})

@app.get("/form/factories", response_class=HTMLResponse)
async def factory_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "mode": "fac_form", "products": PRODUCT_OPTIONS, "fabrics": FABRIC_OPTIONS})

@app.post("/process_factories", response_class=HTMLResponse)
async def process_factories(request: Request, product_type: str = Form(...), fabric_type: str = Form(...), quantity: int = Form(...)):
    prod_list = PRODUCT_OPTIONS
    fab_list = FABRIC_OPTIONS
    p_code = prod_list.index(product_type) if product_type in prod_list else 0
    f_code = fab_list.index(fabric_type) if fabric_type in fab_list else 0
    factory_results = []
    for f_id in df['factory_id'].unique():
        f_info = df[df['factory_id'] == f_id].iloc[0]
        feat = np.array([[p_code, f_code, quantity, 1, f_info['current_load']]])
        days = model_days.predict(feat)[0]
        qual = model_quality.predict(feat)[0]
        speed_score = max(0, 10 - days/3)
        quality_score = (1 - qual) * 10
        final_score = (f_info['brand_rating'] * 0.5) + (speed_score * 0.3) + (quality_score * 0.2)
        factory_results.append({"name": f_id, "rating": round(f_info['brand_rating'], 1), "cap": f"{int(f_info['current_load'] * 100)}%", "time": f"{int(days)} Days", "price": "$$", "score": round(final_score, 1)})
    top_factories = sorted(factory_results, key=lambda x: x['score'], reverse=True)
    return templates.TemplateResponse("index.html", {"request": request, "mode": "fac_result", "factories": top_factories, "best_match": top_factories[0]})

if __name__ == "__main__":
    import uvicorn
    # سطر مهم جداً للـ Deployment
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)