FROM python:3.11-slim

# Install dependencies including wget & gdown
RUN apt-get update && apt-get install -y \
    wget \
    gcc \
    g++ \
    && pip install --no-cache-dir gdown \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure start.sh has execute permissions
RUN chmod +x start.sh

CMD ["./start.sh"]
