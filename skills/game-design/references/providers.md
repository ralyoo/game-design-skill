# Generation providers

Generation is **optional**. The method works with hand-written SVG and a written audio spec alone. When you do generate, this file defines the roles, the recommended defaults, and the contract any provider should follow so the rest of the workflow stays unchanged.

## 1. Roles

| Role | What it must do | Recommended default | Without an API |
|---|---|---|---|
| **Image sketch** | Cheap raster images for exploration | Recraft `recraftv4_1_flash` | Word sketches, quick SVG thumbnails |
| **Vector master** | One clean SVG per character/complex object | Recraft `recraftv4_1_vector` | Hand-written SVG |
| **Style lock** | Keep later masters consistent with chosen ones | Recraft styles | Strict art bible + reuse rig parts |
| **SFX** | Short sound effects from text | ElevenLabs sound generation | CC0/licensed libraries, synth tools |
| **Music** | Loopable instrumental tracks | ElevenLabs music | Licensed/commissioned music, DAW |
| **Voice** | Announcer/character lines | ElevenLabs text-to-speech | Recorded voice, or text-only announcer |

**Why the defaults:** Recraft outputs native SVG (which the derive-by-editing pipeline depends on) and supports reusable styles. ElevenLabs covers SFX, music, and voice with one key. Neither is required.

**Using something else:** any image model works for sketches. For masters, prefer a model that outputs SVG; otherwise generate a clean, flat raster and vectorise it (e.g. with an open-source tracer), then tidy the paths into a rig. Any audio source works if its licence covers your use. Check each provider's current docs and terms; models, prices, and endpoints change.

## 2. Adapter contract

If you write or adapt a script for another provider, keep these behaviours so budgets, records, and reviews stay comparable:

1. **Key from the environment only.** Name it `<PROVIDER>_API_KEY` (e.g. `RECRAFT_API_KEY`, `ELEVENLABS_API_KEY`). Never accept a key as a CLI argument (it lands in shell history), never print it, never write it to disk.
2. **Fail soft when the key is missing.** Exit with a clear message so the agent falls back to the no-API path and reports it.
3. **Save outputs + metadata side by side.** `<outdir>/<name>[-i].<ext>` plus `<name>.json` containing the request (prompt, model, parameters) and the non-secret response (ids, credits). This is the provenance for `LICENSES.md`.
4. **Fix file extensions from content**, not from what the API claims.
5. **Report cost per call** when the API returns it, so you can report usage per kind.
6. **Respect concurrency limits.** Default to sequential; parallelise only within the provider's limit.
7. **Standard library first.** Avoid extra dependencies; if one is needed, install it locally (`./.tools`), never globally.

## 3. Configuration

Copy `.env.example` (repository root) to `.env`, fill in only the keys you have, and load it into your shell or agent environment however your setup prefers. Keep `.env` out of version control.

| Variable | Used by |
|---|---|
| `RECRAFT_API_KEY` | `scripts/recraft.py` |
| `ELEVENLABS_API_KEY` | `scripts/elevenlabs.py` |

## 4. Reporting

At the end of an asset or audio pass, report:
- Provider and model per role.
- Count per kind (sketch × n, master × n, style × n, SFX × n, music seconds, TTS characters) and credits if known.
- How many final assets were made without generation.
- Anything skipped because a key was missing.
