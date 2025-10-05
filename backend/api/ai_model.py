import tensorflow as tf
import numpy as np
import os

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the model file
model_path = os.path.join(current_dir, 'model.keras')

# Global variable to cache the loaded model
_model = None

def get_model():
    """Lazy load the model only when needed"""
    global _model
    if _model is None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found at {model_path}. "
                "Please run 'python manage.py model_loader' first."
            )
        _model = tf.keras.models.load_model(model_path)
    return _model

def classify(data):
    """
    Classify exoplanet data using the trained model.
    
    Args:
        data: Dictionary containing the following keys:
            - orbital_period
            - radius
            - duration
            - transit_depth
            - star_temp
            - star_radius
            - model_snr
    
    Returns:
        Model prediction array
    """
    # Get the model (loads it on first call)
    model = get_model()
    
    # Extract features from the input data, ensuring the order matches the model's training
    features = np.array([
        data.get('orbital_period'),
        data.get('radius'),
        data.get('duration'),
        data.get('transit_depth'),
        data.get('star_temp'),
        data.get('star_radius'),
        data.get('model_snr'),
    ]).reshape(1, -1)  # Reshape for single prediction

    # Make prediction
    prediction = model.predict(features)
    
    return prediction