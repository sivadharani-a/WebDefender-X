import time

class Logger:
    def __init__(self):
        self.logs = []

    def log(self, ip, url, action, reason):
        self.logs.append({
            'time': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
            'ip': ip,
            'url': url,
            'action': action,
            'reason': reason
        })

    def get_logs(self):
        return self.logs
