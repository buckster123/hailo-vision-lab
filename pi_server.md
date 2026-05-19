# Pi Vision Server

The actual FastAPI server lives on the Pi at:

`~/hailo-vision-server/server.py`

It is also installed as a systemd service:

```bash
systemctl --user status hailo-vision
journalctl --user -u hailo-vision -f
```

Source is intentionally kept on the device for now (camera + Hailo drivers are Pi-specific). We can extract a clean package later.
