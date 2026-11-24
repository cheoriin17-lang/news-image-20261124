#!/usr/bin/env python3
"""Draw the news-image-20261124 variant front page (v2, split layout).

A one-page newspaper front page for 24 November 2026: the lead story
in a left column with a "by the numbers" strip, a tall dusk-sea
illustration panel on the right, then six stories in a three-column
grid, a black ticker strip and a sources footer. All stories are the
verified 23-24 Nov 2026 facts from the live entry; only the layout
and artwork differ.

Render: python3 draw_poster.py  -> writes entry.png (1024x1024).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 241, 229)
INK = (17, 17, 17)
RED = (163, 22, 33)
NAVY = (31, 58, 95)
GREY = (85, 85, 85)
RULE = (60, 60, 60)
GOLD = (212, 175, 55)
DUSK_TOP = (22, 35, 62)
DUSK_MID = (39, 75, 115)
GLOW = (217, 123, 63)
SEA = (22, 50, 78)
SUN = (232, 161, 60)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    if not os.path.exists(path):
        path = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
    return ImageFont.truetype(path, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


def sea_panel(draw, x0, y0, x1, y1):
    """Dusk over Benghazi naval base: dark sky, low sun, corvette
    with smoke, sea drones closing in on dotted paths."""
    draw.rectangle([x0, y0, x1, y0 + 200], fill=DUSK_TOP)
    draw.rectangle([x0, y0 + 200, x1, y0 + 225], fill=DUSK_MID)
    draw.rectangle([x0, y0 + 225, x1, y0 + 250], fill=GLOW)
    draw.rectangle([x0, y0 + 250, x1, y1 - 36], fill=SEA)
    # low sun on the horizon
    draw.ellipse([x1 - 96, y0 + 196, x1 - 48, y0 + 244], fill=SUN)
    # corvette silhouette with smoke
    hx0, hx1, hy = x0 + 24, x1 - 90, y1 - 96
    draw.polygon([(hx0, hy), (hx1, hy), (hx1 - 26, hy + 22),
                  (hx0 + 30, hy + 22)], fill=INK)
    draw.rectangle([hx0 + 66, hy - 26, hx0 + 150, hy], fill=INK)
    draw.rectangle([hx0 + 100, hy - 44, hx0 + 112, hy - 26], fill=INK)
    draw.line([hx0 + 106, hy - 44, hx0 + 106, hy - 62], fill=INK, width=3)
    draw.polygon([(hx0 + 106, hy - 62), (hx0 + 128, hy - 56),
                  (hx0 + 106, hy - 50)], fill=RED)
    for ex, ey, er in ((hx0 + 84, hy - 52, 14), (hx0 + 72, hy - 78, 18),
                       (hx0 + 88, hy - 104, 22)):
        draw.ellipse([ex - er, ey - er, ex + er, ey + er],
                     fill=(140, 140, 140))
    # sea drones on dotted approach paths
    for dx, dy in ((x1 - 66, y0 + 96), (x1 - 40, y0 + 132),
                   (x1 - 110, y0 + 150)):
        for t in range(0, 11):
            px = dx + (hx1 - dx) * t / 10.0
            py = dy + (hy - dy) * (t / 10.0) ** 1.4
            if t % 2 == 0:
                draw.ellipse([px - 2, py - 2, px + 2, py + 2],
                             fill=(255, 255, 255))
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=INK,
                     outline=(255, 255, 255), width=1)
    # wave lines
    for wy in (y1 - 66, y1 - 52):
        for wx in range(x0 + 10, x1 - 30, 64):
            draw.arc([wx, wy, wx + 56, wy + 14], start=200, end=340,
                     fill=(120, 160, 195), width=2)
    # caption band
    draw.rectangle([x0, y1 - 36, x1, y1], fill=(16, 16, 16))
    centered(draw, (x0 + x1) // 2, y1 - 29,
             "BENGHAZI NAVAL BASE  —  SUNDAY NIGHT", SANS_B(14),
             fill=(255, 255, 255))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def story_cell(draw, x, y, w, kicker, headline, deck):
    draw.text((x, y), kicker, font=SANS_B(15), fill=RED)
    y += 21
    hf = SERIF_B(21)
    lines = wrap(draw, headline, hf, w)
    for ln in lines[:2]:
        draw.text((x, y), ln, font=hf, fill=INK)
        y += 26
    y += 3
    df = SERIF(15)
    for ln in wrap(draw, deck, df, w)[:2]:
        draw.text((x, y), ln, font=df, fill=(40, 40, 40))
        y += 19
    return y


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # dateline
    centered(d, W // 2, 26, "TUESDAY  ·  24 NOVEMBER 2026  ·  WORLD EDITION",
             SANS_B(19), fill=GREY)
    # masthead
    centered(d, W // 2, 56, "THE DAILY GLOBE", SERIF_B(78), fill=INK)
    # tagline
    centered(d, W // 2, 148, "The world's news, summed up in a single page",
             SERIF_I(22), fill=GREY)
    # double rule
    d.line([40, 182, W - 40, 182], fill=RULE, width=3)
    d.line([40, 188, W - 40, 188], fill=RULE, width=1)

    # ---- split zone: lead column (left) + sea panel (right) ----
    # lead kicker + headline + deck
    d.text((40, 206), "UKRAINE  ·  BENGHAZI, LIBYA", font=SANS_B(20),
           fill=RED)
    y = 236
    for ln in ("UKRAINE DRONES", "HIT RUSSIAN", "WARSHIP OFF LIBYA"):
        d.text((40, y), ln, font=SERIF_B(48), fill=INK)
        y += 58
    deck = ("Seven sea drones struck the corvette Merkury at Benghazi "
            "naval base — 2,400 km from the front.")
    y = 420
    for ln in wrap(d, deck, SERIF(22), 580):
        d.text((40, y), ln, font=SERIF(22), fill=(40, 40, 40))
        y += 27
    # by-the-numbers strip
    d.line([40, 500, 620, 500], fill=RULE, width=1)
    stats = [("7", "SEA DRONES"), ("2,400 KM", "FROM THE FRONT"),
             ("2", "SHIPS HIT")]
    for i, (num, lab) in enumerate(stats):
        cx = 40 + i * 194 + 97
        centered(d, cx, 510, num, SERIF_B(30), fill=NAVY)
        centered(d, cx, 544, lab, SANS_B(12), fill=GREY)
        if i:
            d.line([40 + i * 194, 508, 40 + i * 194, 556],
                   fill=(180, 176, 168), width=1)
    # sea illustration panel
    sea_panel(d, 636, 200, W - 40, 556)

    # rule above the grid
    d.line([40, 572, W - 40, 572], fill=RULE, width=2)

    stories = [
        ("IRAN",
         "Trump: deal, or strikes after New Year",
         "Trump: close to a deal — but 'inclined' to resume strikes if "
         "talks fail."),
        ("CLIMATE",
         "COP31 ends with no deal as EU walks out",
         "Longest UN climate talks ever end with no deal as the EU and UK "
         "walk out."),
        ("MARKETS",
         "Huang back; Nvidia +31%",
         "Jensen Huang reinstated as CEO 11 days after resigning; "
         "Nasdaq +6.5%."),
        ("NEPAL",
         "Nepal PM Shah meets Modi",
         "Balendra Shah holds talks on energy, trade and flood recovery "
         "in Delhi."),
        ("UKRAINE",
         "Russian strike kills at least 11 in Dymer",
         "Strikes also hit Kryvyi Rih — a child among the dead; 25 blocks "
         "damaged."),
        ("SPORT",
         "India post record 720/9 in Wellington",
         "Pant hits 128 as India post the highest Test total ever on "
         "NZ soil."),
    ]
    col_w = 296
    col_x = [40, 364, 688]
    # vertical dividers
    d.line([352, 588, 352, 868], fill=(180, 176, 168), width=1)
    d.line([676, 588, 676, 868], fill=(180, 176, 168), width=1)
    # horizontal divider between rows
    d.line([40, 720, W - 40, 720], fill=(180, 176, 168), width=1)
    for i, (kick, head, deck_txt) in enumerate(stories):
        row, col = divmod(i, 3)
        story_cell(d, col_x[col], 588 + row * 140, col_w, kick, head,
                   deck_txt)

    # ticker strip (two fixed lines: line 1 shares the bar with the label)
    d.rectangle([40, 884, W - 40, 936], fill=INK)
    d.text((56, 894), "ALSO TODAY", font=SANS_B(16), fill=GOLD)
    d.text((206, 895),
           "METS SIGN SKUBAL FOR $450M — RECORD PITCHER DEAL  ·  NIGERIA "
           "FUNERAL BOAT CAPSIZES, 24 DEAD",
           font=SANS(14), fill=(255, 255, 255))
    d.text((56, 912),
           "EISENKOT CALLS SETTLER ARSON “JEWISH TERRORISM”  ·  FBI PROBES "
           "HACK OF NATIONAL POLICE DATABASE",
           font=SANS(14), fill=(255, 255, 255))

    # footer
    centered(d, W // 2, 948,
             "Sources: AP · NPR · Reuters · Just Security · Wisden · ESPN  —  "
             "Stories verified 23–24 November 2026",
             SANS(14), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
