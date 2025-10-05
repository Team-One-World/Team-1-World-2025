# api/ai_model.py

import os
import numpy as np
import pandas as pd
import joblib
import tensorflow as tf
from tensorflow.keras.models import load_model #type: ignore

# ---------------- Initialization ----------------
# You can adjust this if your model/scaler paths are different.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.keras")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.joblib")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.joblib")

# Load everything once at import time to avoid reloading per request
try:
    print("Loading ML model, scaler, and label encoder...")
    model = load_model(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    label_encoder = joblib.load(ENCODER_PATH)
    print("✅ Model, scaler, and label encoder loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model/scaler/encoder: {e}")
    model = None
    scaler = None
    label_encoder = None


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
