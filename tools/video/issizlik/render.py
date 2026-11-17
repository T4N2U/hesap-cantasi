"""'İşsizlik maaşı ne kadar? Kaç ay alırım?' (publish 1 Dec 2026).
Visual variant: soft blush-to-cream gradient, rose accent, single big numbers that zoom in, card-flip reveals,
floor/ceiling meter and a month-strip calendar for the payment duration. Music preset: lofi-piano.
Figures: E.issizlik() in static/assets/engine.js (2026 brüt asgari 33.030 ₺).
Usage: python3 render.py long|short [stills]"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

MODE = sys.argv[1] if len(sys.argv) > 1 else 'long'
L = MODE == 'long'
W, H = (1920, 1080) if L else (1080, 1920)
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

INK = (40, 30, 38); MUTED = (122, 104, 114); BRAND = (15, 107, 79); WHITE = (255, 255, 255)
ROSE = (196, 62, 112); ROSE_S = (250, 222, 232); CARD = (255, 252, 250); LINE = (238, 218, 226)

# --- figures (from engine.js, 2026) ---
EN_AZ, EN_COK = 13111.72, 26223.44
ORN_ORT, ORN_BRUT, ORN_DAMGA, ORN_NET = 50000, 20000.00, 151.80, 19848.20
ORN_TOPLAM = 198482.00  # 10 ay

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def prog(t, s, d=0.5): return ease((t - s) / d)
def tr(n, d=2): return f'{n:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def T(d, xy, s, f, fill=INK, a='la'): d.text(xy, s, font=f, fill=fill, anchor=a)

def _gradient():
    top, bot = (251, 228, 236), (252, 247, 240)
    g = Image.new('RGB', (1, H))
    for y in range(H):
        k = y / (H - 1); g.putpixel((0, y), tuple(int(top[i] + (bot[i] - top[i]) * k) for i in range(3)))
    im = g.resize((W, H))
    d = ImageDraw.Draw(im)  # a few soft circles for depth
    for cx, cy, r in ((W * .88, H * .12, 260), (W * .08, H * .9, 200)):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(246, 214, 226), width=6)
    return im
BGIM = _gradient()

class Fr:
    def __init__(s): s.im = BGIM.copy(); s.d = ImageDraw.Draw(s.im)

def layer(fn):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay)); return lay

def flip(fr, t, s, box, fn, dur=0.5):
    """Card flip: the card opens horizontally from its centre line (this video's transition)."""
    p = prog(t, s, dur)
    if p <= 0: return
    x0, y0, x1, y1 = box
    card = layer(fn).crop(box)
    if p < 1:
        w = max(1, int((x1 - x0) * p))
        card = card.resize((w, y1 - y0))
        x0 = x0 + ((x1 - x0) - w) // 2
    fr.im.paste(card, (x0, y0), card)

def zoom(fr, t, s, center, fn, dur=0.6):
    """Big number zooms in from 140% to 100% while fading in."""
    p = prog(t, s, dur)
    if p <= 0: return
    lay = layer(fn)
    if p < 1:
        k = 1.4 - .4 * p
        cx, cy = center
        lay = lay.resize((int(W * k), int(H * k)))
        ox, oy = int(cx * k - cx), int(cy * k - cy)
        lay = lay.crop((ox, oy, ox + W, oy + H))
        lay.putalpha(lay.getchannel('A').point(lambda v: int(v * p)))
    fr.im.paste(lay, (0, 0), lay)

_LOGO = {}
def logo(size):
    """The channel logo (briefcase with keypad), from tools/video/logo.png."""
    if size not in _LOGO:
        _LOGO[size] = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logo.png')).convert('RGBA').resize((size, size), Image.LANCZOS)
    return _LOGO[size]

def brand(fr, x, y):
    lg = logo(52); fr.im.paste(lg, (x, y), lg)
    T(fr.d, (x + 68, y + 26), 'Hesap Çantası', F('b', 30), INK, 'lm')

M = 120 if L else 80
R = W - M if L else 920
TOP = 70 if L else 250
CX = W // 2 if L else (M + R) // 2

def header(fr, title, sub=None):
    brand(fr, M, TOP)
    ty = 200 if L else 370
    T(fr.d, (M, ty), title, F('k', 70 if L else 58), INK)
    if sub: T(fr.d, (M, ty + (92 if L else 80)), sub, F('s', 40 if L else 34), MUTED)

def pill(d, cx, cy, text, f, bg, fg, padx=40, h=90):
    w = d.textlength(text, font=f) + padx * 2
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), h // 2, fill=bg); T(d, (cx, cy), text, f, fg, 'mm')

# ---------------- scenes ----------------
def s_hook(fr, t, dur):
    brand(fr, M, TOP)
    if L:
        flip(fr, t, .1, (M, 230, W - M, 520), lambda d: (T(d, (CX, 300), 'İşsizlik maaşı', F('k', 120), INK, 'mm'), T(d, (CX, 440), 'ne kadar, kaç ay?', F('k', 100), ROSE, 'mm')))
        zoom(fr, t, 1.0, (CX, 680), lambda d: (T(d, (CX, 650), tr(EN_AZ, 0) + ' ₺  –  ' + tr(EN_COK, 0) + ' ₺', F('k', 110), INK, 'mm'), T(d, (CX, 750), '2026’da aylık en az ve en çok', F('s', 40), MUTED, 'mm')))
        flip(fr, t, 2.0, (0, 830, W, 930), lambda d: pill(d, CX, 880, 'Son 4 ay brüt ortalaması × %40', F('b', 44), ROSE, WHITE))
    else:
        flip(fr, t, .1, (M, 460, R, 760), lambda d: (T(d, (CX, 530), 'İşsizlik', F('k', 120), INK, 'mm'), T(d, (CX, 670), 'maaşı ne kadar?', F('k', 90), ROSE, 'mm')))
        zoom(fr, t, .9, (CX, 960), lambda d: (T(d, (CX, 900), tr(EN_AZ, 0) + ' ₺', F('k', 110), INK, 'mm'), T(d, (CX, 990), '–', F('k', 70), MUTED, 'mm'), T(d, (CX, 1080), tr(EN_COK, 0) + ' ₺', F('k', 110), ROSE, 'mm')))
        flip(fr, t, 1.8, (M, 1180, R, 1280), lambda d: pill(d, CX, 1230, '2026 · aylık en az / en çok', F('b', 40), INK, WHITE))

def s_who(fr, t, dur):
    header(fr, 'Kimler alabilir?', 'Dört şartın hepsi gerekir')
    items = [('Son 3 yılda', 'en az 600 gün prim'), ('Son 120 gün', 'kesintisiz çalışmış'), ('Kendi kusuru', 'olmadan işten çıkmış'), ('30 gün içinde', 'İŞKUR’a başvurmuş')]
    for i, (a, b) in enumerate(items):
        if L:
            cw = (W - 2 * M - 3 * 30) // 4; x = M + i * (cw + 30); box = (x, 400, x + cw, 760)
            def card(d, x=x, a=a, b=b, i=i):
                d.rounded_rectangle((x, 400, x + cw, 760), 30, fill=CARD, outline=LINE, width=3)
                d.ellipse((x + 40, 440, x + 120, 520), fill=ROSE); T(d, (x + 80, 480), str(i + 1), F('k', 44), WHITE, 'mm')
                T(d, (x + 40, 590), a, F('k', 44), INK, 'lm'); T(d, (x + 40, 660), b, F('s', 32), MUTED, 'lm')
        else:
            y = 560 + i * 190; box = (M, y, R, y + 165)
            def card(d, y=y, a=a, b=b, i=i):
                d.rounded_rectangle((M, y, R, y + 165), 28, fill=CARD, outline=LINE, width=3)
                d.ellipse((M + 30, y + 42, M + 110, y + 122), fill=ROSE); T(d, (M + 70, y + 82), str(i + 1), F('k', 44), WHITE, 'mm')
                T(d, (M + 140, y + 55), a, F('k', 46), INK, 'lm'); T(d, (M + 140, y + 115), b, F('s', 34), MUTED, 'lm')
        flip(fr, t, .4 + i * .55, box, card)
    if L: flip(fr, t, 3.0, (0, 820, W, 920), lambda d: pill(d, CX, 870, 'İstifa edene kural olarak ödenmez', F('b', 40), INK, WHITE))

def s_formula(fr, t, dur):
    header(fr, 'Nasıl hesaplanır?', 'Örnek: son 4 ay ortalama brüt 50.000 ₺')
    rows = [('Ortalama brüt', tr(ORN_ORT) + ' ₺', INK), ('× %40', tr(ORN_BRUT) + ' ₺', INK), ('− Damga vergisi', tr(ORN_DAMGA) + ' ₺', MUTED)]
    if L:
        for i, (a, b, c) in enumerate(rows):
            y = 390 + i * 120
            flip(fr, t, .4 + i * .5, (M, y, 900, y + 100), lambda d, a=a, b=b, c=c, y=y: (d.rounded_rectangle((M, y, 900, y + 100), 24, fill=CARD, outline=LINE, width=3), T(d, (M + 30, y + 50), a, F('s', 38), MUTED, 'lm'), T(d, (870, y + 50), b, F('k', 44), c, 'rm')))
        zoom(fr, t, 2.2, (1400, 560), lambda d: (T(d, (1400, 430), 'Aylık net', F('b', 44), MUTED, 'mm'), T(d, (1400, 545), tr(ORN_NET * prog(t, 2.2, 1.0)) + ' ₺', F('k', 104), ROSE, 'mm'), T(d, (1400, 650), 'Gelir vergisi ve SGK kesilmez', F('s', 34), MUTED, 'mm')))
        flip(fr, t, 3.6, (M, 790, W - M, 900), lambda d: (d.rounded_rectangle((M, 790, W - M, 900), 30, fill=ROSE_S), T(d, (M + 40, 845), 'Tavan: brüt asgari ücretin %80’i  →  en çok ' + tr(EN_COK) + ' ₺ net', F('b', 42), INK, 'lm')))
    else:
        for i, (a, b, c) in enumerate(rows):
            y = 540 + i * 140
            flip(fr, t, .4 + i * .5, (M, y, R, y + 120), lambda d, a=a, b=b, c=c, y=y: (d.rounded_rectangle((M, y, R, y + 120), 24, fill=CARD, outline=LINE, width=3), T(d, (M + 30, y + 60), a, F('s', 36), MUTED, 'lm'), T(d, (R - 30, y + 60), b, F('k', 44), c, 'rm')))
        zoom(fr, t, 2.0, (CX, 1080), lambda d: (T(d, (CX, 1000), 'Aylık net', F('b', 44), MUTED, 'mm'), T(d, (CX, 1100), tr(ORN_NET * prog(t, 2.0, 1.0)) + ' ₺', F('k', 104), ROSE, 'mm')))
        flip(fr, t, 3.2, (M, 1200, R, 1300), lambda d: pill(d, CX, 1250, 'En çok ' + tr(EN_COK, 0) + ' ₺', F('b', 42), INK, WHITE))

def s_range(fr, t, dur):
    header(fr, 'Alt ve üst sınır', 'Ortalama brüt maaşa göre aylık net ödenek')
    ex = [('asgari ücret', 33030, EN_AZ), ('50.000 ₺', 50000, ORN_NET), ('60.000 ₺', 60000, 23817.84), ('66.060 ₺ ve üstü', 66060, EN_COK)]
    if L:
        x0, x1, y = M + 40, W - M - 40, 600
        p = prog(t, .3, .9)
        fr.d.rounded_rectangle((x0, y - 18, x0 + int((x1 - x0) * p), y + 18), 18, fill=ROSE_S)
        fr.d.rounded_rectangle((x0, y - 18, x0 + int((x1 - x0) * p * .999), y + 18), 18, outline=ROSE, width=3)
        for i, (lab, avg, net) in enumerate(ex):
            k = (net - EN_AZ) / (EN_COK - EN_AZ); x = int(x0 + (x1 - x0) * k)
            q = prog(t, 1.0 + i * .55, .5)
            if q <= 0: continue
            ax = 'lm' if i == 0 else ('rm' if i == 3 else 'mm')
            def mk(d, x=x, lab=lab, net=net, i=i, ax=ax):
                d.ellipse((x - 30, y - 30, x + 30, y + 30), fill=ROSE if i in (0, 3) else INK, outline=WHITE, width=6)
                up = i % 2 == 0
                tx = x - 30 if ax == 'lm' else (x + 30 if ax == 'rm' else x)
                T(d, (tx, y - 140 if up else y + 90), tr(net, 0) + ' ₺', F('k', 56), INK, ax)
                T(d, (tx, y - 80 if up else y + 150), 'ort. brüt ' + lab, F('s', 32), MUTED, ax)
            zoom(fr, t, 1.0 + i * .55, (x, y), mk, .45)
        flip(fr, t, 3.6, (0, 870, W, 960), lambda d: pill(d, CX, 915, 'Ortalama brüt 66.060 ₺’yi aşınca ödenek artmaz', F('b', 40), INK, WHITE))
    else:
        x0, y0, y1 = 260, 560, 1340
        p = prog(t, .3, .9)
        fr.d.rounded_rectangle((x0 - 18, y1 - int((y1 - y0) * p), x0 + 18, y1), 18, fill=ROSE_S, outline=ROSE, width=3)
        for i, (lab, avg, net) in enumerate(ex):
            k = (net - EN_AZ) / (EN_COK - EN_AZ); y = int(y1 - (y1 - y0) * k)
            def mk(d, y=y, lab=lab, net=net, i=i):
                d.ellipse((x0 - 30, y - 30, x0 + 30, y + 30), fill=ROSE if i in (0, 3) else INK, outline=WHITE, width=6)
                T(d, (x0 + 70, y - 25), tr(net, 0) + ' ₺', F('k', 54), INK, 'lm'); T(d, (x0 + 70, y + 30), 'ort. brüt ' + lab, F('s', 32), MUTED, 'lm')
            zoom(fr, t, 1.0 + i * .5, (x0, y), mk, .45)

def s_months(fr, t, dur):
    header(fr, 'Kaç ay alırsınız?', 'Son 3 yıldaki prim gününe göre')
    rows = [('600 gün', 6), ('900 gün', 8), ('1080 gün', 10)]
    for i, (lab, n) in enumerate(rows):
        if L:
            y = 380 + i * 150; bx = M + 330; cw = 100
        else:
            y = 560 + i * 230; bx = M; cw = 70
        s0 = .4 + i * .9
        if prog(t, s0, .3) > 0:
            T(fr.d, (M, y + 50) if L else (M, y), lab, F('k', 50 if L else 46), INK, 'lm' if L else 'la')
            if L: T(fr.d, (M, y + 105), f'{n * 30} gün', F('s', 30), MUTED, 'lm')
        by = y if L else y + 75
        for m in range(10):
            on = m < n
            q = prog(t, s0 + .08 * m, .25)
            if q <= 0: continue
            x = bx + m * (cw + (14 if L else 12))
            def cell(d, x=x, on=on, m=m):
                d.rounded_rectangle((x, by, x + cw, by + 110), 18, fill=ROSE if on else CARD, outline=ROSE if on else LINE, width=3)
                d.rectangle((x + 8, by + 8, x + cw - 8, by + 26), fill=(226, 120, 158) if on else LINE)
                T(d, (x + cw // 2, by + 70), str(m + 1), F('k', 40 if L else 34), WHITE if on else LINE, 'mm')
            flip(fr, t, s0 + .08 * m, (x, by, x + cw, by + 110), cell, .25)
        if L and prog(t, s0 + .9, .3) > 0:
            T(fr.d, (W - M, y + 55), f'{n} ay', F('k', 56), ROSE, 'rm')
    if L:
        zoom(fr, t, 3.6, (CX, 900), lambda d: (d.rounded_rectangle((M, 845, W - M, 955), 30, fill=INK), T(d, (CX, 900), 'Örnek: 19.848 ₺ × 10 ay = ' + tr(ORN_TOPLAM, 0) + ' ₺ toplam', F('k', 48), WHITE, 'mm')), .5)
    else:
        zoom(fr, t, 3.3, (CX, 1330), lambda d: (d.rounded_rectangle((M, 1270, R, 1390), 30, fill=INK), T(d, (CX, 1330), '10 ay = ' + tr(ORN_TOPLAM, 0) + ' ₺', F('k', 50), WHITE, 'mm')), .5)

def s_cta(fr, t, dur):
    fr.d.rectangle((0, 0, W, H), fill=ROSE)
    big = F('k', 76 if L else 62)
    zoom(fr, t, .1, (CX, 330 if L else 600), lambda d: T(d, (CX, 330 if L else 600), 'Kendi işsizlik maaşını hesapla' if L else 'İşsizlik maaşını hesapla', big, WHITE, 'mm'))
    def url(d):
        w2 = 640 if L else (R - M) // 2; y = 470 if L else 760
        d.rounded_rectangle((CX - w2, y, CX + w2, y + 110), 55, fill=WHITE)
        T(d, (CX, y + 55), 'hesapcantasi.com/issizlik-maasi-hesaplama' if L else 'hesapcantasi.com', F('k', 46 if L else 60), INK, 'mm')
    flip(fr, t, .8, (0, 0, W, H), url)
    flip(fr, t, 1.6, (0, 0, W, H), lambda d: T(d, (CX, 660 if L else 940), 'Aylık tutar · kaç ay · toplam ödenek', F('s', 40 if L else 34), WHITE, 'mm'))
    if L: flip(fr, t, 2.3, (0, 0, W, H), lambda d: T(d, (CX, 760), 'Link açıklamada', F('s', 34), (255, 220, 232), 'mm'))

LONG = [(s_hook, 4.5), (s_who, 7.0), (s_formula, 7.5), (s_range, 7.0), (s_months, 7.5), (s_cta, 6.0)]
SHORT = [(s_hook, 3.5), (s_formula, 6.5), (s_months, 6.0), (s_cta, 5.0)]
SCENES = LONG if L else SHORT

def draw(i, t):
    fn, dur = SCENES[i]; fr = Fr(); fn(fr, t, dur)
    if fn is not s_cta:
        yb = H - 12 if L else 232
        fr.d.rectangle((0, yb, int(W * min(1, t / dur)), yb + 10), fill=ROSE)
    a = min(1, t / .18, (dur - t) / .18)
    if a < 1: fr.im = Image.blend(Image.new('RGB', (W, H), ROSE) if fn is s_cta else BGIM, fr.im, max(0, a))
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
