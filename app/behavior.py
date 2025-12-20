from collections import defaultdict
import time

REQUEST_WINDOW = 60
REQUEST_LIMIT = 20

client_requests = defaultdict(list)

def record_request(client_ip: str) -> int:
    now = time.time()
    client_requests[client_ip].append(now)

    client_requests[client_ip] = [
        t for t in client_requests[client_ip]
        if now - t <= REQUEST_WINDOW
    ]

    return len(client_requests[client_ip])
