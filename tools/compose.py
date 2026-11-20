#!/usr/bin/env python3
"""Compose the gta6-meme-x-01 meme: Vice City loading-bar scene + make.fun ghost.

This is the exact script that produced meme.png in this repository. It was
run from the build session with these working files:
  - the background: an AI-generated Vice City dusk scene with an empty neon
    loading bar (no text), saved as bg-loading.png
  - the ghost: make.fun's press-kit mark (https://make.fun/press/mark-1024.png)

Steps:
  1. Stretch the neon bar's pink fill to 99% (the joke: stuck at 99%).
  2. Seat the whole press-kit mark on top of the loading bar, at its 99%
     end, with a soft contact shadow — the ghost is the character waiting
     at the end of the bar, not a corner sticker.
  3. Overlay crisp meme text with PIL (correct spelling, readable at 480px).

Asset paths default to the build session's working files; pass them as
environment variables to rebuild elsewhere:
  MEME_BG, MEME_MARK, MEME_OUT
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BG = os.environ.get('MEME_BG', '/tmp/gta6meme/media-generation-bg-loading-0-8e18aadb-9db2-45d6-9967-ed0af3cbd75e.png')
MARK = os.environ.get('MEME_MARK', '/tmp/gta6meme/mark-1024.png')
OUT = os.environ.get('MEME_OUT', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'meme.png'))

BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

img = Image.open(BG).convert('RGBA')
W, H = img.size
px = img.load()

# --- measured bar geometry (2352x1008 image) --------------------------------
bar_left, bar_top, bar_right, bar_bottom = 483, 762, 1879, 862
mid_y = (bar_top + bar_bottom) // 2
print('bar bbox', bar_left, bar_top, bar_right, bar_bottom)

# --- locate the pink fill inside the bar (measured: ends ~x1087) --------------
fill_left, fill_right = 485, 1087
print('fill', fill_left, fill_right, 'mid_y', mid_y)
inner_top = bar_top + 8
inner_bottom = bar_bottom - 8

# --- stretch the fill to 99% of the inner track (flat end: fill stops here) --
target_right = bar_left + int((bar_right - bar_left) * 0.99)
slice_x0 = fill_left + 60
slice_x1 = fill_left + 160
slice_img = img.crop((slice_x0, inner_top, slice_x1, inner_bottom))
stretched = slice_img.resize((target_right - slice_x0, inner_bottom - inner_top))
img.paste(stretched, (slice_x0, inner_top))

# --- ghost: the whole press-kit mark, as shipped (its own alpha) ------------
mark = Image.open(MARK).convert('RGBA')
bbox = mark.getchannel('A').getbbox()
ghost = mark.crop(bbox)
print('ghost bbox', bbox, 'size', ghost.size)
# scale: ghost ~300px tall, sitting on the bar
GH = 300
gw = int(ghost.size[0] * GH / ghost.size[1])
ghost = ghost.resize((gw, GH), Image.LANCZOS)
gx = int(W * 0.68 - gw / 2)
gy = bar_top - GH + 18  # feet just overlapping the bar's top edge

# soft contact shadow on the bar under the ghost
shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.ellipse([gx + 10, bar_top - 6, gx + gw - 10, bar_top + 26], fill=(0, 0, 0, 140))
shadow = shadow.filter(ImageFilter.GaussianBlur(8))
img = Image.alpha_composite(img, shadow)
img.paste(ghost, (gx, gy), ghost)
print('ghost placed at', gx, gy, 'size', gw, GH)

# --- meme text (white, black outline) ---------------------------------------
draw = ImageDraw.Draw(img)

def text_center(y, s, size, stroke=6):
    f = ImageFont.truetype(BOLD, size)
    bb = draw.textbbox((0, 0), s, font=f, stroke_width=stroke)
    tw = bb[2] - bb[0]
    draw.text(((W - tw) / 2 - bb[0], y), s, font=f, fill='white',
              stroke_width=stroke, stroke_fill='black')
    return bb[3] - bb[1]

text_center(28, '13 YEARS. 2 DELAYS.', 108, stroke=7)
text_center(158, '1 DOWNLOAD BAR.', 108, stroke=7)

# 99% label above the bar's right end
f99 = ImageFont.truetype(BOLD, 58)
bb99 = draw.textbbox((0, 0), '99%', font=f99, stroke_width=4)
draw.text((target_right - (bb99[2] - bb99[0]) - bb99[0], bar_top - 78),
          '99%', font=f99, fill='white', stroke_width=4, stroke_fill='black')

# punchline under the bar
text_center(bar_bottom + 18, 'STILL 47 HOURS REMAINING', 66, stroke=5)

# make.fun name, bottom-right corner
fname = ImageFont.truetype(BOLD, 44)
bb = draw.textbbox((0, 0), 'make.fun', font=fname, stroke_width=4)
draw.text((W - (bb[2] - bb[0]) - 36 - bb[0], H - (bb[3] - bb[1]) - 28 - bb[1]),
          'make.fun', font=fname, fill='white', stroke_width=4, stroke_fill='black')

img.convert('RGB').save(OUT, 'PNG')
print('saved', OUT)
