Real-Time Event Analytics Dashboard

ML-Driven Event Classification • Real-Time Visualization • Browser Integration

This project is a real-time analytics platform that processes live events, classifies them using a combination of rule-based logic + machine learning, and visualizes insights in a modern interactive analytics dashboard.It includes a FastAPI backend for event processing and a React frontend for high-tech visualization.

 Key Features
 1. Machine-Learning Based Event Classification

Uses an Isolation Forest model to detect unusual or anomalous events.
Applies rule-based classification for known patterns.
Aggregates results into categorical labels such as:
allowed
blocked
anomaly_detected
pattern_match

2. Real-Time Event Stream Processing

Backend exposes a lightweight API (/api/inspect, /api/logs)

Each decision is logged with:

Source (IP)
Target URL / input
Status
Category label
Data refreshes automatically every few seconds in the dashboard.

3. High-Tech Visual Analytics Dashboard (React + Recharts)

The dashboard displays:

KPI Summary
Total events
Successful vs error events
Success rate

Visualizations:

Event Throughput (line chart)
Status Composition Over Time (stacked area chart)
Category Breakdown (bar chart)
Top Event Sources (horizontal ranking bar chart)
Live Event Stream Table
Designed with a modern, dark UI using Tailwind CSS.

Screenshots of WebDefender-X dashboard:

<img width="1892" height="918" alt="Screenshot 2025-12-11 190134" src="https://github.com/user-attachments/assets/329d4548-7e68-4bb7-96d5-f335be843482" />
<img width="1891" height="914" alt="Screenshot 2025-12-11 190156" src="https://github.com/user-attachments/assets/6a5a2345-cd4e-4ad2-8902-269b20ec0774" />
<img width="1889" height="913" alt="Screenshot 2025-12-11 190216" src="https://github.com/user-attachments/assets/f2c6793f-bbb5-47a1-bf88-7caee5b5a886" />
