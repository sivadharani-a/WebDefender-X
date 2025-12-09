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
