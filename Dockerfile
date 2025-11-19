# Verwende Python 3.11 slim als Basis-Image
FROM python:3.11-slim

# Setze Arbeitsverzeichnis
WORKDIR /app

# Installiere System-Dependencies für PostgreSQL und andere Packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Kopiere requirements.txt zuerst für besseres Caching
COPY requirements.txt .

# Installiere Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Anwendungscode
COPY . .

# Erstelle einen non-root User für Sicherheit
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Setze Umgebungsvariablen
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Exponiere Port (Standard ist 10000 basierend auf der App)
EXPOSE 10000

# Gesundheitscheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:10000/ || exit 1

# Starte die Anwendung
CMD ["python", "app.py"]