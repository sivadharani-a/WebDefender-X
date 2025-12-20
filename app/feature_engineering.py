import math
import pandas as pd

SUSPICIOUS_KEYWORDS = ["select", "union", "script", "../", "or 1=1"]

def entropy(s):
    if not s:
        return 0
    probs = [s.count(c) / len(s) for c in set(s)]
    return -sum(p * math.log2(p) for p in probs)

def extract_features(df: pd.DataFrame):
    features = []
    for req in df["request"]:
        r = req.lower()
        features.append({
            "length": len(r),
            "entropy": entropy(r),
            "keyword_hits": sum(k in r for k in SUSPICIOUS_KEYWORDS)
        })
    return pd.DataFrame(features)
