import os
import uuid
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
from flask_cors import CORS

# =================================================
# FLASK APP + CORS
# =================================================
app = Flask(__name__)
CORS(app)

# =================================================
# MODEL
# =================================================
MODEL_PATH = "model/tomato_model.h5"
model = load_model(MODEL_PATH)

# =================================================
# STATIC FOLDERS
# =================================================
UPLOAD_FOLDER = "static/uploads"
GRAPH_FOLDER = "static/graphs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GRAPH_FOLDER, exist_ok=True)

# =================================================
# STATIC FILE ROUTES
# =================================================
@app.route("/static/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/static/graphs/<filename>")
def graph_file(filename):
    return send_from_directory(GRAPH_FOLDER, filename)

# =================================================
# API PREDICT
# =================================================
@app.route("/api/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save file
    img_id = f"{uuid.uuid4()}.jpg"
    img_path = os.path.join(UPLOAD_FOLDER, img_id)
    file.save(img_path)

    # Preprocess
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array)
    classes = ["Mentah", "Setengah Matang", "Matang"]
    prediction = classes[np.argmax(preds)]

    # Create graph
    graph_id = f"{uuid.uuid4()}.png"
    graph_path = os.path.join(GRAPH_FOLDER, graph_id)

    img_np = image.img_to_array(image.load_img(img_path)) / 255.0
    r, g, b = img_np[:, :, 0], img_np[:, :, 1], img_np[:, :, 2]

    plt.figure(figsize=(6, 4))
    plt.plot(r.mean(axis=0), "r")
    plt.plot(g.mean(axis=0), "g")
    plt.plot(b.mean(axis=0), "b")
    plt.title("RGB Color Spread")
    plt.tight_layout()
    plt.savefig(graph_path)
    plt.close()

    return jsonify({
        "prediction": prediction,
        "image_url": f"/static/uploads/{img_id}",
        "graph_url": f"/static/graphs/{graph_id}"
    })

# =================================================
# RUN SERVER
# =================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Backend running at: http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)
