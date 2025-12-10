# src/utils/rate_limiter.py
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, limit_per_hour=3):
        self.limit = limit_per_hour
        self.data = defaultdict(list)  # user_id -> [timestamps]

    def allow(self, user_id):
        now = time.time()
        window_start = now - 3600
        arr = [t for t in self.data[user_id] if t > window_start]
        self.data[user_id] = arr
        if len(arr) >= self.limit:
            return False
        arr.append(now)
        self.data[user_id] = arr
        return True

rate_limiter = RateLimiter()
