"""'Yılsonu ikramiyesi net ne kadar kalır?' (publish 8 Dec 2026).
Visual variant: midnight-navy ground with faint confetti, champagne-gold accent, an envelope (ikramiye zarfı),
a brüt → net waterfall, rise-up transitions (elements float up from below). Music preset: musicbox-light.
Figures: E.ikramiye() in static/assets/engine.js (75.000 ₺ brüt maaş, 1 maaş ikramiye in December).
Usage: python3 render.py long|short [stills]"""
import os, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

MODE = sys.argv[1] if len(sys.argv) > 1 else 'long'
L = MODE == 'long'
W, H = (1920, 1080) if L else (1080, 1920)
FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, MODE)
os.makedirs(OUT, exist_ok=True)
FD = '/usr/share/fonts/opentype/inter/'
_fc = {}
def F(w, s):
    k = (w, s)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FD + {'b': 'InterDisplay-Bold.otf', 'k': 'InterDisplay-Black.otf', 's': 'InterDisplay-SemiBold.otf', 'r': 'InterDisplay-Regular.otf'}[w], s)
    return _fc[k]

BG = (16, 24, 48); CARD = (28, 40, 74); LINE = (48, 62, 102); INK = (240, 243, 250); MUTED = (156, 168, 200)
GOLD = (242, 193, 78); GOLD_S = (92, 76, 40); RED = (236, 112, 99); BRAND = (15, 107, 79); WHITE = (255, 255, 255)

# --- figures (engine.js, 2026) ---
BRUT, IK = 75000, 75000
SGK, GV, DAMGA, NET = 11250.00, 17212.50, 569.25, 45968.25
ORAN = NET / IK
TABLO = [('35.000 ₺', 23534.35, '%67'), ('50.000 ₺', 30645.50, '%61'), ('75.000 ₺', 45968.25, '%61'), ('100.000 ₺', 61291.00, '%61')]

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def prog(t, s, d=0.5): return ease((t - s) / d)
def tr(n, d=2): return f'{n:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def T(d, xy, s, f, fill=INK, a='la'): d.text(xy, s, font=f, fill=fill, anchor=a)

def _bg():
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im); rnd = random.Random(7)
    cols = [(46, 60, 100), (60, 56, 70), (40, 70, 90)]
    for _ in range(140 if L else 160):
        x, y, s = rnd.randrange(W), rnd.randrange(H), rnd.choice((6, 8, 10, 14))
        c = rnd.choice(cols)
        if rnd.random() < .5: d.ellipse((x, y, x + s, y + s), fill=c)
        else: d.rounded_rectangle((x, y, x + s * 2, y + s), 3, fill=c)
    return im
BGIM = _bg()

class Fr:
    def __init__(s): s.im = BGIM.copy(); s.d = ImageDraw.Draw(s.im)

def layer(fn):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay)); return lay

def rise(fr, t, s, fn, dur=0.55, dist=60):
    """Rise-up: the element floats up from below while fading in (this video's transition)."""
    p = prog(t, s, dur)
    if p <= 0: return
    lay = layer(fn)
    if p < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * p)))
    fr.im.paste(lay, (0, int((1 - p) * dist)), lay)

_LOGO = {}
def logo(size):
    """The channel logo (briefcase with keypad), from tools/video/logo.png."""
    if size not in _LOGO:
        _LOGO[size] = Image.open(os.path.join(HERE, '..', 'logo.png')).convert('RGBA').resize((size, size), Image.LANCZOS)
    return _LOGO[size]

def brand(fr, x, y):
    lg = logo(52); fr.im.paste(lg, (x, y), lg)
    T(fr.d, (x + 68, y + 26), 'Hesap Çantası', F('b', 30), INK, 'lm')

def envelope(d, cx, cy, s=1.0, open_=0.0):
    w, h = int(420 * s), int(270 * s)
    x0, y0, x1, y1 = cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2
    if open_ > 0:  # a cheque slides out of the top
        ch = int(220 * s * open_)
        d.rounded_rectangle((x0 + 30 * s, y0 - ch, x1 - 30 * s, y0 + 60 * s), int(14 * s), fill=WHITE)
        if open_ > .6:
            T(d, (cx, y0 - ch + int(60 * s)), 'İKRAMİYE', F('k', int(34 * s)), BG, 'mm')
            T(d, (cx, y0 - ch + int(115 * s)), tr(IK, 0) + ' ₺', F('k', int(44 * s)), GOLD_S, 'mm')
    d.rounded_rectangle((x0, y0, x1, y1), int(22 * s), fill=GOLD)
    d.polygon([(x0, y0 + 10 * s), (cx, cy + 20 * s), (x1, y0 + 10 * s)], fill=(222, 170, 60))
    d.line([(x0 + 8 * s, y1 - 8 * s), (cx, cy + 10 * s), (x1 - 8 * s, y1 - 8 * s)], fill=(214, 160, 52), width=int(6 * s))

M = 120 if L else 80
R = W - M if L else 920
TOP = 70 if L else 250
CX = W // 2 if L else (M + R) // 2

def header(fr, title, sub=None):
    brand(fr, M, TOP)
    ty = 200 if L else 370
    T(fr.d, (M, ty), title, F('k', 70 if L else 56), INK)
    if sub: T(fr.d, (M, ty + (92 if L else 78)), sub, F('s', 38 if L else 34), MUTED)

def pill(d, cx, cy, text, f, bg, fg, padx=40, h=90):
    w = d.textlength(text, font=f) + padx * 2
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), h // 2, fill=bg); T(d, (cx, cy), text, f, fg, 'mm')

# ---------------- scenes ----------------
def s_hook(fr, t, dur):
    brand(fr, M, TOP)
    op = prog(t, 1.4, 1.2)
    if L:
        rise(fr, t, .1, lambda d: (T(d, (M, 300), 'İkramiyenin', F('k', 110), INK), T(d, (M, 430), 'ne kadarı cebine', F('k', 96), GOLD), T(d, (M, 545), 'kalır?', F('k', 96), GOLD)))
        rise(fr, t, .4, lambda d: envelope(d, 1450, 640, 1.15, op), dist=90)
        rise(fr, t, 2.4, lambda d: pill(d, M + 330, 760, '75.000 ₺ brüt maaş · Aralık', F('b', 40), CARD, INK))
    else:
        rise(fr, t, .3, lambda d: envelope(d, CX, 760, 1.0, op), dist=90)
        rise(fr, t, .1, lambda d: (T(d, (CX, 1060), 'İkramiyenin', F('k', 96), INK, 'mm'), T(d, (CX, 1170), 'ne kadarı kalır?', F('k', 84), GOLD, 'mm')))
        rise(fr, t, 1.6, lambda d: pill(d, CX, 1300, '75.000 ₺ brüt · Aralık', F('b', 40), CARD, INK))

def s_fall(fr, t, dur):
    header(fr, 'Brütten nete', '75.000 ₺ brüt ikramiye, Aralık ayında')
    steps = [('Brüt ikramiye', IK, GOLD, 0), ('SGK + işsizlik %15', -SGK, RED, 1), ('Gelir vergisi %27', -GV, RED, 2), ('Damga vergisi', -DAMGA, RED, 3), ('Net ikramiye', NET, GOLD, 4)]
    if L:
        x0, base, top = M + 40, 950, 470
        sc = (base - top) / IK; bw, gap = 230, 90
        level = 0
        for lab, v, col, i in steps:
            x = x0 + i * (bw + gap)
            if i in (0, 4): y_a, y_b = base - abs(v) * sc, base
            else: y_a, y_b = base - level * sc, base - (level + v) * sc
            s0 = .5 + i * .75
            def bar(d, x=x, y_a=y_a, y_b=y_b, col=col, lab=lab, v=v, s0=s0, i=i):
                p = prog(t, s0, .6)
                ya = y_b - (y_b - y_a) * p
                d.rounded_rectangle((x, min(ya, y_b), x + bw, max(ya, y_b) + 1), 14, fill=col)
                T(d, (x + bw // 2, min(ya, y_b) - 40), ('−' if v < 0 else '') + tr(abs(v) * p, 0) + ' ₺', F('k', 42), INK, 'mm')
                T(d, (x + bw // 2, base + 40), lab, F('s', 28), MUTED, 'mm')
            rise(fr, t, s0, bar, .4, 30)
            level = abs(v) if i == 0 else level + (v if 0 < i < 4 else 0)
    else:
        level = 0
        for lab, v, col, i in steps:
            y = 560 + i * 150; s0 = .4 + i * .65
            def rowf(d, y=y, lab=lab, v=v, col=col, i=i, s0=s0):
                final = i in (0, 4)
                d.rounded_rectangle((M, y, R, y + 125), 24, fill=GOLD if i == 4 else CARD)
                fg = BG if i == 4 else INK
                T(d, (M + 32, y + 62), lab, F('b' if final else 's', 36), fg if final else MUTED, 'lm')
                T(d, (R - 32, y + 62), ('−' if v < 0 else '') + tr(abs(v) * prog(t, s0, .6), 0) + ' ₺', F('k', 46), fg if i == 4 else (RED if v < 0 else INK), 'rm')
            rise(fr, t, s0, rowf, .45, 40)
    rise(fr, t, 4.6 if L else 3.9, lambda d: pill(d, CX, 1010 if L else 1360, f'Cebine kalan: %{tr(ORAN * 100, 0)}', F('k', 44), GOLD, BG) if not L else pill(d, W - M - 260, 330, f'Cebine kalan: %{tr(ORAN * 100, 0)}', F('k', 44), GOLD, BG))

def s_why(fr, t, dur):
    header(fr, 'Neden bu kadar vergi?', 'Aralık’ta matrah yılın en yüksek seviyesinde')
    dil = [(190000, '%15'), (400000, '%20'), (1500000, '%27')]
    if L:
        x0, x1, y = M, W - M, 520
        mx = 900000
        segs = [(0, 190000, (40, 70, 110)), (190000, 400000, (60, 90, 140)), (400000, mx, GOLD_S)]
        p = prog(t, .4, .9)
        for a, b, col in segs:
            xa, xb = x0 + (x1 - x0) * a / mx, x0 + (x1 - x0) * b / mx
            fr.d.rectangle((xa, y, xa + (xb - xa) * p, y + 70), fill=col)
        if p > .8:
            for a, b, lab in ((0, 190000, '%15'), (190000, 400000, '%20'), (400000, mx, '%27')):
                T(fr.d, ((x0 + (x1 - x0) * (a + b) / 2 / mx), y + 35), lab, F('k', 40), INK, 'mm')
        def mk(d, v, lab, col, up):
            x = x0 + (x1 - x0) * v / mx
            d.line((x, y - 30, x, y + 100), fill=col, width=6)
            T(d, (x, y - 60 if up else y + 140), lab, F('b', 34), col, 'mm')
        rise(fr, t, 1.6, lambda d: mk(d, 701250, 'Kasım sonu: 701.250 ₺', MUTED, True))
        rise(fr, t, 2.3, lambda d: mk(d, 701250 + 63750 + 63750, '+ maaş + ikramiye', GOLD, False))
        rise(fr, t, 3.4, lambda d: (T(d, (M, 790), 'İkramiyenin tamamı %27 diliminden vergilenir.', F('b', 44), INK), T(d, (M, 860), 'Asgari ücret istisnası maaşta kullanıldığı için ikramiyeye ek indirim gelmez.', F('s', 34), MUTED)))
    else:
        items = [('Kasım sonu matrah', '701.250 ₺'), ('Dilim', '%27'), ('Asgari ücret istisnası', 'maaşta kullanıldı')]
        for i, (a, b) in enumerate(items):
            y = 580 + i * 170
            rise(fr, t, .4 + i * .5, lambda d, a=a, b=b, y=y, i=i: (d.rounded_rectangle((M, y, R, y + 145), 24, fill=CARD), T(d, (M + 32, y + 48), a, F('s', 34), MUTED, 'lm'), T(d, (M + 32, y + 105), b, F('k', 48), GOLD if i == 1 else INK, 'lm')))
        rise(fr, t, 2.2, lambda d: (T(d, (CX, 1150), 'İkramiyenin tamamı', F('b', 44), INK, 'mm'), T(d, (CX, 1215), '%27’den vergilenir', F('k', 52), GOLD, 'mm')))

def s_table(fr, t, dur):
    header(fr, 'Maaşına göre net ikramiye', '1 maaş ikramiye, Aralık ayında')
    for i, (b, n, o) in enumerate(TABLO):
        if L: y, x0, x1 = 390 + i * 120, M, 1500
        else: y, x0, x1 = 560 + i * 165, M, R
        hl = i == 2
        def rowf(d, y=y, b=b, n=n, o=o, hl=hl, x0=x0, x1=x1):
            h = 100 if L else 140
            d.rounded_rectangle((x0, y, x1, y + h), 22, fill=GOLD if hl else CARD)
            fg = BG if hl else INK
            if L:
                T(d, (x0 + 36, y + h // 2), 'Brüt ' + b, F('b', 40), fg, 'lm')
                T(d, (x0 + 820, y + h // 2), tr(n, 0) + ' ₺ net', F('k', 46), fg, 'rm')
                T(d, (x1 - 36, y + h // 2), o, F('k', 46), fg if hl else GOLD, 'rm')
            else:
                T(d, (x0 + 30, y + 40), 'Brüt ' + b, F('s', 32), fg if hl else MUTED, 'lm')
                T(d, (x0 + 30, y + 98), tr(n, 0) + ' ₺', F('k', 48), fg, 'lm')
                T(d, (x1 - 30, y + h // 2), o, F('k', 52), fg if hl else GOLD, 'rm')
        rise(fr, t, .4 + i * .45, rowf, .45, 40)
    if L: rise(fr, t, 2.6, lambda d: T(d, (M, 900), 'Düşük maaşta %20 diliminde kalınırsa net oran yükselir.', F('s', 36), MUTED))

def s_month(fr, t, dur):
    header(fr, 'Haziran’da mı, Aralık’ta mı?', 'Ödendiği ay o ayın netini değiştirir, yılın toplamını değil')
    cards = [('Haziran’da ödenirse', '47.193 ₺', 'o ayın ek neti'), ('Aralık’ta ödenirse', '45.968 ₺', 'o ayın ek neti')]
    for i, (a, b, c) in enumerate(cards):
        if L: box = (M + i * 860, 400, M + i * 860 + 800, 700)
        else: box = (M, 560 + i * 330, R, 860 + i * 330)
        rise(fr, t, .4 + i * .5, lambda d, a=a, b=b, c=c, box=box: (d.rounded_rectangle(box, 28, fill=CARD), T(d, (box[0] + 40, box[1] + 70), a, F('b', 40), MUTED, 'lm'), T(d, (box[0] + 40, box[1] + 170), b, F('k', 80), GOLD, 'lm'), T(d, (box[0] + 40, box[1] + 250), c, F('s', 32), MUTED, 'lm')))
    y = 800 if L else 1260
    rise(fr, t, 1.8, lambda d: pill(d, CX, y, 'Yıllık toplam net: ikisinde de +45.968 ₺', F('k', 44 if L else 36), GOLD, BG))

def s_cta(fr, t, dur):
    fr.d.rectangle((0, 0, W, H), fill=GOLD)
    lg = logo(120); fr.im.paste(lg, (CX - 60, 150 if L else 420), lg)
    rise(fr, t, .1, lambda d: T(d, (CX, 360 if L else 640), 'Kendi ikramiyeni hesapla', F('k', 76 if L else 62), BG, 'mm'))
    def url(d):
        w2 = 560 if L else (R - M) // 2; y = 470 if L else 760
        d.rounded_rectangle((CX - w2, y, CX + w2, y + 110), 55, fill=BG)
        T(d, (CX, y + 55), 'hesapcantasi.com/ikramiye-hesaplama' if L else 'hesapcantasi.com', F('k', 46 if L else 60), INK, 'mm')
    rise(fr, t, .7, url)
    rise(fr, t, 1.4, lambda d: T(d, (CX, 660 if L else 940), 'Aylık brüt · ikramiye · ödeneceği ay', F('s', 40 if L else 34), BG, 'mm'))
    if L: rise(fr, t, 2.1, lambda d: T(d, (CX, 760), 'Link açıklamada', F('s', 34), (90, 70, 30), 'mm'))

LONG = [(s_hook, 4.5), (s_fall, 8.0), (s_why, 7.5), (s_table, 6.5), (s_month, 6.5), (s_cta, 6.0)]
SHORT = [(s_hook, 3.5), (s_fall, 7.0), (s_why, 5.5), (s_cta, 5.0)]
SCENES = LONG if L else SHORT

def draw(i, t):
    fn, dur = SCENES[i]; fr = Fr(); fn(fr, t, dur)
    if fn is not s_cta:
        yb = H - 12 if L else 232
        fr.d.rectangle((0, yb, int(W * min(1, t / dur)), yb + 10), fill=GOLD)
    a = min(1, t / .18, (dur - t) / .18)
    if a < 1: fr.im = Image.blend(Image.new('RGB', (W, H), GOLD) if fn is s_cta else BGIM, fr.im, max(0, a))
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
