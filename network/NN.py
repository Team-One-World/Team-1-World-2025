import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks, mixed_precision # type: ignore

from tensorflow.keras.models import load_model # type: ignore

mixed_precision.set_global_policy('mixed_float16')

df = pd.read_csv('Full Data.csv')
print(df.shape)
print(df.dtypes)
df.head()

# ---------------- Data Preprocessing ----------------
fp_flags = ['fp_flag_nt','fp_flag_ss','fp_flag_co','fp_flag_ec']
df['any_fp_flag'] = df[fp_flags].sum(axis=1) > 0

def make_label(row):
    if row['disposition'] == 1:
        return 'confirmed'
    elif row['disposition'] == 0 and row['any_fp_flag']:
        return 'false_positive'
    else:
        return 'candidate'

df['label'] = df.apply(make_label, axis=1)
print(df['label'].value_counts())

# Removed source_kepler and source_tess from features
features = [
    'period','duration','transit_depth','planet_radius',
    'star_temp','star_radius','model_snr'
]
X = df[features].copy()
y = df['label'].copy()

num_cols = ['period','duration','transit_depth','planet_radius','star_temp','star_radius','model_snr']
for c in ['period','duration','planet_radius','star_radius','model_snr']:
    X.loc[X[c] <= 0, c] = np.nan
for c in ['transit_depth','star_temp']:
    X.loc[X[c] < 0, c] = np.nan

# Fill NaNs with median for robustness
for c in num_cols:
    if X[c].isna().any():
        X[c].fillna(X[c].median(), inplace=True)

# Log transforms
X['transit_depth_log'] = np.log1p(X['transit_depth'])
X['planet_radius_log'] = np.log1p(X['planet_radius'])
X = X.drop(columns=['transit_depth','planet_radius'])

# Scale features
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)

# Encode labels
le = LabelEncoder()
y_enc = le.fit_transform(y)
print("Label mapping:", dict(zip(le.classes_, range(len(le.classes_)))))

# ---------------- Train/Test Split ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_enc, test_size=0.20, random_state=42, stratify=y_enc
)

# Class balancing
classes = np.unique(y_train)
class_weights = compute_class_weight('balanced', classes=classes, y=y_train)
class_weight_dict = dict(zip(classes, class_weights))
print("Class weights:", class_weight_dict)

# ---------------- Model Definition ----------------
tf.keras.backend.clear_session()
input_dim = X_train.shape[1]

inputs = keras.Input(shape=(input_dim,))
x = layers.Dense(128, activation='relu')(inputs)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.3)(x)
x = layers.Dense(64, activation='relu')(x)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.2)(x)
x = layers.Dense(32, activation='relu')(x)
outputs = layers.Dense(len(le.classes_), activation='softmax', dtype='float32')(x)  # Force float32 output

model = keras.Model(inputs, outputs)
model.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
model.summary()

# ---------------- Training ----------------
es = callbacks.EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True)
mc_path = 'exoplanet_classifier_best.keras'
mc = callbacks.ModelCheckpoint(mc_path, monitor='val_loss', save_best_only=True)

history = model.fit(
    X_train, y_train,
    validation_split=0.15,
    epochs=100,
    batch_size=64,
    class_weight=class_weight_dict,
    callbacks=[es, mc],
    verbose=2
)

# ---------------- Evaluation ----------------
loss, acc = model.evaluate(X_test, y_test)
print(f"Test accuracy: {acc:.4f}, loss: {loss:.4f}")

y_pred_probs = model.predict(X_test)
y_pred = y_pred_probs.argmax(axis=1)
print(classification_report(y_test, y_pred, target_names=le.classes_))

cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix:\n", cm)

# ---------------- Plots ----------------
plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.plot(history.history['loss'], label='train_loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.legend(); plt.title('Loss')

plt.subplot(1,2,2)
plt.plot(history.history['accuracy'], label='train_acc')
plt.plot(history.history['val_accuracy'], label='val_acc')
plt.legend(); plt.title('Accuracy')

plt.tight_layout()
plt.show()

# ---------------- Save Model ----------------
model.save('exoplanet_classifier_final.keras')
joblib.dump(scaler, 'scaler.joblib')
joblib.dump(le, 'label_encoder.joblib')

print("Saved: exoplanet_classifier_best.keras (checkpoint), exoplanet_classifier_final.keras, scaler.joblib, label_encoder.joblib")

# ---------------- Interactive Prediction ----------------
scaler = joblib.load('scaler.joblib')
le = joblib.load('label_encoder.joblib')
model = load_model('exoplanet_classifier_final.keras')

print("Enter the following parameters for prediction:\n")

period = float(input("Orbital period (days): "))
duration = float(input("Transit duration (hours): "))
star_temp = float(input("Star temperature (K): "))
star_radius = float(input("Star radius (in solar radii): "))
model_snr = float(input("Model SNR (signal-to-noise ratio): "))
transit_depth = float(input("Transit depth (ppm): "))
planet_radius = float(input("Planet radius (in Earth radii): "))

transit_depth_log = np.log1p(transit_depth)
planet_radius_log = np.log1p(planet_radius)

cols = [
    'period', 'duration', 'star_temp', 'star_radius',
    'model_snr', 'transit_depth_log', 'planet_radius_log'
]

xrow = pd.DataFrame([[
    period, duration, star_temp, star_radius,
    model_snr, transit_depth_log, planet_radius_log
]], columns=cols)

xscaled = scaler.transform(xrow)

pred_proba = model.predict(xscaled)[0]
pred_label = le.inverse_transform([pred_proba.argmax()])[0]

print("\n===== Prediction Result =====")
print(f"Predicted Class: {pred_label}")
print("\n Probabilities for each class:")
for cls, prob in zip(le.classes_, pred_proba):
    print(f"  - {cls}: {prob:.4f}")