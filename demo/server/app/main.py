"""FastAPI app: endpoints + startup model load.

Run locally:
    uvicorn server.app.main:app --reload --port 8000
"""

from __future__ import annotations

import asyncio

from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from . import cases as cases_mod
from . import corrections as corrections_mod
from . import gradcam as gradcam_mod
from . import imaging
from . import visualize as visualize_mod
from .config import settings
from .inference import engine
from .schemas import (
    AuthResponse,
    CaseFeedbackResponse,
    CaseFeedbackRetractResponse,
    CaseImageResponse,
    CaseStatsResponse,
    GradcamResponse,
    HealthResponse,
    ODFoveaCorrectionResponse,
    PatientPredictionResponse,
    SelftestResponse,
    VisualizeResponse,
)
from .security import check_password, password_required

app = FastAPI(title="DR-Classifier Demo API", version=settings.resolve_version())

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single CUDA stream → serialize predictions to avoid races on one GPU.
_predict_lock = asyncio.Lock()

# Map imaging-layer exceptions to HTTP status codes (TASK-Demo §C.4).
_IMAGING_STATUS = {
    imaging.PayloadTooLarge: 413,
    imaging.UnsupportedMedia: 415,
    imaging.BadImage: 400,
}


def _http_from_imaging(exc: Exception) -> HTTPException:
    """Translate an imaging exception into an HTTPException."""
    for cls, status in _IMAGING_STATUS.items():
        if isinstance(exc, cls):
            return HTTPException(status_code=status, detail=str(exc))
    return HTTPException(status_code=400, detail=str(exc))


def _require_password(password: str | None) -> None:
    """Enforce the shared-password gate (TASK-Demo §C.2)."""
    if not check_password(password):
        raise HTTPException(status_code=401, detail="Access denied — invalid password.")


async def _read_validated(upload: UploadFile) -> bytes:
    """Read an upload and validate MIME + size before decoding.

    Args:
        upload: The incoming file.

    Returns:
        The raw bytes.

    Raises:
        HTTPException: 413/415 on limit violations.
    """
    data = await upload.read()
    try:
        imaging.check_upload(upload.content_type, len(data))
    except (imaging.PayloadTooLarge, imaging.UnsupportedMedia) as exc:
        raise _http_from_imaging(exc) from exc
    return data


def _model_provenance() -> dict:
    """Serving-model provenance stamped into every new case record."""
    return {
        "model": "config-D (full pipeline + EfficientNet-B3)",
        "checkpoint": settings.checkpoint_id,
        "checkpoint_loaded": engine.checkpoint_loaded,
        "in_channels": settings.in_channels,
        "preset": settings.preset,
        "device": str(engine.device),
        "version": settings.resolve_version(),
        "git_sha": settings.resolve_git_sha(),
    }


def _case_write(action: str, fn, *args, **kwargs):
    """Run a case-store write, downgrading any failure to a warning.

    The case store is a record, never a dependency: a full disk or a case
    directory deleted mid-session must not fail a prediction the clinician is
    waiting on. Returns the callee's result, or ``None`` if it failed.
    """
    try:
        return fn(*args, **kwargs)
    except (OSError, ValueError) as exc:
        print(f"[WARN] case store: could not {action}: {exc}")
        return None


def _active_case(case_id: str | None) -> str | None:
    """Return ``case_id`` when it names an existing case on disk, else ``None``.

    Every artifact-producing endpoint takes an optional ``case_id``; an absent,
    malformed or stale one simply means "do not file this run anywhere".
    """
    return case_id if cases_mod.case_exists(settings.cases_dir, case_id) else None


@app.on_event("startup")
async def _startup() -> None:
    """Load the model once when the server boots."""
    engine.load()
    if not engine.checkpoint_loaded:
        print(f"[WARN] checkpoint not found at {settings.checkpoint_path} — "
              "predictions use random-init weights until one is provided.")
    if not engine.using_dataset_stats:
        print(f"[WARN] norm stats not found at {settings.norm_stats_path} — "
              "Stage 7 falls back to ImageNet (preprocessing drift vs Config D).")


@app.get("/api/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Liveness + provenance for the frontend badge/footer."""
    return HealthResponse(
        status="ok",
        model="config-D",
        checkpoint=settings.checkpoint_id,
        checkpoint_loaded=engine.checkpoint_loaded,
        device=str(engine.device),
        version=settings.resolve_version(),
        git_sha=settings.resolve_git_sha(),
        requires_password=password_required(),
    )


@app.post("/api/auth", response_model=AuthResponse)
async def auth(password: str | None = Form(default=None)) -> AuthResponse:
    """Validate the shared password for the frontend access screen (§C.2).

    Returns ``{ "ok": true }`` when the gate is open or the password matches;
    raises 401 otherwise. Stateless — the frontend re-sends the password on
    every protected request regardless.
    """
    _require_password(password)
    return AuthResponse(ok=True)


@app.post("/api/predict", response_model=PatientPredictionResponse)
async def predict(
    left: UploadFile | None = File(default=None),
    right: UploadFile | None = File(default=None),
    password: str | None = Form(default=None),
    case_id: str | None = Form(default=None),
) -> PatientPredictionResponse:
    """Predict DR grade for one or both eyes (worst-eye patient grade).

    When ``case_id`` names an open patient case, the run (grades, probabilities,
    per-eye breakdown, latency) is appended to that case's record.
    """
    _require_password(password)
    if left is None and right is None:
        raise HTTPException(status_code=400, detail="Provide at least one of left/right.")

    left_bytes = await _read_validated(left) if left is not None else None
    right_bytes = await _read_validated(right) if right is not None else None

    try:
        async with _predict_lock:
            result = engine.predict_patient(left_bytes, right_bytes)
    except (imaging.BadImage, imaging.PayloadTooLarge, imaging.UnsupportedMedia) as exc:
        raise _http_from_imaging(exc) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    cid = _active_case(case_id)
    if cid:
        _case_write("save prediction", cases_mod.save_prediction,
                    settings.cases_dir, cid, result.model_dump())
    return result


@app.post("/api/gradcam", response_model=GradcamResponse)
async def gradcam(
    image: UploadFile = File(...),
    eye: str = Form(default="left"),
    password: str | None = Form(default=None),
    target_class: int | None = Form(default=None),
    case_id: str | None = Form(default=None),
) -> GradcamResponse:
    """Grad-CAM overlay for one eye, computed on the live checkpoint.

    When ``case_id`` names an open patient case, the heatmap and the attention
    overlay are written into it alongside the CAM statistics behind the rationale.
    """
    _require_password(password)
    data = await _read_validated(image)
    try:
        async with _predict_lock:
            payload = gradcam_mod.compute_gradcam(engine, data, eye, target_class)
    except (imaging.BadImage, imaging.PayloadTooLarge) as exc:
        raise _http_from_imaging(exc) from exc

    cid = _active_case(case_id)
    if cid:
        _case_write("save attention map", cases_mod.save_attention,
                    settings.cases_dir, cid, eye, payload)
    return GradcamResponse(**payload)


@app.post("/api/visualize", response_model=VisualizeResponse)
async def visualize(
    image: UploadFile = File(...),
    eye: str = Form(default="left"),
    password: str | None = Form(default=None),
    case_id: str | None = Form(default=None),
) -> VisualizeResponse:
    """preview strip + FOV mask + OD/fovea payload for one image.

    When ``case_id`` names an open patient case, every stage image is cached
    into it (plus the final stage's channel split — the CNN input tensor) and the
    OD/fovea detection is recorded.
    """
    _require_password(password)
    data = await _read_validated(image)
    try:
        payload = visualize_mod.compute_visualization(engine, data, eye)
    except (imaging.BadImage, imaging.PayloadTooLarge) as exc:
        raise _http_from_imaging(exc) from exc

    cid = _active_case(case_id)
    if cid:
        _case_write("cache preprocessing stages", cases_mod.save_preprocessing,
                    settings.cases_dir, cid, eye, payload)
    return VisualizeResponse(**payload)


_MIME_EXT = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}


@app.post("/api/od_fovea/correct", response_model=ODFoveaCorrectionResponse)
async def od_fovea_correct(
    image: UploadFile = File(...),
    eye: str = Form(default="left"),
    od_x: float = Form(...),
    od_y: float = Form(...),
    fovea_x: float = Form(...),
    fovea_y: float = Form(...),
    od_confidence: float = Form(default=0.0),
    fovea_confidence: float = Form(default=0.0),
    notes: str | None = Form(default=None),
    reviewer: str | None = Form(default=None),
    password: str | None = Form(default=None),
    case_id: str | None = Form(default=None),
) -> ODFoveaCorrectionResponse:
    """Persist a clinician OD/fovea correction and re-run the pipeline.

    Corrected centres arrive in the flipped (pre-rotation) frame, where the
    detection slide is edited. They redefine the Stage-1 rotation, so the whole
    pipeline is re-run and the full updated stage strip is echoed back. The
    centres are also mapped back to original-image pixels for the Phase-4
    feedback store (the original image is saved once, content-addressed by
    SHA-256).
    """
    _require_password(password)
    data = await _read_validated(image)
    try:
        async with _predict_lock:
            result = visualize_mod.compute_correction(
                engine, data, eye, (od_x, od_y), (fovea_x, fovea_y)
            )
    except (imaging.BadImage, imaging.PayloadTooLarge) as exc:
        raise _http_from_imaging(exc) from exc

    image_hash = imaging.sha256_hex(data)
    ext = _MIME_EXT.get((image.content_type or "").split(";")[0].strip().lower(), "png")
    record = {
        "eye": eye,
        "od_center_flip": [od_x, od_y],
        "fovea_center_flip": [fovea_x, fovea_y],
        "space_w": result["od_fovea"]["space_w"],
        "space_h": result["od_fovea"]["space_h"],
        "od_center_original": result["original"]["od_center"],
        "fovea_center_original": result["original"]["fovea_center"],
        "original_w": result["original"]["space_w"],
        "original_h": result["original"]["space_h"],
        "od_confidence_at_capture": od_confidence,
        "fovea_confidence_at_capture": fovea_confidence,
        "reviewer": reviewer,
        "notes": notes,
    }
    try:
        record_id = corrections_mod.save_correction(
            settings.corrections_dir, record, data, image_hash, image_ext=ext
        )
        stored = True
    except OSError as exc:  # store is best-effort: never fail the correction
        print(f"[WARN] could not persist OD/fovea correction: {exc}")
        record_id, stored = image_hash, False

    # Mirror the correction into the patient case, together with the pipeline
    # re-run it produced — the case then shows both what the detector proposed
    # and what the clinician moved it to, and the stages of each.
    cid = _active_case(case_id)
    if cid:
        index = _case_write("save OD/fovea correction", cases_mod.save_correction,
                            settings.cases_dir, cid, eye, {
                                "od_corrected": [od_x, od_y],
                                "fovea_corrected": [fovea_x, fovea_y],
                                "od_confidence_at_capture": od_confidence,
                                "fovea_confidence_at_capture": fovea_confidence,
                                "space_w": result["od_fovea"]["space_w"],
                                "space_h": result["od_fovea"]["space_h"],
                                "od_center_original": result["original"]["od_center"],
                                "fovea_center_original": result["original"]["fovea_center"],
                                "reviewer": reviewer,
                                "notes": notes,
                                "corrections_store_id": record_id if stored else "",
                            })
        if index:
            variant = f"corrected_{index}"
            entry = _case_write("cache corrected preprocessing", cases_mod.save_preprocessing,
                                settings.cases_dir, cid, eye, result, variant=variant)
            if entry:
                _case_write("link corrected preprocessing", cases_mod.update_case,
                            settings.cases_dir, cid,
                            lambda rec: rec["corrections"][index - 1].__setitem__(
                                "preprocessing_dir", entry["directory"]))

    return ODFoveaCorrectionResponse(
        od_fovea=result["od_fovea"], stored=stored, record_id=record_id,
        fov_mask_png_b64=result["fov_mask_png_b64"],
        fov_base_png_b64=result["fov_base_png_b64"],
        detect_base_png_b64=result["detect_base_png_b64"],
        stages=result["stages"],
    )


@app.post("/api/case/image", response_model=CaseImageResponse)
async def case_image(
    image: UploadFile = File(...),
    eye: str = Form(default="left"),
    case_id: str | None = Form(default=None),
    is_fundus: bool | None = Form(default=None),
    laterality: str | None = Form(default=None),
    laterality_confidence: float | None = Form(default=None),
    source: str = Form(default="upload"),
    password: str | None = Form(default=None),
) -> CaseImageResponse:
    """Open (or extend) a patient case with one uploaded eye.

    Called by the demo the moment an image lands in a slot, before any
    inference: the first accepted image mints the case, the second eye joins the
    same one. The original is stored byte-for-byte and its metadata — file name,
    size, resolution, SHA-256 and the client-side fundus/laterality check — goes
    into the case log.

    An image the client-side check rejected as *not* a fundus photograph is not
    filed at all (``stored=False``): the case store holds patients, not stray
    files. Every other failure is also non-fatal — the demo works without it.
    """
    _require_password(password)
    data = await _read_validated(image)
    try:
        imaging.decode_rgb(data)  # reject undecodable/oversized before storing
    except (imaging.BadImage, imaging.PayloadTooLarge) as exc:
        raise _http_from_imaging(exc) from exc

    existing = _active_case(case_id) or ""
    if is_fundus is False:
        return CaseImageResponse(
            case_id=existing, eye=eye, stored=False,
            reason="Image was not recognised as a fundus photograph.",
        )

    cid = existing or _case_write("open case", cases_mod.create_case,
                                  settings.cases_dir, _model_provenance())
    if not cid:
        return CaseImageResponse(case_id="", eye=eye, stored=False,
                                 reason="Case store is unavailable.")

    ext = _MIME_EXT.get((image.content_type or "").split(";")[0].strip().lower(), "png")
    stored = _case_write(
        "store original image", cases_mod.add_image,
        settings.cases_dir, cid, eye, data, imaging.sha256_hex(data),
        filename=image.filename, content_type=image.content_type, extension=ext,
        source=source,
        checks={
            "is_fundus": is_fundus,
            "laterality": laterality,
            "laterality_confidence": laterality_confidence,
        },
    )
    return CaseImageResponse(
        case_id=cid, eye=eye, stored=bool(stored),
        reason="" if stored else "Original image could not be written.",
    )


@app.post("/api/case/{case_id}/feedback", response_model=CaseFeedbackResponse)
async def case_feedback(
    case_id: str,
    verdict: str = Form(...),
    corrected_grade: int = Form(...),
    predicted_grade: int | None = Form(default=None),
    confidence: float | None = Form(default=None),
    reviewer: str | None = Form(default=None),
    notes: str | None = Form(default=None),
    password: str | None = Form(default=None),
) -> CaseFeedbackResponse:
    """Persist the ophthalmologist's verdict on a case's prediction.

    ``verdict`` is ``"confirmed"`` or ``"rejected"``; ``corrected_grade`` is the
    grade the reviewer considers correct (equal to the model's grade when
    confirming). A case can be re-graded — verdicts accumulate in order.
    """
    _require_password(password)
    if verdict not in ("confirmed", "rejected"):
        raise HTTPException(status_code=400,
                            detail="verdict must be 'confirmed' or 'rejected'.")
    if not 0 <= corrected_grade <= 4:
        raise HTTPException(status_code=400, detail="corrected_grade must be 0–4.")
    if not _active_case(case_id):
        raise HTTPException(status_code=404, detail=f"No such case: {case_id}")

    index = _case_write("save verdict", cases_mod.save_feedback, settings.cases_dir, case_id, {
        "verdict": verdict,
        "corrected_grade": corrected_grade,
        "predicted_grade": predicted_grade,
        "confidence": confidence,
        "reviewer": reviewer,
        "notes": notes,
    })
    return CaseFeedbackResponse(
        case_id=case_id, stored=bool(index), index=index or 0,
        reason="" if index else "Verdict could not be written.",
    )


@app.delete("/api/case/{case_id}/feedback", response_model=CaseFeedbackRetractResponse)
async def retract_case_feedback(
    case_id: str,
    index: int | None = Query(default=None),
    password: str | None = Query(default=None),
) -> CaseFeedbackRetractResponse:
    """Withdraw a verdict the reviewer took back (the most recent one by default).

    The demo lets a reviewer undo their confirm/reject, and undoing must leave
    nothing behind — a retracted verdict would otherwise keep skewing
    ``/api/cases/stats`` and keep being exported as a training label.
    """
    _require_password(password)
    if not _active_case(case_id):
        raise HTTPException(status_code=404, detail=f"No such case: {case_id}")

    removed = _case_write("retract verdict", cases_mod.retract_feedback,
                          settings.cases_dir, case_id, index)
    if not removed:
        return CaseFeedbackRetractResponse(case_id=case_id, retracted=False)
    return CaseFeedbackRetractResponse(
        case_id=case_id, retracted=True,
        verdict=str(removed.get("verdict", "")),
        corrected_grade=removed.get("corrected_grade"),
    )


@app.get("/api/cases/stats", response_model=CaseStatsResponse)
async def case_stats(password: str | None = Query(default=None)) -> CaseStatsResponse:
    """Aggregate counters over every stored case — the demo's statistics panel.

    Read from the case directories, so the numbers survive a cleared browser
    buffer, a reload, or a different machine on the same backend.
    """
    _require_password(password)
    return CaseStatsResponse(**cases_mod.collect_stats(settings.cases_dir))


@app.get("/api/case/{case_id}")
async def get_case(case_id: str, password: str | None = Query(default=None)) -> dict:
    """Return one case record (``case.json``) — the case as the server holds it."""
    _require_password(password)
    try:
        return cases_mod.load_case(settings.cases_dir, case_id)
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/selftest", response_model=SelftestResponse)
async def selftest(password: str | None = Query(default=None)) -> SelftestResponse:
    """Run predict + gradcam + visualize on synthetic fundus images (§C.7)."""
    _require_password(password)
    from .selftest import run_selftest
    return SelftestResponse(**run_selftest(engine))
