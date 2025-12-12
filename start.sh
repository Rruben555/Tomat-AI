#!/bin/bash

MODEL_DIR="model"
MODEL_FILE="model/tomato_model.h5"
MODEL_URL="https://drive.google.com/file/d/1d50zWVCxGQYEhBEVv9h523JytnrZo6Tx/view?usp=sharing"

mkdir -p $MODEL_DIR

# Download model jika belum ada
if [ ! -f "$MODEL_FILE" ]; then
    echo "Model not found. Downloading..."
    wget -O "$MODEL_FILE" "$MODEL_URL"
else
    echo "Model already exists. Skipping download."
fi

gunicorn app:app --bind 0.0.0.0:$PORT
