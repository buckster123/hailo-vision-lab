#!/usr/bin/env python3
"""Simple example: Capture one frame and run inference."""
import requests
import json

PI = "http://192.168.0.114:8765"

def main():
    # Activate a model first (optional but recommended)
    requests.post(f"{PI}/api/model/activate", json={
        "model_path": "/usr/share/hailo-models/yolov8m_h10.hef",
        "threshold": 0.25
    })

    # Run inference on current frame
    r = requests.post(f"{PI}/api/inference", json={
        "model_path": "/usr/share/hailo-models/yolov8m_h10.hef",
        "threshold": 0.25
    })

    data = r.json()
    print(json.dumps(data, indent=2))

    # Save image with overlay
    img = requests.get(f"{PI}/api/frame", params={"overlay": True})
    with open("detection.jpg", "wb") as f:
        f.write(img.content)
    print("Saved detection.jpg")


if __name__ == "__main__":
    main()
