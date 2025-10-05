import tensorflow as tf
import numpy as np
import os

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the model file
model_path = os.path.join(current_dir, 'model.keras')

# Load the pre-trained model
model = tf.keras.models.load_model(model_path)

def classify(data):
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