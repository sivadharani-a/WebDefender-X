import csv
from datetime import datetime
import os

LOG_FILE = "logs/waf_audit_log.csv"

def log_decision(client_ip, request, risk, decision, reasons):
    os.makedirs("logs", exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp", "client_ip", "request",
                "risk_score", "decision", "reasons"
            ])

        writer.writerow([
            datetime.utcnow().isoformat(),
            client_ip,
            request,
            risk,
            decision,
            "|".join(reasons)
        ])
