# Visual assets

Assets come **after** story, mechanics, and screen flow are approved. Assets exist to support the experience. If an asset is beautiful but does not help players understand or feel, cut it.

## 1. Art bible first (`design/art-bible.md`, template in `templates/art-bible.md`)

Before generating anything, write:
- Mood and 3 feeling words (same as the GDD's experience pillars).
- A locked palette with hex values: 1 dominant, 2 supporting, 1 accent, plus neutrals. Player colours defined by the platform must stay readable on this palette (measure contrast; see §6).
- Shape language (round = friendly, sharp = danger, square = stable), line weight, lighting, texture.
- Readability: every important object's silhouette is recognisable in 0.5 s from the play distance. Test with black silhouettes at real size.
- Hierarchy: players > threats > goals > decoration. Decoration is never busier than gameplay.
- **A complete asset list with a "how made" column**: `hand` (SVG written directly), `derived` (edited from a master), or `generated` (vector master from a generator). This list is also the generation budget (§3).

## 2. Pipeline

The rule that saves most of the cost: **generate as little as possible per asset, and make variations by editing SVG**, not by regenerating. Tool roles are defined in `providers.md`; Recraft is the recommended default because it outputs native SVG and supports reusable styles.

| Stage | Role (provider-agnostic) | Used for | Relative cost |
|---|---|---|---|
| **Sketch** | Cheap raster image model | Exploration: character shapes, composition, mood. At least 3 truly different visual directions. | Low |
| **Master** | Vector image model (or raster + vectoriser) | **One parent design** per character or complex object, after the owner picks a direction | High |
| **Harmonise** | Style reference / style lock | Created once from a good master, so later masters match | Low |
| **Derived** | **Hand-edit the SVG** | Poses, expressions, states (hit, dizzy, burnt), colour/player variants, sizes, shine, shadows | Zero |
| **Hand** | **Write SVG directly** | Simple shapes: arrows, ticks, sparkles, frames, receipts, panels, particles, lines, UI icons | Zero |

No generator at all? Skip Sketch/Master/Harmonise: sketch in words or simple SVG thumbnails, then write masters by hand. The rest of the pipeline is unchanged.

### Making derivatives from a master (the core saving)

1. **Turn the master into a rig.** Open the master SVG and group paths into `<g id="body">`, `<g id="eyes">`, `<g id="mouth">`, `<g id="arm-left">`, and so on. Split compound paths if needed. Save as `design/source/<character>-rig.svg`.
2. **Make variants by editing groups**, not by regenerating:
   - **Pose:** `transform` (rotate, translate, skew) on limb groups; squash & stretch on the body.
   - **Expression:** replace the eye and mouth groups (simple shapes: arcs, dots, crosses, dizzy spirals).
   - **State:** tint/darken fills; add sweat, stars, smoke, bandages as small hand-made shapes.
   - **Colour variant:** swap hex values from the palette. Never regenerate for another colour.
3. **Render and look.** Render SVG to PNG (`scripts/svg2png.mjs` or any SVG renderer), open the image, and check: identity holds, silhouette reads, line weight matches. Repeat until right.
4. **Hand animation to code where possible.** Wobble, breathing, squash, blink, and tint can be done at runtime from one pose. Write it in the asset integration notes instead of producing separate frames.

Identity does not drift because every variant comes from the same paths. Per-pose generation (text-to-image or image-to-image) has been shown to drift identity and to be expensive.

### When generating another master is allowed

- A new character or complex object that cannot be derived from an existing master.
- The master failed completely (not "needs tidying"). Small fixes are done in SVG.
- A pose that changes the whole drawing (e.g. back view) and cannot be reached by editing the rig. Try editing first.

Not allowed: vector generation for exploration, for colour variants, for simple props, or `n > 1` "to have options" after the direction is locked (options belong to the sketch stage).

## 3. Generation budget

- **Write the budget before production** in the Gate 2 package: number of planned masters and the reason per asset.
- Rule of thumb: **≤ 1 master generation per asset, at most 1 retry.** For a game with ~4 characters, a few complex objects, and a background, target **≤ 12 vector generations**. The first game designed without this rule used 41 (about 3,300 Recraft credits), roughly 400 of them on failed pose attempts. Do not repeat that. Going over budget requires the owner's approval with a reason.
- Remove backgrounds **locally** (flood-fill from edges on rasters, or delete background paths in SVG) rather than through a paid API that also tends to erase white parts of the object.
- Report usage per kind at the end: sketches × n, masters × n, styles × n, and how many final assets were made **without** generation.
- Keep parallel requests low (3–4, or the provider's limit).

## 4. Monotony warning (styles)

Style locks tend to flatten colour and form.
- The palette comes from the art bible, not the style. Name colours explicitly per object in prompts.
- Use separate styles per asset group when needed (characters vs. environment). Backgrounds are often better **without** a style; styled backgrounds frequently fail to fill to the edge.
- Check every batch: are players, threats, and background still easy to tell apart?

## 5. Helper scripts (optional)

```bash
# sketch (cheap raster)
python3 -I <skill>/scripts/recraft.py <outdir> <name> <prompt.txt> --n 4 --size 16:9
# master (vector), n=1
python3 -I <skill>/scripts/recraft.py <outdir> <name> <prompt.txt> --n 1 --model recraftv4_1_vector [--style-id <uuid>]
# style from 1–5 chosen masters (style model must match the generation model)
python3 -I <skill>/scripts/recraft.py style <outdir> <style-name> --model recraftv4_1_vector --base vector_illustration ref1.svg ref2.svg
# render SVG to PNG for inspection (install once: npm i --prefix ./.tools @resvg/resvg-js)
node <skill>/scripts/svg2png.mjs <in.svg> <out.png> [width-px] [background]
```

- The key is read from `RECRAFT_API_KEY`. If it is missing, do only `hand` and `derived` assets and say so in your report.
- Using another provider? Follow the adapter contract in `providers.md` so outputs, metadata, and budget reporting stay the same.
- Keep style ids, prompts (`design/prompts/`), and source SVGs (`design/source/`) so later assets stay consistent.
- Install helper tools locally in the working directory (`./.tools`), never globally, and never commit them.

## 6. Formats, budgets, and QA

- The source is always SVG. Runtime: SVG for flat shapes, or a WebP atlas for sprites (e.g. 256 px for a ~130 px display size). Never ship a 2048 px image for a 64 px object.
- Respect the platform profile's download and memory budgets. Assets used later load later; write the load order in the integration notes.
- Never bake text into images. Frames (receipts, boards, emblems) are empty with a **measured safe area**; the game renders text at the platform's minimum size.
- 3D: image generators do not make 3D models. Use them for textures, decals, UI, and icons.
- **Mockup QA is required before hand-off.** Assemble each screen from final assets, then check: hierarchy (background does not compete with the play area; darken/desaturate if needed), player-colour contrast on the game's background (below 3:1 → add an outline), text and safe areas, display sizes. Attach the mockups to your report with the fixes you made.

## 7. Licensing and records

Record every final asset in the game's `LICENSES.md`: file name, how made (hand / derived from which master / generated), provider and model, style id, prompt path, date. Check that your provider plan grants the commercial rights you need. Keep provenance metadata (e.g. C2PA manifests) in source files.

## 8. Review

Send an exploration board (a grid labelled A/B/C…) with one recommendation and the reason. The owner chooses and may mix ("A with the lighting of C"). Record decisions and rejections in the art bible.

## Recraft notes (verified November 2026; check current docs)

- Endpoint `POST https://external.api.recraft.ai/v1/images/generations`.
- `recraftv4_1_flash`: ~7 credits, WebP (1344×768 at 16:9). Good for sketches.
- `recraftv4_1_vector`: ~80 credits, SVG with a 2048 px viewBox. Accepts a `style_id` created with the same model.
- `POST /v1/styles` with `model=recraftv4_1_vector`, `style=vector_illustration`: ~5 credits.
- Vector image-to-image costs the same as a master and drifts identity. Do not use it for variants.
- If you truly need several poses from the generator: ask for **one sheet with several poses** in a single image (consistent identity, one generation), then split it in SVG.
