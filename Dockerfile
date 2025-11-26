FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required by PTB 13.x
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    firefox-esr \
    wget \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    xvfb \
    libxt6 \
    libx11-xcb1 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/app/main.py"]
