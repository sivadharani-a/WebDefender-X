import joblib
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "models/waf_model.pkl"

def train_model(X, y):
    model = LogisticRegression()
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)

def load_model():
    return joblib.load(MODEL_PATH)

def predict(model, X):
    return model.predict_proba(X)[:, 1]
