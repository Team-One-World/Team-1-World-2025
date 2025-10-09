import os
import joblib
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model # type: ignore

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.keras")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.joblib")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.joblib")

# URLs to download model and related files if not present
FILES_TO_DOWNLOAD = {
    "model.keras": "https://huggingface.co/nimitjalan/1-world-2025-final/resolve/main/model.keras",
    "scaler.joblib": "https://huggingface.co/nimitjalan/1-world-2025-final/resolve/main/scaler.joblib",
    "label_encoder.joblib": "https://huggingface.co/nimitjalan/1-world-2025-final/resolve/main/label_encoder.joblib",
}

model = scaler = label_encoder = None

def load_resources():
    """Load ML assets if not already loaded."""
    global model, scaler, label_encoder
    if model and scaler and label_encoder:
        return  # already loaded

    print("🔄 Attempting to load model, scaler, and label encoder...")
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Model not found at {MODEL_PATH}")
        # Attempt to download missing files
        import requests
        os.makedirs(BASE_DIR, exist_ok=True)
        for filename, url in FILES_TO_DOWNLOAD.items():
            file_path = os.path.join(BASE_DIR, filename)
            if not os.path.exists(file_path):
                print(f"⬇️ Downloading {filename} from {url}...")
                response = requests.get(url, stream=True)
                response.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✅ Downloaded {filename} to {file_path}")
            else:
                print(f"ℹ️ {filename} already exists, skipping download.")

    try:
        tf.config.threading.set_intra_op_parallelism_threads(1)
        tf.config.threading.set_inter_op_parallelism_threads(1)
        model = load_model(MODEL_PATH, compile=False)
        scaler = joblib.load(SCALER_PATH)
        label_encoder = joblib.load(ENCODER_PATH)
        print("✅ Model and preprocessors loaded successfully.")
    except Exception as e:
        print(f"❌ Failed to load ML resources: {e}")
        model = scaler = label_encoder = None


def classify(data: dict):
    if model is None or scaler is None or label_encoder is None:
        load_resources()  # Try loading now
        if model is None:
            raise RuntimeError("Model or scaler not loaded properly.")

    # --- Classification logic (same as yours) ---
    ...
