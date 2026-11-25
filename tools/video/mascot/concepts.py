"""Mascot concept sketches (original characters) — drawn with PIL so they can be animated frame by frame."""
import math, sys
from PIL import Image, ImageDraw, ImageFont
FD = '/usr/share/fonts/opentype/inter/'
F = lambda w, s: ImageFont.truetype(FD + {'k': 'InterDisplay-Black.otf', 'b': 'InterDisplay-Bold.otf', 's': 'InterDisplay-SemiBold.otf'}[w], s)
GREEN = (15, 107, 79); GREEN_D = (10, 78, 58); GOLD = (240, 176, 48); CREAM = (250, 246, 238); INK = (24, 28, 34)
WHITE = (255, 255, 255); PINKC = (244, 150, 140)

def eyes(d, cx, cy, gap, r, blink=0.0, look=(0, 0)):
    for sx in (-1, 1):
        x = cx + sx * gap
        h = max(2, r * (1 - blink))
        d.ellipse((x - r, cy - h, x + r, cy + h), fill=WHITE)
        if blink < 0.7: d.ellipse((x - r * .5 + look[0], cy - r * .5 + look[1], x + r * .5 + look[0], cy + r * .5 + look[1]), fill=INK)

def smile(d, cx, cy, w, open_=0.0):
    d.arc((cx - w, cy - w * .6, cx + w, cy + w * .6), 20, 160, fill=INK, width=6)
    if open_ > 0: d.chord((cx - w * .6, cy, cx + w * .6, cy + w * .5 * open_ + 4), 0, 180, fill=INK)

# A: "Çanta" — the channel's briefcase logo comes alive (keypad tummy, gold key, little arms and legs)
def briefcase(d, cx, cy, s=1.0, t=0.0, wave=0.0, blink=0.0):
    b = math.sin(t * 6) * 6 * s  # idle bounce
    cy = cy + b
    w, h = 300 * s, 230 * s
    d.rounded_rectangle((cx - 70 * s, cy - h / 2 - 60 * s, cx + 70 * s, cy - h / 2 + 10 * s), 28 * s, outline=GREEN_D, width=int(18 * s))  # handle
    d.line((cx - 60 * s, cy + h / 2, cx - 70 * s, cy + h / 2 + 70 * s), fill=GREEN_D, width=int(16 * s)); d.line((cx + 60 * s, cy + h / 2, cx + 70 * s, cy + h / 2 + 70 * s), fill=GREEN_D, width=int(16 * s))
    d.ellipse((cx - 100 * s, cy + h / 2 + 58 * s, cx - 40 * s, cy + h / 2 + 84 * s), fill=INK); d.ellipse((cx + 40 * s, cy + h / 2 + 58 * s, cx + 100 * s, cy + h / 2 + 84 * s), fill=INK)
    ang = -40 - 50 * wave
    ax, ay = cx + w / 2, cy - 10 * s
    ex, ey = ax + 110 * s * math.cos(math.radians(ang)), ay + 110 * s * math.sin(math.radians(ang))
    d.line((cx - w / 2, cy, cx - w / 2 - 70 * s, cy + 70 * s), fill=GREEN_D, width=int(16 * s)); d.ellipse((cx - w / 2 - 92 * s, cy + 52 * s, cx - w / 2 - 52 * s, cy + 92 * s), fill=CREAM)
    d.line((ax, ay, ex, ey), fill=GREEN_D, width=int(16 * s)); d.ellipse((ex - 20 * s, ey - 20 * s, ex + 20 * s, ey + 20 * s), fill=CREAM)
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 40 * s, fill=GREEN)
    eyes(d, cx, cy - 40 * s, 52 * s, 26 * s, blink)
    smile(d, cx, cy + 5 * s, 40 * s)
    for r in range(2):
        for c in range(4):
            x0 = cx - 104 * s + c * 54 * s; y0 = cy + 40 * s + r * 34 * s
            d.rounded_rectangle((x0, y0, x0 + 44 * s, y0 + 26 * s), 7 * s, fill=GOLD if (r, c) == (1, 3) else CREAM)

# B: "Hesap Dede / Nine" style is a person — kept generic here: a round retiree-friendly owl with reading glasses
def owl(d, cx, cy, s=1.0, t=0.0, wave=0.0, blink=0.0):
    b = math.sin(t * 5) * 5 * s; cy += b
    d.ellipse((cx - 150 * s, cy - 170 * s, cx + 150 * s, cy + 170 * s), fill=(120, 92, 70))
    d.ellipse((cx - 105 * s, cy - 40 * s, cx + 105 * s, cy + 150 * s), fill=(214, 190, 160))
    d.polygon([(cx - 130 * s, cy - 150 * s), (cx - 95 * s, cy - 215 * s), (cx - 70 * s, cy - 150 * s)], fill=(120, 92, 70))
    d.polygon([(cx + 130 * s, cy - 150 * s), (cx + 95 * s, cy - 215 * s), (cx + 70 * s, cy - 150 * s)], fill=(120, 92, 70))
    for sx in (-1, 1):
        x = cx + sx * 58 * s
        d.ellipse((x - 48 * s, cy - 118 * s, x + 48 * s, cy - 22 * s), fill=WHITE, outline=GOLD, width=int(8 * s))
        hh = 22 * s * (1 - blink)
        d.ellipse((x - 20 * s, cy - 70 * s - hh, x + 20 * s, cy - 70 * s + hh), fill=INK)
    d.line((cx - 10 * s, cy - 70 * s, cx + 10 * s, cy - 70 * s), fill=GOLD, width=int(8 * s))
    d.polygon([(cx - 16 * s, cy - 18 * s), (cx + 16 * s, cy - 18 * s), (cx, cy + 12 * s)], fill=GOLD)
    a = math.radians(-20 - 60 * wave)
    d.ellipse((cx + 120 * s, cy - 20 * s, cx + 120 * s + 60 * s, cy + 100 * s), fill=(98, 74, 56))
    d.rounded_rectangle((cx - 60 * s, cy + 50 * s, cx + 60 * s, cy + 120 * s), 10 * s, fill=GREEN)  # holds a little ledger
    d.text((cx, cy + 85 * s), '₺', font=F('k', int(46 * s)), fill=CREAM, anchor='mm')

# C: "Tuş" — the gold key from the logo as a tiny energetic sidekick
def key(d, cx, cy, s=1.0, t=0.0, wave=0.0, blink=0.0):
    b = abs(math.sin(t * 7)) * 22 * s; cy -= b
    sq = 1 + 0.06 * math.sin(t * 14)
    w, h = 170 * s * sq, 170 * s / sq
    d.ellipse((cx - 80 * s, cy + h / 2 + b + 6 * s, cx + 80 * s, cy + h / 2 + b + 26 * s), fill=(0, 0, 0, 60))
    d.rounded_rectangle((cx - w / 2, cy - h / 2 + 14 * s, cx + w / 2, cy + h / 2 + 14 * s), 34 * s, fill=(196, 132, 20))
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 34 * s, fill=GOLD)
    eyes(d, cx, cy - 18 * s, 34 * s, 17 * s, blink, (4 * s, 0))
    smile(d, cx, cy + 22 * s, 28 * s, open_=0.6)
    d.ellipse((cx - 68 * s, cy + 6 * s, cx - 48 * s, cy + 20 * s), fill=PINKC); d.ellipse((cx + 48 * s, cy + 6 * s, cx + 68 * s, cy + 20 * s), fill=PINKC)

CHARS = [('A', 'Çanta', 'The logo comes alive', briefcase), ('B', 'Baykuş', 'Wise owl with reading glasses', owl), ('C', 'Tuş', 'The gold key as a tiny sidekick', key)]

def sheet(path):
    W, H = 1920, 1080
    im = Image.new('RGB', (W, H), (243, 240, 233)); d = ImageDraw.Draw(im, 'RGBA')
    d.text((80, 60), 'Hesap Çantası: maskot taslakları', font=F('k', 64), fill=INK)
    for i, (k, name, sub, fn) in enumerate(CHARS):
        cx = 330 + i * 630
        d.rounded_rectangle((cx - 290, 190, cx + 290, 1010), 40, fill=WHITE)
        fn(d, cx, 560, 1.0 if fn is not key else 1.3, t=0.3)
        d.text((cx, 860), f'{k}  {name}', font=F('k', 56), fill=INK, anchor='mm')
        d.text((cx, 930), sub, font=F('s', 32), fill=(110, 116, 126), anchor='mm')
    im.save(path, quality=90)

def clip(path, dur=6.0, fps=30):
    """Short motion test, 9:16: all three idle, blink and wave, so the user can judge movement."""
    import subprocess
    W, H = 1080, 1920
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for k in range(int(dur * fps)):
        t = k / fps
        im = Image.new('RGB', (W, H), (243, 240, 233)); d = ImageDraw.Draw(im, 'RGBA')
        blink = 1.0 if (t % 2.2) < 0.12 else 0.0
        wave = (math.sin(t * 8) + 1) / 2 if 1.0 < t < 3.0 else 0.0
        for i, (kk, name, sub, fn) in enumerate(CHARS):
            cy = 340 + i * 600
            fn(d, 540, cy, 0.8 if fn is not key else 1.0, t=t + i, wave=wave, blink=blink)
            d.text((540, cy + 255), f'{kk}  {name}', font=F('k', 44), fill=INK, anchor='mm')
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    sheet('mascot-concepts.jpg'); clip('mascot-motion-test.mp4')
