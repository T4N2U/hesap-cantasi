"""'Emlak vergisi nasıl hesaplanır?' — 2. taksit son gün 30 Kasım.
Visual variant: light stone ground with a faint roof-line pattern, amber (vergi) accent, house illustration,
formula-left / result-right split, left-to-right wipe reveals. Music preset: rhodes-groove.
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

BG = (242, 239, 232); INK = (34, 33, 30); MUTED = (112, 106, 96); BRAND = (15, 107, 79); WHITE = (255, 255, 255)
AMBER = (214, 138, 24); AMBER_S = (250, 232, 200); CARD = (255, 253, 248); LINE = (226, 220, 208); ROOF = (234, 229, 219); RED = (184, 64, 44)

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def prog(t, s, d=0.5): return ease((t - s) / d)
def tr(n, d=2): return f'{n:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def T(d, xy, s, f, fill=INK, a='la'): d.text(xy, s, font=f, fill=fill, anchor=a)

class Fr:
    def __init__(s, bg=BG): s.im = Image.new('RGB', (W, H), bg); s.d = ImageDraw.Draw(s.im)

def wipe(fr, t, s, box, fn, dur=0.55):
    """Draw fn on a layer and reveal it left-to-right inside box (this video's transition)."""
    p = prog(t, s, dur)
    if p <= 0: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay))
    x0, y0, x1, y1 = box
    mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).rectangle((x0, y0, x0 + int((x1 - x0) * p), y1), fill=255)
    a = lay.getchannel('A'); a = Image.composite(a, Image.new('L', (W, H), 0), mask); lay.putalpha(a)
    fr.im.paste(lay, (0, 0), lay)

def roofs(fr):  # faint repeating roof-line pattern
    d = fr.d; s = 120
    for y in range(0, H + s, s):
        for x in range(-s, W + s, s * 2):
            off = s if (y // s) % 2 else 0
            d.line((x + off, y + 40, x + off + s // 2, y, x + off + s, y + 40), fill=ROOF, width=4)

def brand(fr, x, y):
    d = fr.d
    d.rounded_rectangle((x, y, x + 52, y + 52), 13, fill=BRAND); T(d, (x + 26, y + 26), '₺', F('b', 32), WHITE, 'mm')
    T(d, (x + 68, y + 26), 'Hesap Çantası', F('b', 30), INK, 'lm')

def house(d, cx, base, s=1.0, col=AMBER):
    w = int(360 * s); h = int(240 * s)
    d.polygon([(cx - w // 2 - 30 * s, base - h), (cx, base - h - int(170 * s)), (cx + w // 2 + 30 * s, base - h)], fill=col)
    d.rectangle((cx - w // 2, base - h, cx + w // 2, base), fill=CARD, outline=col, width=int(8 * s))
    d.rectangle((cx - int(45 * s), base - int(130 * s), cx + int(45 * s), base), fill=col)
    for dx in (-1, 1):
        x = cx + dx * int(110 * s)
        d.rectangle((x - int(38 * s), base - int(190 * s), x + int(38 * s), base - int(115 * s)), fill=AMBER_S, outline=col, width=int(5 * s))

M = 120 if L else 80
R = W - M if L else 920
TOP = 70 if L else 250

def header(fr, title, sub=None):
    roofs(fr); brand(fr, M, TOP)
    ty = 210 if L else 370
    T(fr.d, (M, ty), title, F('k', 70 if L else 58), INK)
    if sub: T(fr.d, (M, ty + (95 if L else 80)), sub, F('s', 40 if L else 36), MUTED)

# ---------------- scenes ----------------
def s_hook(fr, t, dur):
    roofs(fr); brand(fr, M, TOP)
    if L:
        wipe(fr, t, .1, (M, 250, 1150, 560), lambda d: (T(d, (M, 260), 'Emlak vergisi', F('k', 120), INK), T(d, (M, 400), 'nasıl hesaplanır?', F('k', 100), AMBER)))
        wipe(fr, t, .9, (M, 600, 1100, 720), lambda d: (d.rounded_rectangle((M, 610, M + 760, 700), 45, fill=INK), T(d, (M + 380, 655), '2. taksit: son gün 30 Kasım', F('b', 44), WHITE, 'mm')))
        p = prog(t, .3, .8)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); house(ImageDraw.Draw(lay), 1480, 820 + int((1 - p) * 60), 1.2)
        if p < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * p)))
        fr.im.paste(lay, (0, 0), lay)
    else:
        p = prog(t, .2, .8)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); house(ImageDraw.Draw(lay), 500, 760 + int((1 - p) * 60), 1.0)
        if p < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * p)))
        fr.im.paste(lay, (0, 0), lay)
        wipe(fr, t, .5, (M, 820, R, 1120), lambda d: (T(d, (M, 830), 'Emlak vergisi', F('k', 104), INK), T(d, (M, 960), 'ne kadar?', F('k', 104), AMBER)))
        wipe(fr, t, 1.2, (M, 1150, R, 1260), lambda d: (d.rounded_rectangle((M, 1160, R - 40, 1250), 45, fill=INK), T(d, ((M + R - 40) // 2, 1205), 'Son gün 30 Kasım', F('b', 46), WHITE, 'mm')))

def s_formula(fr, t, dur):
    header(fr, 'Formül tek satır', 'Vergi değeri × oran × hisse payınız')
    if L:
        y = 420
        parts = [('Vergi değeri', '4.000.000 ₺'), ('×', None), ('Oran', 'binde 2'), ('×', None), ('Hisse', '%100')]
        x = M
        for i, (lab, v) in enumerate(parts):
            if v is None:
                wipe(fr, t, .5 + i * .35, (x, y, x + 80, y + 200), lambda d, x=x: T(d, (x + 40, y + 100), '×', F('k', 80), AMBER, 'mm')); x += 90; continue
            wdt = 380 if i == 0 else 300
            wipe(fr, t, .5 + i * .35, (x, y, x + wdt, y + 200), lambda d, x=x, lab=lab, v=v, wdt=wdt: (d.rounded_rectangle((x, y, x + wdt, y + 200), 26, fill=CARD, outline=LINE, width=3), T(d, (x + 30, y + 50), lab, F('s', 34), MUTED, 'lm'), T(d, (x + 30, y + 130), v, F('k', 54), INK, 'lm')))
            x += wdt + 10
        def res(d):
            d.rounded_rectangle((M, 700, W - M, 900), 30, fill=AMBER)
            T(d, (M + 50, 800), 'Yıllık emlak vergisi', F('b', 50), WHITE, 'lm')
            T(d, (W - M - 50, 800), tr(8000 * prog(t, 3.0, .9)) + ' ₺', F('k', 84), WHITE, 'rm')
        wipe(fr, t, 2.7, (M, 700, W - M, 900), res)
    else:
        rows = [('Vergi değeri', '4.000.000 ₺'), ('× Oran (büyükşehir konut)', 'binde 2'), ('× Hisse payı', '%100')]
        for i, (lab, v) in enumerate(rows):
            y = 560 + i * 150
            wipe(fr, t, .4 + i * .45, (M, y, R, y + 130), lambda d, lab=lab, v=v, y=y: (d.rounded_rectangle((M, y, R, y + 130), 26, fill=CARD, outline=LINE, width=3), T(d, (M + 36, y + 40), lab, F('s', 34), MUTED, 'lm'), T(d, (M + 36, y + 92), v, F('k', 50), INK, 'lm')))
        def res(d):
            d.rounded_rectangle((M, 1040, R, 1260), 30, fill=AMBER)
            T(d, ((M + R) // 2, 1100), 'Yıllık vergi', F('b', 44), WHITE, 'mm')
            T(d, ((M + R) // 2, 1195), tr(8000 * prog(t, 2.2, .9)) + ' ₺', F('k', 92), WHITE, 'mm')
        wipe(fr, t, 1.9, (M, 1040, R, 1260), res)
        wipe(fr, t, 3.4, (M, 1300, R, 1400), lambda d: T(d, (M, 1310), 'İki taksit: Mayıs ve Kasım’da 4.000 ₺', F('s', 38), MUTED))

def s_rates(fr, t, dur):
    header(fr, 'Oranlar (binde)', 'Büyükşehir ve mücavir alanlarda iki katı')
    rows = [('Konut', '1', '2'), ('İşyeri', '2', '4'), ('Arsa', '3', '6'), ('Arazi', '1', '2')]
    x0, x1 = M, (1180 if L else R)
    y0 = 400 if L else 560
    rh = 110 if L else 130
    c1, c2 = (x0 + (x1 - x0) * .55, x0 + (x1 - x0) * .85)
    wipe(fr, t, .3, (x0, y0, x1, y0 + 80), lambda d: (T(d, (x0 + 30, y0 + 40), 'Taşınmaz', F('b', 34), MUTED, 'lm'), T(d, (c1, y0 + 40), 'Diğer', F('b', 34), MUTED, 'mm'), T(d, (c2, y0 + 40), 'Büyükşehir', F('b', 34), AMBER, 'mm')))
    for i, (a, b, c) in enumerate(rows):
        y = y0 + 90 + i * rh
        wipe(fr, t, .6 + i * .35, (x0, y, x1, y + rh - 14), lambda d, a=a, b=b, c=c, y=y: (d.rounded_rectangle((x0, y, x1, y + rh - 14), 22, fill=CARD, outline=LINE, width=3), T(d, (x0 + 30, y + (rh - 14) // 2), a, F('b', 46), INK, 'lm'), T(d, (c1, y + (rh - 14) // 2), b, F('k', 52), MUTED, 'mm'), T(d, (c2, y + (rh - 14) // 2), c, F('k', 56), AMBER, 'mm')))
    if L:
        p = prog(t, 1.0, .8)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); house(ImageDraw.Draw(lay), 1530, 880, 0.9, BRAND)
        if p < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * p)))
        fr.im.paste(lay, (0, 0), lay)

def s_cap(fr, t, dur):
    header(fr, '2026’da “3 kat” sınırı', 'Yeni değer, 2025 değerinin 3 katını geçemez')
    if L:
        bars = [('2025 değeri', 1000000, MUTED), ('Belediyenin yeni değeri', 9000000, LINE), ('Vergide kullanılan', 3000000, AMBER)]
        y0 = 400; maxv = 9000000; x0 = M + 480; x1 = W - M
        for i, (lab, v, col) in enumerate(bars):
            y = y0 + i * 150
            p = prog(t, .5 + i * .6, .8)
            T(fr.d, (M, y + 40), lab, F('b', 40), INK, 'lm') if p > 0 else None
            if p > 0:
                fr.d.rounded_rectangle((x0, y, x0 + max(20, int((x1 - x0) * v / maxv * p)), y + 80), 20, fill=col)
                T(fr.d, (x0 + int((x1 - x0) * v / maxv * p) + 20, y + 40), tr(v * p, 0) + ' ₺', F('k', 40), INK, 'lm') if v < 8000000 else T(fr.d, (x1 - 20, y + 40), tr(v * p, 0) + ' ₺', F('k', 40), INK, 'rm')
        wipe(fr, t, 2.8, (M, 860, W - M, 960), lambda d: (d.rounded_rectangle((M, 860, W - M, 960), 30, fill=AMBER_S), T(d, (M + 40, 910), 'Vergi 18.000 ₺ yerine 6.000 ₺ olur', F('k', 48), INK, 'lm')))
    else:
        cards = [('2025 değeri', '1.000.000 ₺', CARD, INK), ('Belediyenin yeni değeri', '9.000.000 ₺', CARD, MUTED), ('Vergide kullanılan', '3.000.000 ₺', AMBER, WHITE)]
        for i, (lab, v, bg, fg) in enumerate(cards):
            y = 560 + i * 170
            wipe(fr, t, .4 + i * .5, (M, y, R, y + 150), lambda d, lab=lab, v=v, bg=bg, fg=fg, y=y: (d.rounded_rectangle((M, y, R, y + 150), 26, fill=bg, outline=LINE, width=3), T(d, (M + 36, y + 45), lab, F('s', 34), fg if bg == AMBER else MUTED, 'lm'), T(d, (M + 36, y + 105), v, F('k', 54), fg, 'lm')))
        wipe(fr, t, 2.2, (M, 1100, R, 1220), lambda d: (d.rounded_rectangle((M, 1100, R, 1220), 30, fill=AMBER_S), T(d, ((M + R) // 2, 1160), 'Vergi: 18.000 ₺ yerine 6.000 ₺', F('k', 44), INK, 'mm')))

def s_exempt(fr, t, dur):
    header(fr, 'Kimler ödemez?', 'Konut vergisi oranı sıfır uygulanır')
    items = ['Tek konutu var ve brüt 200 m²’yi geçmiyor', 'Geliri yok ya da yalnızca emekli aylığı alıyor', 'Gazi, engelli, şehit dul ve yetimleri', 'Belediyeye dilekçe vermek gerekir']
    for i, s in enumerate(items):
        y = 400 + i * 120
        last = i == 3
        wipe(fr, t, .4 + i * .5, (M, y, 1500, y + 90), lambda d, s=s, y=y, last=last: (d.ellipse((M, y + 10, M + 70, y + 80), fill=INK if last else AMBER), T(d, (M + 35, y + 45), '!' if last else '✓', F('k', 40), WHITE, 'mm'), T(d, (M + 110, y + 45), s, F('b' if last else 's', 46), INK, 'lm')))

def s_cta(fr, t, dur):
    fr.d.rectangle((0, 0, W, H), fill=AMBER)
    cx = W // 2 if L else (M + R) // 2
    big = F('k', 76 if L else 64)
    wipe(fr, t, .1, (0, 0, W, H), lambda d: T(d, (cx, 330 if L else 600), 'Kendi emlak vergini hesapla', big, WHITE, 'mm'), dur=.6)
    def url(d):
        w2 = 680 if L else (R - M) // 2; y = 470 if L else 760
        d.rounded_rectangle((cx - w2, y, cx + w2, y + 110), 55, fill=WHITE)
        T(d, (cx, y + 55), 'hesapcantasi.com/emlak-vergisi-hesaplama' if L else 'hesapcantasi.com', F('k', 48 if L else 60), INK, 'mm')
    wipe(fr, t, .8, (0, 0, W, H), url)
    wipe(fr, t, 1.6, (0, 0, W, H), lambda d: T(d, (cx, 660 if L else 940), 'Konut, işyeri, arsa · 3 kat sınırı · taksitler', F('s', 40 if L else 34), INK, 'mm'))
    if L: wipe(fr, t, 2.3, (0, 0, W, H), lambda d: T(d, (cx, 760), 'Link açıklamada', F('s', 34), INK, 'mm'))

LONG = [(s_hook, 4.5), (s_formula, 7.5), (s_rates, 7.0), (s_cap, 7.5), (s_exempt, 7.0), (s_cta, 6.0)]
SHORT = [(s_hook, 3.5), (s_formula, 7.0), (s_cap, 6.5), (s_cta, 5.5)]
SCENES = LONG if L else SHORT

def draw(i, t):
    fn, dur = SCENES[i]; fr = Fr(); fn(fr, t, dur)
    if fn is not s_cta:
        yb = H - 12 if L else 232
        fr.d.rectangle((0, yb, int(W * min(1, t / dur)), yb + 10), fill=AMBER)
    a = min(1, t / .18, (dur - t) / .18)
    if a < 1: fr.im = Image.blend(Image.new('RGB', (W, H), AMBER if fn is s_cta else BG), fr.im, max(0, a))
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
