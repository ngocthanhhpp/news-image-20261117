"""Draws entry.png: one front page summing up the world news of Tuesday 17 November 2026.

Run from the repository root:  python tools/draw.py
Needs Pillow and the Windows fonts Georgia, Arial and Arial Narrow (C:/Windows/Fonts).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONTS = Path("C:/Windows/Fonts")
OUT = Path(__file__).resolve().parent.parent / "entry.png"

INK = (24, 26, 33)
PAPER = (247, 243, 234)
NAVY = (18, 32, 58)
RED = (186, 32, 38)
MUTED = (92, 96, 106)
RULE = (196, 188, 172)
SEA = (60, 112, 160)
LAND = (226, 214, 188)

REGION = {
    "MIDDLE EAST": (186, 32, 38),
    "EUROPE": (36, 92, 170),
    "ASIA-PACIFIC": (20, 132, 110),
    "TECH & MARKETS": (110, 64, 160),
    "AFRICA": (200, 120, 20),
}


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, xy, text, f, width, fill, gap=4):
    x, y = xy
    for line in wrap(d, text, f, width):
        d.text((x, y), line, font=f, fill=fill)
        y += f.size + gap
    return y


def tag(d, xy, label):
    f = font("arialbd.ttf", 13)
    x, y = xy
    w = d.textlength(label, font=f) + 14
    d.rounded_rectangle((x, y, x + w, y + 21), radius=4, fill=REGION[label])
    d.text((x + 7, y + 3), label, font=f, fill="white")
    return y + 30


def flame(d, cx, cy, s=1.0):
    d.polygon([(cx, cy - 16 * s), (cx + 9 * s, cy + 2 * s), (cx + 5 * s, cy + 10 * s),
               (cx - 5 * s, cy + 10 * s), (cx - 9 * s, cy + 2 * s)], fill=(240, 120, 30))
    d.polygon([(cx, cy - 7 * s), (cx + 4 * s, cy + 4 * s), (cx, cy + 9 * s), (cx - 4 * s, cy + 4 * s)],
              fill=(255, 214, 80))


def hormuz_map(d, box):
    """A schematic (not to scale) of the Gulf and the Strait of Hormuz."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=SEA)
    def P(px, py):
        return (x0 + px * (x1 - x0), y0 + py * (y1 - y0))
    iran = [P(0, 0), P(1, 0), P(1, 0.30), P(0.80, 0.34), P(0.62, 0.40), P(0.45, 0.30), P(0.25, 0.22), P(0, 0.12)]
    arabia = [P(0, 0.62), P(0.20, 0.55), P(0.38, 0.70), P(0.55, 0.62), P(0.60, 0.48), P(0.66, 0.58),
              P(0.72, 0.62), P(0.86, 0.66), P(1, 0.80), P(1, 1), P(0, 1)]
    d.polygon(iran, fill=LAND)
    d.polygon(arabia, fill=LAND)
    d.ellipse((*P(0.55, 0.43), *P(0.68, 0.48)), fill=LAND)  # Qeshm
    d.ellipse((*P(0.17, 0.55), *P(0.21, 0.60)), fill=LAND)  # Bahrain
    lab = font("arialbd.ttf", 12)
    sm = font("arial.ttf", 11)
    d.text(P(0.40, 0.06), "IRAN", font=lab, fill=INK)
    d.text(P(0.10, 0.80), "ARABIA", font=lab, fill=INK)
    d.text(P(0.74, 0.70), "OMAN", font=lab, fill=INK)
    d.text(P(0.51, 0.50), "Qeshm", font=sm, fill="white")
    d.text(P(0.05, 0.47), "Bahrain", font=sm, fill="white")
    d.text(P(0.70, 0.44), "Strait of Hormuz", font=sm, fill="white")
    for px, py in [(0.76, 0.52), (0.84, 0.50), (0.90, 0.58)]:
        flame(d, *P(px, py), 0.9)
    # strike marks on Qeshm and the drone on Bahrain
    for (px, py) in [(0.615, 0.455), (0.19, 0.575)]:
        cx, cy = P(px, py)
        d.line((cx - 7, cy - 7, cx + 7, cy + 7), fill=RED, width=3)
        d.line((cx - 7, cy + 7, cx + 7, cy - 7), fill=RED, width=3)


def tile(d, box, region, head, body):
    x0, y0, x1, y1 = box
    y = tag(d, (x0, y0), region)
    y = block(d, (x0, y), head, font("georgiab.ttf", 21), x1 - x0, INK, 3)
    block(d, (x0, y + 4), body, font("arial.ttf", 14), x1 - x0, MUTED, 3)


def main():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    # Masthead
    d.rectangle((0, 0, W, 118), fill=NAVY)
    d.text((32, 16), "THE WORLD IN ONE PAGE  ·  WORLD NEWS OF THE DAY", font=font("arialbd.ttf", 15),
           fill=(176, 190, 214))
    d.text((32, 38), "Tuesday 17 November 2026", font=font("georgiab.ttf", 52), fill="white")
    d.rectangle((0, 118, W, 124), fill=RED)

    # Lead story
    M = 32
    y = tag(d, (M, 142), "MIDDLE EAST")
    y = block(d, (M, y), "Tankers ablaze in the Strait of Hormuz as the US–Iran war spreads",
              font("georgiab.ttf", 34), 560, INK, 4)
    bullets = [
        "A supertanker carrying over 2 million barrels of crude and a gas carrier are hit; Iran's Revolutionary Guard says by naval mines.",
        "Bahrain intercepts an Iranian drone aimed at a US radar at Sheikh Isa air base, the third such attack in five days.",
        "US forces strike Iran's Qeshm Island again; Pakistan, Qatar and Oman push to restart talks.",
    ]
    y += 6
    bf = font("arial.ttf", 16)
    for b in bullets:
        d.ellipse((M, y + 6, M + 7, y + 13), fill=RED)
        y = block(d, (M + 16, y), b, bf, 544, INK, 3) + 6
    hormuz_map(d, (624, 142, W - M, 398))
    d.text((624, 402), "Schematic, not to scale", font=font("ariali.ttf", 11), fill=MUTED)

    d.line((M, 424, W - M, 424), fill=RULE, width=2)

    # Second row
    col2 = (W - 2 * M - 32) // 2
    tile(d, (M, 440, M + col2, 600), "EUROPE",
         "Russia says Ukraine launched 2,000+ drones in a day, the war's biggest attack",
         "Kerch Bridge to Crimea struck for a second day; Russian strikes kill at least 7 in Ukraine and Kyiv logs a record 17 air-raid alerts.")
    d.line((M + col2 + 16, 444, M + col2 + 16, 596), fill=RULE, width=1)
    tile(d, (M + col2 + 32, 440, W - M, 600), "ASIA-PACIFIC",
         "Trump lands in Manila; the Quad signs critical-minerals deals to counter China",
         "Hundreds arrested at protests. Next: a first Trump–Xi–Putin summit in Shenzhen at APEC, and maybe Kim Jong Un.")

    d.line((M, 616, W - M, 616), fill=RULE, width=2)

    # Third row
    col3 = (W - 2 * M - 64) // 3
    xs = [M, M + col3 + 32, M + 2 * (col3 + 32)]
    tile(d, (xs[0], 632, xs[0] + col3, 820), "TECH & MARKETS",
         "Nvidia reports earnings without Jensen Huang",
         "First results since its CEO resigned on 12 Nov; shares are down about 39% from their October high.")
    tile(d, (xs[1], 632, xs[1] + col3, 820), "MIDDLE EAST",
         "Netanyahu aides accused of meddling in Israel's election",
         "Channel 12: tips to police led to arrests of Arab party activists on 27 Oct election day. He denies it.")
    tile(d, (xs[2], 632, xs[2] + col3, 820), "EUROPE",
         "Five EU states plan migrant 'return hub' in Rwanda",
         "Austria, Denmark, Germany, Greece and the Netherlands aim to start transfers by 2027.")
    for x in xs[1:]:
        d.line((x - 16, 636, x - 16, 816), fill=RULE, width=1)

    # Also today
    d.rectangle((0, 836, W, H), fill=(234, 227, 212))
    d.text((M, 850), "ALSO ON 17 NOVEMBER", font=font("arialbd.ttf", 14), fill=RED)
    also = [
        ("AFRICA", "Ebola in DR Congo spreads at a record pace: 11,254 cases, 5,505 deaths"),
        ("ASIA-PACIFIC", "Mongolia's president Khurelsukh says he will resign over a graft claim"),
        ("EUROPE", "Turkey raids opposition Sözcü TV and takes it off air"),
        ("ASIA-PACIFIC", "Japan scrambles jets as Russian aircraft enter its airspace off Fukuoka"),
        ("MIDDLE EAST", "Iraq and Jordan block Telegram  ·  COP31 climate talks go on in Antalya"),
    ]
    af = font("ARIALN.TTF", 16)
    y = 874
    for i, (reg, text) in enumerate(also):
        x = M if i % 2 == 0 else W // 2 + 8
        if i == 4:
            x = M
        d.rectangle((x, y + 4, x + 8, y + 14), fill=REGION[reg])
        d.text((x + 16, y), text, font=af, fill=INK)
        if i % 2 == 1 or i == 4:
            y += 26
    d.text((M, H - 24), "Sources: wire and daily news briefings published 17 Nov 2026 (Reuters, AP, AA, Democracy Now!, Foreign Exchanges).",
           font=font("ariali.ttf", 11), fill=MUTED)

    im.save(OUT, "PNG", optimize=True)
    print(OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
