import os
import joblib
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import LabelEncoder, StandardScaler

MODELS_DIR = '../models'
LOG_FILE = '../logs/attack_log.csv'

models = {
    'SQL Injection': 'sql_injection_model.pkl',
    'DDoS': 'ddos_model.pkl',
    'Phishing': 'phishing_model.pkl',
    'XSS': 'xss_model.pkl',
    'Ransomware': 'ransomware_model.pkl',
    'MITM': 'mitm_model.pkl',
    'Zero-Day': 'zero_day_model.pkl',
    'Insider Threat': 'insider_threat_model.pkl',
    'API Misuse': 'api_misuse_model.pkl',
    'Credential Stuffing': 'credential_stuffing_model.pkl',
    'Botnet': 'botnet_model.pkl',
    'Cryptojacking': 'cryptojacking_model.pkl',
    'Privilege Escalation': 'privilege_escalation_model.pkl',
    'Data Exfiltration': 'data_exfiltration_model.pkl',
    'AI-based Attacks': 'ai_attacks_model.pkl',
}

loaded_models = {}
for attack, filename in models.items():
    path = os.path.join(MODELS_DIR, filename)
    if os.path.exists(path):
        loaded_models[attack] = joblib.load(path)

def preprocess_input(input_data):
    df = pd.DataFrame([input_data])
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = LabelEncoder().fit_transform(df[col])
    df = pd.DataFrame(StandardScaler().fit_transform(df), columns=df.columns)
    return df

def detect_and_block(input_data):
    input_vector = preprocess_input(input_data)
    for attack, model in loaded_models.items():
        try:
            prediction = model.predict(input_vector)
            if prediction[0] == 1:  # 1 = attack
                log_attack(attack, input_data, blocked=True)
                return f"[BLOCKED] {attack} detected and blocked!"
        except Exception as e:
            print(f"[ERROR] {attack}: {e}")

    log_attack("Legitimate", input_data, blocked=False)
    return "[ALLOWED] Clean traffic processed."

def log_attack(attack_type, details, blocked):
    log_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'attack_type': attack_type,
        'details': str(details),
        'blocked': blocked
    }
    df = pd.DataFrame([log_data])
    df.to_csv(LOG_FILE, mode='a', header=False, index=False)
