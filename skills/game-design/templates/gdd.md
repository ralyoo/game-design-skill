# <Game Name> — Game Design Document

> Status: idea | concept | approved | production · Version · Date · Task/issue link
> Platform profile: <name and link>

## 0. One sentence
<Who does what, why, and what makes it fun.>

## 1. Experience pillars
- **Story** (what is this game about):
- **Motivation** (what do we need to do):
- **Experience** (what do I feel, physically and emotionally): 3 emotion words +
- Main MDA aesthetics: fellowship + …
- Designed peak moments (2–3):
- Lenses used (from `references/philosophy.md`) and why:

## 2. Concept
- High concept / player fantasy:
- Platform pillar or mode, player count, round and session length:
- Why it is fun to watch:
- Why it differs from other games in the catalogue:
- Feel references (not to copy):

## 3. Story and world
- World, characters, conflict, tone:
- How the story shows on screen without long text screens:
- Key lines (target language and register):

## 4. Mechanics
- Player verbs:
- Core loop (seconds) / round loop (minutes) / session loop:
- Rules, win/lose conditions, scoring:
- Input layout per phase (per device: controls, orientation, labels):
- Initial tuning numbers (table: name, value, reason, test range):
- Skill balancers (catch-up, luck, roles for eliminated players):

## 5. Unity
| Element | Feeling supported | If removed? |
|---|---|---|

## 6. Progression
- Within a session (round to round):
- Between sessions (where it is stored, per the platform profile):
- New content: characters, enemies, arenas/levels, items, skills, shop, collectibles:
- Level/content data: `design/data/*.json` (schema + example)

## 7. Screen flow & transitions
(See `references/screen-flow.md`. Required.)
- Flow diagram (mermaid): screen → trigger → duration → who can skip.

| # | Screen | Experience goal | Main screen | Second screen | Music/sound | Transition in | Buildable now / needs platform |
|---|---|---|---|---|---|---|---|

- Interim versions for screens that need the platform:
- Platform requests (which hook, why):

## 7b. Art direction (details in `design/art-bible.md`)
- Mood, palette (hex), shapes, line, light, camera:
- Style lock used (id, reason), and how monotony is avoided:
- Asset list (file name, size, format, how made, budget):

## 8. Experience control & juice
- Round tempo curve (tension–release):
- Juice per action (visual / audio / second-screen feedback):
- Reduced-motion alternatives:
- Music (mood, BPM, structure, dynamic intensity), SFX (list), announcer (details in `design/audio-bible.md`):

## 9. Risks and questions
- Design risks:
- Technical risks for developers (performance, missing platform capabilities):
- What playtests must prove:

## 10. Playtest plan
- Hypotheses, what to observe, success criteria.
