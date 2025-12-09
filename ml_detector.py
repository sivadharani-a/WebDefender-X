import pandas as pd
from sklearn.ensemble import IsolationForest

class MLDetector:
    def __init__(self):
        self.model = None
        self.train_model()

    def train_model(self):
        # Train on synthetic normal traffic
        data = pd.DataFrame([
            [30, 1],
            [25, 2],
            [35, 1],
            [40, 3],
            [28, 1]
        ], columns=['url_len', 'param_count'])
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.model.fit(data)

    def extract_features(self, url):
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        return [len(url), len(params)]

    def predict(self, url):
        features = [self.extract_features(url)]
        pred = self.model.predict(features)[0]
        return pred  # -1 anomaly, 1 normal
