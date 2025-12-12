FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model secara paksa
COPY model ./model

# Copy semua file lainnya
COPY . .

RUN chmod +x /app/start.sh

EXPOSE 5000
CMD ["./start.sh"]
