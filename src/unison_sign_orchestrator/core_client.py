from __future__ import annotations

import uuid
from typing import Optional

from .schemas import IntentRequest, ResponseEnvelope


class CoreOrchestratorClient:
    """
    Placeholder client for Phase 2.

    Later revisions will post to the real orchestrator API or event bus.
    """

    def __init__(self, host: str = "orchestrator", port: int = 8080):
        self.host = host
        self.port = port

    def send_intent(self, intent_req: IntentRequest) -> ResponseEnvelope:
        """
        Phase 2 stub: echo the intent as a ResponseEnvelope.
        """
        text = intent_req.intent.get("arguments", {}).get("text") or intent_req.intent.get("name", "")
        return ResponseEnvelope(
            request_id=str(uuid.uuid4()),
            text=text or intent_req.spoken_text,
            channel=intent_req.channel,
            subject_id=intent_req.subject_id,
            session_id=intent_req.session_id,
        )
