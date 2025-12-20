from collections import deque

WINDOW_SIZE = 50
ml_scores = deque(maxlen=WINDOW_SIZE)

def record_ml_score(score: float):
    ml_scores.append(score)

def detect_drift():
    if len(ml_scores) < WINDOW_SIZE:
        return False
    avg_score = sum(ml_scores) / len(ml_scores)
    return avg_score > 0.65
