# src/utils/screenshot.py

import requests
from src.config import SCREENSHOT_API_KEY, ALLOW_PUBLIC_SCREENSHOT

SCREENSHOT_API_URL = "https://api.screenshotapi.net/screenshot"


def screenshot_url(url):
    if not (SCREENSHOT_API_KEY and ALLOW_PUBLIC_SCREENSHOT):
        return None

    params = {
        "token": SCREENSHOT_API_KEY,
        "url": url,
        "output": "image"
    }

    try:
        r = requests.get(SCREENSHOT_API_URL, params=params)
        if r.status_code == 200:
            return r.content
        return None
    except Exception:
        return None
