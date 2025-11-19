# Verwende Python 3.11 slim als Basis-Image
FROM python:3.11-slim

# Setze Arbeitsverzeichnis
WORKDIR /app

# Installiere System-Dependencies für PostgreSQL, Git und curl
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Klone das Repository direkt in den Container
RUN git clone https://github.com/JayJay889/CODE-Network.git . && \
    git checkout main

# Installiere Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Erstelle einen non-root User für Sicherheit
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Setze Umgebungsvariablen
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Exponiere Port 7860 für Hugging Face Spaces
EXPOSE 7860

# Gesundheitscheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Starte die Anwendung
CMD ["python", "app.py"]