from fastapi.testclient import TestClient
import httpx
import json

from unison_sign_orchestrator.server import _make_app


def test_handle_interpretation_endpoint(monkeypatch):
    # mock core orchestrator response
    class FakeClient:
        def __enter__(self):  # noqa: D401
            return self

        def __exit__(self, exc_type, exc, tb):  # noqa: D401
            return False

        def post(self, url, json=None, **kwargs):
            class Resp:
                status_code = 200

                def json(self_inner):
                    return {"request_id": "abc", "text": "Opening settings.", "gloss": ["OPEN", "SETTINGS"]}

            return Resp()

    monkeypatch.setattr(httpx, "Client", lambda timeout=2.5: FakeClient())

    app = _make_app()
    client = TestClient(app)
    # readiness/health parity with other services
    assert client.get("/healthz").status_code == 200
    assert client.get("/readyz").status_code == 200
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
    assert data["response"]["text"] == "Opening settings."
    assert data["signing_output"]["language"] == "asl"
