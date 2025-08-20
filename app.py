from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/get_stats")
def get_stats():
     
    data = {
        "total_requests": random.randint(10000, 20000),  
        "blocked_attacks": random.randint(50, 150),
        "malware_uploads": random.randint(1, 10),
        "detection_accuracy": round(random.uniform(90.0, 99.9), 2),
        "top_ips": [{"ip": f"192.168.0.{i}", "count": random.randint(5, 20)} for i in range(1, 3)],
        "attack_distribution": {"SQL Injection": random.randint(20, 40), "XSS": random.randint(15, 30), "DDoS": random.randint(30, 50)},
        "real_time_traffic": [random.randint(15, 30) for _ in range(10)],
        "threat_severity": {"High": random.randint(5, 15), "Medium": random.randint(10, 25), "Low": random.randint(5, 20), "Info": random.randint(1, 10)}
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

