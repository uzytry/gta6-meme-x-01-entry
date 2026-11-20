# Your job, in one page

You are entering make.fun's GTA 6 meme bounty: make one meme about GTA 6
(Rockstar's Grand Theft Auto VI, out this week) with make.fun's ghost mascot,
logo or name in the picture, post it on X from a public account with
make.fun (a link or written out) and/or a tag of @makefunai and your play
code in the post's text, telling people they can earn money on make.fun, and
hand in the post's address. An AI judge compares the posts two at a time,
and the top 50 share $500. The post itself is your entry: the judge sees its
first picture, then its text, exactly as the house read it from X.

## The meme (already made, in `meme.png`)

A Vice City sunset skyline with a neon loading bar stuck at 99% — and
make.fun's ghost mascot (the white ghost with sparkle eyes, holding its
magenta star coin, on its magenta disc) sitting on top of the bar, waiting
at the end of it. The caption reads:

- Top: "13 YEARS. 2 DELAYS. 1 DOWNLOAD BAR."
- On the bar: "99%"
- Under the bar: "STILL 47 HOURS REMAINING"
- Corner: "make.fun"

The joke is GTA 6 specific (the thirteen-year wait, the delays, the
download), the ghost is large and worked into the scene (not a corner
sticker), and every word is spelled right and readable at 480 px. The
picture was built in this session: an AI-generated Vice City scene, the
bar's fill stretched to 99%, the real press-kit ghost
(`https://make.fun/press/mark-1024.png`) composited onto the bar, and the
text overlaid with PIL — see `tools/compose.py` for the exact steps.

## The post (to be published on X)

Post `meme.png` as the first picture from a public X account, at or after
the bounty's opening (2026-11-19T14:00:00Z) and before its deadline
(2026-11-23T14:00:00Z), with exactly this text:

```
13 years. 2 delays. 1 download bar stuck at 99%. #GTA6

My AI agent made this meme — and it's competing for real money on @makefunai. People and their agents earn cash winning bounties on make.fun. Put yours to work: https://make.fun/bounty/gta6-meme-x-01

makefun-relay-hay-garden
```

The text carries the make.fun bounty link, the `@makefunai` tag, and the
play code `makefun-relay-hay-garden` (code 0 of the account's 4). Keep the
post up and the account public until the results are out.

## After the post is live

1. Copy the post's address (Share, then Copy link) and put it in
   `POST.json` as `{"url": "https://x.com/<handle>/status/<id>"}` —
   it currently holds the placeholder, which the gate refuses.
2. Run the program the way the grader does:
   `mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts`
   It copies `POST.json` to `out/POST.json` and prints nothing on success.
3. Commit, push, and submit the commit with the kit's CLI (see the kit's
   `RULES.txt`, Enter) together with the transcripts bundle.

## Hard rules

- One account per person; a team enters under one account.
- The repository is yours, created after the contest opens, under an
  OSI-approved license (MIT, see `LICENSE`).
- Upload the transcripts of every agent session that made the meme and
  wrote this repository: an entry without them is refused.
- No network, no wall clock and no files outside the repository in
  `main.ts`; the two runs of an entry must write the same bytes.
- At most 5 submissions a day and 10 in all. Each submission may name a
  new post; your last submission before the deadline is your final entry,
  and its post is the one judged.
