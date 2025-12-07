# unison-sign-orchestrator

Modality gateway for sign-language interaction in UnisonOS. It adapts `SignInterpretation` events into canonical `IntentRequest` objects, sends them to the core orchestrator, and routes responses to the signing avatar and shell captions. Policy and skills remain in the core orchestrator.

## Status
Phase 0 scaffolding — schemas, gateway adapter stub, tests. No runtime server yet.

## Layout
- `src/unison_sign_orchestrator/schemas.py` — SignInterpretation/IntentRequest/ResponseEnvelope dataclasses.
- `src/unison_sign_orchestrator/gateway.py` — adapter for mapping interpretations to intent requests.
- `tests/` — unit tests for mapping and schema serialization.

## Quickstart (dev)
```bash
cd unison-sign-orchestrator
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest
```

## Notes
- The gateway intentionally omits policy/skills logic; it only adapts sign data and defers decisions to the existing core orchestrator.
- Future phases will add FastAPI wiring, bus/client integration, clarification prompts, and telemetry.
