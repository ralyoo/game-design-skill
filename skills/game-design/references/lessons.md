# Lessons from a shipped game

These lessons come from the first game designed with this method: a 2–4 player couch party game where phones are controllers and a laptop is the shared screen. The owner rated the result satisfying. Repeat what worked, fix what did not. Read before starting a new game.

## What worked: repeat it

- **One strong world sentence.** "The toppings refuse to be boxed" was approved immediately. The story gave a reason to every mechanic (knife, box, burning) and every screen (the food cart opening to closing).
- **Keep the feel that already works.** The old push numbers were left untouched; what was added was a world, a second verb, and a role for eliminated players. Redesign does not mean throwing away what feels right.
- **Eliminated players keep playing** (cutting, cheering). Nobody watches without a role.
- **Labelled option boards + one recommendation.** The owner decided in a single reply and could mix ("A, but with lighting like C").
- **Screens as part of the world.** Players never saw a "menu"; they saw the cart at work. Every transition was a movement from the story (awning rolled up, tray swept clean).
- **Every player leaves with something**: a funny per-player title in the final celebration, plus a progression teaser.
- **Second screens never idle**: one meaningful button on every screen ("Hi!", "Got it!", "Cheer").
- **QA through mockups made of final assets** caught problems before they reached developers: background too bright, a yellow player ring with poor contrast, the title overlapping an ornament, text below the minimum size.

## What fell short: fix it

- **Screen flow was missing from the first package**, costing an extra design round, an extra asset round, and three extra implementation tasks. → Screen flow is part of Gate 1 (see `screen-flow.md`).
- **Too many vector generations**: 41 images (~3,300 credits), ~400 of them on failed pose attempts. → One master per asset; variants edited in SVG (see `assets.md` §2–3).
- **Peak-based audio normalisation left SFX quiet** (hisses near −30 LUFS). → Match by loudness, then limit peaks (see `audio.md`).
- **Default TTS voices were English** for a non-English audience. → Use a native voice from the provider's library and send samples for the owner to hear.
- **Total assets exceeded the download target.** → Plan load order from the start: what the opening uses loads first, the rest follows.

## Hand-off to developers (proven pattern)

1. Once Gate 1 is approved, **immediately open implementation tasks for the mechanics** with testable acceptance criteria. Developers start with placeholders while assets are produced.
2. Write `design/asset-integration.md`: layers, display sizes, safe areas, which poses/states code produces (squash, tint, shine), an **event → audio file** map, load order, contrast rules.
3. Put numbers and content in data (`design/data/*.json`) so developers read data instead of copying from prose.
4. Separate tasks into (a) what can be built inside the game now and (b) new platform capabilities. State dependency order (e.g. "after the asset PR is merged").
5. Name the single most urgent fix when there is a feel bug (real example: "while the menu is open the knife keeps cutting; do the pause hook first").
6. Developers often have limited resources. Acceptance criteria must be checkable without running the whole test suite repeatedly.

## State your own limits

- If you cannot hear audio, check it by measurement (LUFS, peaks, waveform, loop seams), then **ask the owner to listen to a reel** and say what to listen for.
- If you can see images, render SVGs and mockups to PNG and inspect them before sending.
- API keys often cannot read quota. Report usage from your own count.
