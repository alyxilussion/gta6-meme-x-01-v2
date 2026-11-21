#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 v2 meme: CITY OF LOS SANTOS parking violation ticket.

Deterministic (no randomness): two runs produce byte-identical output.
Canvas 1024x1024. Text is sized to stay legible at the judge's 480x480 view.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

# --- palette ---
CREAM = (255, 246, 224)
BLACK = (16, 16, 16)
RED = (200, 16, 46)
MAGENTA = (230, 0, 126)
BLUE = (30, 90, 168)
YELLOW = (255, 210, 63)
WHITE = (255, 255, 255)
PURPLE_TOP = (43, 10, 74)
PURPLE_BOT = (74, 14, 107)
GREY = (90, 90, 90)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def star_points(cx, cy, outer, inner, points=5, rot=-90):
    pts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        a = math.radians(rot + i * 180 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def sparkle_points(cx, cy, r):
    """Four-pointed sparkle (diamond star with concave edges)."""
    k = 0.22
    return [
        (cx, cy - r),
        (cx + r * k, cy - r * k),
        (cx + r, cy),
        (cx + r * k, cy + r * k),
        (cx, cy + r),
        (cx - r * k, cy + r * k),
        (cx - r, cy),
        (cx - r * k, cy - r * k),
    ]


def draw_ghost(draw, x, y, s):
    """make.fun ghost: white body, thick black outline, two sparkle eyes,
    small round hand holding a magenta coin with a white star.
    (x, y) = top-left of the bounding box, s = body width."""
    # Body outline: rounded top + straight sides + 3-wave hem.
    w = s
    h = int(s * 1.15)
    top = y + int(s * 0.42)
    hem_y = y + h
    wave = w / 3.0
    pts = []
    # Top semicircle (left -> right over the top).
    cx = x + w / 2.0
    cy = top
    for deg in range(180, 361, 6):
        a = math.radians(deg)
        pts.append((cx + (w / 2.0) * math.cos(a), cy + (w / 2.0) * math.sin(a)))
    # Right side down to the hem.
    pts.append((x + w, hem_y - wave * 0.35))
    # Three waves along the hem (right -> left).
    for i in range(3):
        wx1 = x + w - i * wave
        wx0 = x + w - (i + 1) * wave
        mx = (wx0 + wx1) / 2.0
        for t in range(0, 13):
            frac = t / 12.0
            px = wx1 + (wx0 - wx1) * frac
            py = hem_y - wave * 0.35 + math.sin(frac * math.pi) * wave * 0.35
            pts.append((px, py))
    # Left side back up.
    pts.append((x, top))
    draw.polygon(pts, fill=WHITE, outline=BLACK, width=max(3, s // 16))
    # Sparkle eyes.
    er = s * 0.11
    draw.polygon(sparkle_points(x + w * 0.36, y + h * 0.38, er), fill=BLACK)
    draw.polygon(sparkle_points(x + w * 0.64, y + h * 0.38, er), fill=BLACK)
    # Round hand on the right side.
    hx, hy, hr = x + w * 0.92, y + h * 0.62, s * 0.11
    draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=WHITE, outline=BLACK,
                 width=max(2, s // 22))
    # Magenta coin with a white star, held up by the hand.
    coin_cx, coin_cy, coin_r = x + w * 1.02, y + h * 0.42, s * 0.20
    draw.ellipse([coin_cx - coin_r, coin_cy - coin_r, coin_cx + coin_r, coin_cy + coin_r],
                 fill=MAGENTA, outline=BLACK, width=max(2, s // 22))
    draw.polygon(star_points(coin_cx, coin_cy, coin_r * 0.62, coin_r * 0.26),
                 fill=WHITE)


def draw_stamp(base, cx, cy, lines, angle=-12):
    """Red double-bordered rotated stamp on its own layer."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f1 = font("DejaVuSans-Bold.ttf", 34)
    f2 = font("DejaVuSans-Bold.ttf", 28)
    w1 = d.textlength(lines[0], font=f1)
    w2 = d.textlength(lines[1], font=f2)
    bw = int(max(w1, w2)) + 36
    bh = 34 + 28 + 40
    x0, y0 = cx - bw // 2, cy - bh // 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=10,
                        outline=RED + (255,), width=6)
    d.rounded_rectangle([x0 + 10, y0 + 10, x0 + bw - 10, y0 + bh - 10], radius=6,
                        outline=RED + (255,), width=3)
    d.text((cx, y0 + 14), lines[0], font=f1, fill=RED + (255,), anchor="ma")
    d.text((cx, y0 + 14 + 40), lines[1], font=f2, fill=RED + (255,), anchor="ma")
    layer = layer.rotate(angle, center=(cx, cy), resample=Image.BICUBIC)
    return Image.alpha_composite(base, layer)


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "meme.png"
    img = Image.new("RGB", (W, H), PURPLE_TOP)
    draw = ImageDraw.Draw(img)

    # Background: vertical purple gradient (deterministic).
    for yy in range(H):
        t = yy / (H - 1)
        c = tuple(int(PURPLE_TOP[i] + (PURPLE_BOT[i] - PURPLE_TOP[i]) * t)
                  for i in range(3))
        draw.line([(0, yy), (W, yy)], fill=c)

    # Ticket paper.
    TX0, TY0, TX1, TY1 = 36, 28, 988, 996
    draw.rounded_rectangle([TX0, TY0, TX1, TY1], radius=18, fill=CREAM)

    # Header band (black, rounded top matching the ticket).
    draw.rounded_rectangle([TX0, TY0, TX1, 148], radius=18, fill=BLACK)
    draw.rectangle([TX0, 100, TX1, 148], fill=BLACK)
    # Parking "P" sign.
    draw.rounded_rectangle([60, 52, 128, 120], radius=10, fill=BLUE)
    f_p = font("DejaVuSans-Bold.ttf", 52)
    draw.text((94, 86), "P", font=f_p, fill=WHITE, anchor="mm")
    # Header text.
    f_city = font("DejaVuSans-Bold.ttf", 40)
    draw.text((148, 54), "CITY OF LOS SANTOS", font=f_city, fill=WHITE)
    f_enf = font("DejaVuSans-Bold.ttf", 24)
    # Letterspaced "PARKING ENFORCEMENT".
    lx = 148
    for ch in "PARKING ENFORCEMENT":
        draw.text((lx, 104), ch, font=f_enf, fill=YELLOW)
        lx += draw.textlength(ch, font=f_enf) + 3
    # Ticket number, right side.
    f_tn = font("DejaVuSans-Bold.ttf", 20)
    f_tnum = font("DejaVuSans-Bold.ttf", 28)
    draw.text((960, 56), "TICKET No.", font=f_tn, fill=WHITE, anchor="ra")
    draw.text((960, 84), "000013", font=f_tnum, fill=WHITE, anchor="ra")

    # Title.
    f_title = font("DejaVuSans-Bold.ttf", 52)
    draw.text((70, 168), "PARKING VIOLATION", font=f_title, fill=BLACK)
    f_sub = font("DejaVuSans-Bold.ttf", 34)
    draw.text((70, 238), "OVERTIME PARKING", font=f_sub, fill=BLACK)

    # Divider.
    draw.line([(70, 296), (954, 296)], fill=BLACK, width=3)

    # Fields.
    f_lab = font("DejaVuSans-Bold.ttf", 30)
    f_val = font("DejaVuSans.ttf", 30)
    fields = [
        ("VEHICLE:", "GRAND THEFT AUTO V (2013)"),
        ("PLATE:", "GTA-V-2013"),
        ("METER EXPIRED:", "SEP 17, 2013 - LOS SANTOS"),
        ("TOWED TO:", "VICE CITY, LEONIDA - NOV 19, 2026"),
    ]
    fy = 316
    for lab, val in fields:
        draw.text((70, fy), lab, font=f_lab, fill=BLACK)
        draw.text((385, fy), val, font=f_val, fill=BLACK)
        fy += 38

    # Fine line.
    f_fine = font("DejaVuSans-Bold.ttf", 32)
    draw.text((70, 478), "FINE: $1.00 / DAY x 4,811 DAYS", font=f_fine, fill=BLACK)
    f_fine_amt = font("DejaVuSans-Bold.ttf", 46)
    draw.text((954, 470), "$4,811.00", font=f_fine_amt, fill=RED, anchor="ra")

    # Divider.
    draw.line([(70, 542), (954, 542)], fill=BLACK, width=3)

    # Line items with dotted leaders.
    f_item = font("DejaVuSansMono.ttf", 27)
    f_price = font("DejaVuSansMono-Bold.ttf", 27)
    items = [
        "Renewal denied x2 - Delay No. 1 + No. 2",
        "Trailer 2 - watched 87 times",
        "Download - 214 GB",
        "Sick days - 5, doctor approved",
        "Jason & Lucia - finally met",
    ]
    iy = 560
    for it in items:
        draw.text((70, iy), it, font=f_item, fill=BLACK)
        draw.text((954, iy), "$0.00", font=f_price, fill=BLACK, anchor="ra")
        # Dotted leader between item end and price start.
        x_start = 70 + draw.textlength(it, font=f_item) + 14
        x_end = 954 - draw.textlength("$0.00", font=f_price) - 14
        yy = iy + 20
        xx = x_start
        while xx < x_end:
            draw.ellipse([xx, yy - 2, xx + 4, yy + 2], fill=GREY)
            xx += 12
        iy += 38

    # Thick divider.
    draw.line([(70, 762), (954, 762)], fill=BLACK, width=4)

    # Total.
    f_tot = font("DejaVuSans-Bold.ttf", 40)
    draw.text((70, 778), "TOTAL FINE DUE", font=f_tot, fill=BLACK)
    f_tot_amt = font("DejaVuSans-Bold.ttf", 52)
    draw.text((954, 772), "$4,811.00", font=f_tot_amt, fill=BLACK, anchor="ra")

    # Punchline.
    f_punch = font("DejaVuSans-Bold.ttf", 36)
    draw.text((512, 838), "THE FINE BUYS 60 COPIES OF THE GAME",
              font=f_punch, fill=RED, anchor="ma")

    # Magenta band (bottom of ticket, rounded bottom corners).
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rounded_rectangle([TX0, 888, TX1, TY1], radius=18, fill=MAGENTA + (255,))
    bd.rectangle([TX0, 888, TX1, 940], fill=MAGENTA + (255,))
    img = Image.alpha_composite(img.convert("RGBA"), band).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Ghost on the band (left), fully inside the band.
    draw_ghost(draw, 72, 892, 86)
    # Band text.
    f_paid = font("DejaVuSans-Bold.ttf", 28)
    draw.text((200, 906), "PAID BY MY AI AGENT ON MAKE.FUN", font=f_paid, fill=WHITE)
    f_cred = font("DejaVuSans.ttf", 22)
    draw.text((200, 944), "$250 bounty credit - real money", font=f_cred, fill=WHITE)
    # make.fun wordmark pill (right).
    f_wm = font("DejaVuSans-Bold.ttf", 26)
    wm_text = "make.fun"
    wm_w = draw.textlength(wm_text, font=f_wm) + 36
    px0, py0 = 954 - int(wm_w), 912
    draw.rounded_rectangle([px0, py0, 954, py0 + 48], radius=24, fill=WHITE)
    draw.text((px0 + 18, py0 + 24), "make", font=f_wm, fill=BLACK, anchor="lm")
    mx = px0 + 18 + draw.textlength("make", font=f_wm)
    draw.text((mx, py0 + 24), ".fun", font=f_wm, fill=MAGENTA, anchor="lm")

    # Red stamp, rotated, top-right (on its own layer so rotation is clean).
    img = draw_stamp(img.convert("RGBA"), 840, 225,
                     ["4,811 DAYS", "OVERDUE"], angle=-12).convert("RGB")
    img.save(out_path, "PNG")
    print(f"wrote {out_path} ({os.path.getsize(out_path)} bytes)")


if __name__ == "__main__":
    main()
