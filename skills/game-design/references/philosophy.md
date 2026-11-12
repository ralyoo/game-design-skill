# Design philosophy and player psychology

A toolbox, not dogma. Use the lenses that fit, and write in the GDD which lens you used and why.

## 1. Start from the experience (MDA, reversed)

Hunicke, LeBlanc, Zubek: **Mechanics → Dynamics → Aesthetics.** Developers build from the left, players feel from the right. Designers **start from the right**: decide the feeling (aesthetics) first, then the dynamics that produce it, then the mechanics.

The eight MDA aesthetics: sensation, fantasy, narrative, challenge, fellowship, discovery, expression, submission. For local multiplayer, **fellowship is almost always required**, plus one or two others.

## 2. Player motivation

- **Self-Determination Theory** (Deci & Ryan): people are driven by *competence* (I am getting better), *autonomy* (I choose), and *relatedness* (I am with them). A good round gives all three.
- **Player types** (Bartle, adapted for groups): *challengers* (want to win), *entertainers* (want to make people laugh), *explorers* (want to try tricks), *spectators* (want to join without pressure). A real group mixes all four; give each a moment.
- **Intrinsic over extrinsic.** Rewards (coins, trophies) amplify an activity that is already fun; they do not replace fun. Overjustification effect: rewards that are too prominent make play feel like work.
- **Clear goals, immediate feedback, meaningful actions.** Players always know: what is my goal, what just happened because of me, what can I choose now.

## 3. Flow and difficulty

- **Flow** (Csikszentmihalyi): challenge matches skill. Too hard → anxiety, too easy → boredom. The flow path is a wave, not a straight line: tense, release, tenser.
- **Interest curve** (Schell): a hook, small rises and falls, a climax at the end. Even a 60–120 second round has this curve.
- **Easy to learn, hard to master.** The core rule fits in one sentence on screen and one button label. Depth comes from interaction between players, not from extra rules.
- **Group difficulty ≠ solo difficulty.** Players of different skill share the same couch. Balancing tools: soft *catch-up* (the leader becomes a target, stronger items for those behind), *controlled luck* (variance that gives hope without making skill meaningless), short rounds (losing one round does not hurt), and *elimination without long waits* (eliminated players keep a role: ghost, saboteur, betting spectator).
- **Avoid kingmaking and runaway leaders**: the winner must not be decided halfway through a round.

## 4. Satisfaction

- **Fun is learning** (Koster): enjoyment comes from mastering patterns. When patterns run out, the game gets boring → progression must open new patterns.
- **Mastery loop**: try → fail with a clear cause → understand → succeed. Failure must feel *fair* and *funny*, not punishing.
- **Peak moments**: design 2–3 moments that make people shout ("SO CLOSE!", "HOW?!"). Write them in the GDD before detailing mechanics; mechanics are built to produce them.
- **Peak-end rule**: people remember the peak and the end. Results screens, highlight replays, and the last seconds of a round deserve real attention.
- **Fiero**: pride after overcoming a challenge. Give it a pause and a spotlight.

## 5. Game feel and juice

- **Game feel** (Swink): input → response → context → polish. Response must feel **< 100 ms** from press to picture and sound.
- **Juice**: squash & stretch, screen shake (respect reduced motion), hit-stop 40–80 ms, particles, flashes, popping numbers, layered sounds. Every important action gives feedback on every available channel: visual, audio, and haptic/text on any second screen.
- **Anticipation → action → reaction.** Telegraph before it happens, so players can react and failure feels fair.
- **Experience control**: steer tempo with music (intensity rises in the last 20 seconds), camera, and information. Reduce UI noise in tense moments.

## 6. Unity

Every element (story, mechanic, asset, sound, text) answers to the same experience pillars. Quick test for each element:
1. Which feeling does this element support?
2. If removed, is anything lost?
3. Does it contradict the story?

Example: a game about slippery chilli-sauce couriers → slipping mechanic, wet arena, squelchy SFX, fast upbeat folk-pop, chilli-red palette. Horror theme with goofy sounds = unity failure, unless it is deliberate horror-comedy.

## 7. Local multiplayer laws

Apply when players share a room or a screen. Adapt or drop for online or solo games, and say so in the GDD.

- **The shared screen is a stage.** Spectators must understand and laugh along. Design for the audience, not only the players.
- **Eyes on the shared screen.** Personal devices are controllers; players should not need to look down unless the mechanic is a deliberate "secret screen".
- **Player interaction is the content.** Push, betray, cooperate, shout instructions.
- **Zero onboarding.** The first round is the tutorial. No long rules screen.
- **Short sessions, fast replay.** Rounds of 45–150 seconds; results to next round < 10 seconds.
- **Fun at every player count.** Check in your head: is it fun with the minimum? With the maximum?

## Idea test (before concept)

Score 1–5. An idea passes with a total ≥ 22 and no score of 1:
- Can it be explained in one sentence?
- Is it fun to watch?
- Does it create interaction between players (or, for solo games, between player and world)?
- Does it have a clear peak moment?
- Does it fit the platform's input model (see the platform profile)?
- Does it have an identity distinct from other games in the same catalogue?
- Can it be built within the platform's performance budget?
