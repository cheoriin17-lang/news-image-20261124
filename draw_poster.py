#!/usr/bin/env python3
"""Render THE DAILY GLOBE — a 1024x1024 newspaper front page summing up
24 November 2026 world news. Stdlib + Pillow only. Deterministic output.

Run:  python3 draw_poster.py
Writes entry.png next to this file.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (247, 243, 234)      # warm newsprint
INK = (17, 17, 17)           # near-black
RED = (178, 28, 28)          # kicker / accent red
NAVY = (26, 42, 74)          # lead headline + sea
SKY = (214, 231, 242)        # motif sky
SEA = (47, 109, 163)         # motif sea
GREY = (90, 86, 78)          # footer grey
RULE = (120, 112, 98)        # thin rule grey

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load a DejaVu font, falling back to Pillow's default bitmap font."""
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except (OSError, IOError):
        return ImageFont.load_default()


SERIF_BOLD = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, fnt, fill):
    """Draw one line centred on the page."""
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)


def draw_masthead(draw):
    draw_centered(draw, 18, "THE DAILY GLOBE", SERIF_BOLD(68), INK)
    draw.line([(40, 102), (984, 102)], fill=RULE, width=2)
    draw.line([(40, 107), (984, 107)], fill=RULE, width=1)
    draw_centered(draw, 118, "TUESDAY  \u2014  24 NOVEMBER 2026  \u00b7  WORLD EDITION",
                  SANS_BOLD(19), INK)


def draw_lead(draw):
    draw_centered(draw, 150, "UKRAINE DRONES HIT", SERIF_BOLD(46), NAVY)
    draw_centered(draw, 198, "RUSSIAN WARSHIP OFF LIBYA", SERIF_BOLD(46), NAVY)
    deck = ("Seven sea drones struck the corvette Merkury at Benghazi naval "
            "base \u2014 2,400 km from the front. The sanctioned arms ship "
            "Angara was also hit; a Ka-27 helicopter destroyed.")
    fnt = SANS(20)
    lines = wrap(draw, deck, fnt, 920)
    y = 254
    for line in lines:
        draw_centered(draw, y, line, fnt, INK)
        y += 26


def draw_motif(draw):
    """Simple ship-and-waves scene in a framed box."""
    x0, y0, x1, y1 = 40, 310, 984, 428
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    # Sky and sea.
    draw.rectangle([x0 + 2, y0 + 2, x1 - 2, y0 + 58], fill=SKY)
    draw.rectangle([x0 + 2, y0 + 58, x1 - 2, y1 - 2], fill=SEA)
    # Sun.
    draw.ellipse([880, y0 + 12, 924, y0 + 56], fill=(240, 196, 90))
    # Caption inside the sky, top left.
    draw.text((x0 + 14, y0 + 12), "SEVEN DRONES  \u00b7  2,400 KM FROM THE FRONT",
              font=SANS_BOLD(15), fill=NAVY)
    # Ship: hull, cabin, mast, red flag.
    hull = [(300, y0 + 82), (700, y0 + 82), (660, y0 + 108), (340, y0 + 108)]
    draw.polygon(hull, fill=(30, 30, 34))
    draw.polygon([(430, y0 + 82), (560, y0 + 82), (560, y0 + 58),
                  (430, y0 + 58)], fill=(60, 60, 66))
    draw.line([(500, y0 + 58), (500, y0 + 14)], fill=(30, 30, 34), width=4)
    draw.polygon([(500, y0 + 14), (500, y0 + 32), (536, y0 + 23)],
                 fill=RED)
    # Portholes.
    for cx in (380, 440, 500, 560, 620):
        draw.ellipse([cx - 5, y0 + 90, cx + 5, y0 + 100], fill=(220, 225, 230))
    # Waves: three white arcs across the sea.
    for wy, wx0 in ((y0 + 66, 60), (y0 + 88, 760), (y0 + 106, 180)):
        draw.arc([wx0, wy, wx0 + 150, wy + 26], start=180, end=360,
                 fill=(235, 242, 248), width=4)
    # Drones: small dark dots with dashed approach lines, kept clear of
    # the caption at the top left of the sky.
    for dx, dy in ((640, y0 + 18), (720, y0 + 26), (800, y0 + 14)):
        draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=INK)
        draw.line([(dx, dy + 6), (dx - 26, dy + 34)], fill=INK, width=1)


def draw_card(draw, x, y, w, h, kicker, headline, deck):
    draw.line([(x, y), (x + w, y)], fill=INK, width=2)
    draw.text((x, y + 10), kicker, font=SANS_BOLD(15), fill=RED)
    fnt_h = SERIF_BOLD(22)
    lines = wrap(draw, headline, fnt_h, w - 8)
    hy = y + 32
    for line in lines[:2]:
        draw.text((x, hy), line, font=fnt_h, fill=INK)
        hy += 26
    fnt_d = SANS(16)
    dlines = wrap(draw, deck, fnt_d, w - 8)
    dy = hy + 4
    for line in dlines[:2]:
        draw.text((x, dy), line, font=fnt_d, fill=(40, 40, 40))
        dy += 21


def draw_cards(draw):
    cards = [
        ("IRAN", "TRUMP: DEAL, OR STRIKES AFTER NEW YEAR",
         "Close to a deal, Trump tells Fox News \u2014 but \u201cinclined\u201d "
         "to resume strikes if talks fail."),
        ("CLIMATE", "COP31 ENDS WITH NO DEAL AS EU WALKS OUT",
         "The longest UN climate talks ever end with no deal after the "
         "EU and UK walk out."),
        ("MARKETS", "HUANG BACK; NVIDIA +31%",
         "Board reinstates Jensen Huang as CEO 11 days after his "
         "resignation; Nasdaq +6.5%."),
        ("NEPAL", "NEPAL PM SHAH MEETS MODI",
         "Balendra Shah holds talks on energy, trade and flood recovery "
         "in Delhi."),
        ("UKRAINE", "DYMER STRIKE KILLS AT LEAST 11",
         "Overnight strikes also hit Kryvyi Rih \u2014 a child among the "
         "dead; 25 blocks damaged."),
        ("SPORT", "INDIA DECLARE ON RECORD 720/9",
         "Pant hits 128 in Wellington as India post the highest Test "
         "total ever on NZ soil."),
    ]
    col_w, row_h = 462, 132
    xs = [40, 522]
    ys = [446, 590, 734]
    for i, (kicker, headline, deck) in enumerate(cards):
        draw_card(draw, xs[i % 2], ys[i // 2], col_w, row_h,
                  kicker, headline, deck)


def draw_ticker(draw):
    draw.rectangle([24, 882, 1000, 936], fill=INK)
    fnt = SANS_BOLD(15)
    line1 = ("METS SIGN SKUBAL FOR $450M \u2014 RECORD PITCHER DEAL"
             "   \u00b7   NIGERIA FUNERAL BOAT CAPSIZES, 24 DEAD")
    line2 = ("EISENKOT CALLS SETTLER ARSON \u201cJEWISH TERRORISM\u201d"
             "   \u00b7   FBI PROBES HACK OF NATIONAL POLICE DATABASE")
    draw_centered(draw, 891, line1, fnt, (255, 255, 255))
    draw_centered(draw, 912, line2, fnt, (255, 255, 255))


def draw_footer(draw):
    draw.line([(40, 952), (984, 952)], fill=RULE, width=1)
    draw_centered(draw, 962,
                  "Sources: AP \u00b7 NPR \u00b7 Reuters \u00b7 Just Security "
                  "\u00b7 Wisden \u00b7 ESPN \u2014 Stories verified 23\u201324 November 2026",
                  SANS(13), GREY)
    draw_centered(draw, 984, "THE DAILY GLOBE \u2014 THE WORLD IN ONE DAY",
                  SANS_BOLD(12), GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    draw_motif(draw)
    draw_cards(draw)
    draw_ticker(draw)
    draw_footer(draw)
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, img.size, img.mode)


if __name__ == "__main__":
    main()
