import os
import time
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
POD_ID = os.getenv("RUNPOD_POD_ID")
INACTIVITY_LIMIT = int(os.getenv("INACTIVITY_LIMIT", 600))  # seconds
LAST_REQUEST_FILE = Path(os.getenv("LAST_REQUEST_FILE", "/tmp/last_request.txt"))


def runpod_api(path, method="GET", data=None):
    url = f"https://api.runpod.io/{path}"
    headers = {"Authorization": f"Bearer {RUNPOD_API_KEY}"}
    r = requests.request(method, url, headers=headers, json=data)
    r.raise_for_status()
    return r.json()


def stop_pod():
    print("[AutoShutdown] Stopping Pod due to inactivity...")
    runpod_api(f"pods/{POD_ID}/stop", "POST")


def get_last_request_time():
    if LAST_REQUEST_FILE.exists():
        return float(LAST_REQUEST_FILE.read_text().strip())
    return time.time()


if __name__ == "__main__":
    while True:
        last_request_time = get_last_request_time()
        if time.time() - last_request_time > INACTIVITY_LIMIT:
            stop_pod()
        time.sleep(60)
