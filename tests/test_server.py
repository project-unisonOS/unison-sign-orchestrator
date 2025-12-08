from fastapi.testclient import TestClient

from unison_sign_orchestrator.server import _make_app


def test_handle_interpretation_endpoint():
    app = _make_app()
    client = TestClient(app)
    payload = {
        "language": "asl",
        "segment_id": "seg-1",
        "start_time_ms": 0,
        "end_time_ms": 1,
        "confidence": 0.9,
        "type": "utterance",
        "text": "open settings",
        "intent": {"name": "open_app", "arguments": {"app": "settings"}},
        "raw_gloss": ["OPEN", "SETTINGS"],
        "metadata": {"source": "test"},
    }
    resp = client.post("/sign/interpretation", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert data["intent_request"]["channel"] == "sign-asl"
    assert data["response"]["text"] == "open_app" or data["response"]["text"] == "open settings"
    assert data["signing_output"]["language"] == "asl"
