#!/usr/bin/env python3
"""Live overlay viewer using the MJPEG stream."""
import cv2
import requests
import numpy as np

STREAM_URL = "http://192.168.0.114:8765/api/stream"

def main():
    print("Opening live stream... Press 'q' to quit.")
    cap = cv2.VideoCapture(STREAM_URL)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Hailo Live", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
