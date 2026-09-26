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
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image as PILImage
from PIL import ImageDraw
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    Flowable,
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

# Palette — the demo dashboard's own tokens (web/src/index.css), so the
# print-out and the screen read as one artifact: slate ink, slit-lamp cobalt
# for structure, and the ICDR grade ramp for everything clinical.
_INK = colors.HexColor("#16212C")
_MUTED = colors.HexColor("#5B6875")
_FAINT = colors.HexColor("#8793A0")
_RULE = colors.HexColor("#DDE2E7")
_COBALT = colors.HexColor("#2340B8")
_ROW_BG = colors.HexColor("#F4F6F7")
_SLATE = (26, 35, 44)  # letterbox behind photographs, as on screen

# ICDR grade 0..4: healthy-retina teal to haemorrhage red, and the same hues
# darkened for text. Mirrors GRADE_COLORS / GRADE_INK in web/src/data.js.
_GRADE = [colors.HexColor(c) for c in ("#3E7C74", "#8A9A3B", "#C98A1B", "#C4521F", "#9E1F24")]
_GRADE_INK = [colors.HexColor(c) for c in ("#2C5F58", "#5A6620", "#855709", "#973A11", "#7E1519")]
_GRADE_WASH = [colors.HexColor(c) for c in ("#E3F0EE", "#EEF1DF", "#F8EFDC", "#F8E9E1", "#F9ECEC")]
# Kept for callers of the old names.
_TEAL = _GRADE_INK[0]
_GREEN, _GREEN_BG = _GRADE_INK[0], _GRADE_WASH[0]
_RED, _RED_BG = _GRADE_INK[4], _GRADE_WASH[4]

_PAGE = A4
_MARGIN = 18 * mm
# SimpleDocTemplate's frame pads 6 pt on each side; tables anchored LEFT at the
# full margin-to-margin width overran the right margin by exactly that much.
_FRAME_PAD = 6
_CONTENT_W = _PAGE[0] - 2 * _MARGIN - 2 * _FRAME_PAD

# Grid geometry for the stage / channel / attention image strips.
_GRID_COLS = 4
_GRID_GAP = 4 * mm

# Panels are embedded at print resolution rather than at their stored size. A
# case holds ~30 512-px PNGs; embedding them verbatim produced a 10 MB report
# for pictures that are never printed larger than ~45 mm.
_TARGET_DPI = 170
_JPEG_QUALITY = 86

# Pre-rendered segmentation panels for the bundled sample images, written by
# `demo/web/scripts/prepare_segmentation_pairs.py`. The index maps the image id
# the client files an upload under to its fovea, disc diameter and the layers
# annotated for it, each measured on the full-size mask (area, foci, quadrants,
# distance to the fovea); a clinician's own photograph is not in it, and then the
# report simply has no such page.
_SEGMENTS_DIR = Path(__file__).resolve().parent / "segments"
_SEGMENT_ORDER = (
    "optic-disc", "microaneurysms", "haemorrhages", "hard-exudates", "soft-exudates",
)
_SEGMENT_INDEX: dict[str, dict] | None = None  # loaded on first report

_FONT = "Helvetica"
_FONT_MEDIUM = "Helvetica"
_FONT_SEMI = "Helvetica-Bold"
_FONT_BOLD = "Helvetica-Bold"

# The report's own typeface: Golos Text (SIL OFL, fonts/OFL.txt), the family
# the dashboard is set in. It is Cyrillic-first and carries every Kazakh letter.
_FONT_DIR = Path(__file__).resolve().parent / "fonts"
_GOLOS = {
    "ReportSans": "GolosText-Regular.ttf",
    "ReportSans-Medium": "GolosText-Medium.ttf",
    "ReportSans-SemiBold": "GolosText-SemiBold.ttf",
    "ReportSans-Bold": "GolosText-Bold.ttf",
}

# Fallback regular/bold TrueType pairs, used only when the bundled family is
# missing. The first ships inside the server's virtualenv (matplotlib bundles
# DejaVu); the second covers a bare Windows box. Both carry Kazakh Cyrillic.
_FONT_CANDIDATES: tuple[tuple[str, str], ...] = (
    ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf"),
    ("arial.ttf", "arialbd.ttf"),
)


def _font_search_dirs() -> list[Path]:
    """Directories to look for a fallback Unicode TrueType font in."""
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
    """Register the report typeface as ``ReportSans*``, or keep Helvetica.

    Tries the bundled Golos Text family first, then a DejaVu/Arial pair. Kazakh
    (``ә ғ қ ң ө ұ ү һ і``) is unrepresentable in reportlab's built-in Type-1
    fonts, which would silently print black boxes; when no TrueType font can be
    found the report still renders — in Helvetica, which is correct for the
    English report and merely degraded for the Kazakh one.
    """
    global _FONT, _FONT_MEDIUM, _FONT_SEMI, _FONT_BOLD
    if _FONT != "Helvetica":  # already registered
        return
    try:
        for name, filename in _GOLOS.items():
            pdfmetrics.registerFont(TTFont(name, str(_FONT_DIR / filename)))
        pdfmetrics.registerFontFamily(
            "ReportSans", normal="ReportSans", bold="ReportSans-SemiBold",
            italic="ReportSans", boldItalic="ReportSans-SemiBold",
        )
        _FONT, _FONT_MEDIUM = "ReportSans", "ReportSans-Medium"
        _FONT_SEMI, _FONT_BOLD = "ReportSans-SemiBold", "ReportSans-Bold"
        return
    except Exception:  # noqa: BLE001 — fall through to the system candidates
        pass
    for regular, bold in _FONT_CANDIDATES:
        for directory in _font_search_dirs():
            reg_path, bold_path = directory / regular, directory / bold
            if not reg_path.is_file():
                continue
            try:
                pdfmetrics.registerFont(TTFont("ReportFallback", str(reg_path)))
                pdfmetrics.registerFont(TTFont(
                    "ReportFallback-Bold", str(bold_path if bold_path.is_file() else reg_path)
                ))
                pdfmetrics.registerFontFamily(
                    "ReportFallback", normal="ReportFallback", bold="ReportFallback-Bold",
                    italic="ReportFallback", boldItalic="ReportFallback-Bold",
                )
            except Exception:  # noqa: BLE001 — try the next candidate
                continue
            _FONT = _FONT_MEDIUM = "ReportFallback"
            _FONT_SEMI = _FONT_BOLD = "ReportFallback-Bold"
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
        "verdict.confirmed": "Confirmed by the ophthalmologist",
        "verdict.rejected": "Regraded by the ophthalmologist",
        "verdict.pending": "Awaiting the ophthalmologist's review",
        "verdict.finding": "Finding",
        "grade.of": "Grade {g} of 4 on the ICDR scale",
        "refer.yes": "Refer to an ophthalmologist",
        "refer.no": "No referral needed",
        "scale.title": "Model probability for each ICDR grade",
        "scale.threshold": "Referable from here",
        "page.of": "Page {n} of {m}",
        "evidence": "Evidence",
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
        "model.notloaded": "not loaded, random-init weights",
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
        "pred.referable": "Referable DR (grade ≥ 2)",
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
        "seg.section": "Annotated structures and lesions",
        "seg.optic-disc": "Optic disc",
        "seg.microaneurysms": "Microaneurysms",
        "seg.haemorrhages": "Haemorrhages",
        "seg.hard-exudates": "Hard exudates",
        "seg.soft-exudates": "Soft exudates",
        "seg.finding": "Finding",
        "seg.absent": "Not detected",
        "seg.foci": "foci",
        "seg.quadrants": "quadrants",
        "seg.of_field": "of the retinal field",
        "seg.nearest": "nearest {d} DD from the fovea",
        "seg.in_macula": "{n} in the macula",
        "seg.macula_clear": "macula clear",
        "seg.dme": "Macular oedema risk (IDRiD, 0\u20132)",
        "seg.about.optic-disc": "Entry of the optic nerve and retinal vessels. Its diameter (DD, "
                                "\u22481.8 mm) and area (DA, \u22482.5 mm\u00b2) are the units "
                                "used on this page; percentages are shares of the retinal "
                                "field. The white ring marks the macula: 1 DD around the "
                                "fovea.",
        "seg.about.microaneurysms": "Saccular bulges of capillary walls, 25\u2013125 \u00b5m "
                                    "across: the earliest visible sign of diabetic retinopathy. "
                                    "A rising count signals progression.",
        "seg.about.haemorrhages": "Blood leaked from damaged vessels into the retina. The "
                                  "quadrants they reach grade the non-proliferative stage: more "
                                  "than 20 in each of four means severe (4-2-1 rule).",
        "seg.about.hard-exudates": "Lipid and protein deposits left by leaking vessels. Near "
                                   "the fovea they signal macular oedema, the main cause of "
                                   "vision loss in diabetes: risk 1 with exudates outside the "
                                   "macula, 2 within 1 DD of the fovea.",
        "seg.about.soft-exudates": "Cotton-wool spots: swelling of the nerve-fibre layer where "
                                   "capillaries have closed. They mark retinal ischaemia and "
                                   "often precede progression.",
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
        "verdict.confirmed": "Офтальмолог растады",
        "verdict.rejected": "Офтальмолог дәрежені өзгертті",
        "verdict.pending": "Офтальмолог тексеруін күтуде",
        "verdict.finding": "Қорытынды",
        "grade.of": "ICDR шкаласы бойынша {g}-дәреже (0–4)",
        "refer.yes": "Офтальмологқа жіберу керек",
        "refer.no": "Жіберу қажет емес",
        "scale.title": "Әр ICDR дәрежесіне модель ықтималдығы",
        "scale.threshold": "Осыдан бастап жіберіледі",
        "page.of": "{n}-бет, барлығы {m}",
        "evidence": "Дәлелдер",
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
        "model.notloaded": "жүктелмеген, кездейсоқ салмақтар",
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
        "pred.referable": "Жіберуді талап ететін ДР (дәреже ≥ 2)",
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
        "seg.section": "Белгіленген құрылымдар мен зақымданулар",
        "seg.optic-disc": "Көру жүйкесінің дискісі",
        "seg.microaneurysms": "Микроаневризмалар",
        "seg.haemorrhages": "Қан құйылулар",
        "seg.hard-exudates": "Қатты экссудаттар",
        "seg.soft-exudates": "Жұмсақ экссудаттар",
        "seg.finding": "Белгі",
        "seg.absent": "Анықталмады",
        "seg.foci": "ошақ",
        "seg.quadrants": "квадрант",
        "seg.of_field": "тор қабық аумағынан",
        "seg.nearest": "фовеаға ең жақыны {d} ДД",
        "seg.in_macula": "макулада {n}",
        "seg.macula_clear": "макула таза",
        "seg.dme": "Макулярлы ісіну қаупі (IDRiD, 0\u20132)",
        "seg.about.optic-disc": "Көру жүйкесі мен тор қабық тамырларының кіру орны. Оның "
                                "диаметрі (ДД, \u22481,8 мм) мен ауданы (ДА, \u22482,5 мм\u00b2) "
                                "осы беттегі өлшем бірліктері; пайыздар — тор қабық "
                                "аумағының үлесі. Ақ сақина — макула: фовеа айналасындағы "
                                "1 ДД аймақ.",
        "seg.about.microaneurysms": "Капилляр қабырғаларының 25\u2013125 мкм қапшық тәрізді "
                                    "кеңеюлері — диабеттік ретинопатияның ең ерте көрінетін "
                                    "белгісі. Санының өсуі аурудың үдеуін көрсетеді.",
        "seg.about.haemorrhages": "Зақымданған тамырлардан тор қабыққа құйылған қан. Олар "
                                  "таралған квадранттар саны пролиферативті емес сатыны анықтайды: "
                                  "төртеуінің әрқайсысында 20-дан көп болса — ауыр саты "
                                  "(4-2-1 ережесі).",
        "seg.about.hard-exudates": "Өткізгіштігі бұзылған тамырлардан бөлінген липид пен ақуыз шөгінділері. "
                                   "Фовеаға жақын болса, макулярлы ісінуді — диабетте көру "
                                   "қабілетін жоғалтудың басты себебін — білдіреді: макуладан "
                                   "тыс болса қауіп 1, фовеадан 1 ДД ішінде болса 2.",
        "seg.about.soft-exudates": "Мақта тәрізді ошақтар — капиллярлар бітелген жердегі жүйке "
                                   "талшықтары қабатының ісінуі. Тор қабық ишемиясын көрсетеді "
                                   "және жиі ауру үдеуінің алдында пайда болады.",
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

    def name(self, grade: int) -> str:
        """The bare grade name, e.g. ``"Moderate NPDR"``."""
        names = _GRADE_NAMES.get(self.lang, _GRADE_NAMES["en"])
        return names[grade] if 0 <= grade < len(names) else "?"

    def grade(self, grade: object) -> str:
        """Render a DR grade as ``"2 – Moderate NPDR"``, or ``"-"`` when absent."""
        if grade is None:
            return "-"
        try:
            value = int(grade)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return str(grade)
        names = _GRADE_NAMES.get(self.lang, _GRADE_NAMES["en"])
        name = names[value] if 0 <= value < len(names) else "?"
        return f"{value} – {name}"


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


def _fmt_time(value: object) -> str:
    """``2026-08-31T08:33:52+00:00`` → ``2026-08-31 08:33:52`` (labels carry UTC)."""
    text = str(value or "")
    if len(text) >= 19 and text[10] == "T":
        return f"{text[:10]} {text[11:19]}"
    return text or "-"


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
    "ch_r": "Ch 0 – R", "ch_g": "Ch 1 – G",
    "ch_b": "Ch 2 – B", "ch_fov": "Ch 3 – FOV",
}


# ---------------------------------------------------------------------------
# Flowable builders
# ---------------------------------------------------------------------------


class _Styles:
    """The paragraph styles the report uses, bound to the resolved font."""

    def __init__(self) -> None:
        base = getSampleStyleSheet()["BodyText"]
        self.body = ParagraphStyle(
            "rBody", parent=base, fontName=_FONT, fontSize=8.8, leading=12.4, textColor=_INK,
        )
        self.small = ParagraphStyle(
            "rSmall", parent=self.body, fontSize=7.6, leading=10, textColor=_MUTED,
        )
        self.key = ParagraphStyle("rKey", parent=self.small, textColor=_MUTED)
        self.caption = ParagraphStyle(
            "rCaption", parent=self.small, alignment=TA_CENTER, fontSize=7, leading=9,
        )
        self.h1 = ParagraphStyle(
            "rH1", parent=base, fontName=_FONT_BOLD, fontSize=17, leading=20,
            textColor=_INK, spaceAfter=1,
        )
        self.h2 = ParagraphStyle(
            "rH2", parent=base, fontName=_FONT_SEMI, fontSize=11.5, leading=14,
            textColor=_INK, spaceBefore=12, spaceAfter=3,
        )
        self.h3 = ParagraphStyle(
            "rH3", parent=base, fontName=_FONT_SEMI, fontSize=8.8, leading=11.5,
            textColor=_INK, spaceBefore=5, spaceAfter=2,
        )
        self.lead = ParagraphStyle(
            "rLead", parent=self.body, fontName=_FONT_SEMI, fontSize=11, leading=14,
        )
        self.grade = ParagraphStyle(
            "rGrade", parent=base, fontName=_FONT_BOLD, fontSize=25, leading=28, textColor=_INK,
        )
        self.meta = ParagraphStyle(
            "rMeta", parent=self.small, alignment=TA_RIGHT, leading=10.5,
        )
        self.eye = ParagraphStyle(
            "rEye", parent=self.body, fontName=_FONT_BOLD, fontSize=12, leading=14,
        )


def _rule(color=_RULE, weight: float = 0.6, width: float = _CONTENT_W) -> Table:
    """A full-width horizontal rule."""
    line = Table([[""]], colWidths=[width], rowHeights=[weight])
    line.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return line


def _heading(text: str, st: _Styles) -> list:
    """A section heading over a hairline."""
    return [Paragraph(_esc(text), st.h2), _rule(), Spacer(1, 5)]


def _kv_table(
    rows: list[tuple[str, object]],
    st: _Styles,
    key_w: float = 38 * mm,
    total_width: float = _CONTENT_W,
) -> Table:
    """A two-column ``label / value`` table, rows divided by hairlines.

    ``total_width`` must be the width actually available: these tables are also
    nested inside columns and next to thumbnails, where assuming the full
    content width would run the rows out past their container.
    """
    data = [[Paragraph(_esc(k), st.key), Paragraph(_esc(v), st.body)] for k, v in rows]
    table = Table(data, colWidths=[key_w, total_width - key_w], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, _RULE),
    ]))
    return table


class _Mark(Flowable):
    """A verdict mark — tick or cross in a filled disc, drawn as vector paths.

    The report font has no ✓/✗ glyphs, and a drawn mark stays crisp at any zoom.
    """

    def __init__(self, kind: str, color, size: float = 11) -> None:
        super().__init__()
        self.kind, self.color, self.size = kind, color, size
        self.width = self.height = size

    def draw(self) -> None:
        c, r = self.canv, self.size / 2
        c.setFillColor(self.color)
        c.circle(r, r, r, stroke=0, fill=1)
        c.setStrokeColor(colors.white)
        c.setLineWidth(self.size * 0.13)
        c.setLineCap(1)
        c.setLineJoin(1)
        path = c.beginPath()
        if self.kind == "confirmed":
            path.moveTo(r * 0.52, r * 1.02)
            path.lineTo(r * 0.86, r * 0.66)
            path.lineTo(r * 1.5, r * 1.36)
        elif self.kind == "rejected":
            path.moveTo(r * 0.62, r * 0.62)
            path.lineTo(r * 1.38, r * 1.38)
            path.moveTo(r * 1.38, r * 0.62)
            path.lineTo(r * 0.62, r * 1.38)
        else:  # pending: a clock-like open ring
            c.setFillColor(colors.white)
            c.circle(r, r, r * 0.22, stroke=0, fill=1)
        c.drawPath(path, stroke=1, fill=0)


class _Pill(Flowable):
    """A rounded label with a leading dot — the referral call."""

    def __init__(self, text: str, fg, bg, font_size: float = 8.6) -> None:
        super().__init__()
        self.text, self.fg, self.bg, self.fs = text, fg, bg, font_size
        self.height = font_size + 8
        self.width = pdfmetrics.stringWidth(text, _FONT_SEMI, font_size) + 26

    def draw(self) -> None:
        c, h = self.canv, self.height
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self.width, h, h / 2, stroke=0, fill=1)
        c.setFillColor(self.fg)
        c.circle(9, h / 2, 2.6, stroke=0, fill=1)
        c.setFont(_FONT_SEMI, self.fs)
        c.drawString(16, h / 2 - self.fs * 0.35, self.text)


class _GradeScale(Flowable):
    """The ICDR grade scale — the report's signature figure, as on screen.

    Five steps in the grade ramp, the model's probability standing on each as a
    column (scaled to the tallest; percentages carry the absolute values), the
    predicted grade in full colour, the others washed out, and the referral
    threshold dashed between grade 1 and grade 2.
    """

    def __init__(self, probs: list[float], pred: int | None, t: "_T",
                 width: float = _CONTENT_W, col_h: float = 24 * mm) -> None:
        super().__init__()
        self.probs = [max(0.0, float(p)) for p in probs][:5]
        self.pred, self.t, self.col_h = pred, t, col_h
        self.width = width
        self.gap = 2.2 * mm
        self.track_h = 2.4 * mm
        self.height = col_h + self.track_h + 17 * mm

    def draw(self) -> None:
        c, t = self.canv, self.t
        n = len(self.probs)
        if not n:
            return
        cw = (self.width - self.gap * (n - 1)) / n
        base = 15.5 * mm              # baseline of the columns (top of the track)
        top = max(self.probs) or 1.0
        label_font = 7.4

        for g, p in enumerate(self.probs):
            x = g * (cw + self.gap)
            is_pred = g == self.pred
            h = max(0.8, (p / top) * (self.col_h - 6 * mm))
            c.setFillColor(_GRADE[g] if is_pred else _GRADE_WASH[g])
            c.roundRect(x, base, cw, h, 1.6, stroke=0, fill=1)
            # square off the bottom so the column sits flush on the track
            c.rect(x, base, cw, min(h, 1.6), stroke=0, fill=1)
            # percentage above the column
            pct = f"{p * 100:.1f}%" if p < 0.1 else f"{p * 100:.0f}%"
            c.setFillColor(_INK if is_pred else _MUTED)
            c.setFont(_FONT_BOLD if is_pred else _FONT, 8.2 if is_pred else 7.6)
            c.drawCentredString(x + cw / 2, base + h + 2.2, pct)
            # the step of the scale itself
            c.setFillColor(_GRADE[g])
            c.rect(x, base - self.track_h, cw, self.track_h, stroke=0, fill=1)
            # grade number and name under the track
            c.setFillColor(_INK)
            c.setFont(_FONT_BOLD, 9.5)
            c.drawCentredString(x + cw / 2, base - self.track_h - 4.6 * mm, str(g))
            name = t.name(g)
            fs = label_font
            while fs > 5.6 and pdfmetrics.stringWidth(name, _FONT, fs) > cw - 2:
                fs -= 0.2
            c.setFillColor(_MUTED)
            c.setFont(_FONT, fs)
            c.drawCentredString(x + cw / 2, base - self.track_h - 8.6 * mm, name)

        # referral threshold: between grade 1 and grade 2
        tx = 2 * cw + 1.5 * self.gap
        c.setStrokeColor(_INK)
        c.setLineWidth(0.8)
        c.setDash(2.2, 1.8)
        c.line(tx, base - self.track_h - 1.5 * mm, tx, base + self.col_h + 1 * mm)
        c.setDash()
        c.setFillColor(_INK)
        c.setFont(_FONT_SEMI, 7.6)
        c.drawString(tx + 2.2 * mm, base + self.col_h - 1.8 * mm, t("scale.threshold"))


def _image_flowable(
    path: Path | io.BytesIO, width: float, max_height: float | None = None, box: bool = False,
) -> Image | None:
    """Scale an on-disk image to ``width`` (and at most ``max_height``).

    Args:
        path: The image file inside the case directory.
        width: Target width in points.
        max_height: Cap on the rendered height; the width shrinks to keep the
            aspect ratio when it bites.
        box: Letterbox the picture onto a ``width`` × ``max_height`` slate
            frame, so panels of different aspect ratios line up on a grid and
            the photograph's own black border stays distinguishable.

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
            frame = im.convert("RGB")
            if box and max_height:
                box_w, box_h = width, max_height
                scale = min(box_w / iw, box_h / ih)
                px_w = max(1, round(box_w / 72 * _TARGET_DPI))
                px_h = max(1, round(box_h / 72 * _TARGET_DPI))
                fit = (max(1, round(iw * scale / box_w * px_w)),
                       max(1, round(ih * scale / box_h * px_h)))
                canvas = PILImage.new("RGB", (px_w, px_h), _SLATE)
                canvas.paste(frame.resize(fit, PILImage.LANCZOS),
                             ((px_w - fit[0]) // 2, (px_h - fit[1]) // 2))
                frame, width, height = canvas, box_w, box_h
            else:
                height = width * ih / iw
                if max_height and height > max_height:
                    width, height = max_height * iw / ih, max_height
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
    cell_ratio: float = 1.0,
) -> list:
    """Lay captioned images out on a grid, dropping any that cannot be read.

    Args:
        cell_ratio: Cell height as a fraction of cell width. Square by default,
            which lines up panels of mixed aspect ratios; pass the pictures' own
            ratio when they all share one, to spend the page on retina rather
            than on letterbox.
    """
    cell_w = (total_width - _GRID_GAP * (cols - 1)) / cols
    cell_h = cell_w * cell_ratio
    cells: list[list] = []
    for path, caption in items:
        img = _image_flowable(path, cell_w, max_height=cell_h, box=True)
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


def _bare_eye(t: _T, side: str) -> str:
    """``"Right eye (OD)"`` → ``"Right eye"`` — the OD/OS code is set separately."""
    return t("eye." + side).split(" (")[0]


def _as_grade(value: object) -> int | None:
    try:
        g = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    return g if 0 <= g <= 4 else None


def _finding_section(record: dict, directory: Path, st: _Styles, t: _T) -> list:
    """Page one's headline: the finding on the left, the two photographs right.

    The report is produced *after* the review, so the reviewer's grade — not the
    prediction — is the document's finding and is set largest. Before a verdict
    exists the model's grade stands in, labelled as awaiting review.
    """
    verdict = _latest_verdict(record)
    runs = record.get("predictions") or []
    run = runs[-1] if runs else {}
    model_grade = _as_grade(run.get("pred"))

    if verdict is not None:
        kind = "confirmed" if verdict.get("verdict") == "confirmed" else "rejected"
        final = _as_grade(verdict.get("corrected_grade"))
        if final is None:
            final = _as_grade(verdict.get("predicted_grade"))
        status = t("verdict.confirmed" if kind == "confirmed" else "verdict.rejected")
    else:
        kind, final, status = "pending", model_grade, t("verdict.pending")

    left_w = _CONTENT_W * 0.52
    right_w = _CONTENT_W - left_w - 6 * mm
    mark_color = {"confirmed": _GRADE[0], "rejected": _GRADE[4]}.get(kind, _FAINT)
    status_style = ParagraphStyle("rStatus", parent=st.lead, fontSize=10,
                                  textColor=_GRADE_INK[0] if kind == "confirmed"
                                  else _GRADE_INK[4] if kind == "rejected" else _MUTED)
    status_row = Table([[_Mark(kind, mark_color, 11), Paragraph(_esc(status), status_style)]],
                       colWidths=[15, left_w - 15], hAlign="LEFT")
    status_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    left: list = [Paragraph(_esc(t("verdict.finding")), st.small), Spacer(1, 3), status_row,
                  Spacer(1, 7)]
    if final is None:
        left.append(Paragraph(_esc(t("pred.none")), st.body))
    else:
        grade_style = ParagraphStyle("rGradeC", parent=st.grade, textColor=_GRADE_INK[final])
        left += [
            Paragraph(_esc(t.name(final)), grade_style),
            Paragraph(_esc(t("grade.of").replace("{g}", str(final))), st.small),
            Spacer(1, 7),
            _Pill(t("refer.yes") if final >= 2 else t("refer.no"),
                  _GRADE_INK[3] if final >= 2 else _GRADE_INK[0],
                  _GRADE_WASH[3] if final >= 2 else _GRADE_WASH[0]),
        ]
    rows: list[tuple[str, object]] = []
    if verdict is not None:
        rows.append((t("verdict.model"), t.grade(verdict.get("predicted_grade"))))
        if verdict.get("reviewer"):
            rows.append((t("verdict.reviewer"), verdict.get("reviewer")))
        if verdict.get("notes"):
            rows.append((t("verdict.notes"), verdict.get("notes")))
        rows.append((t("verdict.recorded"), _fmt_time(verdict.get("recorded_utc"))))
    elif model_grade is not None:
        rows.append((t("verdict.model"), t.grade(model_grade)))
    if rows:
        left += [Spacer(1, 9), _kv_table(rows, st, key_w=34 * mm, total_width=left_w)]

    # The photographs, OD on the left as ophthalmologists lay a pair out.
    images = record.get("images") or {}
    cell_w = (right_w - 4 * mm) / 2
    heads, pics = [], []
    for side in ("right", "left"):
        entry = images.get(side)
        code = "OD" if side == "right" else "OS"
        heads.append(Paragraph(
            f'<font name="{_FONT_BOLD}" size="12">{code}</font>&nbsp;&nbsp;'
            f'<font color="#5B6875">{_esc(_bare_eye(t, side))}</font>', st.body))
        img = (_image_flowable(directory / (entry.get("stored_file") or ""), cell_w,
                               max_height=cell_w * 0.8, box=True) if entry else None)
        pics.append(img or Paragraph(_esc(t("images.none")) if not entry else "-", st.small))
    photos = Table([heads, pics], colWidths=[cell_w + 4 * mm, cell_w], hAlign="RIGHT")
    photos.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, -1), 4 * mm), ("RIGHTPADDING", (1, 0), (1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
    ]))

    block = Table([[left, photos]], colWidths=[left_w + 6 * mm, right_w], hAlign="LEFT")
    block.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return [block, Spacer(1, 6)]


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
    ], st, key_w=34 * mm)]


def _images_section(record: dict, directory: Path, st: _Styles, t: _T) -> list:
    """Provenance of the uploaded originals, the two eyes side by side.

    The photographs themselves are on page one; this is the record of what
    exactly was received — file, size, hash, the browser's own checks.
    """
    images = record.get("images") or {}
    out = _heading(t("images.section"), st)
    if not images:
        return out + [Paragraph(_esc(t("images.none")), st.small)]

    col_w = (_CONTENT_W - 8 * mm) / 2
    cols = []
    for side in ("right", "left"):
        entry = images.get(side)
        if not entry:
            cols.append([Paragraph(f"<b>{_esc(t('eye.' + side))}</b>", st.h3),
                         Paragraph("-", st.small)])
            continue
        checks = entry.get("client_checks") or {}
        fundus = checks.get("is_fundus")
        fundus_txt = {True: t("yes"), False: t("no")}.get(fundus, "-")
        conf = checks.get("laterality_confidence")
        conf_txt = f" ({float(conf):.2f})" if isinstance(conf, (int, float)) else ""
        sha = entry.get("sha256") or ""
        cols.append([
            Paragraph(f"<b>{_esc(t('eye.' + side))}</b>", st.h3),
            _kv_table([
                (t("images.file"), f"{entry.get('filename') or '-'} "
                                   f"({_fmt_bytes(entry.get('bytes'))})"),
                (t("images.resolution"), f"{entry.get('width', 0)} × {entry.get('height', 0)} px"),
                (t("images.check"), f"{fundus_txt}, {checks.get('laterality') or '-'}{conf_txt}"),
                (t("images.sha"), f"{sha[:24]}…" if len(sha) > 24 else (sha or "-")),
                (t("images.source"), entry.get("source") or "-"),
                (t("images.received"), _fmt_time(entry.get("received_utc"))),
            ], st, key_w=27 * mm, total_width=col_w),
        ])
    row = Table([cols], colWidths=[col_w + 8 * mm, col_w], hAlign="LEFT")
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, -1), 8 * mm), ("RIGHTPADDING", (1, 0), (1, -1), 0),
    ]))
    return out + [KeepTogether(row)]


def _prediction_section(record: dict, st: _Styles, t: _T) -> list:
    """The grade scale with the model's distribution, then the run's facts."""
    runs = record.get("predictions") or []
    out = _heading(t("scale.title"), st)
    if not runs:
        return out + [Paragraph(_esc(t("pred.none")), st.small)]

    run = runs[-1]  # the run the verdict judged is the case's latest
    pred = _as_grade(run.get("pred"))
    probs = [float(p) for p in (run.get("probs") or [])]
    if probs:
        out += [Spacer(1, 4), _GradeScale(probs, pred, t), Spacer(1, 4)]

    confidence = float(run.get("confidence") or 0.0)
    value = ParagraphStyle("rFact", parent=st.body, fontName=_FONT_SEMI, fontSize=12, leading=15)
    cells = [
        (t("pred.confidence"), f"{confidence * 100:.1f}%", ""),
        (t("pred.latency"), f"{run.get('latency_ms', 0)} ms",
         f"{t('pred.run')} {run.get('index', '?')}, {_fmt_time(run.get('run_utc'))}"),
    ]
    per_eye = {str(item.get("eye")): item for item in (run.get("per_eye") or [])}
    for side in ("right", "left"):
        item = per_eye.get(side)
        if item:
            g = _as_grade(item.get("pred"))
            cells.append((
                f"{_bare_eye(t, side)} ({'OD' if side == 'right' else 'OS'})",
                (g, t.grade(g)),
                f"{float(item.get('confidence') or 0) * 100:.1f}%, {item.get('latency_ms', 0)} ms",
            ))
    row = []
    for key, val, sub in cells:
        if isinstance(val, tuple):
            g, text = val
            style = ParagraphStyle("rFactG", parent=value, fontSize=10.5, leading=15,
                                   textColor=_GRADE_INK[g] if g is not None else _INK)
            val_p = Paragraph(_esc(text), style)
        else:
            val_p = Paragraph(_esc(val), value)
        row.append([Paragraph(_esc(key), st.key), val_p]
                   + ([Paragraph(_esc(sub), st.small)] if sub else []))
    widths = [_CONTENT_W / len(row)] * len(row)
    facts = Table([row], colWidths=widths, hAlign="LEFT")
    facts.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEABOVE", (0, 0), (-1, 0), 0.6, _RULE),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, _RULE),
        ("LINEBEFORE", (1, 0), (-1, 0), 0.6, _RULE),
        ("LEFTPADDING", (0, 0), (0, 0), 0), ("LEFTPADDING", (1, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return out + [Spacer(1, 6), facts]


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
                (t("detect.axis"), f"{float(det.get('angle_deg') or 0):.2f}° "
                                   f"(SD {float(det.get('rotation_sigma_deg') or 0):.2f}°)"),
                (t("detect.confident"), t("yes") if det.get("confident") else t("no")),
                (t("detect.frame"), f"{det.get('space_w', 0)} × {det.get('space_h', 0)} px"),
            ], st, key_w=34 * mm))
            out.append(Spacer(1, 3))

    if corrections:
        out += _heading(t("corr.section"), st)
        for corr in corrections:
            side = str(corr.get("eye", "left"))
            out.append(Paragraph(
                f"<b>{_esc(corr.get('index', '?'))}. {_esc(t('eye.' + side))}</b> "
                f"<font color='#5B6875'>{_esc(_fmt_time(corr.get('recorded_utc')))}</font>", st.h3))
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
        title = t("eye." + side) + (f", {variant}" if variant else "")
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
            # Keep the heading with its row, so it never ends a page alone.
            out.append(KeepTogether(
                [Paragraph(f"<b>{_esc(t('prep.channels'))}</b>", st.h3)]
                + _image_grid(sorted(channels, key=lambda c: c[1]), st, cols=4)))
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


def _segment_index() -> dict[str, dict]:
    """Read the bundled panel index once, tolerating its absence."""
    global _SEGMENT_INDEX
    if _SEGMENT_INDEX is None:
        try:
            _SEGMENT_INDEX = json.loads(
                (_SEGMENTS_DIR / "index.json").read_text(encoding="utf-8")
            )
        except Exception:  # noqa: BLE001 — no panels is a report without the page
            _SEGMENT_INDEX = {}
    return _SEGMENT_INDEX


def _fmt_num(value: float, lang: str, small: str = "<0.01") -> str:
    """A measured quantity, with as many decimals as its size needs."""
    if value < 0.01:
        text = small
    elif value < 1:
        text = f"{value:.2f}"
    elif value < 10:
        text = f"{value:.1f}"
    else:
        text = f"{value:.0f}"
    return text.replace(".", ",") if lang == "kk" else text


# One disc diameter is ~1.8 mm, so one disc area is ~2.5 mm². Only a reading
# aid: a photograph has no scale of its own, and discs vary between eyes.
_DA_MM2 = 3.14159 * 0.9 ** 2


def _segment_measure(layer: str, stats: dict | None, code: str, st: _Styles, t: _T) -> list:
    """One eye's line in the findings column: extent, spread and macular reach."""
    lang = t.lang
    head = f"<font name='{_FONT_SEMI}' color='#{_INK.hexval()[2:]}'>{code}</font>&nbsp;&nbsp;"
    out: list = []
    if not stats or "area_pct" not in stats:
        out.append(Paragraph(head + _esc(t("seg.absent").lower()), st.small))
    elif layer == "optic-disc":
        text = f"{_fmt_num(stats['area_pct'], lang)}\u00a0% {t('seg.of_field')}"
        out.append(Paragraph(head + _esc(text), st.small))
    else:
        da = float(stats.get("area_da") or 0)
        parts = [
            f"{stats.get('count', 0)} {t('seg.foci')}",
            f"{stats.get('quadrants', 0)}/4 {t('seg.quadrants')}",
            f"{_fmt_num(da, lang, '<0.01')}\u00a0{'ДА' if lang == 'kk' else 'DA'} "
            f"\u2248\u00a0{_fmt_num(da * _DA_MM2, lang)}\u00a0{'мм' if lang == 'kk' else 'mm'}\u00b2",
            f"{_fmt_num(stats['area_pct'], lang)}\u00a0%",
        ]
        near = t("seg.nearest").format(d=_fmt_num(float(stats.get("nearest_dd", 0)), lang))
        in_mac = int(stats.get("in_macula") or 0)
        reach = t("seg.in_macula").format(n=in_mac) if in_mac else t("seg.macula_clear")
        text = " · ".join(parts) + f". {near[0].upper()}{near[1:]}; {reach}."
        out.append(Paragraph(head + _esc(text), st.small))
    return out


def _marked_panel(path: Path, eye: dict) -> io.BytesIO | None:
    """The panel with the macula ring (1 DD round the fovea) and a fovea cross."""
    try:
        with PILImage.open(path) as im:
            panel = im.convert("RGB")
    except Exception:  # noqa: BLE001 — a missing panel must not fail the report
        return None
    fovea, dd = eye.get("fovea"), eye.get("disc_diameter")
    if fovea and dd:
        scale = 2  # draw at twice the size so the ring stays smooth when shrunk
        panel = panel.resize((panel.width * scale, panel.height * scale), PILImage.LANCZOS)
        w, h = panel.size
        cx, cy, r = fovea[0] * w, fovea[1] * h, dd * w
        draw = ImageDraw.Draw(panel)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 255, 255), width=scale)
        arm = r * 0.18
        draw.line((cx - arm, cy, cx + arm, cy), fill=(255, 255, 255), width=scale)
        draw.line((cx, cy - arm, cx, cy + arm), fill=(255, 255, 255), width=scale)
    buf = io.BytesIO()
    panel.save(buf, format="JPEG", quality=92)
    buf.seek(0)
    return buf


def _absent_cell(width: float, height: float, text: str, st: _Styles) -> Table:
    """A slate frame the size of a panel, for a layer this eye does not show."""
    style = ParagraphStyle("rAbsent", parent=st.caption, textColor=colors.HexColor("#9AA6B2"))
    cell = Table([[Paragraph(_esc(text), style)]], colWidths=[width], rowHeights=[height])
    cell.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.Color(*(c / 255 for c in _SLATE))),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return cell


def _segmentation_section(record: dict, st: _Styles, t: _T) -> list:
    """The annotated layers of both eyes, one row per structure or lesion type.

    Three columns: the right eye's panel, the left eye's panel, and the layer's
    name, what it is clinically and, per eye, how many foci it has, how many
    fovea-centred quadrants they reach, their area in disc areas and as a share
    of the retinal field, and how close they come to the fovea. The hard
    exudates row adds IDRiD's macular oedema risk. Every panel carries the
    macula ring. The layers are the dataset's own expert annotations, not a
    model output — there is no segmentation network in the demo — so only the
    bundled sample images carry them.
    """
    index = _segment_index()
    if not index:
        return []

    images = record.get("images") or {}
    eyes: dict[str, tuple[str, dict]] = {}
    for side in ("right", "left"):
        filename = str((images.get(side) or {}).get("filename") or "")
        eye = index.get(filename)
        if eye and eye.get("layers"):
            eyes[side] = (filename, eye)
    if not eyes:
        return []

    gap = 3 * mm
    img_w = 46 * mm
    img_h = img_w * 2 / 3  # boxed at the samples' own 3:2
    text_w = _CONTENT_W - 2 * img_w - 2 * gap
    codes = {"right": "OD", "left": "OS"}
    label = ParagraphStyle("rSegHead", parent=st.h3, spaceBefore=0, spaceAfter=0)
    about_style = ParagraphStyle("rSegAbout", parent=st.small, textColor=_INK)

    rows: list[list] = [[
        Paragraph(_esc(t("eye.right")), label),
        Paragraph(_esc(t("eye.left")), label),
        Paragraph(_esc(t("seg.finding")), label),
    ]]
    for layer in _SEGMENT_ORDER:
        if not any(layer in eye["layers"] for _, eye in eyes.values()):
            continue
        row: list = []
        for side in ("right", "left"):
            filename, eye = eyes.get(side, ("", {"layers": {}}))
            img = None
            if layer in eye["layers"]:
                panel = _marked_panel(_SEGMENTS_DIR / f"{filename}__{layer}.jpg", eye)
                if panel is not None:
                    img = _image_flowable(panel, img_w, max_height=img_h, box=True)
            row.append(img or _absent_cell(
                img_w, img_h, t("seg.absent") if side in eyes else "\u2014", st))
        about: list = [
            Paragraph(_esc(t("seg." + layer)), label),
            Spacer(1, 1.5),
            Paragraph(_esc(t("seg.about." + layer)), about_style),
        ]
        present = [side for side in ("right", "left") if side in eyes]
        if layer == "optic-disc":
            # Both discs on one line: their share of the field is all they add.
            shares = [
                f"<font name='{_FONT_SEMI}' color='#{_INK.hexval()[2:]}'>{codes[side]}</font>"
                f"&nbsp;{_fmt_num(stat['area_pct'], t.lang)}\u00a0%"
                for side in present
                if (stat := eyes[side][1]["layers"].get(layer))
            ]
            about += [Spacer(1, 2.5), Paragraph(
                " · ".join(shares) + " " + _esc(t("seg.of_field")), st.small)]
        else:
            for side in present:
                about.append(Spacer(1, 2.5))
                about += _segment_measure(
                    layer, eyes[side][1]["layers"].get(layer), codes[side], st, t)
        if layer == "hard-exudates":
            # IDRiD's own macular oedema scale, read off the exudate annotation:
            # 0 none, 1 outside the macula only, 2 within 1 DD of the fovea.
            grades = []
            for side in present:
                stat = eyes[side][1]["layers"].get(layer)
                grade = 0 if not stat else (2 if int(stat.get("in_macula") or 0) else 1)
                grades.append(f"{codes[side]}&nbsp;<font name='{_FONT_SEMI}'>{grade}</font>")
            dme = ParagraphStyle("rDme", parent=st.small, textColor=_INK)
            about += [Spacer(1, 2.5), Paragraph(
                _esc(t("seg.dme")) + ": " + " · ".join(grades), dme)]
        row.append(about)
        rows.append(row)

    table = Table(rows, colWidths=[img_w + gap, img_w + gap, text_w],
                  hAlign="LEFT", repeatRows=1)
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (1, -1), gap),
        ("RIGHTPADDING", (2, 0), (2, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, _RULE),
    ]))
    return _heading(t("seg.section"), st) + [table]


def _verdict_history(record: dict, st: _Styles, t: _T) -> list:
    """Every verdict on this patient, in order — a regrade leaves both entries."""
    feedback = record.get("feedback") or []
    if len(feedback) < 2:
        return []  # a single standing verdict is already the banner
    rows = [[
        Paragraph(f"<b>{_esc(item.get('index', '?'))}</b>", st.small),
        Paragraph(_esc(_fmt_time(item.get("recorded_utc"))), st.small),
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


class _BrandMark(Flowable):
    """The dashboard's mark — a fundus disc with its optic disc — in vector."""

    def __init__(self, size: float = 9 * mm) -> None:
        super().__init__()
        self.width = self.height = size

    def draw(self) -> None:
        c, r = self.canv, self.width / 2
        c.setFillColor(_COBALT)
        c.circle(r, r, r, stroke=0, fill=1)
        c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.35))
        c.setLineWidth(0.5)
        c.circle(r, r, r * 0.68, stroke=1, fill=0)
        c.setFillColor(colors.white)
        c.circle(r * 1.35, r * 1.11, r * 0.22, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#9FB4F5"))
        c.circle(r * 0.77, r * 0.95, r * 0.11, stroke=0, fill=1)


def _title_block(record: dict, st: _Styles, t: _T) -> list:
    """Report title on the left; the case identity and its times on the right."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    meta = "<br/>".join([
        f'{_esc(t("case"))} <font name="{_FONT_SEMI}" color="#16212C">'
        f'{_esc(record.get("case_id", "-"))}</font>',
        f'{_esc(t("created"))} {_esc(_fmt_time(record.get("created_utc")))}',
        f'{_esc(t("updated"))} {_esc(_fmt_time(record.get("updated_utc")))}',
        f'{_esc(t("generated"))} {_esc(_fmt_time(now))}',
    ])
    title = Table([[_BrandMark(), [Paragraph(_esc(t("title")), st.h1),
                                   Paragraph(_esc(t("subtitle")), st.small)]]],
                  colWidths=[12 * mm, _CONTENT_W * 0.58 - 12 * mm])
    title.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (0, 0), 3),
    ]))
    head = Table([[title, Paragraph(meta, st.meta)]],
                 colWidths=[_CONTENT_W * 0.58, _CONTENT_W * 0.42], hAlign="LEFT")
    head.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return [head, _rule(_INK, 1.1), Spacer(1, 12)]


def _numbered_canvas(case_id: str, t: _T):
    """A canvas class that knows the page count, for "Page n of m" footers.

    reportlab only learns the total once every page is laid out, so pages are
    held back and their furniture is drawn in one pass at save time.
    """

    class NumberedCanvas(Canvas):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self._saved: list[dict] = []

        def showPage(self) -> None:  # noqa: N802 — reportlab API
            self._saved.append(dict(self.__dict__))
            self._startPage()

        def save(self) -> None:
            total = len(self._saved)
            for state in self._saved:
                self.__dict__.update(state)
                self._furniture(total)
                super().showPage()
            super().save()

        def _furniture(self, total: int) -> None:
            w, _ = _PAGE
            self.saveState()
            y = _MARGIN - 8 * mm
            self.setStrokeColor(_RULE)
            self.setLineWidth(0.5)
            self.line(_MARGIN, y + 4 * mm, w - _MARGIN, y + 4 * mm)
            self.setFont(_FONT, 7)
            self.setFillColor(_MUTED)
            self.drawString(_MARGIN, y, t("disclaimer"))
            self.drawRightString(w - _MARGIN, y, t("page.of").replace(
                "{n}", str(self._pageNumber)).replace("{m}", str(total)))
            if self._pageNumber > 1:  # running head on the evidence pages
                top = _PAGE[1] - _MARGIN + 7 * mm
                self.drawString(_MARGIN, top, t("title"))
                self.drawRightString(w - _MARGIN, top, f"{t('case')} {case_id}")
                self.line(_MARGIN, top - 2.6 * mm, w - _MARGIN, top - 2.6 * mm)
            self.restoreState()

    return NumberedCanvas


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

    # Page 1 is the clinical summary — the finding, the photographs it rests
    # on, the model's distribution over the scale and where it came from.
    story: list = []
    story += _title_block(record, st, t)
    story += _finding_section(record, directory, st, t)
    story += _prediction_section(record, st, t)
    story += _verdict_history(record, st, t)
    story += _model_section(record, st, t)

    # Page 2, when the case is built on sample images: their annotated
    # structures and lesions, both eyes side by side with what each layer is
    # and how much of the retinal field it covers.
    segments = _segmentation_section(record, st, t)
    if segments:
        story.append(PageBreak())
        story += segments

    # What follows is the evidence: what exactly was received, where the
    # detector put the landmarks, how the images were transformed and what the
    # network attended to.
    appendix: list = []
    appendix += _images_section(record, directory, st, t)
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
        topMargin=_MARGIN, bottomMargin=_MARGIN + 2 * mm,
        title=f"DR report {case_id}", author="DR-Classifier demo",
        subject=t("title"),
    )
    doc.build(story, canvasmaker=_numbered_canvas(case_id, t))
    return buffer.getvalue()


def report_filename(case_id: str, lang: str = "en") -> str:
    """The download file name for one case's report."""
    return f"dr-report-{case_id}-{normalize_lang(lang)}.pdf"
