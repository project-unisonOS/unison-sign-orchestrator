from __future__ import annotations

import uuid
from typing import Optional

import httpx

from .schemas import IntentRequest, ResponseEnvelope


class CoreOrchestratorClient:
    """
    Client to forward sign intents to the core orchestrator.
    """

    def __init__(self, host: str = "orchestrator", port: int = 8080, path: str = "/intent"):
        self.host = host
        self.port = port
        self.path = path

    def send_intent(self, intent_req: IntentRequest) -> ResponseEnvelope:
        """
        Post the intent to the orchestrator; fallback to echo if the call fails.
        """
        url = f"http://{self.host}:{self.port}{self.path}"
        payload = intent_req.to_dict()
        try:
            with httpx.Client(timeout=2.5) as client:
                resp = client.post(url, json=payload)
                if resp.status_code in (200, 201, 202):
                    data = resp.json()
                    text = data.get("text") or intent_req.spoken_text
                    gloss = data.get("gloss")
                    return ResponseEnvelope(
                        request_id=str(data.get("request_id", uuid.uuid4())),
                        text=text,
                        channel=intent_req.channel,
                        subject_id=intent_req.subject_id,
                        session_id=intent_req.session_id,
                        gloss=gloss,
                        metadata=data if isinstance(data, dict) else {},
                    )
        except Exception:
            pass
        # Fallback echo behavior
        text = intent_req.intent.get("arguments", {}).get("text") or intent_req.intent.get("name", "")
        return ResponseEnvelope(
            request_id=str(uuid.uuid4()),
            text=text or intent_req.spoken_text,
            channel=intent_req.channel,
            subject_id=intent_req.subject_id,
            session_id=intent_req.session_id,
        )
