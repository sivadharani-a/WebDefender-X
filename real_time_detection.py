# real_time_detection.py

import pandas as pd
import joblib
import numpy as np
from datetime import datetime
import json
import os

MODEL_PATH = 'models/combined_model.pkl'
ENCODER_PATH = 'models/label_encoder.pkl'
SCALER_PATH = 'models/scaler.pkl'
LOG_PATH = 'logs/detections.json'

# Load model and encoders
def load_artifacts():
    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, encoder, scaler

# Detect attack type
def detect_attack(input_dict):
    model, encoder, scaler = load_artifacts()

    df = pd.DataFrame([input_dict])
    df = pd.get_dummies(df)

    # Load training columns from scaler
    scaler_columns = scaler.feature_names_in_
    for col in scaler_columns:
        if col not in df.columns:
            df[col] = 0
    df = df[scaler_columns]

    input_scaled = scaler.transform(df)
    prediction = model.predict(input_scaled)
    attack_name = encoder.inverse_transform(prediction)[0]
    return attack_name

# Log the detection
def log_detection(input_data, attack_type):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "attack_type": attack_type,
        "details": input_data
    }
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'w') as f:
            json.dump([entry], f, indent=2)
    else:
        with open(LOG_PATH, 'r+') as f:
            logs = json.load(f)
            logs.append(entry)
            f.seek(0)
            json.dump(logs, f, indent=2)

if __name__ == '__main__':
    # Sample input for testing (replace with actual input structure)
    input_data = {
        "duration": 0,
        "src_bytes": 491,
        "dst_bytes": 0,
        "flag": "SF",
        "protocol_type": "tcp",
        "service": "http",
        "land": 0,
        "wrong_fragment": 0,
        "urgent": 0
    }

    detected = detect_attack(input_data)
    print(f"[✓] Detected attack type: {detected}")
    log_detection(input_data, detected)
    print("[✓] Detection logged successfully.")
