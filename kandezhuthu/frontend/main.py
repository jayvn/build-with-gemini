"""FastAPI proxy and web server for Kandezhuthu AI.

Supports both:
1. Local Development Mode (Default): Runs directly with ADK Runner and InMemorySessionService.
2. Cloud Deployed Mode: When AGENT_ENGINE_RESOURCE_NAME is set, proxies to Agent Engine via A2A protocol.
"""

import os
import sys
import uuid
from typing import Optional

# Ensure parent directory is in pythonpath
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()

app = FastAPI(title="Kandezhuthu AI Web UI")

RESOURCE = os.environ.get("AGENT_ENGINE_RESOURCE_NAME")
LOCAL_MODE = not bool(RESOURCE)

if LOCAL_MODE:
    print("[Kandezhuthu UI] Starting in LOCAL DIRECT MODE (In-memory ADK Runner)")
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types
    from app.agent import root_agent

    _session_service = InMemorySessionService()
    _runner = Runner(agent=root_agent, session_service=_session_service, app_name="kandezhuthu")
    _user_sessions: dict[str, str] = {}
else:
    print(f"[Kandezhuthu UI] Starting in CLOUD A2A PROXY MODE for {RESOURCE}")
    import google.auth
    import google.auth.transport.requests
    import httpx
    from a2a.client import ClientConfig, ClientFactory
    from a2a.types import (
        AgentCard,
        FilePart,
        Message,
        Part,
        Role,
        TaskArtifactUpdateEvent,
        TextPart,
        TransportProtocol,
    )

    AGENT_DIRECTORY = os.environ.get("AGENT_DIRECTORY", "app")
    LOCATION = RESOURCE.split("/locations/")[1].split("/")[0]
    A2A_BASE = (
        f"https://{LOCATION}-aiplatform.googleapis.com/reasoningEngines/v1/"
        f"{RESOURCE}/api/a2a/{AGENT_DIRECTORY}"
    )
    A2A_CARD_URL = f"{A2A_BASE}/.well-known/agent-card.json"
    _A2UI_MIME = "application/json+a2ui"
    _creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    _contexts: dict[str, str] = {}
    _card: Optional[AgentCard] = None

    def _auth_headers() -> dict[str, str]:
        _creds.refresh(google.auth.transport.requests.Request())
        return {
            "Authorization": f"Bearer {_creds.token}",
            "Content-Type": "application/json",
        }

    async def _get_card(client: httpx.AsyncClient) -> AgentCard:
        global _card
        if _card is None:
            resp = await client.get(A2A_CARD_URL)
            resp.raise_for_status()
            card = AgentCard(**resp.json())
            card.url = A2A_BASE
            _card = card
        return _card

    def _extract_parts(parts: list) -> list[dict]:
        out: list[dict] = []
        for p in parts:
            root = getattr(p, "root", p)
            if isinstance(root, TextPart) and getattr(root, "text", None):
                out.append({"kind": "text", "text": root.text})
            elif getattr(root, "data", None) is not None:
                meta = getattr(root, "metadata", None) or {}
                mime = meta.get("mimeType") if isinstance(meta, dict) else None
                if mime == _A2UI_MIME:
                    out.append({"kind": "a2ui", "data": root.data})
            elif isinstance(root, FilePart):
                uri = getattr(getattr(root, "file", None), "uri", None)
                if uri:
                    out.append({"kind": "text", "text": uri})
        return out


@app.exception_handler(Exception)
async def _json_errors(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200,
        content={"parts": [{"kind": "text", "text": f"Error: {type(exc).__name__}: {exc}"}]},
    )


@app.get("/api/config")
async def get_config():
    return {
        "google_maps_api_key": os.environ.get("GOOGLE_MAPS_API_KEY", "") or os.environ.get("VITE_GOOGLE_MAPS_API_KEY", "")
    }


@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    message = body.get("message", "")
    user_id = body.get("user_id") or "kandezhuthu-user"
    parts: list[dict] = []

    if LOCAL_MODE:
        session_id = _user_sessions.get(user_id)
        if not session_id:
            session = _session_service.create_session_sync(user_id=user_id, app_name="kandezhuthu")
            session_id = session.id
            _user_sessions[user_id] = session_id

        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=message)],
        )

        reply_chunks = []
        events = _runner.run(
            new_message=content,
            user_id=user_id,
            session_id=session_id,
        )

        for event in events:
            if event.content and event.content.parts:
                for p in event.content.parts:
                    if getattr(p, "text", None):
                        reply_chunks.append(p.text)

        full_text = "".join(reply_chunks)
        if full_text:
            parts.append({"kind": "text", "text": full_text})
    else:
        async with httpx.AsyncClient(headers=_auth_headers(), timeout=120) as client:
            card = await _get_card(client)
            factory = ClientFactory(
                ClientConfig(
                    supported_transports=[TransportProtocol.jsonrpc, TransportProtocol.http_json],
                    httpx_client=client,
                )
            )
            a2a_client = factory.create(card)
            msg = Message(
                message_id=str(uuid.uuid4()),
                role=Role.user,
                parts=[Part(root=TextPart(text=message))],
                context_id=_contexts.get(user_id),
            )
            last_task = None
            got_artifact_update = False
            async for event in a2a_client.send_message(msg):
                if not isinstance(event, tuple):
                    continue
                task, update = event
                if task is not None:
                    last_task = task
                    if getattr(task, "context_id", None):
                        _contexts[user_id] = task.context_id
                if isinstance(update, TaskArtifactUpdateEvent):
                    got_artifact_update = True
                    parts.extend(_extract_parts(update.artifact.parts))

            if not got_artifact_update and last_task is not None:
                for artifact in getattr(last_task, "artifacts", None) or []:
                    parts.extend(_extract_parts(artifact.parts))

    if not parts:
        parts = [{"kind": "text", "text": "(No reply was returned by the auditor agent.)"}]
    return JSONResponse({"parts": parts})


# Mount static assets
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    print(f"Server starting on http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
