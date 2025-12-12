#!/bin/bash

MODEL_PATH="model/tomato_model.h5"
MODEL_URL="https://drive.google.com/uc?id=1d50zWVCxGQYEhBEVv9h523JytnrZo6Tx"

if [ ! -f "$MODEL_PATH" ]; then
    echo "Model not found. Downloading..."
    mkdir -p model
    gdown "$MODEL_URL" -O "$MODEL_PATH"
fi

echo "Starting server..."
exec gunicorn -b 0.0.0.0:8080 app:app
