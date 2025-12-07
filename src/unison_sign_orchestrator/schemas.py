"""
Dataclasses for the sign orchestrator gateway.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import time

JsonDict = Dict[str, Any]


def _now_ms() -> int:
    return int(time.time() * 1000)


@dataclass
class SignInterpretation:
    language: str
    segment_id: str
    start_time_ms: int
    end_time_ms: int
    confidence: float
    type: str = "utterance"
    text: Optional[str] = None
    intent: Optional[JsonDict] = None
    raw_gloss: Optional[List[str]] = None
    metadata: JsonDict = field(default_factory=dict)

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class IntentRequest:
    intent: JsonDict
    spoken_text: str
    channel: str
    subject_id: str
    session_id: str
    context_baton: Optional[str] = None
    extra: JsonDict = field(default_factory=dict)

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class AvatarInstructions:
    version: str = "1.0"
    rig: str = "default_humanoid"
    keyframes: List[JsonDict] = field(default_factory=list)

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class SigningOutput:
    language: str
    text: str
    gloss: Optional[List[str]] = None
    avatar_instructions: AvatarInstructions = field(default_factory=AvatarInstructions)

    def to_dict(self) -> JsonDict:
        data = asdict(self)
        data["avatar_instructions"] = self.avatar_instructions.to_dict()
        return data


@dataclass
class ResponseEnvelope:
    request_id: str
    text: str
    channel: str
    subject_id: str
    session_id: str
    gloss: Optional[List[str]] = None
    metadata: JsonDict = field(default_factory=dict)
    created_ms: int = field(default_factory=_now_ms)

    def to_dict(self) -> JsonDict:
        return asdict(self)
