#!/usr/bin/env python3
"""World news of Thursday 19 November 2026, summed up in one image.

Deterministic: no network, no clock, no randomness. Draws a 1024x1024
PNG with Pillow from the fixed story list below and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

Stories were researched on 19 Nov 2026 from Reuters, AP/NPR, The Hindu,
IMD and other reporting of 19 Nov 2026; full sources are in SOURCES.md.
Two of the six stories are the day's scheduled headline events (the ICJ
verdict at 10:00 in The Hague and the Trump-Xi-Putin talks in Shenzhen);
at build time (early morning WIB) their outcomes were not yet known, so
the image states them as happening today, with no invented outcome.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 234)
NAVY = (11, 37, 69)
GOLD = (232, 184, 75)
INK = (17, 24, 39)
GREY = (71, 85, 105)
CARD = (255, 255, 255)
LINE = (216, 210, 196)

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def font(bold, size):
    for p in FONT_PATHS:
        if bold and "Bold" in p and os.path.exists(p):
            return ImageFont.truetype(p, size)
        if not bold and "Bold" not in p and os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    {
        "kicker": "CULTURE  •  GAMES",
        "color": (180, 35, 24),
        "headline": "GTA VI Arrives After 13 Years",
        "fact": "Rolls out at midnight in each market from New Zealand; Metacritic 99; ~16m copies, $1.5bn in pre-sales; PS5 and Xbox.",
        "icon": "gamepad",
    },
    {
        "kicker": "UNITED STATES  •  POLITICS",
        "color": (29, 78, 216),
        "headline": "Jeffries Nominated as First Black House Speaker",
        "fact": "House Democrats pick Jeffries 251-11; full House votes 3 Jan 2027; he would be the first Black Speaker.",
        "icon": "capitol",
    },
    {
        "kicker": "WORLD  •  JUSTICE",
        "color": (21, 128, 61),
        "headline": "World Court Rules Today on Rohingya Genocide",
        "fact": "ICJ delivers its verdict at 10:00 in The Hague, seven years after The Gambia filed the case; 700,000+ Rohingya fled in 2017.",
        "icon": "scales",
    },
    {
        "kicker": "DIPLOMACY  •  CHINA",
        "color": (180, 83, 9),
        "headline": "Trump, Xi and Putin Meet in Shenzhen",
        "fact": "Trilateral talks on the APEC sidelines; agenda: nuclear arms cuts and the US war with Iran.",
        "icon": "flags",
    },
    {
        "kicker": "INDIA  •  WEATHER",
        "color": (14, 116, 144),
        "headline": "Cyclone Akvan Nears India's East Coast",
        "fact": "Severe storm to cross between Narsapur and Puri by noon on 20 Nov; winds 90-100 km/h; schools shut in six Odisha districts.",
        "icon": "cyclone",
    },
    {
        "kicker": "EUROPE  •  UKRAINE",
        "color": (124, 58, 237),
        "headline": "EU Proposes \u20ac45 Billion Loan for Ukraine",
        "fact": "Brussels would borrow on capital markets to cover Kyiv's 2027 budget gap until Russia pays reparations.",
        "icon": "chart",
    },
]


def draw_icon(d, kind, x, y, s, color):
    if kind == "gamepad":
        # Controller body, d-pad and buttons
        d.rounded_rectangle([x + 4, y + 22, x + 64, y + 52], radius=12,
                            fill=color)
        d.polygon([(x + 4, y + 34), (x + 12, y + 26), (x + 16, y + 38),
                   (x + 16, y + 50), (x + 4, y + 46)], fill=color)
        d.polygon([(x + 64, y + 34), (x + 56, y + 26), (x + 52, y + 38),
                   (x + 52, y + 50), (x + 64, y + 46)], fill=color)
        d.rectangle([x + 16, y + 30, x + 26, y + 46], fill=(255, 255, 255))
        d.rectangle([x + 12, y + 34, x + 30, y + 42], fill=(255, 255, 255))
        for bx, by in [(x + 44, y + 30), (x + 54, y + 30), (x + 44, y + 40),
                       (x + 54, y + 40)]:
            d.ellipse([bx, by, bx + 7, by + 7], fill=(245, 158, 11))
        d.ellipse([x + 32, y + 44, x + 36, y + 48], fill=(255, 255, 255))
    elif kind == "scales":
        # Post, beam, two pans and base
        d.line([x + 34, y + 8, x + 34, y + 56], fill=color, width=5)
        d.line([x + 6, y + 14, x + 62, y + 14], fill=color, width=5)
        d.ellipse([x + 31, y + 4, x + 37, y + 10], fill=(245, 158, 11))
        for cx in (x + 6, x + 62):
            d.line([cx, y + 14, cx - 8, y + 34], fill=color, width=3)
            d.line([cx, y + 14, cx + 8, y + 34], fill=color, width=3)
            d.line([cx, y + 14, cx, y + 34], fill=color, width=3)
            d.pieslice([cx - 12, y + 30, cx + 12, y + 48], 0, 180,
                       fill=color)
        d.rectangle([x + 18, y + 56, x + 50, y + 64], fill=NAVY)
    elif kind == "cyclone":
        # Spiral bands around a calm eye
        for i, (rx, ry, w) in enumerate([(8, 10, 5), (20, 20, 5),
                                         (32, 30, 5), (44, 40, 5)]):
            d.arc([x + 34 - rx, y + 34 - ry, x + 34 + rx, y + 34 + ry],
                  start=200 + i * 55, end=380 + i * 55,
                  fill=color, width=w)
        d.ellipse([x + 28, y + 28, x + 40, y + 40], fill=(245, 158, 11))
        d.line([x + 4, y + 62, x + 64, y + 62], fill=NAVY, width=4)
    elif kind == "flags":
        # Two crossed flag poles, red and blue
        d.line([x + 20, y + 8, x + 20, y + 66], fill=NAVY, width=5)
        d.line([x + 48, y + 8, x + 48, y + 66], fill=NAVY, width=5)
        d.polygon([(x + 20, y + 8), (x + 46, y + 14), (x + 20, y + 26)],
                  fill=(180, 35, 24))
        d.polygon([(x + 48, y + 8), (x + 22, y + 14), (x + 48, y + 26)],
                  fill=(29, 78, 216))
        d.rectangle([x + 8, y + 62, x + 60, y + 70], fill=NAVY)
    elif kind == "capitol":
        # Dome, columns and base
        d.pieslice([x + 16, y + 6, x + 52, y + 34], 180, 360, fill=color)
        d.rectangle([x + 32, y + 2, x + 36, y + 10], fill=color)
        d.rectangle([x + 10, y + 34, x + 58, y + 40], fill=color)
        for cx in [x + 14, x + 26, x + 38, x + 50]:
            d.rectangle([cx, y + 40, cx + 4, y + 58], fill=color)
        d.rectangle([x + 6, y + 58, x + 62, y + 66], fill=NAVY)
        d.ellipse([x + 28, y + 42, x + 40, y + 56], fill=(255, 255, 255))
    elif kind == "chart":
        # Rising bars with an arrow
        bars = [(x + 6, 44), (x + 22, 34), (x + 38, 24), (x + 54, 12)]
        for bx, bh in bars:
            d.rectangle([bx, y + 66 - bh, bx + 12, y + 66], fill=color)
        d.line([x + 4, y + 66, x + 66, y + 66], fill=NAVY, width=4)
        d.line([x + 8, y + 52, x + 26, y + 40, x + 44, y + 28, x + 62, y + 12],
               fill=(245, 158, 11), width=5)
        d.polygon([(x + 62, y + 12), (x + 54, y + 10), (x + 58, y + 20)],
                  fill=(245, 158, 11))


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 156], fill=GOLD)
    f_date = font(True, 46)
    f_sub = font(True, 28)
    d.text((W // 2, 52), "THURSDAY 19 NOVEMBER 2026", font=f_date,
           fill=(255, 255, 255), anchor="mm")
    d.text((W // 2, 112), "THE WORLD IN ONE DAY  \u2022  SIX STORIES",
           font=f_sub, fill=GOLD, anchor="mm")

    # Story grid: 2 columns x 3 rows
    gx, gy = 16, 168
    pw, ph, gap = 490, 262, 12
    f_kick = font(True, 17)
    f_head = font(True, 27)
    f_fact = font(False, 18)
    for i, s in enumerate(STORIES):
        x = gx + (i % 2) * (pw + gap)
        y = gy + (i // 2) * (ph + gap)
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=10,
                            fill=CARD, outline=LINE, width=2)
        d.rectangle([x, y, x + pw, y + 8], fill=s["color"])
        d.text((x + 18, y + 26), s["kicker"], font=f_kick, fill=s["color"])
        draw_icon(d, s["icon"], x + pw - 88, y + 18, 68, s["color"])
        tx = x + 18
        tw = pw - 36
        lines = wrap(d, s["headline"], f_head, tw - 96)
        ly = y + 56
        for ln in lines[:3]:
            d.text((tx, ly), ln, font=f_head, fill=INK)
            ly += 33
        flines = wrap(d, s["fact"], f_fact, tw)
        ly += 6
        for ln in flines[:3]:
            d.text((tx, ly), ln, font=f_fact, fill=GREY)
            ly += 23

    # Footer
    f_foot = font(False, 16)
    d.text((W // 2, 1002),
           "Sources: Reuters  \u2022  AP/NPR  \u2022  The Hindu  \u2022  IMD  \u2014  All events reported on 19 November 2026",
           font=f_foot, fill=GREY, anchor="mm")

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "entry.png")
    img.save(out, "PNG", compress_level=6)
    print("wrote", out)


if __name__ == "__main__":
    main()
