# Python 3.11 bazlı bir resmi kullanıyoruz
FROM python:3.11-slim

# Çalışma dizinini oluşturuyoruz
WORKDIR /app

# Gereksinim dosyasını kopyalayıp kurulum yapıyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyalıyoruz
COPY . .

# FastAPI için uvicorn çalıştırma komutu
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

RUN pip install google-generativeai
