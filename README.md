# Hailo Vision Lab

Raspberry Pi 5 + Hailo-10H computer vision playground.

## Current Capabilities

- FastAPI vision server with live MJPEG stream + overlay
- YOLOv8m / YOLOv11m / ResNet / SCRFD / Pose models running at ~15 FPS with overlay
- Web UI at `http://pi-ip:8765/`
- MCP tools for Hermes (status, capture, inference, model activation, benchmark)

## Room Entry Detector (WIP)

The goal is a lightweight watcher that:
- Detects when a person enters the room
- Writes a high-salience memory into CerebroCortex
- Can trigger Hermes context ("Andre is home", last project state, reminders)

## Hardware

- Raspberry Pi 5 (8GB)
- Hailo-10H AI HAT+
- IMX219 camera module

## Models Available

See `/usr/share/hailo-models/` on the Pi:
- `yolov8m_h10.hef` — 80-class COCO detection (best general purpose)
- `yolov11m_h10.hef` — newer YOLO
- `yolov8m_pose_h10.hef` — pose estimation
- `scrfd_2.5g_h8l.hef` — face detection
- `resnet_v1_50_h10.hef` — classification

## Quick Start

On the Pi:
```bash
systemctl --user status hailo-vision
curl http://localhost:8765/api/status
```

Web UI: `http://192.168.0.114:8765/`

## Future Ideas

- Multi-camera setup
- Person re-identification / "is it me?"
- Pose-based activity detection
- Integration with SensorHead (motion + vision fusion)
- Local LLM vision captions via ryzenai-serve VLM

## Quick Start on the Pi

```bash
# Vision server (already running via systemd)
systemctl --user status hailo-vision

# Web UI
open http://192.168.0.114:8765/

# Activate detection
curl -X POST http://192.168.0.114:8765/api/model/activate \
  -d '{"model_path":"/usr/share/hailo-models/yolov8m_h10.hef","threshold":0.25}'
```

## Room Entry Watcher

```bash
python room_entry_watcher.py
```

It will:
- Poll the vision server every second
- Require 3 consecutive person detections
- Write an episodic memory into CerebroCortex with tag `room-entry`
- Cooldown of 2 minutes between triggers

Future: turn the memory into an intention that can wake Hermes and give context.
