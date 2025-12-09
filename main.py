from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import asyncio

from threat_intel import ThreatIntel
from ml_detector import MLDetector
from logger import Logger

app = FastAPI()

# --- CORS so Chrome extension can call this API ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # for dev; later you can restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

threat_intel = ThreatIntel()
ml_detector = MLDetector()
logger = Logger()


# Periodically update threat intel (simplified here)
@app.on_event("startup")
async def startup_event():
    await threat_intel.update()


# ---------- Chrome extension & external clients ----------
class InspectRequest(BaseModel):
    url: str
    ip: str | None = None


@app.post("/api/inspect")
async def inspect_url(payload: InspectRequest, request: Request):
    """
    Mini firewall decision endpoint for Chrome extension.
    Returns {decision: 'allow'|'block', reason: str}
    """
    client_ip = payload.ip or request.client.host
    url = payload.url

    decision = "allow"
    reason = "passed_checks"

    # 1. IP blacklist check
    if threat_intel.is_ip_blacklisted(client_ip):
        decision = "block"
        reason = "blacklisted_ip"

    # 2. Traditional attack patterns
    elif threat_intel.check_patterns(url):
        decision = "block"
        reason = "traditional_attack_pattern"

    # 3. ML anomaly detection
    elif ml_detector.predict(url) == -1:
        decision = "block"
        reason = "anomaly_detected"

    # Log the decision
    logger.log(client_ip, url, decision, reason)

    return {"decision": decision, "reason": reason}


# ---------- Existing reverse-proxy style middleware ----------
@app.middleware("http")
async def webdefender_middleware(request: Request, call_next):
    client_ip = request.client.host
    url = str(request.url)

    # 1. IP blacklist check
    if threat_intel.is_ip_blacklisted(client_ip):
        logger.log(client_ip, url, "blocked", "blacklisted_ip")
        return JSONResponse(
            status_code=403,
            content={"detail": "Forbidden: Malicious IP"},
        )

    # 2. Traditional attack patterns
    if threat_intel.check_patterns(url):
        logger.log(client_ip, url, "blocked", "traditional_attack_pattern")
        return JSONResponse(
            status_code=403,
            content={"detail": "Forbidden: Attack pattern detected"},
        )

    # 3. ML anomaly detection
    if ml_detector.predict(url) == -1:
        logger.log(client_ip, url, "blocked", "anomaly_detected")
        return JSONResponse(
            status_code=403,
            content={"detail": "Forbidden: Anomalous request detected"},
        )

    # ✅ 4. If all checks passed, continue to the actual FastAPI route
    response = await call_next(request)
    logger.log(client_ip, url, "allowed", "passed_checks")
    return response



@app.get("/")
async def root():
    return {"status": "WebDefender-X backend running"}

