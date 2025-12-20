import aiohttp
import asyncio

class ThreatIntel:
    def __init__(self):
        # Store blacklisted IPs and suspicious patterns
        self.blacklisted_ips = set()
        self.suspicious_patterns = []

    async def fetch_abuseipdb(self):
        # Dummy fetch - in real project, integrate AbuseIPDB API or other feeds
        # For demo, hardcoded IPs
        self.blacklisted_ips.update({"1.2.3.4", "5.6.7.8"})

    async def fetch_suspicious_patterns(self):
        # Could fetch latest regex from feeds
        self.suspicious_patterns = [
            r"union\s+select",  # SQLi
            r"<script.*?>",     # XSS
            r"(etc/passwd)",    # Path traversal
        ]

    async def update(self):
        # Fetch threat feeds asynchronously
        await asyncio.gather(
            self.fetch_abuseipdb(),
            self.fetch_suspicious_patterns()
        )

    def is_ip_blacklisted(self, ip):
        return ip in self.blacklisted_ips

    def check_patterns(self, text):
        import re
        for pattern in self.suspicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
