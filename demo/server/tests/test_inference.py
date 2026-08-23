"""Smoke tests for the inference API.

Run from the repo root:
    pytest server/tests/test_inference.py

These boot the app via FastAPI's TestClient (triggers startup model load).
They pass without a trained checkpoint — the model runs on random-init weights,
which still yields a valid softmax. They assert *shape/behaviour*, not accuracy.
"""

from __future__ import annotations

import io

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from server.app.main import app


def _synthetic_fundus(size: int = 600) -> bytes:
    """Make a fundus-like image (bright disc on black) so FOV crop succeeds."""
    yy, xx = np.mgrid[0:size, 0:size]
    cx = cy = size / 2
    r = size * 0.45
    disc = ((xx - cx) ** 2 + (yy - cy) ** 2) <= r ** 2
    img = np.zeros((size, size, 3), dtype=np.uint8)
    img[disc] = (180, 90, 40)  # warm retina-ish tone
    buf = io.BytesIO()
    Image.fromarray(img, "RGB").save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


def test_health(client: TestClient) -> None:
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["model"] == "config-D"
    assert "checkpoint_loaded" in body
    # Provenance fields for the demo footer (§D.7).
    assert "version" in body and "git_sha" in body


def test_predict_left_only(client: TestClient) -> None:
    r = client.post("/api/predict", files={"left": ("left.png", _synthetic_fundus(), "image/png")})
    assert r.status_code == 200, r.text
    body = r.json()
    assert len(body["probs"]) == 5
    assert abs(sum(body["probs"]) - 1.0) < 1e-3
    assert 0 <= body["pred"] <= 4
    assert len(body["per_eye"]) == 1


def test_predict_both_eyes(client: TestClient) -> None:
    files = {
        "left": ("left.png", _synthetic_fundus(), "image/png"),
        "right": ("right.png", _synthetic_fundus(), "image/png"),
    }
    r = client.post("/api/predict", files=files)
    assert r.status_code == 200, r.text
    body = r.json()
    assert len(body["per_eye"]) == 2
    assert body["pred"] == max(e["pred"] for e in body["per_eye"])


def test_predict_rejects_non_image(client: TestClient) -> None:
    # text/plain is rejected by the MIME gate (415); a mislabeled image would
    # be caught by the decoder (400). Either is an acceptable rejection.
    r = client.post("/api/predict", files={"left": ("note.txt", b"not an image", "text/plain")})
    assert r.status_code in (400, 415)


def test_predict_requires_an_eye(client: TestClient) -> None:
    r = client.post("/api/predict")
    assert r.status_code == 400


def test_gradcam(client: TestClient) -> None:
    r = client.post(
        "/api/gradcam",
        data={"eye": "left"},
        files={"image": ("left.png", _synthetic_fundus(), "image/png")},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["gradcam_png_b64"] and body["attention_overlay_png_b64"]
    assert 0 <= body["target_class"] <= 4


def test_visualize(client: TestClient) -> None:
    r = client.post(
        "/api/visualize",
        data={"eye": "left"},
        files={"image": ("left.png", _synthetic_fundus(), "image/png")},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["preview_png_b64"] and body["fov_mask_png_b64"]
    assert body["fov_base_png_b64"]  # analysis-space base for mask/marker overlay
    assert "confident" in body["od_fovea"]
    # OD/fovea coords are in the square analysis frame (no flip to undo).
    assert body["od_fovea"]["space_w"] == body["od_fovea"]["space_h"]
    assert body["od_fovea"]["flipped"] is False


def test_selftest(client: TestClient) -> None:
    r = client.get("/api/selftest")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["predict"] == "pass"
    assert body["gradcam"] == "pass"
    assert body["visualize"] == "pass"


def test_health_reports_password_requirement(client: TestClient) -> None:
    # §C.2/D: the frontend reads this flag to decide whether to show the gate.
    body = client.get("/api/health").json()
    assert isinstance(body.get("requires_password"), bool)


def test_gradcam_emits_rationale(client: TestClient) -> None:
    # §D.3: a one-line predicted-class rationale + the CAM stats behind it.
    r = client.post(
        "/api/gradcam",
        data={"eye": "left"},
        files={"image": ("left.png", _synthetic_fundus(), "image/png")},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert isinstance(body["rationale"], str) and body["rationale"]
    assert f"grade {body['target_class']}" in body["rationale"]
    assert body["cam_pixel_count"] >= 0
    assert 0.0 <= body["cam_area_frac"] <= 1.0
    assert body["cam_region"]


def test_case_records_the_whole_session(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    """A case collects originals, stages, attention, prediction and the verdict."""
    from server.app import cases, config, main

    monkeypatch.setattr(config.settings, "cases_dir", tmp_path)
    monkeypatch.setattr(main.settings, "cases_dir", tmp_path)

    image = _synthetic_fundus()
    opened = client.post(
        "/api/case/image",
        data={"eye": "right", "is_fundus": "true", "laterality": "right",
              "laterality_confidence": "0.71", "source": "upload"},
        files={"image": ("right.png", image, "image/png")},
    )
    assert opened.status_code == 200, opened.text
    case_id = opened.json()["case_id"]
    assert opened.json()["stored"] is True
    assert cases.is_valid_case_id(case_id)
    assert (tmp_path / case_id / "original" / "right.png").read_bytes() == image
    assert (tmp_path / case_id / "case.txt").exists()

    # The second eye joins the SAME case rather than opening another one.
    second = client.post(
        "/api/case/image",
        data={"eye": "left", "case_id": case_id, "is_fundus": "true"},
        files={"image": ("left.png", image, "image/png")},
    )
    assert second.json()["case_id"] == case_id

    for endpoint in ("/api/visualize", "/api/gradcam"):
        r = client.post(
            endpoint,
            data={"eye": "right", "case_id": case_id},
            files={"image": ("right.png", image, "image/png")},
        )
        assert r.status_code == 200, r.text

    predicted = client.post(
        "/api/predict",
        data={"case_id": case_id},
        files={"right": ("right.png", image, "image/png")},
    )
    assert predicted.status_code == 200, predicted.text
    grade = predicted.json()["pred"]

    verdict = client.post(
        f"/api/case/{case_id}/feedback",
        data={"verdict": "rejected", "corrected_grade": "3", "predicted_grade": str(grade)},
    )
    assert verdict.status_code == 200, verdict.text
    assert verdict.json()["stored"] is True

    record = client.get(f"/api/case/{case_id}").json()
    assert set(record["images"]) == {"left", "right"}
    assert record["images"]["right"]["client_checks"]["laterality"] == "right"
    assert record["detection"]["right"]["space_w"] > 0
    assert record["preprocessing"]["right"]["stage_count"] > 0
    assert record["attention"]["right"]["files"]
    assert len(record["predictions"]) == 1
    assert record["feedback"][0]["verdict"] == "rejected"
    assert record["feedback"][0]["corrected_grade"] == 3

    # Cached artifacts are real files, and case.txt reflects the final state.
    stage_dir = tmp_path / case_id / "preprocessing" / "right"
    assert list(stage_dir.glob("*.png"))
    assert (stage_dir / "input_channels" / "ch_fov.png").exists()
    assert (tmp_path / case_id / "attention" / "right_attention_overlay.png").exists()
    report = (tmp_path / case_id / "case.txt").read_text(encoding="utf-8")
    assert case_id in report
    assert "REJECTED" in report
    assert "Severe NPDR" in report


def test_verdict_can_be_retracted_and_leaves_no_trace(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    """Undoing a verdict removes it from the record and from the statistics."""
    from server.app import config, main

    monkeypatch.setattr(config.settings, "cases_dir", tmp_path)
    monkeypatch.setattr(main.settings, "cases_dir", tmp_path)

    image = _synthetic_fundus()
    case_id = client.post(
        "/api/case/image", data={"eye": "left"},
        files={"image": ("left.png", image, "image/png")},
    ).json()["case_id"]

    client.post(f"/api/case/{case_id}/feedback",
                data={"verdict": "rejected", "corrected_grade": "3", "predicted_grade": "1"})
    assert client.get("/api/cases/stats").json()["verdicts"] == 1

    undone = client.request("DELETE", f"/api/case/{case_id}/feedback")
    assert undone.status_code == 200, undone.text
    assert undone.json()["retracted"] is True
    assert undone.json()["corrected_grade"] == 3

    record = client.get(f"/api/case/{case_id}").json()
    assert record["feedback"] == []
    report = (tmp_path / case_id / "case.txt").read_text(encoding="utf-8")
    assert "REJECTED" not in report

    stats = client.get("/api/cases/stats").json()
    assert stats["verdicts"] == 0 and stats["rejected"] == 0
    assert stats["reviewed_patients"] == 0 and stats["agreement"] is None
    assert stats["grades"] == [0, 0, 0, 0, 0]

    # Nothing left to withdraw → reported, not an error.
    again = client.request("DELETE", f"/api/case/{case_id}/feedback")
    assert again.status_code == 200 and again.json()["retracted"] is False


def test_case_stats_aggregate_the_store(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    """Statistics count patients across cases and survive an empty browser buffer."""
    from server.app import config, main

    monkeypatch.setattr(config.settings, "cases_dir", tmp_path)
    monkeypatch.setattr(main.settings, "cases_dir", tmp_path)

    assert client.get("/api/cases/stats").json()["patients"] == 0

    image = _synthetic_fundus()
    grades = {"rejected": 4, "confirmed": 0}
    for verdict, grade in grades.items():
        case_id = client.post(
            "/api/case/image", data={"eye": "right"},
            files={"image": ("right.png", image, "image/png")},
        ).json()["case_id"]
        client.post("/api/predict", data={"case_id": case_id},
                    files={"right": ("right.png", image, "image/png")})
        client.post(f"/api/case/{case_id}/feedback",
                    data={"verdict": verdict, "corrected_grade": str(grade)})

    stats = client.get("/api/cases/stats").json()
    assert stats["patients"] == 2
    assert stats["images"] == 2
    assert stats["predictions"] == 2
    assert stats["verdicts"] == 2 and stats["reviewed_patients"] == 2
    assert stats["confirmed"] == 1 and stats["rejected"] == 1
    assert stats["agreement"] == 0.5
    assert stats["grades"] == [1, 0, 0, 0, 1]
    assert stats["last_activity_utc"]


def test_case_verdicts_rebuild_the_relabeling_buffer(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    """The buffer is read back from the store, so a reload cannot empty it."""
    from server.app import config, main

    monkeypatch.setattr(config.settings, "cases_dir", tmp_path)
    monkeypatch.setattr(main.settings, "cases_dir", tmp_path)

    empty = client.get("/api/cases/verdicts").json()
    assert empty["entries"] == [] and empty["total"] == 0

    image = _synthetic_fundus()
    case_id = client.post(
        "/api/case/image", data={"eye": "right"},
        files={"image": ("right.png", image, "image/png")},
    ).json()["case_id"]
    client.post("/api/predict", data={"case_id": case_id},
                files={"right": ("right.png", image, "image/png")})
    client.post(f"/api/case/{case_id}/feedback",
                data={"verdict": "rejected", "corrected_grade": "3"})

    payload = client.get("/api/cases/verdicts").json()
    assert payload["total"] == 1
    row = payload["entries"][0]
    # The row carries what the buffer table shows and the JSONL export writes.
    assert row["id"] == f"{case_id}#1" and row["case_id"] == case_id
    assert row["verdict"] == "rejected" and row["corrected_grade"] == 3
    assert row["predicted"] is not None and len(row["probs"]) == 5
    assert row["images"] == [{"eye": "right", "source": "right.png"}]
    assert row["timestamp"]

    # A withdrawn verdict leaves the buffer as well — it is the same record.
    client.request("DELETE", f"/api/case/{case_id}/feedback")
    assert client.get("/api/cases/verdicts").json()["total"] == 0


def test_case_refuses_a_non_fundus_image(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    """The store holds patients: an image the client check rejected is not filed."""
    from server.app import config, main

    monkeypatch.setattr(config.settings, "cases_dir", tmp_path)
    monkeypatch.setattr(main.settings, "cases_dir", tmp_path)

    r = client.post(
        "/api/case/image",
        data={"eye": "left", "is_fundus": "false"},
        files={"image": ("left.png", _synthetic_fundus(), "image/png")},
    )
    assert r.status_code == 200, r.text
    assert r.json()["stored"] is False and r.json()["case_id"] == ""
    assert not list(tmp_path.iterdir())


def test_case_rejects_bad_ids_and_verdicts(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    """Case ids come from the client, so malformed ones must never touch disk."""
    from server.app import config, main

    monkeypatch.setattr(config.settings, "cases_dir", tmp_path)
    monkeypatch.setattr(main.settings, "cases_dir", tmp_path)

    assert client.get("/api/case/../../etc").status_code in (404, 400)
    assert client.get("/api/case/case_20260101T000000Z_deadbeef").status_code == 404

    opened = client.post(
        "/api/case/image",
        data={"eye": "left"},
        files={"image": ("left.png", _synthetic_fundus(), "image/png")},
    )
    case_id = opened.json()["case_id"]
    bad_verdict = client.post(
        f"/api/case/{case_id}/feedback", data={"verdict": "maybe", "corrected_grade": "1"}
    )
    assert bad_verdict.status_code == 400
    bad_grade = client.post(
        f"/api/case/{case_id}/feedback", data={"verdict": "confirmed", "corrected_grade": "9"}
    )
    assert bad_grade.status_code == 400

    # A stale/unknown case id on an inference call is ignored, not an error.
    ok = client.post(
        "/api/predict",
        data={"case_id": "case_20200101T000000Z_00000000"},
        files={"left": ("left.png", _synthetic_fundus(), "image/png")},
    )
    assert ok.status_code == 200


def test_auth_open_when_no_password(client: TestClient) -> None:
    # With DEMO_PASSWORD unset (default in tests) the gate is open.
    r = client.post("/api/auth")
    assert r.status_code == 200, r.text
    assert r.json()["ok"] is True


def test_password_gate_enforced(monkeypatch: pytest.MonkeyPatch) -> None:
    # When DEMO_PASSWORD is set: wrong/absent password → 401, correct → 200,
    # and /api/health advertises the requirement.
    from server.app import config, security

    monkeypatch.setattr(config.settings, "demo_password", "s3cret")
    monkeypatch.setattr(security.settings, "demo_password", "s3cret")
    with TestClient(app) as c:
        assert c.get("/api/health").json()["requires_password"] is True
        assert c.post("/api/auth").status_code == 401
        assert c.post("/api/auth", data={"password": "wrong"}).status_code == 401
        ok = c.post("/api/auth", data={"password": "s3cret"})
        assert ok.status_code == 200 and ok.json()["ok"] is True
        # A protected endpoint rejects a missing password too.
        denied = c.post(
            "/api/gradcam",
            data={"eye": "left"},
            files={"image": ("left.png", _synthetic_fundus(), "image/png")},
        )
        assert denied.status_code == 401
