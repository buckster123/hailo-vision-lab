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
