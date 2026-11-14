"""'Aralık'ta maaşım neden düşüyor?' — maaş/bordro explainer.
Visual variant: dark green ground, blue (maaş) accent, payslip document + 12-month bar strip, slide-in transitions.
Usage: python3 render.py long|short [stills]"""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

MODE = sys.argv[1] if len(sys.argv) > 1 else 'long'
W, H = (1920, 1080) if MODE == 'long' else (1080, 1920)
FPS = 30
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), MODE)
os.makedirs(OUT, exist_ok=True)
FD = '/usr/share/fonts/opentype/inter/'
_fc = {}
def F(w, s):
    k = (w, s)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FD + {'b': 'InterDisplay-Bold.otf', 'x': 'InterDisplay-ExtraBold.otf', 'k': 'InterDisplay-Black.otf', 's': 'InterDisplay-SemiBold.otf', 'r': 'InterDisplay-Regular.otf'}[w], s)
    return _fc[k]

BG = (10, 46, 36); BG2 = (16, 62, 48); INK = (238, 244, 240); MUTED = (160, 190, 176); BRAND = (15, 107, 79)
BLUE = (96, 170, 255); BLUE_D = (40, 104, 196); PAPER = (250, 249, 245); PINK = INK
DARK = (28, 31, 29); GREY = (110, 116, 112); LINE = (226, 224, 216); RED = (232, 110, 92); GOLD = (244, 196, 48)

# figures from the site engine (brütNet(75000), 2026)
NETS = [58080.27, 58080.27, 58017.77, 54892.77, 54892.77, 54892.77, 51981.70, 51834.05, 51834.05, 51834.05, 51834.05, 51834.05]
CUM = [63750, 127500, 191250, 255000, 318750, 382500, 446250, 510000, 573750, 637500, 701250, 765000]
AY = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara']

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def prog(t, s, d=0.5): return ease((t - s) / d)
def tr(n, d=2): return f'{n:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

class Fr:
    def __init__(s): s.im = Image.new('RGB', (W, H), BG); s.d = ImageDraw.Draw(s.im)
    def layer(s, a, fn, dx=0, dy=0):
        if a <= 0: return
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay), dx, dy)
        if a < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * a)))
        s.im.paste(lay, (0, 0), lay)

def slide(fr, t, s, fn, dur=0.5, dist=80):  # slide in from the right (this video's transition)
    p = prog(t, s, dur); fr.layer(p, fn, dx=int((1 - p) * dist))

def T(d, xy, s, f, fill=INK, a='la'): d.text(xy, s, font=f, fill=fill, anchor=a)

def grid(fr):  # faint ledger grid as the background texture
    d = fr.d
    for x in range(0, W, 60): d.line((x, 0, x, H), fill=(14, 54, 42), width=1)
    for y in range(0, H, 60): d.line((0, y, W, y), fill=(14, 54, 42), width=1)

def brand(fr, x, y, s=1.0):
    d = fr.d; z = int(52 * s)
    d.rounded_rectangle((x, y, x + z, y + z), int(13 * s), fill=INK); T(d, (x + z // 2, y + z // 2), '₺', F('b', int(32 * s)), BRAND, 'mm')
    T(d, (x + z + 16, y + z // 2), 'Hesap Çantası', F('b', int(30 * s)), INK, 'lm')

L = MODE == 'long'
M = 120 if L else 80          # side margin
R = W - M if L else 920       # right bound (Shorts UI safe area)
TOP = 110 if L else 250

# ---------------- scenes ----------------
def s_hook(fr, t, dur):
    grid(fr)
    if L:
        slide(fr, t, .1, lambda d, dx, dy: T(d, (M + dx, 370), 'Brütün aynı,', F('k', 96), INK))
        slide(fr, t, .35, lambda d, dx, dy: T(d, (M + dx, 485), 'netin neden düşüyor?', F('k', 96), BLUE))
        slide(fr, t, 1.0, lambda d, dx, dy: (d.rounded_rectangle((M + dx, 680, M + 700 + dx, 770), 45, fill=BG2), T(d, (M + 40 + dx, 725), 'Aralık maaşının sırrı · 2026', F('b', 44), MUTED, 'lm')))
        # mini payslip icon on the right
        def icon(d, dx, dy):
            x0, y0 = 1320 + dx, 250
            d.rounded_rectangle((x0, y0, x0 + 480, y0 + 600), 28, fill=PAPER)
            T(d, (x0 + 40, y0 + 50), 'BORDRO', F('k', 44), DARK)
            for i in range(6):
                y = y0 + 150 + i * 70
                d.rounded_rectangle((x0 + 40, y, x0 + 260, y + 22), 11, fill=LINE)
                d.rounded_rectangle((x0 + 320, y, x0 + 440, y + 22), 11, fill=(200, 222, 248) if i == 5 else LINE)
        slide(fr, t, .6, icon, dist=140)
    else:
        slide(fr, t, .1, lambda d, dx, dy: T(d, (M + dx, 600), 'Brütün aynı,', F('k', 110), INK))
        slide(fr, t, .35, lambda d, dx, dy: T(d, (M + dx, 730), 'netin neden', F('k', 110), BLUE))
        slide(fr, t, .55, lambda d, dx, dy: T(d, (M + dx, 860), 'düşüyor?', F('k', 110), BLUE))
        slide(fr, t, 1.1, lambda d, dx, dy: (d.rounded_rectangle((M + dx, 1050, M + 640 + dx, 1140), 45, fill=BG2), T(d, (M + 40 + dx, 1095), 'Aralık maaşının sırrı', F('b', 46), MUTED, 'lm')))
    brand(fr, M, TOP - 40 if L else 250)

def s_slip(fr, t, dur):
    grid(fr); brand(fr, M, TOP - 40 if L else 250)
    y0 = 230 if L else 400
    T(fr.d, (M, y0 - 10), 'Ocak bordrosu · 75.000 ₺ brüt', F('k', 64 if L else 56), INK, 'ls')
    x0, x1 = (M, 1100) if L else (M, R)
    top = y0 + 40
    rows = [('Brüt maaş', '75.000,00 ₺', DARK), ('SGK + işsizlik (%15)', '− 11.250,00 ₺', GREY), ('Gelir vergisi (%15 dilim)', '− 5.351,18 ₺', BLUE_D), ('Damga vergisi', '− 318,55 ₺', GREY)]
    def paper(d, dx, dy):
        d.rounded_rectangle((x0 + dx, top, x1 + dx, top + (560 if L else 700)), 30, fill=PAPER)
    slide(fr, t, .2, paper, dist=60)
    rh = 95 if L else 110
    for i, (lab, v, col) in enumerate(rows):
        y = top + 70 + i * rh
        slide(fr, t, .6 + i * .45, lambda d, dx, dy, lab=lab, v=v, col=col, y=y: (T(d, (x0 + 50 + dx, y), lab, F('s', 44 if L else 42), col, 'lm'), T(d, (x1 - 50 + dx, y), v, F('x', 48 if L else 46), col, 'rm')))
    def net(d, dx, dy):
        y = top + 70 + 4 * rh + 20
        d.line((x0 + 50 + dx, y - 40, x1 - 50 + dx, y - 40), fill=LINE, width=4)
        T(d, (x0 + 50 + dx, y + 20), 'Net maaş', F('k', 52), DARK, 'lm')
        T(d, (x1 - 50 + dx, y + 20), tr(58080.27 * prog(t, 2.8, 1.0)) + ' ₺', F('k', 62), BRAND, 'rm')
    slide(fr, t, 2.6, net)
    if L:
        def side(d, dx, dy):
            d.rounded_rectangle((1180 + dx, top, W - M + dx, top + 560), 30, fill=BG2)
            T(d, (1230 + dx, top + 70), 'Dikkat', F('k', 48), BLUE)
            for j, ln in enumerate(['Gelir vergisi her ay', 'yıl başından beri biriken', 'matrah üzerinden', 'hesaplanır.']):
                T(d, (1230 + dx, top + 160 + j * 64), ln, F('s', 42), INK)
        slide(fr, t, 4.0, side)
    else:
        slide(fr, t, 4.0, lambda d, dx, dy: T(d, (M + dx, top + 760), 'Vergi, yıl boyu biriken matraha göre kesilir.', F('s', 38), MUTED))

def s_meter(fr, t, dur):
    grid(fr); brand(fr, M, TOP - 40 if L else 250)
    y0 = 230 if L else 400
    T(fr.d, (M, y0 - 10), 'Matrah birikir, dilim değişir', F('k', 64 if L else 56), INK, 'ls')
    x0, x1 = M, (W - M if L else R)
    by = y0 + (260 if L else 330); bh = 90
    maxv = 800000
    def X(v): return x0 + (x1 - x0) * v / maxv
    fr.d.rounded_rectangle((x0, by, x1, by + bh), 45, fill=BG2)
    p = prog(t, .8, 4.2)
    cur = CUM[-1] * p
    fr.d.rounded_rectangle((x0, by, max(x0 + 90, X(cur)), by + bh), 45, fill=BLUE)
    for k, (lim, lab, s) in enumerate([(190000, '%15 → %20', 1.4), (400000, '%20 → %27', 2.6)]):
        py = by + bh + 60 + (0 if L else k * 110)
        xl = X(lim)
        fr.d.line((xl, by - 40, xl, by + bh + 40), fill=GOLD, width=5)
        T(fr.d, (xl, by - 60), tr(lim, 0) + ' ₺', F('b', 34 if L else 30), GOLD, 'ms')
        if cur >= lim:
            slide(fr, t, s, lambda d, dx, dy, xl=xl, lab=lab, py=py: (d.rounded_rectangle((xl - 150 + dx, py, xl + 150 + dx, py + 80), 40, fill=PAPER), T(d, (xl + dx, py + 40), lab, F('k', 40), DARK, 'mm')), dur=.35, dist=40)
    mi = min(11, int(p * 12))
    T(fr.d, (x0, by + bh + (260 if L else 360)), f'{AY[mi]} sonu birikmiş matrah: {tr(cur, 0)} ₺', F('s', 44 if L else 40), INK)
    if L:
        slide(fr, t, 4.4, lambda d, dx, dy: T(d, (x0 + dx, by + bh + 340), 'Mart’ta %20’ye, Temmuz’da %27’ye geçersiniz.', F('s', 44), MUTED))
    else:
        slide(fr, t, 4.4, lambda d, dx, dy: (T(d, (x0 + dx, by + bh + 440), 'Mart’ta %20’ye,', F('s', 44), MUTED), T(d, (x0 + dx, by + bh + 500), 'Temmuz’da %27’ye geçilir.', F('s', 44), MUTED)))

def s_bars(fr, t, dur):
    grid(fr); brand(fr, M, TOP - 40 if L else 250)
    y0 = 230 if L else 400
    T(fr.d, (M, y0 - 10), '12 ayda net maaş', F('k', 64 if L else 56), INK, 'ls')
    x0, x1 = M, (W - M if L else R)
    base = (H - 170) if L else 1350
    top = y0 + (120 if L else 260)
    lo, hi = 48000, 59000
    n = 12; gap = 14 if L else 10
    bw = (x1 - x0 - gap * (n - 1)) / n
    for i, v in enumerate(NETS):
        p = prog(t, .4 + i * .12, .5)
        h = (base - top) * (v - lo) / (hi - lo) * p
        xa = x0 + i * (bw + gap)
        col = BLUE if NETS[i] > 55000 else (BLUE_D if NETS[i] > 52500 else (96, 120, 170))
        if i in (0, 11): col = GOLD if i == 11 else BLUE
        fr.d.rounded_rectangle((xa, base - h, xa + bw, base), 12, fill=col)
        T(fr.d, (xa + bw / 2, base + 36), AY[i], F('s', 30 if L else 24), MUTED, 'mm')
        if i in (0, 11) and p > .9:
            T(fr.d, (xa + bw / 2, base - h - 24), tr(v, 0), F('b', 34 if L else 28), INK, 'ms')
    def diff(d, dx, dy):
        bx = (x1 - 640) if L else x0
        by_ = top - 10 if L else top - 200
        d.rounded_rectangle((bx + dx, by_, bx + 640 + dx, by_ + 120), 30, fill=PAPER)
        T(d, (bx + 40 + dx, by_ + 60), 'Ocak → Aralık', F('s', 40), DARK, 'lm')
        T(d, (bx + 600 + dx, by_ + 60), '− 6.246 ₺', F('k', 50), (200, 60, 45), 'rm')
    slide(fr, t, 2.4, diff)

def s_why(fr, t, dur):
    grid(fr); brand(fr, M, TOP - 40 if L else 250)
    y0 = 230 if L else 400
    T(fr.d, (M, y0 - 10), 'Peki Ocak’ta ne olur?', F('k', 64 if L else 56), INK, 'ls')
    items = [('1', 'Brüt maaşınız aynı kalsa da net azalır: kesinti artar, maaş değil.'),
             ('2', 'Ocak’ta birikmiş matrah sıfırlanır; tekrar %15 dilimden başlarsınız.'),
             ('3', 'Asgari ücret kadar kısım her ay vergiden istisnadır.')]
    for i, (n_, s) in enumerate(items):
        y = y0 + 120 + i * (150 if L else 230)
        def f(d, dx, dy, n_=n_, s=s, y=y):
            d.ellipse((M + dx, y, M + 90 + dx, y + 90), fill=BLUE)
            T(d, (M + 45 + dx, y + 45), n_, F('k', 46), BG, 'mm')
            if L:
                T(d, (M + 130 + dx, y + 45), s, F('s', 44), INK, 'lm')
            else:
                words = s.split(' '); line = ''; lines = []
                for w in words:
                    if F('s', 40).getlength(line + ' ' + w) > (R - M - 130): lines.append(line); line = w
                    else: line = (line + ' ' + w).strip()
                lines.append(line)
                for j, ln in enumerate(lines): T(d, (M + 130 + dx, y + 20 + j * 52), ln, F('s', 40), INK)
        slide(fr, t, .4 + i * .8, f)

def s_cta(fr, t, dur):
    fr.d.rectangle((0, 0, W, H), fill=BRAND)
    cx = W // 2 if L else (M + R) // 2
    slide(fr, t, .1, lambda d, dx, dy: T(d, (cx + dx, (340 if L else 560)), 'Kendi 12 aylık bordronu gör', F('k', 80 if L else 66), INK, 'mm'))
    def url(d, dx, dy):
        w2 = 640 if L else (R - M) // 2
        y = 520 if L else 760
        d.rounded_rectangle((cx - w2 + dx, y, cx + w2 + dx, y + 110), 55, fill=PAPER)
        T(d, (cx + dx, y + 55), 'hesapcantasi.com/maas-hesaplama' if L else 'hesapcantasi.com', F('k', 50 if L else 60), BRAND, 'mm')
    slide(fr, t, .7, url)
    slide(fr, t, 1.5, lambda d, dx, dy: T(d, (cx + dx, (720 if L else 940)), 'Brütten nete, netten brüte · ücretsiz' if L else 'Maaş hesaplama · ücretsiz', F('s', 40), (210, 236, 224), 'mm'))
    if L: slide(fr, t, 2.4, lambda d, dx, dy: T(d, (cx + dx, 830), 'Link açıklamada', F('s', 34), (210, 236, 224), 'mm'))

LONG = [(s_hook, 4.5), (s_slip, 8.5), (s_meter, 8.0), (s_bars, 8.0), (s_why, 8.0), (s_cta, 6.0)]
SHORT = [(s_hook, 3.5), (s_slip, 7.0), (s_meter, 6.5), (s_bars, 6.5), (s_cta, 5.5)]
SCENES = LONG if L else SHORT

def draw(i, t):
    fn, dur = SCENES[i]; fr = Fr(); fn(fr, t, dur)
    if fn is not s_cta:
        yb = H - 10 if L else 230
        fr.d.rectangle((0, yb, int(W * min(1, t / dur)), yb + 8), fill=BLUE)
    a = min(1, t / .2, (dur - t) / .2)
    if a < 1: fr.im = Image.blend(Image.new('RGB', (W, H), BRAND if fn is s_cta else BG), fr.im, max(0, a))
    return fr.im

def render(i):
    dur = SCENES[i][1]; tmp = f'{OUT}/s{i:02d}.tmp.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for k in range(int(round(dur * FPS))): p.stdin.write(draw(i, k / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0: sys.exit(f'scene {i} failed')
    os.replace(tmp, f'{OUT}/s{i:02d}.mp4')

if __name__ == '__main__':
    if sys.argv[2:3] == ['stills']:
        for i, (fn, dur) in enumerate(SCENES): draw(i, dur - .4).save(f'{OUT}/still{i}.jpg', quality=85)
    else:
        for i in range(len(SCENES)): render(i)
        with open(f'{OUT}/list.txt', 'w') as f:
            for i in range(len(SCENES)): f.write(f"file 's{i:02d}.mp4'\n")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/list.txt', '-c', 'copy', f'{OUT}/silent.mp4'], check=True)
        print('done', sum(d for _, d in SCENES))
