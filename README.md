# game-design-skill

An agent skill for designing games with soul: from a one-sentence idea to approved assets, audio, and micro-feedback.

It packages the workflow and principles used to design games for [Ralyoo](https://docs.ralyoo.com), rewritten so they work for **any game, engine, or platform** and with **any (or no) generation API**.

## What's inside

- **A gated workflow:** idea → concept → story → mechanics → unity → progression → screen flow & transitions → assets → experience control & juice. Two approval gates keep expensive production from starting too early.
- **A player-psychology toolkit:** MDA, Self-Determination Theory, flow, interest curves, peak-end rule, game feel, and laws for local multiplayer.
- **Platform profiles:** one file that holds a target's technical rules (input, screens, budgets, lifecycle hooks), so the design method stays the same everywhere. Includes a template and a complete example.
- **A low-cost asset pipeline:** at most one generated vector master per asset; poses, expressions, states, and colour variants are edited by hand in SVG.
- **Audio direction and mastering:** audio bible, loudness targets, loop and voice practices.
- **Templates:** GDD, art bible, audio bible, platform profile.
- **Optional helpers:** stdlib-only Python callers for Recraft and ElevenLabs, and an SVG→PNG renderer.

```
skills/game-design/
├── SKILL.md                 entry point (workflow, rules, reference map)
├── references/              philosophy, screen flow, assets, audio, providers, lessons
├── templates/               gdd, art-bible, audio-bible, platform-profile
├── examples/                ralyoo-platform-profile.md
└── scripts/                 recraft.py, elevenlabs.py, svg2png.mjs (all optional)
```

## Install

The skill is a plain folder in the open [Agent Skills](https://agentskills.io) format (`SKILL.md` with YAML frontmatter plus supporting files). Nothing in it depends on a particular agent, IDE, or operating system. Pick one:

**Any agent (Claude Code, Codex, Cursor, and others), one command:**

```bash
npx skills add ralyoo/game-design-skill
```

The [`skills`](https://www.npmjs.com/package/skills) CLI asks which agents to install into and whether it is for this project or global. Add `-g` for global, `-a <agent>` to pick the agent, `-y` to skip prompts. Update later with `npx skills update`.

**Claude Code, as a plugin** (gets updates through `/plugin`):

```
/plugin install game-design --marketplace ralyoo/game-design-skill
```

On older Claude Code versions, use two steps: `/plugin marketplace add ralyoo/game-design-skill`, then `/plugin install game-design@ralyoo`.

**Claude apps (claude.ai, desktop):** download [`game-design.zip`](https://github.com/ralyoo/game-design-skill/releases/latest/download/game-design.zip) from the latest release and upload it as a skill.

**No Node, no git (macOS, Linux, WSL, Git Bash):** download only the skill folder into your agent's skills directory (this example targets Claude Code's personal folder):

```bash
mkdir -p ~/.claude/skills && curl -fsSL https://codeload.github.com/ralyoo/game-design-skill/tar.gz/main \
  | tar -xz -C ~/.claude/skills --strip-components=2 game-design-skill-main/skills/game-design
```

**Agents without skill support:** add the folder to your project and tell the agent to read `skills/game-design/SKILL.md` before design work (for example from `AGENTS.md` or your system prompt).

**Humans:** read `SKILL.md` top to bottom; it works as a design handbook too.

As with any skill, review it before use: skills run with your agent's permissions.

## Generation providers (optional)

Image and audio generation are recommended but never required. Without keys, the workflow falls back to hand-written SVG and written audio specs.

| Role | Recommended default | Env variable |
|---|---|---|
| Image sketch, vector master, style lock | [Recraft](https://www.recraft.ai) | `RECRAFT_API_KEY` |
| SFX, music, voice | [ElevenLabs](https://elevenlabs.io) | `ELEVENLABS_API_KEY` |

Prefer a different provider? `references/providers.md` defines each role and a small adapter contract (keys from the environment, outputs plus metadata side by side, cost reporting) so you can swap in anything.

```bash
cp .env.example .env    # fill in only the keys you have; .env is git-ignored
```

The helper scripts need Python 3.9+ and nothing else. `svg2png.mjs` needs Node 18+ and a local install of `@resvg/resvg-js` (instructions in the script).

## Using it with your platform

1. Copy `skills/game-design/templates/platform-profile.md` and fill it from your platform's or engine's official docs.
2. Point the agent at it before the mechanics stage.
3. See `skills/game-design/examples/ralyoo-platform-profile.md` for a complete example.

## Security

- No keys, tokens, or credentials live in this repository. Scripts read keys from environment variables only and never print or save them.
- Scripts use only the Python standard library and talk only to the provider's HTTPS API.
- Report vulnerabilities privately; see [SECURITY.md](SECURITY.md).

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

[MIT](LICENSE). Third-party services (Recraft, ElevenLabs, and others) have their own terms; check that your plan covers your use, especially commercial rights for generated assets.

---

**Bahasa Indonesia:** Skill ini mengemas alur dan prinsip desain game Ralyoo untuk publik: alur bergerbang dari ide sampai aset dan efek mikro, toolkit psikologi pemain, profil platform agar bisa dipakai untuk engine apa pun, serta pipeline aset hemat. Recraft dan ElevenLabs direkomendasikan tetapi opsional; provider lain bisa dipakai lewat kontrak adapter di `references/providers.md`.
