FROM python:3.11-slim

# Directory di dalam container
WORKDIR /app

# Copy requirements dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file backend
COPY . .

# Pastikan start.sh dapat dijalankan
RUN chmod +x /app/start.sh

EXPOSE 5000

# Jalankan backend dengan start.sh
CMD ["./start.sh"]
