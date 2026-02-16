import random
import pandas as pd

def get_ai_response(message: str, df: pd.DataFrame):
    """
    دالة بتاخد رسالة المستخدم والداتا، وترجع رد ذكي بناءً على القواعد.
    """
    msg = message.lower()
    
    # 1. الترحيب
    if "hello" in msg or "hi" in msg or "hey" in msg:
        return "FlowHub AI Online. Ready to assist with manufacturing queries."
    
    # 2. أفضل مصنع (Data Driven)
    elif "best factory" in msg or "top rated" in msg:
        best = df.sort_values('brand_rating', ascending=False).iloc[0]
        return f"Based on current metrics, '{best['factory_id']}' is the top-rated facility with a {best['brand_rating']} rating."
    
    # 3. معلومات الخامات (Data Driven)
    elif "cotton" in msg or "fabric" in msg:
        try:
            avg_gsm = int(df[df['fabric_type']=='Cotton']['gsm'].mean())
            return f"Analyzing Fabric Data... Cotton currently averages {avg_gsm} GSM across our active grid."
        except:
            return "Fabric data is currently being synchronized. Please ask specifically about Cotton."
    
    # 4. حالة الاوردر (Simulated)
    elif "status" in msg or "order" in msg:
        statuses = ["In Production (Cutting)", "Quality Control", "Packaging", "Shipped"]
        return f"Tracking Order #ORD-{random.randint(1000,9999)}... Status: {random.choice(statuses)}. EST Delivery: {random.randint(2,7)} Days."
    
    # 5. ضغط المصانع
    elif "load" in msg or "capacity" in msg:
        return "Global Grid Load is at 67%. High capacity available in Factory F2 and F5."
    
    # 6. المساعدة
    elif "help" in msg:
        return "I can help with: 'Best Factory', 'Fabric Specs', 'Order Status', or 'Grid Load'."
        
    # 7. غير مفهوم
    else:
        return "Command not recognized. Try asking about 'Best Factory', 'Order Status', or 'Fabric Specs'."