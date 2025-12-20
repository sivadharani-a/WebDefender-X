import pandas as pd
from app.feature_engineering import extract_features
from app.model import train_model

df = pd.read_csv("data/http_requests.csv")
X = extract_features(df)
y = df["label"]

train_model(X, y)
print("WAF ML model trained successfully.")
