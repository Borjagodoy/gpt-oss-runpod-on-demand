from fastapi import FastAPI
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
POD_ID = os.getenv("RUNPOD_POD_ID")
HOURLY_PRICE = float(os.getenv("HOURLY_PRICE", 0.16))
MONTHLY_BUDGET = float(os.getenv("MONTHLY_BUDGET", 50.0))
INACTIVITY_LIMIT = int(os.getenv("INACTIVITY_LIMIT", 600))  # seconds

last_request_time = 0
hours_used = 0.0


def runpod_api(path, method="GET", data=None):
    url = f"https://api.runpod.io/{path}"
    headers = {"Authorization": f"Bearer {RUNPOD_API_KEY}"}
    r = requests.request(method, url, headers=headers, json=data)
    r.raise_for_status()
    return r.json()


def pod_running():
    status = runpod_api(f"pods/{POD_ID}")["status"]
    return status == "RUNNING"


@app.post("/chat")
def chat(prompt: str):
    global last_request_time, hours_used

    cost = hours_used * HOURLY_PRICE
    if cost >= MONTHLY_BUDGET:
        return {"error": "Monthly budget reached"}

    if not pod_running():
        runpod_api(f"pods/{POD_ID}/start", "POST")
        time.sleep(45)  # wait for snapshot + model load

    start_time = time.time()
    r = requests.post(f"http://<POD_IP>:8000/v1/ch_
