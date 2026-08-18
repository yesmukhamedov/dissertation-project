"""Speak the burned-in captions and mux the result onto the video.

The subtitle file is the script: every cue is synthesised separately and placed at exactly
its own timecode, so the voice and the caption on screen always say the same thing. A cue
whose speech runs past its window is compressed with `atempo` rather than allowed to spill
over the next one.

Speech comes from the Windows SAPI voices already installed on this machine — nothing is
sent anywhere. Domain terms are respelled for the synthesiser in `SPOKEN` below; that
rewriting affects the audio only, never the captions.

Usage:
    python narrate.py                                   # default: compact video, David
    python narrate.py --voice "Microsoft Zira Desktop"
    python narrate.py --video DR_demo_for_Prof_Al-Haddad.mp4 --out narrated.mp4
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import wave
from array import array
from pathlib import Path
from typing import List, NamedTuple

HERE = Path(__file__).resolve().parent
RATE = 48000                      # assembly sample rate, mono s16
# edge-tts lives in the standalone interpreter, not in the demo's virtualenv.
EDGE_PYTHON = r"C:\Users\PC\AppData\Local\Programs\Python\Python313\python.exe"

# Respellings applied to the SPOKEN text only — the captions are never touched. Without them
# both engines mangle the domain vocabulary (and "DR4" comes out as "doctor four").
SPOKEN = [
    (r"\bGrad-CAM\b", "Grad Cam"),
    (r"\bCLAHE\b", "clah-hee"),
    (r"\bIDRiD\b", "eye-dee-rid"),
    (r"\bEyePACS\b", "eye-pacs"),
    (r"\bAPTOS\b", "ap-toss"),
    (r"\bMessidor-2\b", "Messidor two"),
    (r"\bEfficientNet-B3\b", "Efficient-Net B three"),
    (r"\bJSONL\b", "J-S-O-N-L"),
    (r"\bFLOPs\b", "flops"),
    (r"\bAl-Haddad\b", "Al Haddad"),
    (r"\bOD\b", "optic disc"),
    (r"\bFOV\b", "F-O-V"),
    (r"\bDR3\b", "D R three"),
    (r"\bDR4\b", "D R four"),
    (r"—", ","),                   # an em dash is read as a pause, not a word
    (r"\s+", " "),
]

# The old Desktop voices need extra help with proper nouns the neural voices get right.
SPOKEN_SAPI = [
    (r"\bDeLong\b", "De Long"),
    (r"\bMcNemar\b", "Mac Nemar"),
    (r"\bHolm\b", "Holme"),
]


class Cue(NamedTuple):
    """One subtitle cue and the window it owns on the timeline."""

    index: int
    start: float
    end: float
    text: str


def parse_srt(path: Path) -> List[Cue]:
    """Read cues out of an SRT file.

    Args:
        path: The subtitle file.

    Returns:
        The cues in order, with times in seconds and newlines flattened.
    """
    stamp = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})")
    cues: List[Cue] = []
    block: List[str] = []

    def flush() -> None:
        if len(block) < 3:
            return
        m = stamp.search(block[1])
        if not m:
            return
        g = [int(x) for x in m.groups()]
        start = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        end = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        cues.append(Cue(int(block[0]), start, end, " ".join(l.strip() for l in block[2:]).strip()))

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            block.append(line)
        else:
            flush()
            block = []
    flush()
    return cues


def spoken(text: str, engine: str = "sapi") -> str:
    """Rewrite a caption into something the synthesiser pronounces correctly.

    Args:
        text: The caption as it appears on screen.
        engine: ``"sapi"`` or ``"edge"`` — the older voices need a few extra hints.

    Returns:
        The line to hand to the synthesiser.
    """
    rules = SPOKEN + (SPOKEN_SAPI if engine == "sapi" else [])
    for pattern, replacement in rules:
        text = re.sub(pattern, replacement, text)
    return text.strip()


def synthesise(cues: List[Cue], voice: str, rate: int, work: Path) -> None:
    """Render every cue to its own WAV with Windows SAPI.

    Args:
        cues: The cues to speak.
        voice: Installed voice name.
        rate: SAPI speaking rate, -10..10.
        work: Directory to write `cue_NNN.wav` into.

    Raises:
        SystemExit: If PowerShell reports a failure.
    """
    payload = [{"i": c.index, "t": spoken(c.text, "sapi")} for c in cues]
    (work / "lines.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    script = f"""
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$lines = Get-Content -Raw -Encoding UTF8 '{work / "lines.json"}' | ConvertFrom-Json
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SelectVoice('{voice}')
$s.Rate = {rate}
foreach ($l in $lines) {{
  $p = Join-Path '{work}' ('cue_{{0:d3}}.wav' -f [int]$l.i)
  $s.SetOutputToWaveFile($p)
  $s.Speak([string]$l.t)
}}
$s.SetOutputToNull()
$s.Dispose()
Write-Output 'ok'
"""
    ps = work / "speak.ps1"
    ps.write_text(script, encoding="utf-8")
    done = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps)],
                          capture_output=True, text=True)
    if done.returncode != 0 or "ok" not in done.stdout:
        raise SystemExit(f"speech synthesis failed:\n{done.stdout}\n{done.stderr}")


def synthesise_edge(cues: List[Cue], voice: str, rate: int, work: Path, python: str) -> None:
    """Render every cue with a Microsoft neural voice through the `edge-tts` package.

    Unlike the SAPI path this sends each line to Microsoft's speech endpoint, so it needs a
    network connection and the narration text leaves the machine. It is used only when the
    candidate asks for it explicitly; the voices are far closer to a human reading.

    Args:
        cues: The cues to speak.
        voice: An edge-tts short name, e.g. ``en-US-AndrewNeural``.
        rate: Speed offset in percent, e.g. ``5`` for ``+5%``.
        work: Directory to write `cue_NNN.mp3` into.
        python: Interpreter that has `edge_tts` installed.

    Raises:
        SystemExit: If a cue cannot be synthesised after a retry.
    """
    for cue in cues:
        target = work / f"cue_{cue.index:03d}.mp3"
        if target.exists() and target.stat().st_size > 0:
            continue
        line = spoken(cue.text, "edge")
        for attempt in (1, 2, 3):
            done = subprocess.run(
                [python, "-m", "edge_tts", "--voice", voice, f"--rate={rate:+d}%",
                 "--text", line, "--write-media", str(target)],
                capture_output=True, text=True)
            if done.returncode == 0 and target.exists() and target.stat().st_size > 0:
                break
            if attempt == 3:
                raise SystemExit(f"edge-tts failed on cue {cue.index}: {done.stderr.strip()[:300]}")
        print(f"  cue {cue.index:>2}/{len(cues)}", end="\r")
    print(" " * 24, end="\r")


def ffprobe_duration(path: Path) -> float:
    """Duration of a media file in seconds."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
         "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def fit(src: Path, dst: Path, budget: float) -> float:
    """Resample a cue to the assembly format, compressing it if it overruns its window.

    Args:
        src: The synthesised cue.
        dst: Where to write the normalised clip.
        budget: Seconds available before the next cue starts.

    Returns:
        The tempo factor applied (1.0 = untouched).
    """
    duration = ffprobe_duration(src)
    tempo = 1.0
    if budget > 0.4 and duration > budget:
        tempo = min(duration / budget, 1.6)      # beyond ~1.6 speech stops being pleasant
    chain = "atempo=%.4f," % tempo if tempo > 1.001 else ""
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src),
         "-af", f"{chain}aresample={RATE}", "-ac", "1", "-c:a", "pcm_s16le", str(dst)],
        check=True)
    return tempo


def assemble(clips: List[tuple], total: float, dst: Path) -> None:
    """Paste the clips onto one silent track at their own timecodes.

    Args:
        clips: ``(start_seconds, wav_path)`` pairs.
        total: Length of the finished track in seconds.
        dst: Output WAV path.
    """
    track = bytearray(int(total * RATE) * 2)
    for start, clip in clips:
        with wave.open(str(clip), "rb") as w:
            frames = w.readframes(w.getnframes())
        offset = int(start * RATE) * 2
        end = min(offset + len(frames), len(track))
        if end > offset:
            track[offset:end] = frames[: end - offset]
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(bytes(track))


def normalise(path: Path, target_dbfs: float = -3.0) -> float:
    """Scale a finished track so its loudest sample sits at `target_dbfs`.

    The two engines deliver very different levels — SAPI comes out near full scale, the
    neural voices several dB below it — and the AAC encoder wants headroom either way.

    Args:
        path: The assembled narration WAV, rewritten in place.
        target_dbfs: Peak level to aim for.

    Returns:
        The gain applied.
    """
    with wave.open(str(path), "rb") as w:
        params, frames = w.getparams(), w.readframes(w.getnframes())
    samples = array("h", frames)
    peak = max(max(samples), -min(samples)) or 1
    gain = (10 ** (target_dbfs / 20) * 32767) / peak
    if abs(gain - 1.0) > 0.02:
        limit = 32767
        for i, s in enumerate(samples):
            samples[i] = max(-limit, min(limit, int(s * gain)))
        with wave.open(str(path), "wb") as w:
            w.setparams(params)
            w.writeframes(samples.tobytes())
    return gain


def parse_args() -> argparse.Namespace:
    """Command-line arguments."""
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--video", type=Path, default=HERE / "DR_demo_for_Prof_Al-Haddad_compact.mp4")
    p.add_argument("--srt", type=Path, default=HERE / "subtitles_en.srt")
    p.add_argument("--out", type=Path, default=HERE / "DR_demo_for_Prof_Al-Haddad_narrated.mp4")
    p.add_argument("--engine", choices=("sapi", "edge"), default="sapi",
                   help="sapi = offline Windows voices; edge = Microsoft neural voices (online)")
    p.add_argument("--voice", default=None,
                   help="voice name; defaults to 'Microsoft David Desktop' / 'en-US-AndrewNeural'")
    p.add_argument("--rate", type=int, default=0,
                   help="speaking rate: SAPI -10..10, edge percent offset")
    p.add_argument("--edge-python", default=EDGE_PYTHON,
                   help="interpreter that has edge_tts installed")
    p.add_argument("--keep-wav", action="store_true", help="also keep the narration track as .wav")
    p.add_argument("--work", type=Path, default=None,
                   help="cache directory for the synthesised cues (defaults per engine)")
    p.add_argument("--reuse", action="store_true", help="reuse the cached cues instead of re-speaking")
    p.add_argument("--measure-only", action="store_true",
                   help="speak the cues, write speech.json and stop (feeds build_video.py --speech)")
    return p.parse_args()


def main() -> None:
    """Synthesise the captions and mux the narration onto the video."""
    args = parse_args()
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg is not on PATH")
    cues = parse_srt(args.srt)
    if not cues:
        raise SystemExit(f"no cues in {args.srt}")
    total = ffprobe_duration(args.video)

    ext = "wav" if args.engine == "sapi" else "mp3"
    voice = args.voice or ("Microsoft David Desktop" if args.engine == "sapi" else "en-US-AndrewNeural")
    work = args.work or (HERE / f".narration_{args.engine}")
    work.mkdir(parents=True, exist_ok=True)
    raw_of = lambda cue: work / f"cue_{cue.index:03d}.{ext}"

    print(f"{len(cues)} cues, video {total:.1f}s, {args.engine} voice '{voice}' -> {work}")
    cached = all(raw_of(c).exists() for c in cues)
    if args.reuse and cached:
        print("reusing the cached cues")
    elif args.engine == "sapi":
        synthesise(cues, voice, args.rate, work)
    else:
        synthesise_edge(cues, voice, args.rate, work, args.edge_python)

    # What each cue needs when spoken at a natural pace. build_video.py --speech uses this to
    # hold every caption on screen until its sentence has finished.
    speech = {str(c.index): round(ffprobe_duration(raw_of(c)), 3)
              for c in cues if raw_of(c).exists()}
    (HERE / "speech.json").write_text(json.dumps(speech, indent=1), encoding="utf-8")
    if args.measure_only:
        longest = max(speech.items(), key=lambda kv: kv[1])
        print(f"speech.json written — {len(speech)} cues, longest {longest[1]}s (cue {longest[0]})")
        return

    clips, squeezed = [], 0
    for i, cue in enumerate(cues):
        raw = raw_of(cue)
        if not raw.exists():
            print(f"  ! cue {cue.index} was not synthesised, skipping")
            continue
        next_start = cues[i + 1].start if i + 1 < len(cues) else total
        tempo = fit(raw, work / f"fit_{cue.index:03d}.wav", next_start - cue.start - 0.12)
        if tempo > 1.001:
            squeezed += 1
        clips.append((cue.start, work / f"fit_{cue.index:03d}.wav"))

    track = work / "narration.wav"
    assemble(clips, total, track)
    gain = normalise(track)
    if args.keep_wav:
        shutil.copy(track, args.out.with_suffix(".wav"))

    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(args.video), "-i", str(track),
         "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ac", "1",
         "-map", "0:v:0", "-map", "1:a:0", "-shortest", "-movflags", "+faststart", str(args.out)],
        check=True)

    size = args.out.stat().st_size / (1024 * 1024)
    print(f"{len(clips)} cues spoken, {squeezed} compressed to fit their window, gain x{gain:.2f}")
    print(f"-> {args.out.name}  {size:.1f} MB")


if __name__ == "__main__":
    main()
