"""Per-patient case store — originals, cached preprocessing, attention, log.

A *case* is opened the moment the first fundus image of a patient is accepted by
the demo (the client-side fundus check must not have rejected it). Everything the
session then computes for that patient is filed into one directory, so a defence
session leaves a complete, self-describing record on disk instead of state that
dies with the browser tab:

    <cases_dir>/<case_id>/
    |-- case.json                    machine-readable record (source of truth)
    |-- case.txt                     the same record as a human-readable report
    |-- original/<eye>.<ext>         the uploaded images, byte-for-byte
    |-- preprocessing/<eye>/         one PNG per pipeline stage + FOV mask
    |   |-- input_channels/          the final stage's R/G/B/FOV = the CNN input
    |   `-- <eye>_corrected_<n>/     re-run after a clinician OD/fovea correction
    `-- attention/<eye>_*.png        Grad-CAM heatmap + attention overlay

``case.json`` is written first and ``case.txt`` is rendered from it, so the two
can never disagree. Both are rewritten in full on every update (a case holds a
handful of kilobytes of text), and every write goes through one process-wide
lock — the demo serialises GPU work anyway, so a coarse lock costs nothing.

Every entry point raises only ``OSError``/``ValueError``; callers treat the store
as best-effort and must never fail a prediction because a case could not be
written.
"""

from __future__ import annotations

import base64
import io
import json
import os
import re
import secrets
import threading
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

_WRITE_LOCK = threading.RLock()

_JSON_NAME = "case.json"
_TEXT_NAME = "case.txt"
_ORIGINAL_DIR = "original"
_PREPROC_DIR = "preprocessing"
_ATTENTION_DIR = "attention"
_CHANNELS_DIR = "input_channels"

# Bumped when the on-disk record shape changes incompatibly.
SCHEMA_VERSION = 1

# ``case_20260816T101530Z_ab12cd34`` — the timestamp prefix makes a plain
# directory listing chronological; the suffix keeps ids unique within a second.
_CASE_ID_RE = re.compile(r"^case_\d{8}T\d{6}Z_[0-9a-f]{8}$")

_GRADE_LABELS: dict[int, str] = {
    0: "No DR",
    1: "Mild NPDR",
    2: "Moderate NPDR",
    3: "Severe NPDR",
    4: "Proliferative DR",
}

_EYE_LABELS: dict[str, str] = {"right": "right eye / OD", "left": "left eye / OS"}

_RULE = "-" * 68


# ---------------------------------------------------------------------------
# Identity and paths
# ---------------------------------------------------------------------------


def _utc_now() -> str:
    """Current UTC timestamp, second resolution, ISO-8601."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_case_id() -> str:
    """Mint a fresh case id (``case_<UTC stamp>_<8 hex>``)."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"case_{stamp}_{secrets.token_hex(4)}"


def is_valid_case_id(case_id: str | None) -> bool:
    """Whether ``case_id`` is a well-formed id minted by :func:`new_case_id`.

    Args:
        case_id: Candidate id (may be ``None`` or empty).

    Returns:
        ``True`` when the id matches the minted format. The check doubles as
        path-traversal protection — ids arrive from the client.
    """
    return bool(case_id) and bool(_CASE_ID_RE.match(case_id or ""))


def case_dir(base_dir: Path, case_id: str) -> Path:
    """Resolve the directory of one case.

    Args:
        base_dir: Root of the case store (``settings.cases_dir``).
        case_id: The case id.

    Returns:
        The case directory (not guaranteed to exist).

    Raises:
        ValueError: If ``case_id`` is not a well-formed id.
    """
    if not is_valid_case_id(case_id):
        raise ValueError(f"Malformed case id: {case_id!r}")
    return base_dir / case_id


def _normalize_eye(eye: str) -> str:
    """Coerce an eye label to ``"left"``/``"right"``.

    Raises:
        ValueError: If ``eye`` is neither.
    """
    value = (eye or "").strip().lower()
    if value not in ("left", "right"):
        raise ValueError(f"Unknown eye {eye!r}; expected 'left' or 'right'.")
    return value


# ---------------------------------------------------------------------------
# Record read / write
# ---------------------------------------------------------------------------


def _empty_record(case_id: str, model: dict | None) -> dict:
    """Build the initial record for a freshly opened case."""
    now = _utc_now()
    return {
        "schema": SCHEMA_VERSION,
        "case_id": case_id,
        "created_utc": now,
        "updated_utc": now,
        "model": dict(model or {}),
        "images": {},          # eye -> image metadata
        "detection": {},       # eye -> OD/fovea payload as detected
        "preprocessing": {},   # eye -> cached stage files
        "corrections": [],     # clinician OD/fovea corrections, in order
        "attention": {},       # eye -> Grad-CAM metadata + files
        "predictions": [],     # one entry per /api/predict run, in order
        "feedback": [],        # ophthalmologist verdicts, in order
    }


def _read_record(directory: Path) -> dict:
    """Load ``case.json`` from a case directory.

    Raises:
        OSError: If the file cannot be read.
        ValueError: If the file is not valid JSON.
    """
    try:
        with (directory / _JSON_NAME).open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Corrupt case record at {directory / _JSON_NAME}: {exc}") from exc


def _write_atomic(path: Path, text: str) -> None:
    """Write ``text`` to ``path`` via a temp file + rename (never a torn file)."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def _flush(directory: Path, record: dict) -> None:
    """Persist the record as ``case.json`` and render ``case.txt`` from it."""
    record["updated_utc"] = _utc_now()
    _write_atomic(directory / _JSON_NAME, json.dumps(record, ensure_ascii=False, indent=2))
    _write_atomic(directory / _TEXT_NAME, render_text(record))


def create_case(base_dir: Path, model: dict | None = None) -> str:
    """Open a new case directory and write its initial record.

    Args:
        base_dir: Root of the case store.
        model: Provenance of the serving model (checkpoint, device, version…),
            recorded once so the case is interpretable without the server.

    Returns:
        The new case id.

    Raises:
        OSError: If the directory or record cannot be written.
    """
    case_id = new_case_id()
    directory = base_dir / case_id
    with _WRITE_LOCK:
        directory.mkdir(parents=True, exist_ok=True)
        _flush(directory, _empty_record(case_id, model))
    return case_id


def update_case(base_dir: Path, case_id: str, mutate: Callable[[dict], None]) -> dict:
    """Read-modify-write one case record under the store lock.

    Args:
        base_dir: Root of the case store.
        case_id: The case to update.
        mutate: Callback applied to the loaded record in place.

    Returns:
        The updated record.

    Raises:
        ValueError: If ``case_id`` is malformed or the record is corrupt.
        FileNotFoundError: If the case does not exist.
        OSError: If the record cannot be rewritten.
    """
    directory = case_dir(base_dir, case_id)
    with _WRITE_LOCK:
        if not (directory / _JSON_NAME).exists():
            raise FileNotFoundError(f"No such case: {case_id}")
        record = _read_record(directory)
        mutate(record)
        _flush(directory, record)
        return record


def case_exists(base_dir: Path, case_id: str | None) -> bool:
    """Whether ``case_id`` is well-formed and its record is on disk."""
    if not is_valid_case_id(case_id):
        return False
    return (base_dir / str(case_id) / _JSON_NAME).exists()


def load_case(base_dir: Path, case_id: str) -> dict:
    """Return one case record.

    Raises:
        ValueError: If ``case_id`` is malformed or the record is corrupt.
        FileNotFoundError: If the case does not exist.
    """
    directory = case_dir(base_dir, case_id)
    if not (directory / _JSON_NAME).exists():
        raise FileNotFoundError(f"No such case: {case_id}")
    with _WRITE_LOCK:
        return _read_record(directory)


# ---------------------------------------------------------------------------
# Artifact writers
# ---------------------------------------------------------------------------


def _image_size(image_bytes: bytes) -> tuple[int, int]:
    """Read ``(width, height)`` from encoded image bytes, ``(0, 0)`` on failure.

    Uses the header only — no full decode. The upload has already passed
    ``imaging.check_upload``/``decode_rgb`` by the time this runs.
    """
    try:
        with Image.open(io.BytesIO(image_bytes)) as im:
            return int(im.size[0]), int(im.size[1])
    except Exception:  # noqa: BLE001 — metadata only; never block a save
        return 0, 0


def _write_png_b64(path: Path, png_b64: str) -> bool:
    """Decode a base64 PNG string to ``path``. Returns ``False`` when empty/bad."""
    if not png_b64:
        return False
    try:
        payload = base64.b64decode(png_b64)
    except (ValueError, TypeError):
        return False
    path.write_bytes(payload)
    return True


def add_image(
    base_dir: Path,
    case_id: str,
    eye: str,
    image_bytes: bytes,
    image_hash: str,
    *,
    filename: str | None = None,
    content_type: str | None = None,
    extension: str = "png",
    source: str = "upload",
    checks: dict | None = None,
) -> dict:
    """File one eye's original image into the case and record its metadata.

    Re-uploading the same eye replaces the stored original (any file with a
    different extension is removed first, so the slot never holds two images).

    Args:
        base_dir: Root of the case store.
        case_id: The case to file into.
        eye: ``"left"`` or ``"right"``.
        image_bytes: Raw upload bytes, written byte-for-byte.
        image_hash: SHA-256 hex digest of ``image_bytes``.
        filename: Client-side file name, recorded but not used on disk.
        content_type: Declared MIME type.
        extension: File extension for the stored copy (no dot).
        source: ``"upload"`` (clinician's file) or ``"sample"`` (bundled image).
        checks: The client-side fundus/laterality heuristics for this image.

    Returns:
        The recorded image-metadata entry.

    Raises:
        ValueError / FileNotFoundError / OSError: As :func:`update_case`.
    """
    side = _normalize_eye(eye)
    width, height = _image_size(image_bytes)
    stored_rel = f"{_ORIGINAL_DIR}/{side}.{extension}"

    entry = {
        "eye": side,
        "filename": filename or "",
        "content_type": content_type or "",
        "bytes": len(image_bytes),
        "sha256": image_hash,
        "width": width,
        "height": height,
        "source": source,
        "client_checks": dict(checks or {}),
        "stored_file": stored_rel,
        "received_utc": _utc_now(),
    }

    directory = case_dir(base_dir, case_id)
    with _WRITE_LOCK:
        originals = directory / _ORIGINAL_DIR
        originals.mkdir(parents=True, exist_ok=True)
        for stale in originals.glob(f"{side}.*"):
            stale.unlink()
        (directory / stored_rel).write_bytes(image_bytes)
        update_case(base_dir, case_id, lambda rec: rec["images"].__setitem__(side, entry))
    return entry


def save_preprocessing(
    base_dir: Path,
    case_id: str,
    eye: str,
    payload: dict,
    *,
    variant: str = "",
) -> dict:
    """Cache one eye's preprocessing stage images and the detection payload.

    Every stage slide from ``/api/visualize`` is written as its own PNG, in
    pipeline order, so the case folder holds exactly what the CNN was shown. The
    final stage's channel decomposition is written to ``input_channels/`` — those
    four planes *are* the 4-channel input tensor.

    Args:
        base_dir: Root of the case store.
        case_id: The case to file into.
        eye: ``"left"`` or ``"right"``.
        payload: The visualize payload (``stages``, ``preview_png_b64``,
            ``od_fovea``…).
        variant: Sub-run label, e.g. ``"corrected_1"``. Empty for the detector's
            own run, which also refreshes ``detection[eye]``.

    Returns:
        The recorded preprocessing entry.

    Raises:
        ValueError / FileNotFoundError / OSError: As :func:`update_case`.
    """
    side = _normalize_eye(eye)
    folder = side if not variant else f"{side}_{variant}"
    rel = f"{_PREPROC_DIR}/{folder}"
    directory = case_dir(base_dir, case_id)
    target = directory / _PREPROC_DIR / folder

    files: list[str] = []
    with _WRITE_LOCK:
        target.mkdir(parents=True, exist_ok=True)
        stages = payload.get("stages") or []
        for idx, stage in enumerate(stages):
            name = f"{idx:02d}_{stage.get('key', 'stage')}.png"
            if _write_png_b64(target / name, stage.get("png_b64", "")):
                files.append(f"{rel}/{name}")
        # The last stage carrying a channel split is the CNN input tensor.
        for stage in reversed(stages):
            channels = stage.get("channels") or []
            if not channels:
                continue
            chan_dir = target / _CHANNELS_DIR
            chan_dir.mkdir(exist_ok=True)
            for channel in channels:
                name = f"{channel.get('key', 'ch')}.png"
                if _write_png_b64(chan_dir / name, channel.get("png_b64", "")):
                    files.append(f"{rel}/{_CHANNELS_DIR}/{name}")
            break
        if _write_png_b64(target / "preview_strip.png", payload.get("preview_png_b64", "")):
            files.append(f"{rel}/preview_strip.png")

        entry = {
            "eye": side,
            "variant": variant,
            "directory": rel,
            "stage_count": len(stages),
            "stages": [s.get("key", "") for s in stages],
            "files": files,
            "saved_utc": _utc_now(),
        }
        detection = payload.get("od_fovea")

        def _mutate(rec: dict) -> None:
            key = folder
            rec["preprocessing"][key] = entry
            if not variant and detection:
                rec["detection"][side] = _detection_entry(detection)

        update_case(base_dir, case_id, _mutate)
    return entry


def _detection_entry(od_fovea: dict) -> dict:
    """Strip the base64 heatmaps out of an OD/fovea payload for the record."""
    return {k: v for k, v in od_fovea.items() if not k.endswith("_png_b64")} | {
        "recorded_utc": _utc_now()
    }


def save_correction(base_dir: Path, case_id: str, eye: str, entry: dict) -> int:
    """Append a clinician OD/fovea correction and return its 1-based index.

    The centres the detector originally proposed are filled in from
    ``detection[eye]`` (recorded by the preceding visualize call) unless the
    caller supplies them, so the record shows what was changed, not just the
    final position.

    Args:
        base_dir: Root of the case store.
        case_id: The case to file into.
        eye: ``"left"`` or ``"right"``.
        entry: Correction details (corrected centres, confidences at capture…).

    Returns:
        The correction's ordinal within this case — also the ``corrected_<n>``
        suffix of the directory holding its pipeline re-run.

    Raises:
        ValueError / FileNotFoundError / OSError: As :func:`update_case`.
    """
    side = _normalize_eye(eye)
    box: dict[str, int] = {}

    def _mutate(rec: dict) -> None:
        index = len(rec["corrections"]) + 1
        detected = (rec.get("detection") or {}).get(side) or {}
        item = {"index": index, "eye": side, "recorded_utc": _utc_now()} | dict(entry)
        item.setdefault("od_detected", detected.get("od_center"))
        item.setdefault("fovea_detected", detected.get("fovea_center"))
        rec["corrections"].append(item)
        box["index"] = index

    update_case(base_dir, case_id, _mutate)
    return box["index"]


def save_attention(base_dir: Path, case_id: str, eye: str, payload: dict) -> dict:
    """Store one eye's Grad-CAM heatmap + attention overlay and its statistics.

    Args:
        base_dir: Root of the case store.
        case_id: The case to file into.
        eye: ``"left"`` or ``"right"``.
        payload: The ``/api/gradcam`` response dict.

    Returns:
        The recorded attention entry.

    Raises:
        ValueError / FileNotFoundError / OSError: As :func:`update_case`.
    """
    side = _normalize_eye(eye)
    directory = case_dir(base_dir, case_id)
    target = directory / _ATTENTION_DIR

    files: list[str] = []
    with _WRITE_LOCK:
        target.mkdir(parents=True, exist_ok=True)
        for name, key in (
            (f"{side}_gradcam.png", "gradcam_png_b64"),
            (f"{side}_attention_overlay.png", "attention_overlay_png_b64"),
        ):
            if _write_png_b64(target / name, payload.get(key, "")):
                files.append(f"{_ATTENTION_DIR}/{name}")

        entry = {
            "eye": side,
            "target_class": payload.get("target_class"),
            "rationale": payload.get("rationale", ""),
            "cam_pixel_count": payload.get("cam_pixel_count"),
            "cam_area_frac": payload.get("cam_area_frac"),
            "cam_region": payload.get("cam_region", ""),
            "files": files,
            "saved_utc": _utc_now(),
        }
        update_case(base_dir, case_id, lambda rec: rec["attention"].__setitem__(side, entry))
    return entry


def save_prediction(base_dir: Path, case_id: str, prediction: dict) -> int:
    """Append one model run to the case and return its 1-based index.

    Args:
        base_dir: Root of the case store.
        case_id: The case to file into.
        prediction: A ``PatientPredictionResponse`` as a dict.

    Returns:
        The run's ordinal within this case.

    Raises:
        ValueError / FileNotFoundError / OSError: As :func:`update_case`.
    """
    box: dict[str, int] = {}

    def _mutate(rec: dict) -> None:
        index = len(rec["predictions"]) + 1
        rec["predictions"].append({"index": index, "run_utc": _utc_now()} | dict(prediction))
        box["index"] = index

    update_case(base_dir, case_id, _mutate)
    return box["index"]


def save_feedback(base_dir: Path, case_id: str, entry: dict) -> int:
    """Append an ophthalmologist verdict to the case, returning its index.

    This is the record the whole store exists for: the demo's confirm/reject
    control used to live only in browser memory, so a disagreement and its
    corrected grade were lost when the tab closed.

    Args:
        base_dir: Root of the case store.
        case_id: The case to file into.
        entry: Verdict payload (``verdict``, ``corrected_grade``,
            ``predicted_grade``, ``reviewer``, ``notes``…).

    Returns:
        The verdict's ordinal within this case.

    Raises:
        ValueError / FileNotFoundError / OSError: As :func:`update_case`.
    """
    box: dict[str, int] = {}

    def _mutate(rec: dict) -> None:
        index = len(rec["feedback"]) + 1
        rec["feedback"].append({"index": index, "recorded_utc": _utc_now()} | dict(entry))
        box["index"] = index

    update_case(base_dir, case_id, _mutate)
    return box["index"]


def retract_feedback(base_dir: Path, case_id: str, index: int | None = None) -> dict | None:
    """Withdraw a verdict from a case, dropping it from the record entirely.

    The reviewer can take a verdict back in the demo, and taking it back must
    leave no trace: a retracted verdict that lingered would still be counted in
    the store's statistics and exported as a training label. Remaining verdicts
    are renumbered so ``index`` stays the position in the list.

    Args:
        base_dir: Root of the case store.
        case_id: The case to amend.
        index: 1-based verdict to withdraw; the most recent one when ``None``.

    Returns:
        The removed verdict, or ``None`` if the case has no verdict at that
        position.

    Raises:
        ValueError / FileNotFoundError / OSError: As :func:`update_case`.
    """
    box: dict[str, dict | None] = {"removed": None}

    def _mutate(rec: dict) -> None:
        items = rec.get("feedback") or []
        if not items:
            return
        position = len(items) - 1 if index is None else index - 1
        if not 0 <= position < len(items):
            return
        box["removed"] = items.pop(position)
        for order, item in enumerate(items, start=1):
            item["index"] = order

    update_case(base_dir, case_id, _mutate)
    return box["removed"]


def collect_stats(base_dir: Path) -> dict:
    """Aggregate the whole store into the counters the demo's stats panel shows.

    Reads every ``case.json`` under ``base_dir``. Records are written by atomic
    rename, so this needs no lock; an unreadable case is skipped rather than
    failing the whole tally.

    Args:
        base_dir: Root of the case store.

    Returns:
        Patient/image/run/verdict counts, the confirm-vs-reject split and the
        agreement rate, and ``grades`` — how many reviewed patients sit at each
        DR grade according to the reviewer, not the model.
    """
    stats = {
        "patients": 0, "images": 0, "predictions": 0, "corrections": 0,
        "verdicts": 0, "confirmed": 0, "rejected": 0,
        "reviewed_patients": 0, "agreement": None,
        "grades": [0, 0, 0, 0, 0],
        "last_activity_utc": "",
    }
    if not base_dir.is_dir():
        return stats

    for directory in base_dir.iterdir():
        if not directory.is_dir() or not is_valid_case_id(directory.name):
            continue
        try:
            record = _read_record(directory)
        except (OSError, ValueError):
            continue  # a case being written / hand-edited must not break the tally

        stats["patients"] += 1
        stats["images"] += len(record.get("images") or {})
        stats["predictions"] += len(record.get("predictions") or [])
        stats["corrections"] += len(record.get("corrections") or [])

        verdicts = record.get("feedback") or []
        stats["verdicts"] += len(verdicts)
        for item in verdicts:
            if item.get("verdict") == "confirmed":
                stats["confirmed"] += 1
            elif item.get("verdict") == "rejected":
                stats["rejected"] += 1
        if verdicts:
            stats["reviewed_patients"] += 1
            # The reviewer's latest word on this patient is their DR grade.
            grade = verdicts[-1].get("corrected_grade")
            if isinstance(grade, int) and 0 <= grade <= 4:
                stats["grades"][grade] += 1

        updated = record.get("updated_utc") or ""
        if updated > stats["last_activity_utc"]:
            stats["last_activity_utc"] = updated

    decided = stats["confirmed"] + stats["rejected"]
    if decided:
        stats["agreement"] = round(stats["confirmed"] / decided, 4)
    return stats


def _verdict_row(record: dict, verdict: dict) -> dict:
    """Render one stored verdict as a relabeling-buffer row.

    The row carries exactly what the demo's buffer table shows and its JSONL
    export writes, so a buffer rebuilt from the store is indistinguishable from
    one the tab accumulated itself.

    Args:
        record: The case record the verdict belongs to.
        verdict: One entry of ``record["feedback"]``.

    Returns:
        A buffer-row dict (``id``, ``timestamp``, ``images``, ``predicted``,
        ``confidence``, ``probs``, ``verdict``, ``corrected_grade``…).
    """
    case_id = record.get("case_id", "")
    index = verdict.get("index", 0)
    # Probabilities and latency belong to the run the verdict judged. Only the
    # grade and confidence are stored on the verdict itself, so take the rest
    # from the case's most recent run — the one on screen when it was given.
    runs = record.get("predictions") or []
    run = runs[-1] if runs else {}
    images = [
        {"eye": entry.get("eye", eye), "source": entry.get("filename", "")}
        for eye, entry in (record.get("images") or {}).items()
    ]
    predicted = verdict.get("predicted_grade")
    if predicted is None:
        predicted = run.get("pred")
    confidence = verdict.get("confidence")
    if confidence is None:
        confidence = run.get("confidence")
    return {
        "id": f"{case_id}#{index}",
        "index": index,
        "case_id": case_id,
        "timestamp": verdict.get("recorded_utc", ""),
        "images": images,
        "predicted": predicted,
        "confidence": confidence,
        "probs": run.get("probs") or [],
        "verdict": verdict.get("verdict", ""),
        "corrected_grade": verdict.get("corrected_grade"),
        "latency_ms": run.get("latency_ms"),
        "model": (record.get("model") or {}).get("model", ""),
        "reviewer": verdict.get("reviewer"),
        "notes": verdict.get("notes"),
    }


def collect_verdicts(base_dir: Path, limit: int = 200) -> dict:
    """Rebuild the relabeling buffer from every verdict in the store.

    The buffer used to live only in the tab, so a reload emptied it while the
    verdicts themselves sat safely on disk. This reads them back, newest first,
    so the buffer survives a refresh exactly as the study totals do.

    Args:
        base_dir: Root of the case store.
        limit: Maximum rows to return (newest kept).

    Returns:
        ``{"entries": [...], "total": n}`` — ``total`` counts every verdict in
        the store, which may exceed the rows returned.
    """
    rows: list[dict] = []
    if not base_dir.is_dir():
        return {"entries": [], "total": 0}

    for directory in base_dir.iterdir():
        if not directory.is_dir() or not is_valid_case_id(directory.name):
            continue
        try:
            record = _read_record(directory)
        except (OSError, ValueError):
            continue  # same rule as collect_stats: skip, never fail the whole list
        for verdict in record.get("feedback") or []:
            rows.append(_verdict_row(record, verdict))

    rows.sort(key=lambda r: r["timestamp"], reverse=True)
    return {"entries": rows[:max(0, limit)], "total": len(rows)}


# ---------------------------------------------------------------------------
# Human-readable report
# ---------------------------------------------------------------------------


def grade_label(grade: object) -> str:
    """Render a DR grade as ``"2 - Moderate NPDR"``, or ``"-"`` when absent."""
    if grade is None:
        return "-"
    try:
        value = int(grade)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return str(grade)
    return f"{value} - {_GRADE_LABELS.get(value, 'unknown')}"


def _section(title: str) -> list[str]:
    """Section header lines for the text report."""
    return ["", title.upper(), _RULE]


def _kv(key: str, value: object, indent: int = 2) -> str:
    """One aligned ``key : value`` line of the text report."""
    return f"{' ' * indent}{key:<16}: {value}"


def _fmt_xy(point: object) -> str:
    """Format an ``[x, y]`` pair as ``(x.x, y.y)`` px."""
    if not isinstance(point, (list, tuple)) or len(point) < 2:
        return "-"
    return f"({float(point[0]):.1f}, {float(point[1]):.1f}) px"


def _render_images(record: dict) -> list[str]:
    """Text block: the uploaded originals and their client-side checks."""
    lines = _section("Input images")
    images = record.get("images") or {}
    if not images:
        return lines + ["  (none recorded)"]
    for side in ("right", "left"):
        img = images.get(side)
        if not img:
            continue
        checks = img.get("client_checks") or {}
        fundus = checks.get("is_fundus")
        fundus_txt = {True: "yes", False: "no", None: "not checked"}.get(fundus, str(fundus))
        laterality = checks.get("laterality") or "undetermined"
        conf = checks.get("laterality_confidence")
        conf_txt = f" (confidence {float(conf):.2f})" if isinstance(conf, (int, float)) else ""
        lines += [
            f"  [{_EYE_LABELS[side]}]",
            _kv("File", f"{img.get('filename') or '-'} "
                        f"({img.get('content_type') or 'unknown'}, {img.get('bytes', 0)} bytes)", 4),
            _kv("Resolution", f"{img.get('width', 0)} x {img.get('height', 0)} px", 4),
            _kv("SHA-256", img.get("sha256", "-"), 4),
            _kv("Source", img.get("source", "-"), 4),
            _kv("Fundus check", f"fundus={fundus_txt}, laterality={laterality}{conf_txt}", 4),
            _kv("Stored as", img.get("stored_file", "-"), 4),
            _kv("Received (UTC)", img.get("received_utc", "-"), 4),
        ]
    return lines


def _render_detection(record: dict) -> list[str]:
    """Text block: what the OD/fovea detector found, per eye."""
    detection = record.get("detection") or {}
    if not detection:
        return []
    lines = _section("OD / fovea detection")
    for side in ("right", "left"):
        det = detection.get(side)
        if not det:
            continue
        lines += [
            f"  [{_EYE_LABELS[side]}]",
            _kv("Optic disc", f"{_fmt_xy(det.get('od_center'))}, radius "
                              f"{float(det.get('od_radius') or 0):.1f} px, confidence "
                              f"{float(det.get('od_confidence') or 0):.3f}", 4),
            _kv("Fovea", f"{_fmt_xy(det.get('fovea_center'))}, radius "
                         f"{float(det.get('fovea_radius') or 0):.1f} px, confidence "
                         f"{float(det.get('fovea_confidence') or 0):.3f}", 4),
            _kv("OD-fovea axis", f"{float(det.get('angle_deg') or 0):.2f} deg "
                                 f"(rotation sigma {float(det.get('rotation_sigma_deg') or 0):.2f} deg)", 4),
            _kv("Confident", "yes" if det.get("confident") else "no", 4),
            _kv("Frame", f"flipped (pre-rotation), {det.get('space_w', 0)} x "
                         f"{det.get('space_h', 0)} px", 4),
        ]
    return lines


def _render_corrections(record: dict) -> list[str]:
    """Text block: clinician OD/fovea corrections, in order."""
    corrections = record.get("corrections") or []
    if not corrections:
        return []
    lines = _section("Clinician OD / fovea corrections")
    for corr in corrections:
        side = corr.get("eye", "-")
        lines += [
            f"  {corr.get('index', '?')}. [{_EYE_LABELS.get(side, side)}] "
            f"{corr.get('recorded_utc', '-')}",
            _kv("Optic disc", f"{_fmt_xy(corr.get('od_detected'))} -> "
                              f"{_fmt_xy(corr.get('od_corrected'))}", 4),
            _kv("Fovea", f"{_fmt_xy(corr.get('fovea_detected'))} -> "
                         f"{_fmt_xy(corr.get('fovea_corrected'))}", 4),
            _kv("Pipeline re-run", corr.get("preprocessing_dir", "-"), 4),
        ]
    return lines


def _render_preprocessing(record: dict) -> list[str]:
    """Text block: where each cached preprocessing run lives."""
    preprocessing = record.get("preprocessing") or {}
    if not preprocessing:
        return []
    lines = _section("Preprocessing (cached)")
    for key in sorted(preprocessing):
        entry = preprocessing[key]
        stages = ", ".join(entry.get("stages") or []) or "-"
        lines += [
            f"  [{key}]",
            _kv("Directory", entry.get("directory", "-"), 4),
            _kv("Stages", f"{entry.get('stage_count', 0)} - {stages}", 4),
            _kv("Files", len(entry.get("files") or []), 4),
            _kv("Saved (UTC)", entry.get("saved_utc", "-"), 4),
        ]
    return lines


def _render_predictions(record: dict) -> list[str]:
    """Text block: every model run, with per-class probabilities and per-eye grades."""
    predictions = record.get("predictions") or []
    if not predictions:
        return []
    lines = _section("Model prediction")
    for run in predictions:
        pred = run.get("pred")
        confidence = float(run.get("confidence") or 0.0)
        lines += [
            f"  Run {run.get('index', '?')} - {run.get('run_utc', '-')}",
            _kv("Patient grade", f"{grade_label(pred)} (confidence {confidence * 100:.1f}%)", 4),
            _kv("Referable", "yes" if isinstance(pred, int) and pred >= 2 else "no", 4),
            _kv("Latency", f"{run.get('latency_ms', 0)} ms", 4),
            "    Class probabilities:",
        ]
        for idx, prob in enumerate(run.get("probs") or []):
            marker = " <-- predicted" if idx == pred else ""
            lines.append(f"      grade {idx} - {_GRADE_LABELS.get(idx, '?'):<18}: "
                         f"{float(prob):.4f}{marker}")
        per_eye = run.get("per_eye") or []
        if per_eye:
            lines.append("    Per eye:")
            for eye_pred in per_eye:
                side = eye_pred.get("eye", "-")
                lines.append(
                    f"      {_EYE_LABELS.get(side, side):<16}: {grade_label(eye_pred.get('pred'))}"
                    f" ({float(eye_pred.get('confidence') or 0) * 100:.1f}%), "
                    f"{eye_pred.get('latency_ms', 0)} ms"
                )
    return lines


def _render_attention(record: dict) -> list[str]:
    """Text block: Grad-CAM target, rationale and CAM geometry, per eye."""
    attention = record.get("attention") or {}
    if not attention:
        return []
    lines = _section("Attention maps (Grad-CAM)")
    for side in ("right", "left"):
        att = attention.get(side)
        if not att:
            continue
        area = att.get("cam_area_frac")
        area_txt = f"{float(area) * 100:.2f}%" if isinstance(area, (int, float)) else "-"
        lines += [
            f"  [{_EYE_LABELS[side]}] target {grade_label(att.get('target_class'))}",
            _kv("Rationale", att.get("rationale") or "-", 4),
            _kv("CAM coverage", f"{area_txt} of the retina "
                                f"({att.get('cam_pixel_count', 0)} px), region: "
                                f"{att.get('cam_region') or '-'}", 4),
            _kv("Files", ", ".join(att.get("files") or []) or "-", 4),
        ]
    return lines


def _render_feedback(record: dict) -> list[str]:
    """Text block: the ophthalmologist's verdicts and corrected grades."""
    feedback = record.get("feedback") or []
    lines = _section("Ophthalmologist verdict")
    if not feedback:
        return lines + ["  (no verdict recorded yet)"]
    for item in feedback:
        verdict = str(item.get("verdict", "-")).upper()
        lines += [
            f"  {item.get('index', '?')}. {item.get('recorded_utc', '-')} - {verdict}",
            _kv("Model grade", grade_label(item.get("predicted_grade")), 4),
            _kv("Corrected", grade_label(item.get("corrected_grade")), 4),
            _kv("Reviewer", item.get("reviewer") or "-", 4),
            _kv("Notes", item.get("notes") or "-", 4),
        ]
    return lines


def render_text(record: dict) -> str:
    """Render a case record as the human-readable ``case.txt`` report.

    Args:
        record: A case record as held in ``case.json``.

    Returns:
        The full report text (ends with a newline).
    """
    model = record.get("model") or {}
    loaded = model.get("checkpoint_loaded")
    checkpoint = f"{model.get('checkpoint') or '-'}" + (
        " (loaded)" if loaded else " (NOT loaded - random-init weights)" if loaded is not None else ""
    )
    lines = [
        "DR-CLASSIFIER - PATIENT CASE RECORD",
        "=" * 68,
        _kv("Case id", record.get("case_id", "-"), 0),
        _kv("Created (UTC)", record.get("created_utc", "-"), 0),
        _kv("Updated (UTC)", record.get("updated_utc", "-"), 0),
    ]
    lines += _section("Model")
    lines += [
        _kv("Model", model.get("model") or "-"),
        _kv("Checkpoint", checkpoint),
        _kv("Input", f"{model.get('in_channels', '?')} channels "
                     f"(RGB + FOV mask), preset {model.get('preset') or '-'}"),
        _kv("Device", model.get("device") or "-"),
        _kv("Demo version", f"{model.get('version') or '-'} "
                            f"(git {model.get('git_sha') or 'n/a'})"),
    ]
    lines += _render_images(record)
    lines += _render_detection(record)
    lines += _render_corrections(record)
    lines += _render_preprocessing(record)
    lines += _render_predictions(record)
    lines += _render_attention(record)
    lines += _render_feedback(record)
    lines += [
        "",
        _RULE,
        "Research demo. Not a medical device and not a diagnosis.",
        "",
    ]
    return "\n".join(lines)
