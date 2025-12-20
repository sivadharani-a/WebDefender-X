RULE_PATTERNS = [
    "select", "union", "<script", "../", "or 1=1"
]

PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "act as system",
    "bypass safety",
    "you are now"
]

def rule_based_detect(request: str) -> bool:
    r = request.lower()
    return any(p in r for p in RULE_PATTERNS)

def prompt_injection_detect(request: str) -> bool:
    r = request.lower()
    return any(p in r for p in PROMPT_INJECTION_PATTERNS)
