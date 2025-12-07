from unison_sign_orchestrator.gateway import interpretation_to_intent_request, response_to_signing_output
from unison_sign_orchestrator.schemas import SignInterpretation


def _sample_interp():
    return SignInterpretation(
        language="asl",
        segment_id="seg-1",
        start_time_ms=0,
        end_time_ms=1,
        confidence=0.9,
        type="utterance",
        text="open settings",
        intent={"name": "open_app", "arguments": {"app": "settings"}},
        raw_gloss=["OPEN", "SETTINGS"],
        metadata={"source": "test"},
    )


def test_interpretation_to_intent_request_maps_fields():
    interp = _sample_interp()
    req = interpretation_to_intent_request(interp, subject_id="p1", session_id="s1", baton="b1")
    assert req.channel == "sign-asl"
    assert req.intent["name"] == "open_app"
    assert req.extra["raw_gloss"] == ["OPEN", "SETTINGS"]
    assert req.context_baton == "b1"
    assert req.spoken_text == "open settings"


def test_response_to_signing_output():
    output = response_to_signing_output("Opening settings.", language="asl", gloss=["OPENING", "SETTINGS"])
    assert output.language == "asl"
    assert output.text == "Opening settings."
    assert output.gloss == ["OPENING", "SETTINGS"]
