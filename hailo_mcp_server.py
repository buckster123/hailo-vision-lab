#!/usr/bin/env python3
"""Hailo 10H Vision MCP Server (Improved)
Exposes clean, useful tools for Hermes.
"""
import json
import asyncio
import base64
from typing import Any, Optional

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent, ImageContent

PI_BASE = "http://192.168.0.114:8765"

server = Server("hailo-vision")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="hailo_status",
            description="Get current Hailo 10H device, camera, and inference status",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="hailo_list_models",
            description="List all available HEF models with input shapes and sizes",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="hailo_capture_frame",
            description="Capture the current camera frame. Returns image + optional detection overlay",
            inputSchema={
                "type": "object",
                "properties": {
                    "overlay": {
                        "type": "boolean",
                        "description": "Include detection boxes if a model is active",
                        "default": True,
                    }
                },
            },
        ),
        Tool(
            name="hailo_run_inference",
            description="Run inference on the current frame using a specific model and return detections",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_path": {
                        "type": "string",
                        "description": "Full path to .hef file, e.g. /usr/share/hailo-models/yolov8m_h10.hef",
                    },
                    "threshold": {
                        "type": "number",
                        "description": "Minimum confidence (0.0-1.0)",
                        "default": 0.25,
                    },
                    "return_image": {
                        "type": "boolean",
                        "description": "Also return a JPEG with detections drawn",
                        "default": False,
                    },
                },
                "required": ["model_path"],
            },
        ),
        Tool(
            name="hailo_activate_model",
            description="Activate continuous inference with a model (updates the live overlay)",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_path": {"type": "string"},
                    "threshold": {"type": "number", "default": 0.25},
                },
                "required": ["model_path"],
            },
        ),
        Tool(
            name="hailo_deactivate_model",
            description="Stop continuous inference",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="hailo_benchmark",
            description="Benchmark a model and return FPS + power info",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_name": {
                        "type": "string",
                        "description": "Model name without .hef, e.g. yolov8m_h10",
                    }
                },
                "required": ["model_name"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list:
    async with httpx.AsyncClient(timeout=45.0) as client:
        if name == "hailo_status":
            r = await client.get(f"{PI_BASE}/api/status")
            return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]

        elif name == "hailo_list_models":
            r = await client.get(f"{PI_BASE}/api/models")
            return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]

        elif name == "hailo_capture_frame":
            overlay = arguments.get("overlay", True)
            r = await client.get(f"{PI_BASE}/api/frame", params={"overlay": overlay})
            b64 = base64.b64encode(r.content).decode()
            return [
                TextContent(type="text", text=f"Captured frame ({len(r.content)} bytes)"),
                ImageContent(type="image", mimeType="image/jpeg", data=b64),
            ]

        elif name == "hailo_run_inference":
            payload = {
                "model_path": arguments["model_path"],
                "threshold": arguments.get("threshold", 0.25),
            }
            r = await client.post(f"{PI_BASE}/api/inference", json=payload)
            data = r.json()

            result = [TextContent(type="text", text=json.dumps(data, indent=2))]

            if arguments.get("return_image") and data.get("success"):
                # Re-capture with overlay if possible
                r2 = await client.get(f"{PI_BASE}/api/frame", params={"overlay": True})
                b64 = base64.b64encode(r2.content).decode()
                result.append(ImageContent(type="image", mimeType="image/jpeg", data=b64))

            return result

        elif name == "hailo_activate_model":
            r = await client.post(f"{PI_BASE}/api/model/activate", json={
                "model_path": arguments["model_path"],
                "threshold": arguments.get("threshold", 0.25),
            })
            return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]

        elif name == "hailo_deactivate_model":
            r = await client.post(f"{PI_BASE}/api/model/deactivate")
            return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]

        elif name == "hailo_benchmark":
            r = await client.get(f"{PI_BASE}/api/benchmark/{arguments['model_name']}")
            return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]

        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="hailo-vision",
                server_version="0.2.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
