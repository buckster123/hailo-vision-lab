#!/usr/bin/env python3
"""
Room Entry Watcher
Polls the Hailo Vision Server and triggers when a person is detected.
Writes a memory into CerebroCortex so Hermes can pick it up later.
"""
import time
import json
import requests
from datetime import datetime

VISION_URL = "http://192.168.0.114:8765"
CEREBRO_URL = "http://localhost:8767"   # adjust if running elsewhere
PERSON_CLASS = 0
CONFIDENCE = 0.35
COOLDOWN_SECONDS = 120          # don't spam memories
REQUIRED_FRAMES = 3             # consecutive detections required

last_trigger = 0
consecutive = 0

def post_memory(content: str, tags=None, salience=0.8):
    """Write a memory into CerebroCortex"""
    try:
        payload = {
            "content": content,
            "memory_type": "episodic",
            "tags": tags or ["room-entry", "person-detected"],
            "salience": salience,
            "agent_id": "room-watcher"
        }
        r = requests.post(f"{CEREBRO_URL}/memory", json=payload, timeout=5)
        if r.ok:
            print(f"[Cerebro] Memory stored: {content}")
        else:
            print(f"[Cerebro] Failed: {r.text}")
    except Exception as e:
        print(f"[Cerebro] Error: {e}")

def get_status():
    try:
        r = requests.get(f"{VISION_URL}/api/status", timeout=3)
        return r.json()
    except:
        return None

def main():
    global last_trigger, consecutive

    print("Room Entry Watcher started. Watching for people...")
    while True:
        status = get_status()
        if not status:
            time.sleep(2)
            continue

        detections = status.get("detections", 0)
        active_model = status.get("active_model")

        if detections > 0 and active_model and "yolo" in active_model.lower():
            consecutive += 1
        else:
            consecutive = 0

        if consecutive >= REQUIRED_FRAMES:
            now = time.time()
            if now - last_trigger > COOLDOWN_SECONDS:
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                msg = f"Andre entered the room at {ts}"
                print(f"[DETECTED] {msg}")
                post_memory(msg)
                last_trigger = now
            consecutive = 0   # reset after trigger

        time.sleep(1.0)

if __name__ == "__main__":
    main()
