from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from openai import AzureOpenAI

load_dotenv()

app = FastAPI(title="Trip Planning Expert")

BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = BASE_DIR / "index.html"


def get_azure_settings() -> dict[str, str]:
    """Load required Azure OpenAI settings without exposing the key in errors."""
    settings = {
        "AZURE_ENDPOINT": os.getenv("AZURE_ENDPOINT", "").strip(),
        "AZURE_DEPLOYMENT": os.getenv("AZURE_DEPLOYMENT", "").strip(),
        "AZURE_API_KEY": os.getenv("AZURE_API_KEY", "").strip(),
    }

    missing = [name for name, value in settings.items() if not value]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

    return settings


def build_client() -> tuple[AzureOpenAI, str]:
    settings = get_azure_settings()
    deployment = settings["AZURE_DEPLOYMENT"]

    client = AzureOpenAI(
        azure_endpoint=settings["AZURE_ENDPOINT"].rstrip("/"),
        api_key=settings["AZURE_API_KEY"],
        api_version="2024-10-21",
    )

    return client, deployment


@app.get("/", response_class=HTMLResponse)
async def serve_index() -> str:
    return INDEX_PATH.read_text(encoding="utf-8")


@app.post("/chat")
async def chat(payload: dict[str, Any]) -> dict[str, str]:
    messages = payload.get("messages")
    if not isinstance(messages, list):
        raise HTTPException(status_code=400, detail="Request body must include a 'messages' array.")

    try:
        get_azure_settings()
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    system_message = {
        "role": "system",
        "content": (
            "You are a knowledgeable trip-planning expert. Help with destinations, itineraries, "
            "budgets, flights, trains, lodging, packing lists, travel timing, local tips, and safety. "
            "Keep recommendations practical and clear, and ask clarifying questions when needed. "
            "Always encourage verifying current travel details with official sources before booking."
        ),
    }

    chat_history = [system_message, *messages]

    try:
        client, deployment = build_client()
        response = client.chat.completions.create(
            model=deployment,
            messages=chat_history,
            temperature=0.7,
            max_tokens=700,
        )

        reply = response.choices[0].message.content
        if not reply:
            reply = "I can help plan the trip. Tell me your destination, travel dates, and budget."

        return {"reply": reply}
    except Exception as exc:  # pragma: no cover - safety layer for API errors
        message = str(exc)
        lowered = message.lower()
        if "api_key" in lowered or "authentication" in lowered or "unauthorized" in lowered:
            message = "Azure authentication failed. Check the configured Azure credentials."
        raise HTTPException(status_code=502, detail=message) from exc
