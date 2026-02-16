# استخدام نسخة بايثون خفيفة
FROM python:3.9-slim

# تحديد مكان الكود جوه الحاوية
WORKDIR /app

# نسخ ملف المكتبات وتسطيبها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كل ملفات المشروع (بما فيها الموديلات والداتا)
COPY . .

# تشغيل السيرفر على بورت 8080 (البورت اللي بيستخدمه جوجل كلاود)
CMD ["uvicorn", "task:app", "--host", "0.0.0.0", "--port", "8080"]