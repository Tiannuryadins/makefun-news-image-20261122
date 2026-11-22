#!/usr/bin/env python3
"""Build-time poster renderer for news-image-20261122.

Renders poster.png (1024x1024) with PIL + DejaVu fonts. This script runs
only at build time; the submitted entry point is main.py, which copies
poster.png byte-for-byte to /output/entry.png (stdlib only, no network).

Stories (all verified 22 Nov 2026 morning cycle; see BUILD-TRANSCRIPT.md):
  LEAD  Iran strikes Bahrain (Sat night, 21 Nov; top story of the morning)
  1     M6.7 quake hits Peru (00:09 UTC, 21 Nov; morning-cycle story)
  2     COP31 close to a final deal (Sun 22 Nov, Reuters)
  3     'El Chapo Isidro' captured in Sinaloa (21 Nov, Reuters)
  4     82,500 march in France, 6th Saturday (21 Nov)
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

PAPER = (248, 244, 233)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
WHITE = (255, 255, 255)
RED = (185, 28, 28)
GREY = (110, 108, 100)
CARD = (255, 255, 255)
RULE = (180, 175, 160)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font."""
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip() if cur else word
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                # long word: hard-split by characters
                while draw.textlength(word, font=fnt) > max_w:
                    cut = len(word)
                    while cut > 1 and draw.textlength(word[:cut], font=fnt) > max_w:
                        cut -= 1
                    lines.append(word[:cut])
                    word = word[cut:]
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_lead_art(draw, x, y, w, h):
    """Night panel: missile streaks over dark ground, Bahrain label."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    for sx, sy in ((30, 26), (90, 60), (170, 30), (230, 70), (130, 90),
                   (60, 110), (200, 120), (260, 40), (150, 150), (40, 180)):
        draw.point((x + sx, y + sy), fill=WHITE)
        draw.point((x + sx + 1, y + sy), fill=WHITE)
    # moon
    draw.ellipse([x + w - 74, y + 22, x + w - 30, y + 66], fill=(232, 226, 205))
    draw.ellipse([x + w - 80, y + 16, x + w - 36, y + 60], fill=NAVY)
    # ground
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(12, 20, 38))
    draw.line([(x, y + h - 34), (x + 90, y + h - 58),
               (x + 190, y + h - 34)], fill=(12, 20, 38), width=2)
    # missile streaks ending in bursts
    for (x0, y0, x1, y1) in ((18, 18, 120, 128), (96, 10, 210, 138)):
        draw.line([(x + x0, y + y0), (x + x1, y + y1)], fill=(239, 68, 68), width=3)
        bx, by = x + x1, y + y1
        for dx, dy, r in ((0, 0, 6), (-8, -4, 3), (8, -4, 3), (-4, 8, 3),
                          (4, 8, 3), (-9, 0, 3), (9, 0, 3), (0, -9, 3), (0, 9, 3)):
            draw.ellipse([bx + dx - r, by + dy - r, bx + dx + r, by + dy + r],
                         fill=(250, 204, 21))
    f = font(BOLD, 26)
    draw.text((x + 14, y + h - 30), "BAHRAIN", font=f, fill=WHITE)


LEAD = {
    "kicker": "CONFLICT — GULF",
    "headline": "IRAN STRIKES BAHRAIN",
    "body": ("A missile-and-drone attack hit a civilian industrial site. "
             "Air defences intercepted the rest. No casualties. "
             "The IRGC says US bases were the target."),
}

CARDS = [
    ("Q", (194, 65, 12), "QUAKE — PERU",
     "M6.7 QUAKE HITS PERU",
     "One dead, 16 hurt. 156 homes damaged. Felt in Lima."),
    ("C", (15, 118, 110), "CLIMATE — ANTALYA",
     "COP31 CLOSE TO A DEAL",
     "Talks ran into overtime. A new package is on the table. "
     "Objections by 03:00 GMT."),
    ("M", (30, 58, 95), "CRIME — SINALOA",
     "'EL CHAPO ISIDRO' CAUGHT",
     "Mexico seizes an FBI most-wanted cartel boss, with US "
     "intelligence support."),
    ("F", (146, 64, 14), "PROTESTS — FRANCE",
     "82,500 MARCH IN FRANCE",
     "Sixth Saturday of cost-of-living protests. Turnout down "
     "from 106,000 last week."),
]


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    f_title = font(BOLD, 58)
    title = "THE WORLD IN ONE IMAGE"
    d.text(((W - d.textlength(title, font=f_title)) // 2, 28),
           title, font=f_title, fill=NAVY)
    f_date = font(BOLD, 28)
    date = "SUNDAY 22 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) // 2, 100),
           date, font=f_date, fill=INK)
    d.rectangle([24, 138, W - 24, 141], fill=NAVY)
    d.rectangle([24, 145, W - 24, 146], fill=NAVY)

    # ---- lead story
    f_kick = font(BOLD, 24)
    d.text((24, 162), LEAD["kicker"], font=f_kick, fill=RED)
    f_head = font(BOLD, 54)
    hy = 196
    for ln in wrap(d, LEAD["headline"], f_head, 660):
        d.text((24, hy), ln, font=f_head, fill=INK)
        hy += 62
    f_body = font(REG, 24)
    by = hy + 12
    for ln in wrap(d, LEAD["body"], f_body, 660):
        d.text((24, by), ln, font=f_body, fill=INK)
        by += 32
    draw_lead_art(d, 700, 160, 300, 300)

    # ---- story cards, 2 columns x 2 rows
    gx, gy, cw, ch, gap = 24, 484, 488, 240, 16
    for idx, (letter, colour, kicker, headline, body) in enumerate(CARDS):
        col, row = idx % 2, idx // 2
        x = gx + col * (cw + gap)
        y = gy + row * (ch + gap)
        d.rectangle([x, y, x + cw, y + ch], fill=CARD, outline=RULE, width=1)
        d.rectangle([x + 12, y + 12, x + 60, y + 60], fill=colour)
        f_tile = font(BOLD, 34)
        tw = d.textlength(letter, font=f_tile)
        d.text((x + 12 + (48 - tw) // 2, y + 16), letter, font=f_tile, fill=WHITE)
        f_ck = font(BOLD, 20)
        d.text((x + 72, y + 22), kicker, font=f_ck, fill=colour)
        f_ch = font(BOLD, 30)
        hy2 = y + 74
        for ln in wrap(d, headline, f_ch, cw - 24)[:2]:
            d.text((x + 12, hy2), ln, font=f_ch, fill=INK)
            hy2 += 36
        f_cb = font(REG, 22)
        by2 = hy2 + 6
        for ln in wrap(d, body, f_cb, cw - 24)[:3]:
            d.text((x + 12, by2), ln, font=f_cb, fill=(60, 58, 52))
            by2 += 29

    # ---- footer
    d.rectangle([24, 990, W - 24, 991], fill=RULE)
    f_foot = font(REG, 16)
    foot = "MAKE.FUN NEWS-IMAGE-20261122 — 5 STORIES FROM SUNDAY 22 NOVEMBER 2026"
    d.text(((W - d.textlength(foot, font=f_foot)) // 2, 998),
           foot, font=f_foot, fill=GREY)
    return img


if __name__ == "__main__":
    poster = render()
    poster.save("poster.png", optimize=True)
    print("wrote poster.png")
