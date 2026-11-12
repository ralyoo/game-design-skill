# Security Policy

## Reporting a vulnerability

Please **do not open a public issue** for security problems. Use GitHub's private vulnerability reporting instead: the **Security** tab of this repository → **Report a vulnerability**.

Include what you found, how to reproduce it, and the impact you expect. We aim to acknowledge reports within 7 days.

## Scope

- The skill's helper scripts (`skills/game-design/scripts/`).
- Instructions in the skill that could lead an agent to leak secrets, run unsafe commands, or install untrusted software.

Vulnerabilities in third-party services (Recraft, ElevenLabs, and others) should be reported to those vendors.

## Rules this repository follows

- No API keys, tokens, or credentials are ever committed. `.env` is git-ignored; only `.env.example` with empty values is tracked.
- Scripts read keys from environment variables only, never from CLI arguments, and never print, log, or save them.
- Scripts use only the Python standard library, call only HTTPS endpoints, and refuse non-HTTPS download URLs.
- Output file names are validated to prevent writing outside the chosen output folder.
- The skill tells agents to install helper tools locally (`./.tools`), never globally.
- CI runs `tools/validate.py`, which checks the skill structure and scans for common secret patterns.

If you accidentally commit a key: revoke it at the provider immediately, then remove it from history. Rotating the key matters more than rewriting history.
