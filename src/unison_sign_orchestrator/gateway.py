"""
Gateway helpers that adapt sign interpretations into canonical IntentRequests.
"""

from __future__ import annotations

from typing import Optional

from .schemas import IntentRequest, SignInterpretation, SigningOutput


def interpretation_to_intent_request(
    interpretation: SignInterpretation,
    subject_id: str,
    session_id: str,
    baton: Optional[str] = None,
    channel_prefix: str = "sign",
) -> IntentRequest:
    if not interpretation.intent:
        # Fallback intent shape when upstream model only returns text.
        intent_payload = {"name": "message.freeform", "arguments": {"text": interpretation.text or ""}}
    else:
        intent_payload = interpretation.intent
    channel = f"{channel_prefix}-{interpretation.language}"
    extra = {"raw_gloss": interpretation.raw_gloss or [], "metadata": interpretation.metadata or {}}
    return IntentRequest(
        intent=intent_payload,
        spoken_text=interpretation.text or "",
        channel=channel,
        subject_id=subject_id,
        session_id=session_id,
        context_baton=baton,
        extra=extra,
    )


def response_to_signing_output(response_text: str, language: str, gloss: Optional[list[str]] = None) -> SigningOutput:
    """
    Minimal adapter to pass orchestrator text back to a signing avatar/captions path.
    """
    return SigningOutput(language=language, text=response_text, gloss=gloss or [])
