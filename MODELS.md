# Hailo Models Reference

## Recommended Models (Hailo-10H optimized)

| Model | Task | Input | FPS (approx) | Notes |
|-------|------|-------|--------------|-------|
| `yolov8m_h10.hef` | Object Detection (80 COCO classes) | 640x640 | ~76 (bare), ~15 (overlay) | Best all-rounder |
| `yolov11m_h10.hef` | Object Detection | 640x640 | High | Newer YOLO |
| `yolov8m_pose_h10.hef` | Pose Estimation | 640x640 | Good | 17 keypoints |
| `scrfd_2.5g_h8l.hef` | Face Detection | 640x640 | Very fast | Good for entry detection |
| `resnet_v1_50_h10.hef` | Image Classification | 224x224 | Fast | General purpose |

## How to Activate

```bash
curl -X POST http://192.168.0.114:8765/api/model/activate \
  -d '{"model_path":"/usr/share/hailo-models/yolov8m_h10.hef","threshold":0.25}'
```

## Performance Notes

- Streaming inference (web UI) runs at ~15 FPS with overlay.
- Bare inference is much faster (~70+ FPS).
- Temperature stays low (~31-33°C) even under load.

## Common Post-process Configs

Located in `/usr/share/rpi-camera-assets/`:
- `hailo_yolov8_inference.json`
- `hailo_yolov8_pose.json`
- `hailo_scrfd.json`
- `hailo_yolov5_segmentation.json`
