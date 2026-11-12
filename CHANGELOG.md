# Changelog

All notable changes to this skill are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- One-command install: `npx skills add`, a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`), a release workflow that publishes `game-design.zip`, and a curl/tar fallback.
- `tools/validate.py` checks the marketplace manifest.

## [0.1.0] - 2026-11-12

### Added
- `game-design` skill: gated design workflow, player-psychology toolkit, screen-flow requirements, asset and audio pipelines, lessons from a shipped game.
- Platform profile template and a complete Ralyoo example.
- GDD, art bible, and audio bible templates.
- Provider roles and adapter contract; optional Recraft and ElevenLabs helpers (stdlib only) and an SVG→PNG renderer.
- Repository checks (`tools/validate.py`) and CI.
