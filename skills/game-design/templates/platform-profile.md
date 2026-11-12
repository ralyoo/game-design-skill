# <Platform / Engine> — Platform Profile

A platform profile is the single place where a target's technical rules live, so the design method stays the same across engines and platforms. Fill it from the platform's **official developer documentation**, not from reading engine or platform source code. Anything not documented is treated as unavailable and becomes a platform request in the GDD.

> Source of truth: <link to official docs> · Last checked: <date>
> If this profile and the docs disagree, the docs win.

## Shape of a game
- What runs where (device, server, client), who is authoritative:
- Player count, player identity (ids, names, colours):
- Packaging (project layout, manifest, who owns which folders):

## Input
- Devices (controller, touch, phone-as-controller, keyboard/mouse):
- Available controls/widgets and their limits:
- Latency notes (fast path vs. reliable events):
- What is not available (camera, gyro, custom drawing, …):

## Screens and presentation
- Reference resolution, viewing distance:
- Minimum text size:
- Second screens (if any) and what they can show:
- Accessibility: reduced motion, colour contrast, captions:

## Performance and budgets
- Frame-rate target and reference hardware:
- Download / memory budget for assets and audio:
- Rendering options (DOM, 2D, 3D) and physics:

## Lifecycle and screen ownership
- Lifecycle callbacks (load, start, input, tick, end):
- Screens the platform owns (store, lobby, system menu):
- Hooks the game can use to own opening, pause, results, play again, menu theme:
- Fallback behaviour when the game does not use a hook:

## Storage and progression
- What can persist between sessions, where, and size limits:
- Accounts, inventories, payments (available or not):

## Audio
- Output device(s), buses, mixer/ducking ownership, supported formats:

## Catalogue / store metadata
- Title, description, cover, icon, colour: limits and validation:

## Testing tools
- Simulator / dev server, profilers, linters, packaging commands:
