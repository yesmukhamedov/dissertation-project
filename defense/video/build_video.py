"""Build the subtitle track and the shooting sheet from the storyboard.

The storyboard (`storyboard_en.md`) is the single source for both. Each beat carries an
optional `**Hold:** N` (seconds of picture with no caption, where the action happens) and a
`**Caption:**` block whose lines look like `> [7] text` — seven seconds on screen for that
caption. Time is cumulative across beats, so editing one number moves everything after it.

Outputs:
    subtitles_en.srt  -- burned in by `add_subtitles.ps1`
    shotlist.md       -- absolute timecodes to record against
    beats.json        -- machine-readable beats, consumed by `record_demo.js`

After a recording exists, `--anchors beat_times.json` (written by the runner) re-anchors every
beat to the second it actually started, so the captions stay in sync even if a beat ran long.

Usage:
    python build_video.py
    python build_video.py --gap 0.2 --width 46
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import List, NamedTuple

HERE = Path(__file__).resolve().parent

BEAT = re.compile(r"^##\s+(B\d+)\s*[·.]\s*(.+?)\s*$")
PART = re.compile(r"^#\s+(PART .+?)\s*$")
DO = re.compile(r"^\*\*Do:\*\*\s*(.*)$")
HOLD = re.compile(r"^\*\*Hold:\*\*\s*([\d.]+)\s*$")
CAPTION_MARK = re.compile(r"^\*\*Caption:\*\*\s*$")
CAPTION = re.compile(r"^>\s*\[([\d.]+)\]\s*(.+?)\s*$")
EMPHASIS = re.compile(r"\*{1,2}([^*]+)\*{1,2}")


class Cue(NamedTuple):
    """One caption on the timeline."""

    beat: str
    start: float
    end: float
    text: str


class Beat(NamedTuple):
    """One recorded action and the captions that play over it."""

    part: str
    beat: str
    title: str
    do: str
    hold: float
    start: float
    end: float
    cues: List[Cue]


def parse(path: Path, gap: float) -> List[Beat]:
    """Lay the storyboard out on a timeline.

    Args:
        path: The storyboard Markdown file.
        gap: Blank picture between consecutive captions, in seconds.

    Returns:
        The beats in order, each with absolute start/end and its timed cues.
    """
    beats: List[Beat] = []
    clock = 0.0
    part = ""
    beat_id = title = do = ""
    hold = 0.0
    cues: List[Cue] = []
    started = False
    beat_start = 0.0
    in_caption = False
    in_do = False

    def close() -> None:
        nonlocal started, cues, do, hold
        if started:
            beats.append(Beat(part, beat_id, title, do, hold, beat_start, clock, cues))
        started, cues, do, hold = False, [], "", 0.0

    for raw in path.read_text(encoding="utf-8").splitlines():
        part_match = PART.match(raw)
        if part_match:
            close()
            part = part_match.group(1)
            continue

        beat_match = BEAT.match(raw)
        if beat_match:
            close()
            beat_id, title = beat_match.group(1), beat_match.group(2)
            beat_start = clock
            started, in_caption, in_do = True, False, False
            continue

        if not started:
            continue

        do_match = DO.match(raw)
        if do_match:
            do = clean(do_match.group(1))
            in_caption, in_do = False, True
            continue

        hold_match = HOLD.match(raw)
        if hold_match:
            hold = float(hold_match.group(1))
            clock += hold
            in_caption, in_do = False, False
            continue

        if CAPTION_MARK.match(raw):
            in_caption, in_do = True, False
            continue

        # A `**Do:**` note may wrap onto the following lines; keep them together
        # rather than cutting the instruction off mid-sentence in the shot list.
        if in_do:
            if raw.strip():
                do = clean(f"{do} {raw}")
            else:
                in_do = False
            continue

        caption = CAPTION.match(raw)
        if caption and in_caption:
            duration = float(caption.group(1))
            cues.append(Cue(beat_id, clock, clock + duration, clean(caption.group(2))))
            clock += duration + gap

    close()
    return beats


def clean(text: str) -> str:
    """Strip Markdown emphasis and collapse whitespace."""
    return re.sub(r"\s+", " ", EMPHASIS.sub(r"\1", text)).strip()


def wrap(text: str, width: int, max_lines: int = 2) -> str:
    """Wrap a caption to at most `max_lines` balanced lines."""
    if len(text) <= width:
        return text
    words = text.split()
    lines: List[str] = []
    current = ""
    budget = max(width, len(text) // max_lines + 1)
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > budget and len(lines) < max_lines - 1:
            lines.append(current)
            current = word
        else:
            current = candidate
    lines.append(current)
    return "\n".join(lines)


def stamp(seconds: float, millis: bool = True) -> str:
    """Format seconds as `HH:MM:SS,mmm` (SRT) or `M:SS` (shot list)."""
    if not millis:
        total = int(round(seconds))
        return f"{total // 60}:{total % 60:02d}"
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def render_srt(beats: List[Beat], width: int) -> str:
    """Render every cue as SRT text."""
    blocks = []
    index = 0
    for beat in beats:
        for cue in beat.cues:
            index += 1
            blocks.append(
                f"{index}\n{stamp(cue.start)} --> {stamp(cue.end)}\n{wrap(cue.text, width)}\n"
            )
    return "\n".join(blocks)


def render_shotlist(beats: List[Beat]) -> str:
    """Render the beats as a recording sheet with absolute timecodes."""
    out = [
        "# Shooting sheet — silent screencast",
        "",
        "Generated by `build_video.py` from `storyboard_en.md`. Do not edit by hand.",
        "Record against the **In** column: perform the action at that timecode, then keep the",
        "picture still until the next one. Captions are burned in afterwards, so a beat that runs",
        "a second long is harmless — a beat that runs short leaves a caption over the wrong screen.",
        "",
    ]
    part = None
    for beat in beats:
        if beat.part != part:
            part = beat.part
            out += ["", f"## {part}", "", "| In | Out | Beat | Do |", "|---|---|---|---|"]
        out.append(
            f"| **{stamp(beat.start, False)}** | {stamp(beat.end, False)} | "
            f"{beat.beat} · {beat.title} | {beat.do} |"
        )
    total = beats[-1].end if beats else 0.0
    captions = sum(len(b.cues) for b in beats)
    out += ["", f"**Total: {stamp(total, False)}** · {len(beats)} beats · {captions} captions", ""]
    return "\n".join(out)


def render_beats_json(beats: List[Beat]) -> str:
    """Serialise the beats (and their cues) for the recording runner."""
    return json.dumps(
        [
            {
                "id": b.beat,
                "title": b.title,
                "part": b.part,
                "do": b.do,
                "hold": b.hold,
                "start": round(b.start, 3),
                "end": round(b.end, 3),
                "cues": [{"start": round(c.start, 3), "end": round(c.end, 3), "text": c.text} for c in b.cues],
            }
            for b in beats
        ],
        indent=1,
        ensure_ascii=False,
    )


def apply_anchors(beats: List[Beat], anchors: dict) -> List[Beat]:
    """Shift each beat onto the second it actually started in the recording.

    Args:
        beats: The planned beats.
        anchors: ``{beat_id: actual_start_seconds}`` from the runner.

    Returns:
        The beats with every cue shifted by its beat's measured offset. A beat with no
        anchor inherits the shift of the last anchored beat, so a partial file still helps.
    """
    shifted: List[Beat] = []
    offset = 0.0
    for b in beats:
        if b.beat in anchors:
            offset = float(anchors[b.beat]) - b.start
        cues = [Cue(c.beat, c.start + offset, c.end + offset, c.text) for c in b.cues]
        shifted.append(Beat(b.part, b.beat, b.title, b.do, b.hold, b.start + offset, b.end + offset, cues))
    return shifted


def hold_for_speech(beats: List[Beat], speech: dict) -> List[Beat]:
    """Extend every caption so it stays up until its narration has finished.

    A caption is timed for reading, which is faster than speaking; without this the text
    would vanish mid-sentence in the narrated cut. A cue is never extended into the next
    one, so the pairing of picture, caption and voice stays one-to-one.

    Args:
        beats: The (already anchored) beats.
        speech: ``{cue_number: spoken_seconds}`` from narrate.py.

    Returns:
        The beats with lengthened cue ends.
    """
    flat = [c for b in beats for c in b.cues]
    starts = [c.start for c in flat]
    grown = {}
    for n, cue in enumerate(flat, start=1):
        spoken_len = float(speech.get(str(n), 0))
        ceiling = (starts[n] - 0.05) if n < len(starts) else cue.end + spoken_len
        grown[id(cue)] = min(max(cue.end, cue.start + spoken_len + 0.15), ceiling)
    return [
        b._replace(cues=[c._replace(end=grown[id(c)]) for c in b.cues])
        for b in beats
    ]


def parse_args() -> argparse.Namespace:
    """Command-line arguments."""
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--storyboard", type=Path, default=HERE / "storyboard_en.md")
    p.add_argument("--srt", type=Path, default=HERE / "subtitles_en.srt")
    p.add_argument("--shotlist", type=Path, default=HERE / "shotlist.md")
    p.add_argument("--gap", type=float, default=0.25, help="blank picture between captions, s")
    p.add_argument("--width", type=int, default=46, help="soft line width in characters")
    p.add_argument("--beats", type=Path, default=HERE / "beats.json", help="machine-readable beats")
    p.add_argument("--anchors", type=Path, default=None,
                   help="beat_times.json from the runner: re-anchor cues to the real recording")
    p.add_argument("--speech", type=Path, default=None,
                   help="speech.json from narrate.py: hold each caption until its sentence ends")
    return p.parse_args()


def main() -> None:
    """Generate the subtitle track and the shooting sheet."""
    args = parse_args()
    beats = parse(args.storyboard, args.gap)
    if not beats:
        raise SystemExit(f"no beats found in {args.storyboard}")
    args.beats.write_text(render_beats_json(beats), encoding="utf-8")
    args.shotlist.write_text(render_shotlist(beats), encoding="utf-8")
    if args.anchors:
        anchors = {k: v for k, v in json.loads(args.anchors.read_text(encoding="utf-8")).items()
                   if not k.startswith("_")}
        beats = apply_anchors(beats, anchors)
        print(f"re-anchored to {args.anchors.name} ({len(anchors)} beats)")
    if args.speech:
        beats = hold_for_speech(beats, json.loads(args.speech.read_text(encoding="utf-8")))
        print(f"captions held for the spoken audio ({args.speech.name})")
    args.srt.write_text(render_srt(beats, args.width), encoding="utf-8")
    captions = sum(len(b.cues) for b in beats)
    longest = max((c for b in beats for c in b.cues), key=lambda c: len(c.text))
    print(f"{len(beats)} beats, {captions} captions -> {args.srt.name}, {args.shotlist.name}")
    print(f"total {stamp(beats[-1].end, False)}")
    print(f"longest caption {len(longest.text)} chars ({longest.beat}): {longest.text[:60]}...")


if __name__ == "__main__":
    main()
