# Audio: music, SFX, voice

Audio is half of game feel. Every game has its own sound identity, aligned with the story and the art bible (unity).

## 1. Audio bible (`design/audio-bible.md`, template in `templates/audio-bible.md`)

- Identity: music genre, signature instruments, BPM, key/mood. Example: "fast folk-pop at 140 BPM, hand drums and flute, cheerful but frantic".
- Music structure: short intro (during the countdown), a seamless round loop, an intensity layer for the last 20 seconds, win/lose stingers.
- SFX list per action (from the GDD's juice table): name, when, duration, priority. Frequent actions need 2–4 variations so they do not tire the ear.
- Announcer/voice: needed or not, speaking style, lines, written in the language and register of the target players.

## 2. Generating audio

Roles and alternatives are in `providers.md`. ElevenLabs is the recommended default because one key covers SFX, music, and voice. Any source works if it follows the adapter contract and the licence is recorded.

```bash
# sound effect (0.5–30 s)
python3 -I <skill>/scripts/elevenlabs.py sfx <outdir> <name> "wet rubber slip with a comic squeak" --duration 0.8 --n 3
# music (round loop)
python3 -I <skill>/scripts/elevenlabs.py music <outdir> <name> <prompt.txt> --length 60 --instrumental
# announcer voice
python3 -I <skill>/scripts/elevenlabs.py tts <outdir> <name> "Three... two... one... GO!" --voice <voice_id>
python3 -I <skill>/scripts/elevenlabs.py voices   # list available voices
```

- The key is read from `ELEVENLABS_API_KEY`. If it is missing, write the audio spec only and say so in your report.
- SFX prompts: concrete and in English (material, action, size, space): "small plastic bottle cap flicked onto a wooden table, close, dry".
- Music prompts: genre, instruments, BPM, mood, "instrumental", "seamless loop". Trim and test so the loop seam is inaudible.
- APIs change. If a request is rejected, read the error and the provider's current docs, then adapt the script or report what needs changing.
- Confirm your plan grants commercial rights. Record every file in `LICENSES.md` (prompt, voice id, date).

## 3. Mastering (required before files enter the game's assets)

A common complaint: music and SFX too quiet. Normalise everything:

| Kind | Target | Format |
|---|---|---|
| Music loop | −16 LUFS integrated, true peak −1 dBTP | OGG Vorbis/Opus stereo, 96–128 kbps |
| SFX | match by **loudness** (about −16 to −14 LUFS short-term), then limit peaks at −3 dBFS. Do not normalise by peak alone: hisses and swishes end up near −30 LUFS and sound weak. | OGG mono, 64–96 kbps, trim leading silence (< 10 ms) |
| Voice | −16 LUFS, true peak −1 dBTP | OGG mono |

```bash
ffmpeg -i in.mp3 -af loudnorm=I=-16:TP=-1:LRA=11 -ac 1 -c:a libopus -b:a 80k out.ogg
```

No `ffmpeg`? Install it locally in the working directory, e.g. `npm i --prefix ./.tools ffmpeg-static`, then use the path from `node -p "require('./.tools/node_modules/ffmpeg-static')"`. Never install anything globally for this. Adjust formats to what the target platform supports (see its profile).

Mixing, ducking, and bus levels usually belong to the engine or platform. If a bus level must change, raise it with the developers instead of baking it into the file. Likewise, design runtime ducking/low-pass in the GDD rather than producing "muffled" copies of files.

## 4. Practical notes

- Respect the provider's concurrency limit (ElevenLabs accounts are often limited to 2 parallel requests).
- Default voices are often English. For another language, pick a native voice from the provider's voice library and send samples to the owner.
- Generated music often has ~1.5 s of trailing silence and an inexact tempo. Measure BPM, cut on bar boundaries, then crossfade the loop seam.
- Provide music layers per session part: title, round, final/sudden death, results, plus stingers. One identity (same signature instruments).
- Music used later loads later, so the initial download stays small.
- **If you cannot hear,** verify by measurement (LUFS, peaks, waveform, loop seam), then send **one reel** in order (with the order listed) and ask the owner to listen to loop seams and voice lines.
- API keys often cannot read quota. Report usage from your own count: SFX count, music seconds, TTS characters.

## 5. Audio micro-feedback

- Random pitch ±5–8 % on repeated SFX.
- Escalating sounds: combo 1, 2, 3 rise in pitch.
- 0.3–0.5 s of silence before a big moment makes the impact feel louder.
- Music reacts to the game: intensity up when time runs low, low-pass when a player falls or is eliminated.
