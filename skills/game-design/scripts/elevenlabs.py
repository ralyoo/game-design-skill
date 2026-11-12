"""ElevenLabs helper (optional). Standard library only.

The API key is read from the ELEVENLABS_API_KEY environment variable and is never printed or saved.

  python3 -I elevenlabs.py sfx   <outdir> <name> "<prompt>" [--duration 1.0] [--influence 0.4] [--n 1] [--loop]
  python3 -I elevenlabs.py music <outdir> <name> <prompt-or-prompt-file> [--length 60] [--instrumental]
  python3 -I elevenlabs.py tts   <outdir> <name> "<text>" --voice <voice_id> [--model eleven_multilingual_v2]
  python3 -I elevenlabs.py voices

Writes <outdir>/<name>[-i].mp3 and <name>.json (request, no key). Mastering: see references/audio.md.
Endpoints and parameters change: check https://elevenlabs.io/docs if a request is rejected.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.elevenlabs.io/v1"
ENV_KEY = "ELEVENLABS_API_KEY"
FMT = "mp3_44100_128"


def api_key():
    key = os.environ.get(ENV_KEY)
    if not key:
        sys.exit(f"{ENV_KEY} is not set: write the audio spec only and note it in your report.")
    return key


def safe_name(name):
    if not re.fullmatch(r"[A-Za-z0-9._-]+", name) or name.startswith("."):
        sys.exit(f"invalid name {name!r}: use letters, digits, dot, dash, underscore")
    return name


def request(path, body=None, method="POST"):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"{API}{path}", data=data, method=method,
                                 headers={"xi-api-key": api_key(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read()[:800].decode(errors='replace')}")


def save(outdir, name, audio, meta):
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, name + ".mp3")
    with open(p, "wb") as f:
        f.write(audio)
    with open(os.path.join(outdir, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1, ensure_ascii=False)
    print("saved", p)


def main(argv):
    p = argparse.ArgumentParser(description="Generate SFX, music, or speech with ElevenLabs.")
    p.add_argument("cmd", choices=["sfx", "music", "tts", "voices"])
    p.add_argument("outdir", nargs="?")
    p.add_argument("name", nargs="?")
    p.add_argument("text", nargs="?")
    p.add_argument("--duration", type=float)
    p.add_argument("--influence", type=float, default=0.4)
    p.add_argument("--n", type=int, default=1)
    p.add_argument("--loop", action="store_true")
    p.add_argument("--length", type=int, default=60, help="music length in seconds")
    p.add_argument("--instrumental", action="store_true")
    p.add_argument("--voice")
    p.add_argument("--model", default="eleven_multilingual_v2")
    a = p.parse_args(argv[1:])

    if a.cmd == "voices":
        d = json.loads(request("/voices", method="GET"))
        for v in d.get("voices", []):
            labels = ", ".join(f"{k}={x}" for k, x in (v.get("labels") or {}).items())
            print(v["voice_id"], "|", v["name"], "|", labels)
        return
    if not (a.outdir and a.name and a.text):
        sys.exit("needs <outdir> <name> <text-or-prompt>")
    name = safe_name(a.name)

    if a.cmd == "sfx":
        body = {"text": a.text, "prompt_influence": a.influence}
        if a.duration:
            body["duration_seconds"] = a.duration
        if a.loop:
            body["loop"] = True
        for i in range(a.n):
            out = name if a.n == 1 else f"{name}-{i + 1}"
            save(a.outdir, out, request(f"/sound-generation?output_format={FMT}", body), body)
    elif a.cmd == "music":
        if os.path.isfile(a.text):
            with open(a.text, encoding="utf-8") as f:
                prompt = f.read().strip()
        else:
            prompt = a.text
        body = {"prompt": prompt, "music_length_ms": a.length * 1000}
        if a.instrumental:
            body["force_instrumental"] = True
        save(a.outdir, name, request(f"/music?output_format={FMT}", body), body)
    elif a.cmd == "tts":
        if not a.voice:
            sys.exit("needs --voice <voice_id> (see: elevenlabs.py voices)")
        body = {"text": a.text, "model_id": a.model}
        voice = urllib.parse.quote(a.voice, safe="")
        save(a.outdir, name, request(f"/text-to-speech/{voice}?output_format={FMT}", body),
             {**body, "voice_id": a.voice})


if __name__ == "__main__":
    main(sys.argv)
