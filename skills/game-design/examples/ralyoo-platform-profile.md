# Ralyoo — Platform Profile (example)

An example profile for [Ralyoo](https://docs.ralyoo.com), the couch party-game platform this method was first used on: a laptop or tablet is the shared host screen, and players' phones become controllers in the browser (scan a QR code, no install). Use it as a model for writing your own profile with `templates/platform-profile.md`.

> **Source of truth:** the Ralyoo developer docs, https://docs.ralyoo.com. Agent-friendly Markdown: https://docs.ralyoo.com/llms.txt (index) and https://docs.ralyoo.com/llms-full.txt (single file). If this example and the docs disagree, the docs win. Read these pages before designing mechanics: **Concepts**, **Controller**, **Lifecycle and screen flow**, **Design guidelines**, and **Assets, libraries, and budget**.

## Shape of a game

- The host (laptop/tablet) runs game logic. The server only relays. A game is a bundle in a sandboxed iframe that talks to the platform through `@ralyoo/sdk`.
- 2–4 players. Each has an `id` 1–4, a `name`, and a `color` from the platform.
- Lifecycle: `preload` (during the platform countdown, or before a game-owned opening) → `onStart` → `onInput` / `onTick` → `ctx.end(scores)`, or `ctx.end(scores, { team: 'win' | 'lose' })` for co-op.
- A game is its **own project**, created from a template (`npm create @ralyoo/game`):

```
<game>/
  ralyoo.json      manifest: title, description, cover, icon, colour, players, pillar
  src/             code (developers)
  assets/          final assets (read via ctx.assets.url)
  assets/meta/     catalogue icon and cover
  design/          GDD, art bible, audio bible, exploration boards (designer)
  LICENSES.md      source and licence of every asset
```

The designer writes `design/`, `assets/`, level/content data (`design/data/*.json`), the title/description/`media` in `ralyoo.json`, and `LICENSES.md`. `src/` belongs to developers.

## Input (the phone controller)

The controller is not game code. The game sends a **declarative JSON layout** and the phone renders built-in widgets:

| Widget | Content |
|---|---|
| `text` | Text, size `m` / `l` |
| `button` | A/B/X/Y or another id, `label`, `tone` |
| `dpad` | 4 directions |
| `joystick` | `stick` and/or `stick2`, values −1..1 |
| `cards` | Pages of cards (title + body), player swipes |
| `vote` | Question + options, player picks |

- Layouts: `pad` or `stack`. Orientation: `any`, `portrait`, `landscape`. Widget count and text length limits are on the **Controller** page.
- Layouts can differ per player and change at any time (phase, secret role, eliminated player).
- No custom images, canvas, gyroscope, camera, or microphone on the phone. A new widget is a platform request with a strong reason.
- Buttons and sticks use the fast (low-latency) path. Cards and votes are reliable events, not for reflexes.

## Screens and presentation

- Reference 1920×1080, read from a sofa 2–3 m away. **Minimum text size 28 px.**
- Respect `ctx.reducedMotion`: alternatives for screen shake, flashes, and camera shake.
- Sound comes only from the host, through `sfx` / `music` / `voice` buses.
- The phone must never sit idle: one meaningful button on every screen.

## Performance and budgets

- **60 fps on a laptop with integrated graphics.** Avoid hundreds of active physics bodies, heavy post-processing, unbounded particles.
- Total visuals per game < 1 MB; total assets (with audio) downloaded during the opening < 1.5 MB. Later assets load later.
- Rendering: DOM/CSS (quizzes, cards, words); PixiJS v8 + Rapier2D (2D, sprites, vectors). Three.js + Rapier3D exist on the platform, but the Ralystudioo simulator currently supports 2D only; design new games as 2D unless the owner asks otherwise.

## Lifecycle and screen ownership

The platform owns the game-select lobby and the host menu. Everything else can be owned by the game through SDK hooks:

| Need | Hook | Notes |
|---|---|---|
| Own opening and countdown | `"opening": "game"` in `ralyoo.json` | The platform skips "3·2·1·GO!"; `onStart` runs as soon as `preload` finishes. Play again also skips the platform countdown. |
| Pause that truly stops | `onPause` / `onResume`, `ctx.paused` | Without `onPause` the game keeps running behind the menu. Duck music with `ctx.audio.mix`. |
| Own results and "play again" | `ctx.end(scores, { screen: 'game' })`, then `ctx.exit('again' \| 'lobby')` | If `exit` does not arrive within 60 s, the platform shows a generic results screen. |
| Themed pause menu | `"theme"` in `ralyoo.json` (panel, accent, text, frame, labels) | Applies while the game is showing. |

## Storage and progression

- Per-host settings in `ctx.storage` (host device only, 16 KB per key). No accounts, cross-device inventory, or paid store yet; cross-session progression must live in host storage.

## Pillars

- **Console** (`konsol`): everyone watches the host screen, phones are gamepads.
- **Secret screen** (`rahasia`): phones show private information (role, manual, cards).
- The manifest accepts only these two. Other pillars go into the GDD as platform requests.

## Audio

- Played via `ctx.audio.play('<file>', { bus: 'sfx' | 'music' | 'voice' })`. Mixer, ducking, and bus levels belong to the platform. `ctx.audio.mix({ db, lowpassHz, rampMs })` ducks music (pause, eliminated player).

## Catalogue metadata (enforced on upload)

- **Title** ≤ 22 characters (one line in the lobby). **Description** ≤ 100 characters (two lines).
- **Cover** 16:9, at least 1280×720, at most 500 KB. **Icon** square, single colour on transparent (used as a mask), SVG preferred.
- **Game colour** `#rrggbb` readable on the dark host background (contrast ≥ 3:1).

## Testing tools: Ralystudioo

- `npm run dev` opens a simulator: host screen plus 1–4 virtual phones, with disconnect/reconnect, latency, and reduced-motion controls. Use it to check screen flow, hierarchy, and safe areas with final assets.
- The `GAME` row in the HUD shows fps and frame time; the **Bundle** panel shows total size and the largest files. Use those numbers for the Gate 2 asset budget.
- `npm run lint` validates manifest, cover, icon, and sizes as on upload.
- `npm run pack` produces a `.ralyoo` bundle for submission.

## Audience notes

The first audience was Indonesian university students hanging out in groups of 2–4. Announcer lines and on-screen text were written in casual Indonesian. Adapt language and register to your own audience.
