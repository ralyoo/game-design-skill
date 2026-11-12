# Contributing

Thanks for helping improve the skill.

## What fits

- Clearer wording, better examples, corrections to design theory references.
- New platform profiles under `skills/game-design/examples/` (written from official docs).
- Adapters for other generation providers that follow the contract in `skills/game-design/references/providers.md`.
- Lessons from shipped games, with concrete numbers where possible.

## What does not fit

- Content that ties the core workflow to one engine, platform, agent, or provider. Put platform specifics in a profile and provider specifics in a script or `providers.md`.
- New runtime dependencies in scripts. Standard library only, unless there is a strong reason.
- Anything copied from an existing game (names, characters, art, music, levels).

## Rules

1. Keep `SKILL.md` short; detail goes in `references/`. The `description` field stays under 1024 characters and says both *what* the skill does and *when* to use it.
2. Reference files by path relative to the skill folder, and make sure every referenced file exists.
3. Never commit secrets. Keys come from environment variables named `<PROVIDER>_API_KEY`.
4. Run the checks before opening a pull request:

   ```bash
   python3 -I tools/validate.py
   ```

5. Add a line to `CHANGELOG.md` under "Unreleased".

## Pull requests

Open pull requests against `dev`. Describe what changed and why. Maintainers merge into `main` for releases.
