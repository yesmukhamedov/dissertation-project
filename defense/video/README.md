# defense/video — demonstration video for the foreign consultant

Prof. Al-Haddad asked for a **recorded** walk-through instead of a live session: the inference
backend is only up during Almaty working hours and the time difference is three hours. He named
what he wants to see — **the eight-stage preprocessing pipeline** and **the Grad-CAM attention
maps**.

The video is a **silent screencast**: no voice-over, captions burned into the picture.

| File | What it is |
|---|---|
| `storyboard_en.md` | The scenario: every beat, what to click, and the caption text with its duration. Edit this. |
| `build_video.py` | Reads the storyboard, writes the two files below. |
| `subtitles_en.srt` | Captions with absolute timings. |
| `shotlist.md` | The same beats with absolute timecodes — the sheet to record against. |
| `record_demo.js` | Drives the published demo through the storyboard and records it — no human at the keyboard. |
| `beats.json` / `beat_times.json` | The beats the runner executes, and the second each one actually started. |
| `add_subtitles.ps1` | Burns the captions into the recording with ffmpeg. |

## What is built

| File | |
|---|---|
| `DR_demo_for_Prof_Al-Haddad.mp4` | **The deliverable** — 7:25, 1920x1080, captions burned in, 25.5 MB. |
| `DR_demo_for_Prof_Al-Haddad_compact.mp4` | Same picture at 15 fps / CRF 26, **19.4 MB** — fits a 25 MB mail attachment. |
| `DR_demo_for_Prof_Al-Haddad_narrated_v2.mp4` | **The narrated deliverable** — neural voice (en-US-AndrewNeural), 23.4 MB. Captions kept, so it also works muted. |
| `DR_demo_for_Prof_Al-Haddad_narrated.mp4` | The first take, offline Windows voice. Superseded by v2; kept for comparison. |
| `narrate.py` | Speaks the captions with the local Windows voice and muxes the track onto a cut. |
| `demo_raw.mp4` | The caption-free master. Keep it: re-burning after a caption edit needs no re-recording. |
| `recording/*.webm` | What Playwright wrote, lead-in included. Safe to delete once the mp4s are approved. |

The video was recorded by `record_demo.js` against the published demo with the live GPU backend:
patient 294 loaded by hand, all eight preprocessing stages stepped through on the left eye, live
Grad-CAM from the checkpoint, a confirmed verdict, an undo, a rejection recorded as DR3, then the
Full-mode tour. Every beat started within 0.05 s of its planned second, and the captions were
re-anchored to the measured times, so nothing drifts. The mp4s are gitignored — the deliverable
travels as a OneDrive link, not through the repository.

## Narration

`narrate.py` treats `subtitles_en.srt` as the script: each caption is spoken separately and placed
at its own timecode, so the voice and the text on screen never disagree. Two engines:

- `--engine edge` (**used for v2**) — Microsoft neural voices via the `edge-tts` package,
  `en-US-AndrewNeural` at `--rate 15`. This one is online: each line is sent to Microsoft's speech
  endpoint. Chosen deliberately, because the offline voices sound synthetic.
- `--engine sapi` (default) — the Windows Desktop voices, fully offline, nothing leaves the machine.

Domain terms are respelled for the synthesiser in `SPOKEN` inside the script; that rewriting touches
the audio only, never the captions. The finished track is peak-normalised to -3 dBFS.

Because speaking is slower than reading, captions have to be held until their sentence ends:

```powershell
python narrate.py --measure-only                                   # writes speech.json
python build_video.py --anchors beat_times.json --speech speech.json
# re-burn the captions, then:
python narrate.py --reuse --rate 2
```

Verified on the finished v2 track: all 69 captions carry their speech, no sentence plays with the
caption already gone, none bleeds into the next one, peak -3.0 dBFS, speech over 47 % of the running
time. Three cues are sped up by at most 1.21x to fit their window.

## Order of work

1. **Agree the storyboard.** Patient, beat order, caption wording. Everything downstream is
   generated from it, so changes are cheap here and expensive later.
2. **Rebuild** after any edit:

   ```powershell
   python build_video.py
   ```

   Durations live in the storyboard as `> [5.5] caption text`; `**Hold:** N` is silent picture
   where the action happens. Time is cumulative — one edited number moves every later timecode.
3. **Record.** Either the runner does it:

   ```powershell
   node record_demo.js            # ~8 min, writes recording\*.webm + beat_times.json
   node record_demo.js --to B08   # rehearsal: stop after one beat
   ```

   It opens the published demo in Chrome, seeds the access code into sessionStorage so the PIN
   gate never appears on camera, draws a synthetic cursor (Playwright's recorder does not capture
   the real pointer), and performs each beat's action at its planned second. Every beat's real
   start time lands in `beat_times.json`, and `_offset` in that file is the lead-in to trim off
   the front of the recording.

   Or record it by hand against `shotlist.md` with a timer visible — Xbox Game Bar (`Win+Alt+R`)
   or OBS, 1920x1080, no audio. Perform each action at its **In** timecode and hold the picture
   still until the next one. Overrunning a beat by a second is harmless; running short leaves a
   caption over the wrong screen.
4. **Re-time and attach the captions.** After a runner recording:

   ```powershell
   ffmpeg -ss <_offset> -i recording\<file>.webm -c:v libx264 -crf 20 -pix_fmt yuv420p demo_raw.mp4
   python build_video.py --anchors beat_times.json
   ```

   The first command trims the lead-in so video time equals storyboard time; the second re-anchors
   every caption onto the second its beat actually started, so drift cannot desynchronise them.
   Then:

   ```powershell
   winget install --id Gyan.FFmpeg -e     # once, then open a new terminal
   .\add_subtitles.ps1 -Video ..\..\demo_raw.mp4
   ```

   Burned-in is the default and the right choice here: it survives Outlook preview and OneDrive
   playback, where a soft subtitle track is often ignored. ffmpeg 9.0 is installed on this box and
   the burn-in has been rehearsed on a test clip, so this step is known to work.

   One trap is already handled in the script: the `subtitles` filter is given the **absolute** path
   with the drive colon escaped (`subtitles='D\:/.../subs.srt'`). A bare filename does not work,
   because `Set-Location`/`Push-Location` do not change the working directory a child process
   inherits — ffmpeg then fails with a misleading "Option not found".
5. **Send.** 1080p will not fit the 25 MB mail limit — upload to OneDrive and send the link (mail
   goes out through `D:\mailbot`, work mailbox; a message with an attachment must be sent **from
   Drafts** in web Outlook).

If the recording drifts from the sheet, do not hand-edit timestamps: re-record the beat, or move
the beat's `Hold` in the storyboard and rebuild.

## Two traps in the demo itself

- **Upload the patient's two files by hand.** Only a manual upload runs the **live Grad-CAM from
  the checkpoint**. The bundled walk-through cases ("Test with Random Patient Images" fallback)
  carry pre-generated proxy heat maps derived from flat-field anomalies — not a real Grad-CAM, and
  not something to show a reviewer.
- **Unlock the PIN gate before recording starts** — the PIN must not appear in the picture.

## Rules the captions already follow — keep them if you rewrite

- The Experiment-1 gain (+6.55 pp) belongs to the **integrated configuration as a whole**: the two
  arms differ in initialisation as well as in preprocessing. Preprocessing alone is credited only
  through the ablation, which runs under a single initialisation.
- Grad-CAM is **attention alignment**, never clinical localisation of pathology.
- Nothing claims clinical validation or a medical device.
- Every number comes from `results/`; the provenance table at the end of `storyboard_en.md` lists
  each one with its source.
