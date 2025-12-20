from fastapi import FastAPI, Request, Depends
import pandas as pd

from app.rules import rule_based_detect, prompt_injection_detect
from app.feature_engineering import extract_features
from app.model import load_model, predict
from app.behavior import record_request
from app.drift import record_ml_score, detect_drift
from app.logger import log_decision
from app.security import verify_api_key

app = FastAPI(
    title="WebDefender-X",
    description="AI-Enhanced Web Application Firewall",
    version="1.0.0"
)

model = load_model()

def calculate_risk(rule_hit, ml_score, rate_exceeded, prompt_attack, drift):
    risk = 0
    if rule_hit:
        risk += 40
    if ml_score > 0.6:
        risk += 30
    if rate_exceeded:
        risk += 30
    if prompt_attack:
        risk += 40
    if drift:
        risk += 20
    return min(risk, 100)

@app.get("/")
def root():
    return {"message": "WebDefender-X API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/inspect-request")
def inspect_request(
    request: str,
    http_request: Request,
    api_key: str = Depends(verify_api_key)
):
    client_ip = http_request.client.host
    request_count = record_request(client_ip)

    df = pd.DataFrame({"request": [request]})
    features = extract_features(df)

    ml_score = predict(model, features)[0]
    record_ml_score(ml_score)
    drift_detected = detect_drift()

    rule_hit = rule_based_detect(request)
    prompt_attack = prompt_injection_detect(request)
    rate_exceeded = request_count > 20

    reasons = []
    if rule_hit:
        reasons.append("RULE_MATCH")
    if ml_score > 0.6:
        reasons.append("ANOMALY_SCORE")
    if rate_exceeded:
        reasons.append("BEHAVIORAL_RATE")
    if prompt_attack:
        reasons.append("PROMPT_INJECTION")
    if drift_detected:
        reasons.append("MODEL_DRIFT")

    risk = calculate_risk(
        rule_hit,
        ml_score,
        rate_exceeded,
        prompt_attack,
        drift_detected
    )

    decision = "BLOCK" if risk >= 60 else "ALLOW"

    # ✅ Correct placement
    log_decision(client_ip, request, risk, decision, reasons)

    return {
        "request": request,
        "client_ip": client_ip,
        "ml_score": round(float(ml_score), 2),
        "requests_last_minute": request_count,
        "risk_score": risk,
        "decision": decision,
        "reasons": reasons
    }
