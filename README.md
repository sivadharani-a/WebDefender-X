WebDefender-X (AI-Assisted Web Security Platform)

Overview

WebDefender-X is a backend-focused web security platform designed to inspect incoming web requests and make risk-based access decisions using a combination of rule-based checks and machine learning–assisted anomaly detection.
The project demonstrates secure API design, AI-assisted decision logic, audit logging, and deployment readiness.
This project was developed as an academic capstone and backend security learning initiative.

Key Features

- Request inspection and risk scoring
- Machine learning–assisted anomaly detection
- Rule-based detection for common attack patterns
- Risk-based allow/block decisions
- Audit logging for traceability
- API authentication using API keys
- Containerized deployment using Docker

Technology Stack

Backend: Python, FastAPI
Machine Learning: scikit-learn (Isolation Forest)
Security Concepts: Input validation, request analysis, audit logging
Storage: CSV / SQLite (audit trail)
Deployment: Docker
Tools: Git, Linux

Architecture Overview

Client sends a request to the inspection API
Request is validated and authenticated
Rule-based checks evaluate known attack indicators
ML model evaluates behavioral anomalies
Risk score is calculated
Decision (ALLOW / BLOCK) is generated
Decision is logged for audit and analysis


Machine Learning Component

- Uses an Isolation Forest model for anomaly detection
- Model evaluates request characteristics such as payload length and structure
- Designed to assist decision-making rather than replace rule-based logic
- Includes scope for monitoring model behavior over time
- Logging and Audit Trail

Each inspected request is logged with:

- Timestamp
- Client IP
- Risk score
- Decision
- Detection reasons

This supports traceability and incident review.

Deployment

Run Locally
  pip install -r requirements.txt
  uvicorn app.main:app --reload

Run with Docker
  docker build -t webdefender-x .
  docker run -p 8000:8000 webdefender-x

Security Considerations

- API access protected using API keys
- Input validation applied to request data
- Logging designed to support security monitoring
- Architecture aligned with defensive security principles

Project Scope

This project is intended for:

--> Demonstrating backend engineering skills
--> Applying machine learning in a security context
--> Understanding request inspection and risk evaluation
--> Academic and learning purposes
--> It is not intended for direct production use without further hardening.

License

This project is provided for educational and demonstration purposes only.
