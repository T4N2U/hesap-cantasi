"""Variations on mascot C 'Tuş' (the gold key) and close relatives in the same style. Original characters."""
import math, subprocess
from PIL import Image, ImageDraw, ImageFont
FD = '/usr/share/fonts/opentype/inter/'
F = lambda w, s: ImageFont.truetype(FD + {'k': 'InterDisplay-Black.otf', 'b': 'InterDisplay-Bold.otf', 's': 'InterDisplay-SemiBold.otf'}[w], int(s))
GOLD = (240, 176, 48); GOLD_D = (196, 132, 20); GREEN = (15, 107, 79); GREEN_D = (9, 70, 52); CREAM = (250, 246, 238)
INK = (24, 28, 34); WHITE = (255, 255, 255); BLUSH = (244, 150, 140); BG = (243, 240, 233); GREY = (110, 116, 126)

def face(d, cx, cy, s, blink=0.0, look=0.0, mood='smile', ink=INK):
    for sx in (-1, 1):
        x = cx + sx * 34 * s; r = 17 * s; h = max(2, r * (1 - blink))
        d.ellipse((x - r, cy - h, x + r, cy + h), fill=WHITE)
        if blink < .7: d.ellipse((x - 9 * s + look, cy - 9 * s, x + 9 * s + look, cy + 9 * s), fill=ink)
    if mood == 'smile': d.arc((cx - 28 * s, cy + 14 * s, cx + 28 * s, cy + 46 * s), 20, 160, fill=ink, width=max(3, int(6 * s)))
    elif mood == 'open': d.chord((cx - 20 * s, cy + 18 * s, cx + 20 * s, cy + 50 * s), 0, 180, fill=ink)
    elif mood == 'wow': d.ellipse((cx - 10 * s, cy + 22 * s, cx + 10 * s, cy + 46 * s), fill=ink)
    d.ellipse((cx - 70 * s, cy + 22 * s, cx - 50 * s, cy + 36 * s), fill=BLUSH); d.ellipse((cx + 50 * s, cy + 22 * s, cx + 70 * s, cy + 36 * s), fill=BLUSH)

def keycap(d, cx, cy, s, top, side, t=0.0, label=None, label_col=None):
    """Squash-and-stretch keycap: a lighter top face over a darker base (keyboard-key depth)."""
    sq = 1 + .06 * math.sin(t * 14); w, h = 170 * s * sq, 170 * s / sq
    d.ellipse((cx - 80 * s, cy + 98 * s, cx + 80 * s, cy + 118 * s), fill=(0, 0, 0, 45))
    d.rounded_rectangle((cx - w / 2, cy - h / 2 + 16 * s, cx + w / 2, cy + h / 2 + 16 * s), 36 * s, fill=side)
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 36 * s, fill=top)
    if label: d.text((cx + w / 2 - 26 * s, cy - h / 2 + 24 * s), label, font=F('k', 30 * s), fill=label_col or INK, anchor='mm')
    return w, h

def limbs(d, cx, cy, s, col, wave=0.0):
    d.line((cx - 40 * s, cy + 100 * s, cx - 46 * s, cy + 138 * s), fill=col, width=int(12 * s)); d.line((cx + 40 * s, cy + 100 * s, cx + 46 * s, cy + 138 * s), fill=col, width=int(12 * s))
    d.ellipse((cx - 66 * s, cy + 130 * s, cx - 30 * s, cy + 146 * s), fill=INK); d.ellipse((cx + 30 * s, cy + 130 * s, cx + 66 * s, cy + 146 * s), fill=INK)
    d.line((cx - 86 * s, cy + 10 * s, cx - 128 * s, cy + 50 * s), fill=col, width=int(12 * s)); d.ellipse((cx - 142 * s, cy + 40 * s, cx - 114 * s, cy + 68 * s), fill=CREAM)
    a = math.radians(-35 - 55 * wave); ex, ey = cx + 86 * s + 55 * s * math.cos(a), cy + 10 * s + 55 * s * math.sin(a)
    d.line((cx + 86 * s, cy + 10 * s, ex, ey), fill=col, width=int(12 * s)); d.ellipse((ex - 14 * s, ey - 14 * s, ex + 14 * s, ey + 14 * s), fill=CREAM)

def hop(t, s, amp=22): return abs(math.sin(t * 7)) * amp * s

# 1 Tuş classic
def v1(d, cx, cy, s, t=0, blink=0, wave=0):
    cy -= hop(t, s); keycap(d, cx, cy, s, GOLD, GOLD_D, t); face(d, cx, cy - 18 * s, s, blink, 4 * s)
# 2 Tuş with arms & legs and a ₺ legend on the keycap
def v2(d, cx, cy, s, t=0, blink=0, wave=0):
    cy -= hop(t, s, 10); limbs(d, cx, cy, s, GOLD_D, wave); keycap(d, cx, cy, s, GOLD, GOLD_D, t, '₺'); face(d, cx, cy - 14 * s, s, blink, 0, 'open')
# 3 Duo: green key (Hesap) + gold Tuş
def v3(d, cx, cy, s, t=0, blink=0, wave=0):
    s2 = s * .78
    y1 = cy - hop(t + .3, s2, 14); keycap(d, cx - 70 * s, y1 + 20 * s, s2, (32, 138, 104), GREEN_D, t + .3, '='); face(d, cx - 70 * s, y1 + 6 * s, s2, blink, 3 * s2)
    y2 = cy - hop(t, s2); keycap(d, cx + 75 * s, y2 + 20 * s, s2, GOLD, GOLD_D, t); face(d, cx + 75 * s, y2 + 6 * s, s2, blink, -3 * s2, 'open')
# 4 Para (coin cousin): round ₺ coin, same face
def v4(d, cx, cy, s, t=0, blink=0, wave=0):
    cy -= hop(t, s, 18); sq = 1 + .05 * math.sin(t * 14); r = 88 * s
    d.ellipse((cx - 80 * s, cy + 98 * s, cx + 80 * s, cy + 118 * s), fill=(0, 0, 0, 45))
    d.ellipse((cx - r * sq, cy - r / sq + 14 * s, cx + r * sq, cy + r / sq + 14 * s), fill=GOLD_D)
    d.ellipse((cx - r * sq, cy - r / sq, cx + r * sq, cy + r / sq), fill=GOLD, outline=(255, 214, 110), width=int(8 * s))
    d.text((cx, cy - 58 * s), '₺', font=F('k', 40 * s), fill=GOLD_D, anchor='mm'); face(d, cx, cy - 6 * s, s, blink, 3 * s)
# 5 Tuş with topic props: reading glasses + tiny calendar (emekli/memur zammı episode)
def v5(d, cx, cy, s, t=0, blink=0, wave=0):
    cy -= hop(t, s, 12); keycap(d, cx, cy, s, GOLD, GOLD_D, t); face(d, cx, cy - 18 * s, s, blink, 0)
    for sx in (-1, 1): d.ellipse((cx + sx * 34 * s - 25 * s, cy - 43 * s, cx + sx * 34 * s + 25 * s, cy + 7 * s), outline=INK, width=int(5 * s))
    d.line((cx - 9 * s, cy - 18 * s, cx + 9 * s, cy - 18 * s), fill=INK, width=int(5 * s))
    x0, y0 = cx + 70 * s, cy + 20 * s
    d.rounded_rectangle((x0, y0, x0 + 70 * s, y0 + 70 * s), 10 * s, fill=WHITE, outline=INK, width=int(4 * s)); d.rectangle((x0, y0, x0 + 70 * s, y0 + 20 * s), fill=(214, 84, 64))
    d.text((x0 + 35 * s, y0 + 46 * s), 'OCA', font=F('k', 18 * s), fill=INK, anchor='mm')
# 6 Mini Tuş family in brand colours (one per topic colour)
def v6(d, cx, cy, s, t=0, blink=0, wave=0):
    cols = [((96, 165, 250), (52, 118, 200)), (GOLD, GOLD_D), ((163, 230, 53), (110, 170, 30))]
    for i, (a, b) in enumerate(cols):
        x = cx + (i - 1) * 120 * s; ss = s * .55; y = cy + 10 * s - hop(t + i * .4, ss, 26)
        keycap(d, x, y, ss, a, b, t + i * .4); face(d, x, y - 14 * ss, ss, blink, 0, ['smile', 'open', 'wow'][i])

V = [('C1', 'Tuş (klasik)', 'Your pick, unchanged', v1), ('C2', 'Tuş + kollar', 'Arms and legs, ₺ on the keycap', v2),
     ('C3', 'Tuş ve Eşittir', 'A duo: gold key + green "=" key', v3), ('C4', 'Para', 'Coin cousin, same face', v4),
     ('C5', 'Tuş, emekli bölümü', 'Episode props: glasses + calendar', v5), ('C6', 'Tuş ailesi', 'Mini keys in topic colours', v6)]

def sheet(path):
    W, H = 1920, 1200
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im, 'RGBA')
    d.text((80, 50), 'Tuş: varyasyonlar', font=F('k', 64), fill=INK)
    for i, (k, name, sub, fn) in enumerate(V):
        cx = 330 + (i % 3) * 630; cy0 = 170 + (i // 3) * 510
        d.rounded_rectangle((cx - 290, cy0, cx + 290, cy0 + 480), 36, fill=WHITE)
        fn(d, cx, cy0 + 200, 1.0, t=0.11)
        d.text((cx, cy0 + 400), f'{k}  {name}', font=F('k', 42), fill=INK, anchor='mm')
        d.text((cx, cy0 + 448), sub, font=F('s', 28), fill=GREY, anchor='mm')
    im.save(path, quality=90)

def clip(path, dur=6.0, fps=30):
    W, H = 1080, 1920
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for k in range(int(dur * fps)):
        t = k / fps; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im, 'RGBA')
        blink = 1.0 if (t % 2.2) < .12 else 0.0; wave = (math.sin(t * 8) + 1) / 2 if 1 < t < 3 else 0.0
        for i, (kk, name, sub, fn) in enumerate(V):
            cx = 280 + (i % 2) * 520; cy = 330 + (i // 2) * 600
            fn(d, cx, cy, .9, t=t + i * .2, blink=blink, wave=wave)
            d.text((cx, cy + 210), kk, font=F('k', 40), fill=INK, anchor='mm')
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    sheet('tus-variations.jpg'); clip('tus-variations-motion.mp4')
