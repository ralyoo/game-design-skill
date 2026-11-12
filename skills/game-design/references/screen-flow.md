# Screen flow & transitions

On the first game designed with this method, mechanics and visuals tested well, yet the owner's verdict was: **there are no transitions or screens (menu, after the round, and so on), and that is an essential part of game design.** That lesson applies to every game.

Why it matters: the peak-end rule. The opening sets expectations; the ending shapes memory. A game that jumps straight into the arena and then cuts to a generic score screen feels like a demo, not a game. Screens and transitions are where story, pride, and the reason to "play again" do their strongest work.

## 1. Required screens

Design all of these in the game's own visual and sound language. Write "not needed" only with a reason.

| # | Screen | Experience goal | Minimum content |
|---|---|---|---|
| 1 | **Title** | Enter the world. Identity, tone, theme music. | Logo/title, characters, a living background (idle animation), present players shown as characters |
| 2 | **How to play** | Understood in ≤ 10 seconds without reading paragraphs. | 1–3 illustrated panels or a short demo, controls, goal in one sentence. Skippable; auto-shown only on first session or on request. |
| 3 | **Ready / select** (optional) | Autonomy and identity. | Pick character, colour, team, or rules. Per-player "ready" indicator. |
| 4 | **Round intro** | Anticipation. | Round number, this round's twist, themed countdown |
| 5 | **In-round HUD** | Information without interference. | Only what is needed right now; hide the rest |
| 6 | **Round end** | Release and spotlight. | Who won the round and why, highlight/replay, running score |
| 7 | **Between rounds** | Breathe, then rebuild tension. | Standings, announcer banter, preview of next round |
| 8 | **Final results & celebration** | Fiero and the closing memory. | Themed podium, a funny title per player ("Most Often Burnt"), small stats, new records |
| 9 | **Play again / exit** | A reason for one more round. | Play again, change rules, back to lobby; progression teaser ("2 more sessions to unlock a new menu") |
| 10 | **Pause** | Safe to stop for a moment. | Themed, resume/exit |
| 11 | **Player disconnect / rejoin** | Does not break the mood. | Character "sleeps"/waits; game continues or holds according to the rules |

If the platform has second screens (phones, handhelds, a second monitor), write **what each one shows** on every screen: text, controls, and what the player can do. A second screen must never sit idle without a message.

## 2. Transitions

- Every screen change is a design moment: curtain, cut, zoom, themed wipe (a spatula sweeping the screen, a box lid closing). Avoid hard cuts unless intentional.
- Duration: 300–800 ms for normal transitions, up to 1.5 s for big moments. Round end to next round stays < 10 s total, and a host/lead player can skip ahead.
- Every transition has a sound (whoosh, stinger) and a music change (theme → round loop → win stinger → results theme).
- Reduced motion: replace large motion with fades/cuts and static frames.
- Draw the flow diagram (mermaid) in the GDD: screens, triggers, durations, who can skip.

## 3. Platform vs. game ownership

Most platforms own some screens (store, lobby, system menu) and let the game own the rest through hooks. Read the platform profile's **lifecycle and screen ownership** section and fill in a table like this in the GDD:

| Need | Hook / API | Notes |
|---|---|---|
| Own opening and countdown | e.g. a manifest flag | Does the platform show its own countdown otherwise? |
| Pause that truly stops | e.g. pause/resume callbacks | Without it, does the game keep running behind the menu? |
| Own results and "play again" | e.g. an end call with a game-owned screen | What is the fallback if the game never hands control back? |
| Themed system menus | e.g. theme tokens in a manifest | Scope and limits |

Design rules:
- **Use every available hook by default.** A complete game owns its opening, pause, results, and menu theme where the platform allows it. Platform fallbacks are a safety net.
- If the design needs something no hook provides, write it in the GDD under "Platform requests" (which hook, why), mark the screen **needs platform**, and provide an interim version that can be built today. Never assume a missing hook exists.

## 4. Gate 1 checklist

- [ ] All 11 screens designed or marked "not needed" with a reason.
- [ ] Screen flow + transition diagram with durations.
- [ ] Second-screen view for every screen (if the platform has one).
- [ ] Music/sound for every transition.
- [ ] Each screen marked buildable now / needs platform, plus the platform request list.
- [ ] Screen assets (title, how-to panels, podium, frames) listed in the art bible's asset list.
