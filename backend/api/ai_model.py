import os
import requests
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

# ---------------- Classification Function ----------------
def classify(data: dict):
    """
    Classify a planet candidate using the trained deep learning model.

    Args:
        data (dict): Dictionary containing the required numeric fields:
            - orbital_period
            - duration
            - transit_depth
            - radius
            - star_temp
            - star_radius
            - model_snr

    Returns:
        tuple: (classification_label: str, confidence_score: float)
    """

    load_resources()


    if model is None or scaler is None or label_encoder is None:
        raise RuntimeError("Model or scaler not loaded properly.")

    # --- Step 1: Extract and clean fields ---
    try:
        # Convert all fields to float safely
        period = float(data.get("orbital_period"))
        duration = float(data.get("duration"))
        transit_depth = float(data.get("transit_depth"))
        planet_radius = float(data.get("radius"))
        star_temp = float(data.get("star_temp"))
        star_radius = float(data.get("star_radius"))
        model_snr = float(data.get("model_snr"))
    except (TypeError, ValueError):
        raise ValueError("Invalid or missing numeric input field(s).")

    # --- Step 2: Apply same preprocessing as training ---
    transit_depth_log = np.log1p(transit_depth)
    planet_radius_log = np.log1p(planet_radius)

    # Same column order as training
    columns = [
        "period", "duration", "star_temp", "star_radius",
        "model_snr", "transit_depth_log", "planet_radius_log"
    ]

    # Build a DataFrame for consistency with scaler
    input_df = pd.DataFrame([[
        period, duration, star_temp, star_radius,
        model_snr, transit_depth_log, planet_radius_log
    ]], columns=columns)

    # Scale features
    scaled_input = scaler.transform(input_df)

    # --- Step 3: Predict ---
    pred_proba = model.predict(scaled_input)[0]  # Shape: (num_classes,)
    pred_index = int(np.argmax(pred_proba))
    confidence = float(np.max(pred_proba))
    pred_label = label_encoder.inverse_transform([pred_index])[0]

    # --- Step 4: Return readable output ---
    return pred_label, round(confidence, 4)
