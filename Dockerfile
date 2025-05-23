# Użycie lekkiego obrazu z Pythonem
FROM python:3.10-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Skopiowanie plików
COPY . .

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Uruchomienie FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
