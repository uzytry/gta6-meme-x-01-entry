// gta6-meme-x-01 entry (Node 22, standard library only).
//
// The entry itself is a post on X: an AI-made GTA 6 meme, posted from a
// public account with make.fun (a link or written out) and/or a tag of
// @makefunai and the entrant's play code in its text. POST.json at this
// repository's root names that post's address, and the house reads the post
// from X itself (its first picture and its text) and hands that to the
// judge. Nothing this program writes about the post is judged.
//
// So all this program has to do is hand POST.json to the grader: it reads
// POST.json from the repository, checks it is a JSON object, and writes it
// byte for byte to /output/POST.json, where the gate reads it.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const sourcePath = join(BOT_DIR, 'POST.json');
const outputPath = join(OUTPUT_DIR, 'POST.json');

mkdirSync(OUTPUT_DIR, { recursive: true });

let postText: string;
try {
  postText = readFileSync(sourcePath, 'utf8');
} catch (err) {
  console.error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

let post: unknown;
try {
  post = JSON.parse(postText);
} catch (err) {
  console.error(`POST.json is not valid JSON: ${(err as Error).message}`);
  process.exit(1);
}

if (typeof post !== 'object' || post === null || Array.isArray(post)) {
  console.error('POST.json must be a JSON object, {"url": "https://x.com/<handle>/status/<id>"}');
  process.exit(1);
}

const postUrl = (post as { url?: unknown }).url;
if (typeof postUrl !== 'string' || postUrl.length === 0) {
  console.error('POST.json must name the post: {"url": "https://x.com/<handle>/status/<id>"}');
  process.exit(1);
}

// The starter placeholder is no post's address, so the gate refuses it.
// Warn loudly instead of failing: the file is still copied, and the gate
// is the place that refuses a placeholder.
if (postUrl.includes('<handle>') || postUrl.includes('<id>')) {
  console.error('WARNING: POST.json still holds the placeholder address — replace it with the live post before submitting.');
}

writeFileSync(outputPath, postText);
