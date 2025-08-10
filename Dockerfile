FROM python:3.11-slim

# Ubah mirror Debian ke Indonesia untuk download lebih cepat
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Buat folder kerja
WORKDIR /app

# Copy file requirements lebih dulu untuk memanfaatkan cache
COPY requirements.txt .

# Install dependency Python pakai wheel kalau tersedia
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --only-binary=:all: -r requirements.txt || pip install --no-cache-dir -r requirements.txt

# Copy semua file project
COPY . .

# Jalankan app
CMD ["python", "charts_luxury_loans.py"]