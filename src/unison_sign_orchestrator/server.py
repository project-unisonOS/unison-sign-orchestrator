from __future__ import annotations

import os
from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel

from .gateway import interpretation_to_intent_request, response_to_signing_output
from .schemas import SignInterpretation, IntentRequest, ResponseEnvelope
from .core_client import CoreOrchestratorClient


APP_NAME = "unison-sign-orchestrator"
DEFAULT_SUBJECT_ID = os.getenv("UNISON_DEFAULT_PERSON_ID", "local-user")


class SignInterpretationModel(BaseModel):
    language: str
    segment_id: str
    start_time_ms: int
    end_time_ms: int
    confidence: float
    type: str = "utterance"
    text: Optional[str] = None
    intent: Optional[dict] = None
    raw_gloss: Optional[list[str]] = None
    metadata: dict = {}

    def to_dataclass(self) -> SignInterpretation:
        return SignInterpretation(
            language=self.language,
            segment_id=self.segment_id,
            start_time_ms=self.start_time_ms,
            end_time_ms=self.end_time_ms,
            confidence=self.confidence,
            type=self.type,
            text=self.text,
            intent=self.intent,
            raw_gloss=self.raw_gloss,
            metadata=self.metadata,
        )


class IntentRequestModel(BaseModel):
    intent: dict
    spoken_text: str
    channel: str
    subject_id: str
    session_id: str
    context_baton: Optional[str] = None
    extra: dict = {}

    @classmethod
    def from_dataclass(cls, dc: IntentRequest) -> "IntentRequestModel":
        return cls(**dc.to_dict())


class ResponseEnvelopeModel(BaseModel):
    request_id: str
    text: str
    channel: str
    subject_id: str
    session_id: str
    gloss: Optional[list[str]] = None
    metadata: dict = {}
    created_ms: int

    @classmethod
    def from_dataclass(cls, dc: ResponseEnvelope) -> "ResponseEnvelopeModel":
        return cls(**dc.to_dict())


class SigningOutputModel(BaseModel):
    language: str
    text: str
    gloss: Optional[list[str]] = None
    avatar_instructions: dict


def _make_app() -> FastAPI:
    app = FastAPI(title=APP_NAME)
    core_client = CoreOrchestratorClient(
        host=os.getenv("UNISON_ORCH_HOST", "orchestrator"),
        port=int(os.getenv("UNISON_ORCH_PORT", "8080")),
        path=os.getenv("UNISON_ORCH_INTENT_PATH", "/intent"),
    )

    @app.get("/health")
    @app.get("/healthz")
    def health():
        return {"status": "ok", "service": APP_NAME}

    @app.get("/ready")
    @app.get("/readyz")
    def ready():
        return {"ready": True}

    @app.post("/sign/interpretation")
    def handle_interpretation(
        interpretation: SignInterpretationModel,
        subject_id: str = DEFAULT_SUBJECT_ID,
        session_id: str = "local-session",
        baton: Optional[str] = None,
    ):
        dc_interp = interpretation.to_dataclass()
        intent_req = interpretation_to_intent_request(dc_interp, subject_id=subject_id, session_id=session_id, baton=baton)
        response = core_client.send_intent(intent_req)
        signing_output = response_to_signing_output(response.text, language=dc_interp.language, gloss=response.gloss)
        return {
            "ok": True,
            "intent_request": IntentRequestModel.from_dataclass(intent_req),
            "response": ResponseEnvelopeModel.from_dataclass(response),
            "signing_output": SigningOutputModel(**signing_output.to_dict()),
        }

    return app


app = _make_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8087)
