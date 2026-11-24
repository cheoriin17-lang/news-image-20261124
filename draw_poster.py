#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

Written from scratch for make.fun news-image-20261124 (post-opening
rewrite). All artwork is Pillow primitives: no network, no randomness,
no external assets, so the output is fully deterministic.

Usage:  python3 draw_poster.py   ->  writes entry.png next to this file.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ geometry
SIZE = 1024
MARGIN = 38
X0 = MARGIN
X1 = SIZE - MARGIN
SPAN = X1 - X0

# -------------------------------------------------------------------- palette
NEWS = (248, 243, 232)       # warm newsprint
INK = (18, 18, 18)           # near-black headline ink
KICK = (158, 27, 27)         # kicker red
SEA = (31, 58, 95)           # sea navy
TEXT = (52, 50, 46)          # body ink
FAINT = (92, 88, 80)         # dateline / footer grey
RULE = (178, 172, 158)       # hairline grey
GOLD = (232, 196, 90)        # ticker label gold
BAND = INK                   # ticker background

FONTS = Path("/usr/share/fonts/truetype/dejavu")

# -------------------------------------------------------------------- content
DATELINE = "TUESDAY  \u00b7  24 NOVEMBER 2026  \u00b7  ONE DAY, ONE PAGE"
TITLE = "THE DAILY GLOBE"
SUBTITLE = "The world\u2019s news, summed up in a single page"

TOP_KICKER = "UKRAINE  \u00b7  BENGHAZI, LIBYA"
TOP_LINES = ["SEA DRONES HIT", "RUSSIAN WARSHIP"]
TOP_DECK = (
    "Ukraine says seven naval drones struck the corvette Merkury at a "
    "Libyan naval base \u2014 2,400 km from the front \u2014 and hit the "
    "sanctioned arms cargo ship Angara."
)
TOP_LABEL = "2,400 KM FROM THE FRONT"

# (kicker, headline, body) — six cards, two columns by three rows.
CARDS = [
    (
        "IRAN WAR",
        "Trump: deal, or strikes after the New Year",
        "Trump says he is \u201cinclined\u201d to resume strikes if talks "
        "fail \u2014 but Iran still wants a deal.",
    ),
    (
        "CLIMATE",
        "EU defends COP31 walkout as summit lies in ruins",
        "Brussels calls a text silent on fossil fuels a deal that "
        "\u201cgreenwashes\u201d them; the talks end with no deal.",
    ),
    (
        "MARKETS",
        "Huang returns, Nvidia soars 31% in a day",
        "Nvidia\u2019s board reinstates its founder; shares soar 31%, "
        "adding about $950bn as the Nasdaq jumps 6.5%.",
    ),
    (
        "INDIA \u00b7 NEPAL",
        "Nepal PM Shah meets Modi on first Delhi visit",
        "Rapper-turned-PM Balendra Shah, in office since March, holds "
        "talks on energy, trade and flood recovery.",
    ),
    (
        "UKRAINE",
        "Russian strike on Dymer kills at least 11",
        "A drone and missile barrage hits towns near Kyiv; a child is "
        "among the dead in Kryvyi Rih as rescuers dig on.",
    ),
    (
        "SPORT",
        "India declare on a record 720/9 in Wellington",
        "Pant\u2019s 128 leads a record-breaking innings \u2014 the first "
        "ever with 50-plus stands for each of seven wickets.",
    ),
]

STRIP_HEAD = "ALSO TODAY  \u00b7  "
STRIP_BODY = (
    "NEW YORK: Mets sign Skubal for a record $450M   \u2022   NIGERIA: "
    "24 dead as a funeral boat capsizes   \u2022   WEST BANK: PM-elect "
    "calls settler arson \u201cJewish terrorism\u201d   \u2022   "
    "WASHINGTON: FBI probes police-database hack"
)

CREDIT = (
    "Sources: AP \u00b7 Reuters \u00b7 BBC \u00b7 Just Security \u00b7 "
    "Al Jazeera \u00b7 Wisden  \u2014  All stories dated 22\u201323 "
    "November 2026"
)


# -------------------------------------------------------------------- helpers
def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return font("DejaVuSerif.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning lines that fit inside width pixels."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        line = ""
        for word in words:
            trial = f"{line} {word}".strip()
            if not line or draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


class PageBuilder:
    """Draws the front page top to bottom, tracking a vertical cursor."""

    def __init__(self):
        self.canvas = Image.new("RGB", (SIZE, SIZE), NEWS)
        self.pen = ImageDraw.Draw(self.canvas)
        self.cursor = 0

    # -- small primitives ------------------------------------------------
    def hline(self, y, weight=1, colour=INK, left=X0, right=X1):
        self.pen.line([(left, y), (right, y)], fill=colour, width=weight)

    def center(self, text, y, fnt, colour=INK):
        width = self.pen.textlength(text, font=fnt)
        self.pen.text(((SIZE - width) / 2, y), text, font=fnt, fill=colour)

    def globe(self, cx, cy, radius, colour=INK, weight=3):
        p = self.pen
        p.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                  outline=colour, width=weight)
        p.ellipse([cx - radius // 2, cy - radius,
                   cx + radius // 2, cy + radius], outline=colour, width=2)
        p.line([(cx - radius, cy), (cx + radius, cy)], fill=colour, width=2)
        box = [cx - radius, cy - radius // 2, cx + radius, cy + radius // 2]
        p.arc(box, 200, 340, fill=colour, width=2)
        p.arc(box, 20, 160, fill=colour, width=2)

    # -- sections --------------------------------------------------------
    def header(self):
        self.cursor = 30
        self.center(DATELINE, self.cursor, sans_b(15), FAINT)
        name_y = self.cursor + 34
        self.globe(X0 + 34, name_y + 48, 30)
        self.globe(X1 - 34, name_y + 48, 30)
        self.center(TITLE, name_y, serif_b(72))
        self.center(SUBTITLE, self.cursor + 118, serif(19), FAINT)
        base = self.cursor + 152
        self.hline(base, weight=4)
        self.hline(base + 8, weight=1)
        self.cursor = base + 16

    def ship_and_waves(self, cx, cy, radius):
        """Stylised corvette above two wave lines, inside a sea circle."""
        p = self.pen
        p.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                  outline=SEA, width=4)
        hull = [(cx - 44, cy - 6), (cx + 40, cy - 6), (cx + 30, cy + 12),
                (cx - 34, cy + 12)]
        p.polygon(hull, fill=SEA)
        p.rectangle([cx - 14, cy - 26, cx + 8, cy - 6], fill=SEA)
        p.line([(cx - 2, cy - 42), (cx - 2, cy - 26)], fill=SEA, width=3)
        p.polygon([(cx - 2, cy - 42), (cx + 14, cy - 34), (cx - 2, cy - 32)],
                  fill=KICK)
        for dy in (26, 40):
            points = []
            for step in range(-radius + 8, radius - 7, 8):
                x = cx + step
                y = cy + dy + 5 * math.sin(step / 14.0)
                points.append((x, y))
            p.line(points, fill=SEA, width=3, joint="curve")

    def lead(self):
        top = self.cursor
        text_w = 640
        self.pen.text((X0, top), TOP_KICKER, font=sans_b(17), fill=KICK)
        head = serif_b(54)
        hy = top + 30
        for line in TOP_LINES:
            self.pen.text((X0, hy), line, font=head, fill=INK)
            hy += 62
        deck = serif(21)
        dy = hy + 6
        for line in wrap(self.pen, TOP_DECK, deck, text_w):
            self.pen.text((X0, dy), line, font=deck, fill=INK)
            dy += 28
        self.ship_and_waves(830, 300, 72)
        label = sans_b(13)
        label_w = self.pen.textlength(TOP_LABEL, font=label)
        self.pen.text((830 - label_w / 2, 300 + 72 + 12), TOP_LABEL,
                      font=label, fill=KICK)
        self.cursor = 444

    def card(self, x, y, width, kicker, headline, body):
        p = self.pen
        p.text((x, y), kicker, font=sans_b(15), fill=KICK)
        hy = y + 24
        size = 25
        while size > 12:
            head = serif_b(size)
            lines = wrap(p, headline, head, width)
            if len(lines) <= 2:
                break
            size -= 1
        for line in lines:
            p.text((x, hy), line, font=head, fill=INK)
            hy += 30
        body_f = sans(16)
        by = hy + 2
        for line in wrap(p, body, body_f, width)[:3]:
            p.text((x, by), line, font=body_f, fill=TEXT)
            by += 21
        return by

    def grid(self):
        top = self.cursor + 8
        gap = 28
        col_w = (SPAN - gap) // 2
        split = X0 + col_w + gap // 2
        row_h = 154
        for index, (kicker, headline, body) in enumerate(CARDS):
            row, col = divmod(index, 2)
            x = X0 if col == 0 else split + gap // 2
            cy = top + row * row_h
            if row > 0:
                self.hline(cy - 12, weight=1, colour=RULE)
            self.card(x, cy, col_w, kicker, headline, body)
        bottom = top + 3 * row_h
        self.hline(bottom - 12, weight=1, colour=RULE)
        self.pen.line([(split, top), (split, bottom - 24)],
                      fill=RULE, width=1)
        self.cursor = bottom

    def strip(self):
        top = self.cursor + 6
        height = 64
        self.pen.rectangle([X0, top, X1, top + height], fill=BAND)
        head = sans_b(15)
        self.pen.text((X0 + 14, top + 22), STRIP_HEAD, font=head, fill=GOLD)
        head_w = self.pen.textlength(STRIP_HEAD, font=head)
        body = sans(15)
        lines = wrap(self.pen, STRIP_BODY, body,
                     X1 - (X0 + 14 + head_w) - 14)
        ty = top + 12 if len(lines) > 1 else top + 22
        for line in lines[:2]:
            self.pen.text((X0 + 14 + head_w, ty), line, font=body, fill=NEWS)
            ty += 21
        self.cursor = top + height + 14

    def credits(self):
        self.hline(self.cursor - 8, weight=1, colour=RULE)
        self.center(CREDIT, self.cursor + 2, sans(13), FAINT)

    def build(self):
        self.header()
        self.lead()
        self.grid()
        self.strip()
        self.credits()
        return self.canvas


def main():
    page = PageBuilder()
    image = page.build()
    out = Path(__file__).resolve().parent / "entry.png"
    image.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
