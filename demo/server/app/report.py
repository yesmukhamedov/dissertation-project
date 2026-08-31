"""Case report as a PDF — the printable hand-out for one patient.

``cases.render_text`` already renders a case record as plain text for the
``case.txt`` filed next to it on disk. This module renders the *same* record as
a paginated PDF that also carries the pictures: the uploaded fundus photographs,
every cached preprocessing stage, the four planes of the CNN input tensor and
the Grad-CAM attention maps. It is what the demo hands the ophthalmologist to
take away once they have confirmed or rejected the model's grade — the verdict
is the first thing on page one, above the model's own output.

Nothing here touches the network or the GPU: the case directory holds
everything, so a report can be produced for any case in the store at any later
time.

The layout uses a Unicode TrueType font when one can be found (Kazakh needs
glyphs the built-in Type-1 fonts do not have) and falls back to Helvetica
otherwise — see :func:`_register_fonts`.
"""

from __future__ import annotations

import io
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .visualize import _PANEL_LABELS

# Palette — the demo dashboard's own accents, so the print-out and the screen
# read as one artifact.
_TEAL = colors.HexColor("#0f766e")
_INK = colors.HexColor("#1f2937")
_MUTED = colors.HexColor("#6b7280")
_RULE = colors.HexColor("#d1d5db")
_GREEN = colors.HexColor("#15803d")
_GREEN_BG = colors.HexColor("#ecfdf5")
_RED = colors.HexColor("#b91c1c")
_RED_BG = colors.HexColor("#fef2f2")
_ROW_BG = colors.HexColor("#f9fafb")

_PAGE = A4
_MARGIN = 16 * mm
_CONTENT_W = _PAGE[0] - 2 * _MARGIN

# Grid geometry for the stage / channel / attention image strips.
_GRID_COLS = 4
_GRID_GAP = 4 * mm

# Panels are embedded at print resolution rather than at their stored size. A
# case holds ~30 512-px PNGs; embedding them verbatim produced a 10 MB report
# for pictures that are never printed larger than ~45 mm.
_TARGET_DPI = 170
_JPEG_QUALITY = 86

_FONT = "Helvetica"
_FONT_BOLD = "Helvetica-Bold"

# Regular/bold TrueType pairs to try, in order. The first is shipped inside the
# server's own virtualenv (matplotlib bundles DejaVu); the second covers a bare
# Windows box. Both carry Kazakh Cyrillic.
_FONT_CANDIDATES: tuple[tuple[str, str], ...] = (
    ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf"),
    ("arial.ttf", "arialbd.ttf"),
)


def _font_search_dirs() -> list[Path]:
    """Directories to look for a Unicode TrueType font in, most specific first."""
    dirs: list[Path] = []
    try:  # matplotlib is already installed alongside the server and bundles DejaVu.
        import matplotlib
        dirs.append(Path(matplotlib.get_data_path()) / "fonts" / "ttf")
    except Exception:  # noqa: BLE001 — a missing font is a downgrade, not a failure
        pass
    dirs += [
        Path("C:/Windows/Fonts"),
        Path("/usr/share/fonts/truetype/dejavu"),
        Path("/usr/share/fonts/truetype/msttcorefonts"),
        Path("/Library/Fonts"),
    ]
    return dirs


def _register_fonts() -> None:
    """Register a Unicode font family as ``ReportSans``, or keep Helvetica.

    Kazakh (``ә ғ қ ң ө ұ ү һ і``) is unrepresentable in reportlab's built-in
    Type-1 fonts, which would silently print black boxes. When no TrueType font
    can be found the report still renders — in Helvetica, which is correct for
    the English report and merely degraded for the Kazakh one.
    """
    global _FONT, _FONT_BOLD
    if _FONT != "Helvetica":  # already registered
        return
    for regular, bold in _FONT_CANDIDATES:
        for directory in _font_search_dirs():
            reg_path, bold_path = directory / regular, directory / bold
            if not reg_path.is_file():
                continue
            try:
                pdfmetrics.registerFont(TTFont("ReportSans", str(reg_path)))
                pdfmetrics.registerFont(TTFont(
                    "ReportSans-Bold", str(bold_path if bold_path.is_file() else reg_path)
                ))
                pdfmetrics.registerFontFamily(
                    "ReportSans", normal="ReportSans", bold="ReportSans-Bold",
                    italic="ReportSans", boldItalic="ReportSans-Bold",
                )
            except Exception:  # noqa: BLE001 — try the next candidate
                continue
            _FONT, _FONT_BOLD = "ReportSans", "ReportSans-Bold"
            return


# ---------------------------------------------------------------------------
# Localisation
# ---------------------------------------------------------------------------

# The dashboard is EN/KZ, so the report follows the language the tab is in.
# Language-neutral values (ids, hashes, coordinates) are not translated; only
# the labels around them are.
_STRINGS: dict[str, dict[str, str]] = {
    "en": {
        "title": "Diabetic retinopathy screening report",
        "subtitle": "Automated fundus analysis with ophthalmologist review",
        "case": "Case",
        "generated": "Generated (UTC)",
        "created": "Case opened (UTC)",
        "updated": "Last updated (UTC)",
        "disclaimer": "Research demo. Not a medical device and not a diagnosis.",
        "page": "Page",
        "verdict.section": "Ophthalmologist verdict",
        "verdict.confirmed": "Prediction CONFIRMED by the ophthalmologist",
        "verdict.rejected": "Prediction REJECTED by the ophthalmologist",
        "verdict.none": "No verdict has been recorded for this patient yet.",
        "verdict.model": "Model grade",
        "verdict.final": "Ophthalmologist's grade",
        "verdict.reviewer": "Reviewer",
        "verdict.notes": "Notes",
        "verdict.recorded": "Recorded (UTC)",
        "verdict.history": "Verdict history",
        "verdict.agrees": "The reviewer agrees with the model.",
        "verdict.differs": "The reviewer regrades this patient.",
        "model.section": "Model and provenance",
        "model.model": "Model",
        "model.checkpoint": "Checkpoint",
        "model.loaded": "loaded",
        "model.notloaded": "NOT loaded - random-init weights",
        "model.input": "Input",
        "model.channels": "channels (RGB + FOV mask), preset",
        "model.device": "Device",
        "model.version": "Demo version",
        "images.section": "Input images",
        "images.none": "No images were recorded for this case.",
        "images.file": "File",
        "images.resolution": "Resolution",
        "images.sha": "SHA-256",
        "images.source": "Source",
        "images.check": "Fundus check",
        "images.received": "Received (UTC)",
        "pred.section": "Model prediction",
        "pred.none": "No model run was recorded for this case.",
        "pred.grade": "Patient grade (worst eye)",
        "pred.confidence": "Confidence",
        "pred.referable": "Referable DR (grade >= 2)",
        "pred.latency": "Inference latency",
        "pred.probs": "Class probabilities",
        "pred.pereye": "Per eye",
        "pred.run": "run",
        "pred.grade.col": "DR grade",
        "pred.prob.col": "Probability",
        "detect.section": "Optic disc / fovea detection",
        "detect.od": "Optic disc",
        "detect.fovea": "Fovea",
        "detect.axis": "OD-fovea axis",
        "detect.confident": "Detector confident",
        "detect.frame": "Frame",
        "corr.section": "Clinician OD / fovea corrections",
        "corr.rerun": "Pipeline re-run",
        "prep.section": "Preprocessing pipeline",
        "prep.intro": "The eight-stage pipeline is part of the model: these are the "
                      "images the CNN actually received.",
        "prep.channels": "CNN input tensor (4 channels)",
        "prep.none": "No preprocessing stages were cached for this case.",
        "att.section": "Attention maps (Grad-CAM)",
        "att.rationale": "Rationale",
        "att.coverage": "CAM coverage",
        "att.target": "Target grade",
        "att.region": "Region",
        "att.heatmap": "Grad-CAM heatmap",
        "att.overlay": "Attention overlay",
        "att.of_retina": "of the retina",
        "yes": "yes",
        "no": "no",
        "eye.right": "Right eye (OD)",
        "eye.left": "Left eye (OS)",
    },
    "kk": {
        "title": "Диабеттік ретинопатия скринингі туралы есеп",
        "subtitle": "Көз түбі суретін автоматты талдау және офтальмолог тексеруі",
        "case": "Іс",
        "generated": "Құрылған уақыты (UTC)",
        "created": "Іс ашылған уақыты (UTC)",
        "updated": "Соңғы жаңарту (UTC)",
        "disclaimer": "Зерттеу демонстрациясы. Медициналық құрал емес және диагноз емес.",
        "page": "Бет",
        "verdict.section": "Офтальмолог шешімі",
        "verdict.confirmed": "Болжамды офтальмолог РАСТАДЫ",
        "verdict.rejected": "Болжамды офтальмолог ҚАБЫЛДАМАДЫ",
        "verdict.none": "Бұл пациент бойынша шешім әлі тіркелмеген.",
        "verdict.model": "Модель дәрежесі",
        "verdict.final": "Офтальмолог дәрежесі",
        "verdict.reviewer": "Тексеруші",
        "verdict.notes": "Ескертпелер",
        "verdict.recorded": "Тіркелген уақыты (UTC)",
        "verdict.history": "Шешімдер тарихы",
        "verdict.agrees": "Тексеруші модель болжамымен келіседі.",
        "verdict.differs": "Тексеруші дәрежені өзгертті.",
        "model.section": "Модель және оның шығу тегі",
        "model.model": "Модель",
        "model.checkpoint": "Бақылау нүктесі",
        "model.loaded": "жүктелген",
        "model.notloaded": "ЖҮКТЕЛМЕГЕН - кездейсоқ салмақтар",
        "model.input": "Кіріс",
        "model.channels": "арна (RGB + FOV маскасы), пресет",
        "model.device": "Құрылғы",
        "model.version": "Демо нұсқасы",
        "images.section": "Кіріс кескіндер",
        "images.none": "Бұл іс бойынша кескіндер тіркелмеген.",
        "images.file": "Файл",
        "images.resolution": "Ажыратымдылық",
        "images.sha": "SHA-256",
        "images.source": "Дереккөз",
        "images.check": "Көз түбі тексерісі",
        "images.received": "Қабылданған уақыты (UTC)",
        "pred.section": "Модель болжамы",
        "pred.none": "Бұл іс бойынша модель жүрісі тіркелмеген.",
        "pred.grade": "Пациент дәрежесі (нашар көз)",
        "pred.confidence": "Сенімділік",
        "pred.referable": "Жіберуді талап ететін ДР (дәреже >= 2)",
        "pred.latency": "Есептеу уақыты",
        "pred.probs": "Сынып ықтималдықтары",
        "pred.pereye": "Әр көз бойынша",
        "pred.run": "жүріс",
        "pred.grade.col": "ДР дәрежесі",
        "pred.prob.col": "Ықтималдық",
        "detect.section": "Көру дискі / фовеа анықтамасы",
        "detect.od": "Көру дискі",
        "detect.fovea": "Фовеа",
        "detect.axis": "Диск-фовеа осі",
        "detect.confident": "Анықтағыш сенімді",
        "detect.frame": "Кадр",
        "corr.section": "Дәрігердің диск / фовеа түзетулері",
        "corr.rerun": "Құбырды қайта жүргізу",
        "prep.section": "Алдын ала өңдеу құбыры",
        "prep.intro": "Сегіз сатылы құбыр — модельдің бөлігі: бұл CNN нақты "
                      "қабылдаған кескіндер.",
        "prep.channels": "CNN кіріс тензоры (4 арна)",
        "prep.none": "Бұл іс бойынша өңдеу сатылары сақталмаған.",
        "att.section": "Назар карталары (Grad-CAM)",
        "att.rationale": "Негіздеме",
        "att.coverage": "CAM қамтуы",
        "att.target": "Мақсатты дәреже",
        "att.region": "Аймақ",
        "att.heatmap": "Grad-CAM жылу картасы",
        "att.overlay": "Назар қабаты",
        "att.of_retina": "тор қабықтан",
        "yes": "иә",
        "no": "жоқ",
        "eye.right": "Оң көз (OD)",
        "eye.left": "Сол көз (OS)",
    },
}

_GRADE_NAMES: dict[str, tuple[str, ...]] = {
    "en": ("No DR", "Mild NPDR", "Moderate NPDR", "Severe NPDR", "Proliferative DR"),
    "kk": ("ДР жоқ", "Жеңіл ПДР", "Орташа ПДР", "Ауыр ПДР", "Пролифератив ДР"),
}


def normalize_lang(lang: str | None) -> str:
    """Coerce a requested language tag to one the report has strings for."""
    value = (lang or "en").strip().lower().replace("_", "-").split("-")[0]
    return "kk" if value in ("kk", "kz") else "en"


class _T:
    """Label lookup bound to one language, falling back to English."""

    def __init__(self, lang: str) -> None:
        self.lang = lang
        self._table = _STRINGS[lang]

    def __call__(self, key: str) -> str:
        return self._table.get(key, _STRINGS["en"].get(key, key))

    def grade(self, grade: object) -> str:
        """Render a DR grade as ``"2 - Moderate NPDR"``, or ``"-"`` when absent."""
        if grade is None:
            return "-"
        try:
            value = int(grade)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return str(grade)
        names = _GRADE_NAMES.get(self.lang, _GRADE_NAMES["en"])
        name = names[value] if 0 <= value < len(names) else "?"
        return f"{value} - {name}"


# ---------------------------------------------------------------------------
# Small formatting helpers
# ---------------------------------------------------------------------------


def _esc(value: object) -> str:
    """Escape a value for reportlab's mini-markup (Paragraph text is XML)."""
    text = str(value) if value not in (None, "") else "-"
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _fmt_xy(point: object) -> str:
    """Format an ``[x, y]`` pair as ``(x.x, y.y) px``."""
    if not isinstance(point, (list, tuple)) or len(point) < 2:
        return "-"
    return f"({float(point[0]):.1f}, {float(point[1]):.1f}) px"


def _fmt_bytes(count: object) -> str:
    """Human-readable byte count."""
    try:
        value = float(count)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return "-"
    if value < 1024:
        return f"{value:.0f} B"
    value /= 1024
    if value < 1024:
        return f"{value:.1f} KB"
    return f"{value / 1024:.1f} MB"


def _stage_caption(filename: str) -> str:
    """Turn a cached stage file name (``05_clahe.png``) into a panel caption."""
    stem = Path(filename).stem
    index, _, key = stem.partition("_")
    if not index.isdigit():
        key = stem
    label = _PANEL_LABELS.get(key)
    if label:
        return label
    if key == "fov_mask":
        return "3. FOV mask (4th channel)"
    return key.replace("_", " ").title()


_CHANNEL_CAPTIONS = {
    "ch_r": "Ch 0 - R", "ch_g": "Ch 1 - G",
    "ch_b": "Ch 2 - B", "ch_fov": "Ch 3 - FOV",
}


# ---------------------------------------------------------------------------
# Flowable builders
# ---------------------------------------------------------------------------


class _Styles:
    """The paragraph styles the report uses, bound to the resolved font."""

    def __init__(self) -> None:
        base = getSampleStyleSheet()["BodyText"]
        self.body = ParagraphStyle(
            "rBody", parent=base, fontName=_FONT, fontSize=8.5, leading=12, textColor=_INK,
        )
        self.small = ParagraphStyle(
            "rSmall", parent=self.body, fontSize=7.2, leading=9.5, textColor=_MUTED,
        )
        self.caption = ParagraphStyle(
            "rCaption", parent=self.small, alignment=TA_CENTER, fontSize=6.8, leading=8.5,
        )
        self.h1 = ParagraphStyle(
            "rH1", parent=base, fontName=_FONT_BOLD, fontSize=15, leading=18,
            textColor=_INK, spaceAfter=2,
        )
        self.h2 = ParagraphStyle(
            "rH2", parent=base, fontName=_FONT_BOLD, fontSize=10.5, leading=13,
            textColor=_TEAL, spaceBefore=10, spaceAfter=4,
        )
        self.h3 = ParagraphStyle(
            "rH3", parent=base, fontName=_FONT_BOLD, fontSize=8.5, leading=11,
            textColor=_INK, spaceBefore=4, spaceAfter=2,
        )
        self.lead = ParagraphStyle(
            "rLead", parent=self.body, fontName=_FONT_BOLD, fontSize=11.5, leading=14,
        )


def _rule() -> Table:
    """A thin full-width horizontal rule."""
    line = Table([[""]], colWidths=[_CONTENT_W], rowHeights=[0.6])
    line.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), _RULE)]))
    return line


def _heading(text: str, st: _Styles) -> list:
    """A section heading with its underline."""
    return [Paragraph(_esc(text), st.h2), _rule(), Spacer(1, 4)]


def _kv_table(
    rows: list[tuple[str, object]],
    st: _Styles,
    key_w: float = 38 * mm,
    total_width: float = _CONTENT_W,
) -> Table:
    """A two-column ``label / value`` table.

    ``total_width`` must be the width actually available: these tables are also
    nested inside padded boxes and next to thumbnails, where assuming the full
    content width would run the striped rows out past their container.
    """
    data = [
        [Paragraph(f"<b>{_esc(k)}</b>", st.small), Paragraph(_esc(v), st.body)]
        for k, v in rows
    ]
    table = Table(data, colWidths=[key_w, total_width - key_w], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, _ROW_BG]),
    ]))
    return table


def _image_flowable(path: Path, width: float, max_height: float | None = None) -> Image | None:
    """Scale an on-disk image to ``width`` (and at most ``max_height``).

    Args:
        path: The image file inside the case directory.
        width: Target width in points.
        max_height: Cap on the rendered height; the width shrinks to keep the
            aspect ratio when it bites.

    Returns:
        The flowable, or ``None`` when the file is missing or unreadable — a
        case whose artifacts were partly pruned still produces a report, minus
        those panels.
    """
    try:
        with PILImage.open(path) as im:
            iw, ih = im.size
            if not iw or not ih:
                return None
            height = width * ih / iw
            if max_height and height > max_height:
                width, height = max_height * iw / ih, max_height
            frame = im.convert("RGB")
            cap = max(1, round(width / 72 * _TARGET_DPI))
            if iw > cap:
                frame = frame.resize((cap, max(1, round(ih * cap / iw))), PILImage.LANCZOS)
            buf = io.BytesIO()
            frame.save(buf, format="JPEG", quality=_JPEG_QUALITY, optimize=True)
    except Exception:  # noqa: BLE001 — a missing panel must not fail the report
        return None
    buf.seek(0)
    return Image(buf, width=width, height=height)


def _image_grid(
    items: list[tuple[Path, str]],
    st: _Styles,
    cols: int = _GRID_COLS,
    total_width: float = _CONTENT_W,
) -> list:
    """Lay captioned images out on a grid, dropping any that cannot be read."""
    cell_w = (total_width - _GRID_GAP * (cols - 1)) / cols
    cells: list[list] = []
    for path, caption in items:
        img = _image_flowable(path, cell_w, max_height=cell_w * 1.15)
        if img is None:
            continue
        block = [img]
        if caption:
            block += [Spacer(1, 1.5), Paragraph(_esc(caption), st.caption)]
        cells.append(block)
    if not cells:
        return []

    rows: list[list] = [cells[i:i + cols] for i in range(0, len(cells), cols)]
    rows[-1] += [""] * (cols - len(rows[-1]))
    table = Table(rows, colWidths=[cell_w + _GRID_GAP] * cols, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), _GRID_GAP),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return [table]


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------


def _latest_verdict(record: dict) -> dict | None:
    """The reviewer's standing word on this patient — their most recent verdict."""
    feedback = record.get("feedback") or []
    return feedback[-1] if feedback else None


def _verdict_banner(record: dict, st: _Styles, t: _T) -> list:
    """The headline block: what the ophthalmologist decided, and against what.

    This sits above the model's own output on purpose. The report is produced
    *after* the review, so the reviewer's conclusion — not the prediction — is
    the document's finding.
    """
    verdict = _latest_verdict(record)
    inner_w = _CONTENT_W - 20  # the box pads 10pt on each side
    if verdict is None:
        body: list = [Paragraph(_esc(t("verdict.none")), st.body)]
        frame = [("BACKGROUND", (0, 0), (-1, -1), _ROW_BG),
                 ("BOX", (0, 0), (-1, -1), 0.7, _RULE)]
    else:
        confirmed = verdict.get("verdict") == "confirmed"
        accent, background = (_GREEN, _GREEN_BG) if confirmed else (_RED, _RED_BG)
        mark = "\u2713" if confirmed else "\u2717"
        headline = ParagraphStyle("rVerdict", parent=st.lead, textColor=accent)
        key = "verdict.confirmed" if confirmed else "verdict.rejected"
        body = [
            Paragraph(f"{mark} {_esc(t(key))}", headline),
            Spacer(1, 3),
            _kv_table([
                (t("verdict.model"), t.grade(verdict.get("predicted_grade"))),
                (t("verdict.final"), t.grade(verdict.get("corrected_grade"))),
                (t("verdict.reviewer"), verdict.get("reviewer") or "-"),
                (t("verdict.notes"), verdict.get("notes") or "-"),
                (t("verdict.recorded"), verdict.get("recorded_utc") or "-"),
            ], st, key_w=42 * mm, total_width=inner_w),
            Spacer(1, 3),
            Paragraph(_esc(t("verdict.agrees") if confirmed else t("verdict.differs")), st.small),
        ]
        frame = [("BACKGROUND", (0, 0), (-1, -1), background),
                 ("BOX", (0, 0), (-1, -1), 0.9, accent)]

    box = Table([[body]], colWidths=[_CONTENT_W])
    box.setStyle(TableStyle(frame + [
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return _heading(t("verdict.section"), st) + [box, Spacer(1, 4)]


def _model_section(record: dict, st: _Styles, t: _T) -> list:
    """Which model produced the grades, and whether its weights were real."""
    model = record.get("model") or {}
    loaded = model.get("checkpoint_loaded")
    suffix = ""
    if loaded is True:
        suffix = f" ({t('model.loaded')})"
    elif loaded is False:
        suffix = f" ({t('model.notloaded')})"
    return _heading(t("model.section"), st) + [_kv_table([
        (t("model.model"), model.get("model") or "-"),
        (t("model.checkpoint"), f"{model.get('checkpoint') or '-'}{suffix}"),
        (t("model.input"), f"{model.get('in_channels', '?')} {t('model.channels')} "
                           f"{model.get('preset') or '-'}"),
        (t("model.device"), model.get("device") or "-"),
        (t("model.version"), f"{model.get('version') or '-'} "
                             f"(git {model.get('git_sha') or 'n/a'})"),
    ], st)]


def _images_section(record: dict, directory: Path, st: _Styles, t: _T) -> list:
    """The uploaded originals, each next to its provenance."""
    images = record.get("images") or {}
    out = _heading(t("images.section"), st)
    if not images:
        return out + [Paragraph(_esc(t("images.none")), st.small)]

    thumb_w = 44 * mm
    for side in ("right", "left"):
        entry = images.get(side)
        if not entry:
            continue
        checks = entry.get("client_checks") or {}
        fundus = checks.get("is_fundus")
        fundus_txt = {True: t("yes"), False: t("no")}.get(fundus, "-")
        conf = checks.get("laterality_confidence")
        conf_txt = f" ({float(conf):.2f})" if isinstance(conf, (int, float)) else ""
        sha = entry.get("sha256") or ""
        meta = _kv_table([
            (t("images.file"), f"{entry.get('filename') or '-'} "
                               f"({_fmt_bytes(entry.get('bytes'))})"),
            (t("images.resolution"), f"{entry.get('width', 0)} x {entry.get('height', 0)} px"),
            (t("images.check"), f"{fundus_txt}, {checks.get('laterality') or '-'}{conf_txt}"),
            (t("images.sha"), f"{sha[:40]}..." if len(sha) > 40 else (sha or "-")),
            (t("images.source"), entry.get("source") or "-"),
            (t("images.received"), entry.get("received_utc") or "-"),
        ], st, key_w=28 * mm, total_width=_CONTENT_W - thumb_w - 5 * mm)

        thumb = _image_flowable(directory / (entry.get("stored_file") or ""),
                                thumb_w, max_height=44 * mm)
        row = Table(
            [[[thumb] if thumb else [Paragraph("-", st.small)],
              [Paragraph(f"<b>{_esc(t('eye.' + side))}</b>", st.h3), meta]]],
            colWidths=[thumb_w + 5 * mm, _CONTENT_W - thumb_w - 5 * mm], hAlign="LEFT",
        )
        row.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        out.append(KeepTogether(row))
    return out


def _prob_bar(fraction: float, width: float, highlight: bool) -> Table:
    """A probability bar drawn as a two-cell table (filled / track)."""
    fraction = max(0.0, min(1.0, float(fraction)))
    filled = max(0.4, width * fraction)
    bar = Table([["", ""]], colWidths=[filled, max(0.4, width - filled)], rowHeights=[4.5])
    bar.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), _TEAL if highlight else _MUTED),
        ("BACKGROUND", (1, 0), (1, 0), _ROW_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return bar


def _prediction_section(record: dict, st: _Styles, t: _T) -> list:
    """The model's grade, its probability distribution and the per-eye split."""
    runs = record.get("predictions") or []
    out = _heading(t("pred.section"), st)
    if not runs:
        return out + [Paragraph(_esc(t("pred.none")), st.small)]

    run = runs[-1]  # the run the verdict judged is the case's latest
    pred = run.get("pred")
    confidence = float(run.get("confidence") or 0.0)
    out.append(_kv_table([
        (t("pred.grade"), t.grade(pred)),
        (t("pred.confidence"), f"{confidence * 100:.1f}%"),
        (t("pred.referable"), t("yes") if isinstance(pred, int) and pred >= 2 else t("no")),
        (t("pred.latency"), f"{run.get('latency_ms', 0)} ms "
                            f"({t('pred.run')} {run.get('index', '?')}, "
                            f"{run.get('run_utc', '-')})"),
    ], st, key_w=52 * mm))
    out.append(Spacer(1, 6))

    bar_w = 52 * mm
    label_w = 52 * mm
    rows: list[list] = [[
        Paragraph(f"<b>{_esc(t('pred.grade.col'))}</b>", st.small), "",
        Paragraph(f"<b>{_esc(t('pred.prob.col'))}</b>", st.small),
    ]]
    for idx, prob in enumerate(run.get("probs") or []):
        value = f"{float(prob) * 100:.2f}%"
        rows.append([
            Paragraph(_esc(t.grade(idx)), st.body),
            _prob_bar(float(prob), bar_w, idx == pred),
            Paragraph(f"<b>{value}</b>" if idx == pred else value, st.body),
        ])
    table = Table(rows, hAlign="LEFT",
                  colWidths=[label_w, bar_w + 4 * mm, _CONTENT_W - label_w - bar_w - 4 * mm])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, _RULE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, _ROW_BG]),
    ]))
    out += [Paragraph(f"<b>{_esc(t('pred.probs'))}</b>", st.h3), table]

    per_eye = run.get("per_eye") or []
    if per_eye:
        eye_rows = [[
            Paragraph(_esc(t("eye." + str(item.get("eye", "left")))), st.body),
            Paragraph(_esc(t.grade(item.get("pred"))), st.body),
            Paragraph(f"{float(item.get('confidence') or 0) * 100:.1f}%", st.body),
            Paragraph(f"{item.get('latency_ms', 0)} ms", st.body),
        ] for item in per_eye]
        eye_table = Table(eye_rows, hAlign="LEFT",
                          colWidths=[42 * mm, 48 * mm, 24 * mm, _CONTENT_W - 114 * mm])
        eye_table.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, _ROW_BG]),
        ]))
        out += [Spacer(1, 6), Paragraph(f"<b>{_esc(t('pred.pereye'))}</b>", st.h3), eye_table]
    return out


def _detection_section(record: dict, st: _Styles, t: _T) -> list:
    """What the OD/fovea detector found, and any clinician correction of it."""
    detection = record.get("detection") or {}
    corrections = record.get("corrections") or []
    out: list = []

    if detection:
        out += _heading(t("detect.section"), st)
        for side in ("right", "left"):
            det = detection.get(side)
            if not det:
                continue
            out.append(Paragraph(f"<b>{_esc(t('eye.' + side))}</b>", st.h3))
            out.append(_kv_table([
                (t("detect.od"), f"{_fmt_xy(det.get('od_center'))}, r="
                                 f"{float(det.get('od_radius') or 0):.1f} px, "
                                 f"conf {float(det.get('od_confidence') or 0):.3f}"),
                (t("detect.fovea"), f"{_fmt_xy(det.get('fovea_center'))}, r="
                                    f"{float(det.get('fovea_radius') or 0):.1f} px, "
                                    f"conf {float(det.get('fovea_confidence') or 0):.3f}"),
                (t("detect.axis"), f"{float(det.get('angle_deg') or 0):.2f} deg "
                                   f"(sigma {float(det.get('rotation_sigma_deg') or 0):.2f} deg)"),
                (t("detect.confident"), t("yes") if det.get("confident") else t("no")),
                (t("detect.frame"), f"{det.get('space_w', 0)} x {det.get('space_h', 0)} px"),
            ], st, key_w=34 * mm))
            out.append(Spacer(1, 3))

    if corrections:
        out += _heading(t("corr.section"), st)
        for corr in corrections:
            side = str(corr.get("eye", "left"))
            out.append(Paragraph(
                f"<b>{_esc(corr.get('index', '?'))}. {_esc(t('eye.' + side))}</b> "
                f"&#183; {_esc(corr.get('recorded_utc', '-'))}", st.h3))
            out.append(_kv_table([
                (t("detect.od"), f"{_fmt_xy(corr.get('od_detected'))} \u2192 "
                                 f"{_fmt_xy(corr.get('od_corrected'))}"),
                (t("detect.fovea"), f"{_fmt_xy(corr.get('fovea_detected'))} \u2192 "
                                    f"{_fmt_xy(corr.get('fovea_corrected'))}"),
                (t("corr.rerun"), corr.get("preprocessing_dir") or "-"),
            ], st, key_w=34 * mm))
            out.append(Spacer(1, 3))
    return out


def _preprocessing_section(record: dict, directory: Path, st: _Styles, t: _T) -> list:
    """Every cached pipeline stage as a picture — the feature space the CNN saw."""
    preprocessing = record.get("preprocessing") or {}
    out = _heading(t("prep.section"), st) + [
        Paragraph(_esc(t("prep.intro")), st.small), Spacer(1, 5),
    ]
    if not preprocessing:
        return out + [Paragraph(_esc(t("prep.none")), st.small)]

    for key in sorted(preprocessing):
        entry = preprocessing[key]
        side = str(entry.get("eye", "left"))
        variant = entry.get("variant") or ""
        title = t("eye." + side) + (f" \u00b7 {variant}" if variant else "")
        out.append(Paragraph(f"<b>{_esc(title)}</b>", st.h3))

        stages: list[tuple[Path, str]] = []
        channels: list[tuple[Path, str]] = []
        for rel in entry.get("files") or []:
            name = Path(rel).name
            if name == "preview_strip.png":
                continue  # the strip is only these panels glued together
            if "/input_channels/" in rel:
                channels.append((directory / rel,
                                 _CHANNEL_CAPTIONS.get(Path(name).stem, Path(name).stem)))
            else:
                stages.append((directory / rel, _stage_caption(name)))

        out += _image_grid(stages, st)
        if channels:
            out.append(Paragraph(f"<b>{_esc(t('prep.channels'))}</b>", st.h3))
            out += _image_grid(sorted(channels, key=lambda c: c[1]), st, cols=4)
        out.append(Spacer(1, 4))
    return out


def _attention_section(record: dict, directory: Path, st: _Styles, t: _T) -> list:
    """Grad-CAM heatmap and overlay per eye, with the CAM geometry behind them."""
    attention = record.get("attention") or {}
    if not attention:
        return []
    blocks: list = []
    for side in ("right", "left"):
        att = attention.get(side)
        if not att:
            continue
        area = att.get("cam_area_frac")
        area_txt = (f"{float(area) * 100:.2f}% {t('att.of_retina')} "
                    f"({att.get('cam_pixel_count', 0)} px)"
                    if isinstance(area, (int, float)) else "-")
        block: list = [
            Paragraph(f"<b>{_esc(t('eye.' + side))}</b>", st.h3),
            _kv_table([
                (t("att.target"), t.grade(att.get("target_class"))),
                (t("att.rationale"), att.get("rationale") or "-"),
                (t("att.coverage"), area_txt),
                (t("att.region"), att.get("cam_region") or "-"),
            ], st, key_w=34 * mm),
        ]
        panels = []
        for rel in att.get("files") or []:
            stem = Path(rel).stem
            caption = (t("att.overlay") if stem.endswith("attention_overlay")
                       else t("att.heatmap") if stem.endswith("gradcam")
                       else stem.replace(f"{side}_", "").replace("_", " "))
            panels.append((directory / rel, caption))
        block += _image_grid(panels, st, cols=2, total_width=_CONTENT_W * 0.62)
        blocks.append(KeepTogether(block))

    if not blocks:
        return []
    # Keep the section heading with the first eye, so it never ends a page alone.
    return [KeepTogether(_heading(t("att.section"), st) + [blocks[0]])] + blocks[1:]


def _verdict_history(record: dict, st: _Styles, t: _T) -> list:
    """Every verdict on this patient, in order — a regrade leaves both entries."""
    feedback = record.get("feedback") or []
    if len(feedback) < 2:
        return []  # a single standing verdict is already the banner
    rows = [[
        Paragraph(f"<b>{_esc(item.get('index', '?'))}</b>", st.small),
        Paragraph(_esc(item.get("recorded_utc", "-")), st.small),
        Paragraph(_esc(t("verdict.confirmed") if item.get("verdict") == "confirmed"
                        else t("verdict.rejected") if item.get("verdict") == "rejected"
                        else "-"), st.small),
        Paragraph(_esc(t.grade(item.get("predicted_grade"))), st.small),
        Paragraph(_esc(t.grade(item.get("corrected_grade"))), st.small),
    ] for item in feedback]
    table = Table(rows, hAlign="LEFT",
                  colWidths=[8 * mm, 32 * mm, 60 * mm, 32 * mm, _CONTENT_W - 132 * mm])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, _ROW_BG]),
    ]))
    return _heading(t("verdict.history"), st) + [table]


# ---------------------------------------------------------------------------
# Document
# ---------------------------------------------------------------------------


def _title_block(record: dict, st: _Styles, t: _T) -> list:
    """Report title, patient case identity and the timestamps around it."""
    return [
        Paragraph(_esc(t("title")), st.h1),
        Paragraph(_esc(t("subtitle")), st.small),
        Spacer(1, 6), _rule(), Spacer(1, 5),
        _kv_table([
            (t("case"), record.get("case_id", "-")),
            (t("created"), record.get("created_utc", "-")),
            (t("updated"), record.get("updated_utc", "-")),
            (t("generated"), datetime.now(timezone.utc).isoformat(timespec="seconds")),
        ], st, key_w=44 * mm),
        Spacer(1, 6),
    ]


def _page_furniture(case_id: str, t: _T):
    """Build the per-page callback drawing the footer rule, note and page number."""

    def draw(canvas, doc) -> None:
        canvas.saveState()
        y = _MARGIN - 6 * mm
        canvas.setStrokeColor(_RULE)
        canvas.setLineWidth(0.5)
        canvas.line(_MARGIN, y + 4 * mm, _PAGE[0] - _MARGIN, y + 4 * mm)
        canvas.setFont(_FONT, 6.8)
        canvas.setFillColor(_MUTED)
        canvas.drawString(_MARGIN, y, f"{t('disclaimer')}  \u00b7  {case_id}")
        canvas.drawRightString(_PAGE[0] - _MARGIN, y, f"{t('page')} {doc.page}")
        canvas.restoreState()

    return draw


def build_case_report(record: dict, directory: Path, lang: str = "en") -> bytes:
    """Render one case record and its stored artifacts as a PDF.

    Args:
        record: The case record, as held in ``case.json``.
        directory: The case directory the record's relative file paths resolve
            against. Missing artifacts are skipped, never fatal.
        lang: ``"en"`` or ``"kk"``; anything else falls back to English.

    Returns:
        The PDF document as bytes.
    """
    _register_fonts()
    st = _Styles()
    t = _T(normalize_lang(lang))
    case_id = str(record.get("case_id", "-"))

    # Page 1 is the clinical summary — verdict, grade, the images it was given.
    story: list = []
    story += _title_block(record, st, t)
    story += _verdict_banner(record, st, t)
    story += _prediction_section(record, st, t)
    story += _images_section(record, directory, st, t)
    story += _model_section(record, st, t)
    story += _verdict_history(record, st, t)

    # What follows is the evidence: how the images were transformed, where the
    # detector put the landmarks and what the network attended to.
    appendix: list = []
    appendix += _detection_section(record, st, t)
    appendix += _preprocessing_section(record, directory, st, t)
    appendix += _attention_section(record, directory, st, t)
    if appendix:
        story.append(PageBreak())
        story += appendix

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=_PAGE,
        leftMargin=_MARGIN, rightMargin=_MARGIN,
        topMargin=_MARGIN, bottomMargin=_MARGIN + 4 * mm,
        title=f"DR report {case_id}", author="DR-Classifier demo",
        subject=t("title"),
    )
    furniture = _page_furniture(case_id, t)
    doc.build(story, onFirstPage=furniture, onLaterPages=furniture)
    return buffer.getvalue()


def report_filename(case_id: str, lang: str = "en") -> str:
    """The download file name for one case's report."""
    return f"dr-report-{case_id}-{normalize_lang(lang)}.pdf"
