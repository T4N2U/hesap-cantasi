"""'2027 asgari ücret senaryoları: %25 / %30 zamla net ne olur?' (publish 15 Dec 2026, Short 17 Dec).
Visual variant: warm paper ground with a faint dot grid, teal accent, a zam slider that sweeps %15 → %30,
odometer-style rolling numbers, a "SENARYO" stamp on every figure. Music preset: soft-pad.
Figures: 2026 asgari ücret (engine.js PARAMS) × (1 + zam); net = brüt × 0.85 (SGK %14 + işsizlik %1, no tax);
employer cost × 1.1875 with the 5-point SGK incentive, × 1.2575 without. Same as /asgari-ucret-2027/.
Usage: python3 render.py long|short [stills]"""
import os, subprocess, sys
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

BG = (250, 246, 238); DOT = (232, 224, 210); CARD = (255, 255, 255); LINE = (230, 222, 208); INK = (30, 34, 36); MUTED = (118, 112, 100)
TEAL = (14, 143, 163); TEAL_S = (214, 238, 242); STAMP = (200, 72, 60); BRAND = (15, 107, 79); WHITE = (255, 255, 255)

BRUT26, NET26 = 33030.00, 28075.50
K_NET, K_TES, K_TESYOK = 0.85, 1.1875, 1.2575
def senaryo(z): b = BRUT26 * (1 + z); return b, b * K_NET, b * K_NET - NET26, b * K_TES, b * K_TESYOK

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def prog(t, s, d=0.5): return ease((t - s) / d)
def tr(n, d=2): return f'{n:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def T(d, xy, s, f, fill=INK, a='la'): d.text(xy, s, font=f, fill=fill, anchor=a)

def _bg():
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    for y in range(20, H, 40):
        for x in range(20, W, 40): d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=DOT)
    return im
BGIM = _bg()

class Fr:
    def __init__(s): s.im = BGIM.copy(); s.d = ImageDraw.Draw(s.im)

def roll(fr, t, s, xy, text, f, fill=INK, a='la', dur=0.7):
    """Odometer roll: characters drop into place one after another (this video's transition)."""
    if t < s: return
    d = fr.d; x, y = xy
    total = d.textlength(text, font=f)
    if a[0] == 'm': x -= total / 2
    elif a[0] == 'r': x -= total
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    for i, ch in enumerate(text):
        p = prog(t, s + i * 0.035, dur * 0.6)
        if p > 0:
            ld.text((x, y - (1 - p) * f.size * 0.6), ch, font=f, fill=fill + (int(255 * p),), anchor='l' + a[1])
        x += d.textlength(ch, font=f)
    fr.im.paste(lay, (0, 0), lay)

def fade(fr, t, s, fn, dur=0.45):
    p = prog(t, s, dur)
    if p <= 0: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay))
    if p < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * p)))
    fr.im.paste(lay, (0, 0), lay)

_LOGO = {}
def logo(size):
    """The channel logo (briefcase with keypad), from tools/video/logo.png."""
    if size not in _LOGO:
        _LOGO[size] = Image.open(os.path.join(HERE, '..', 'logo.png')).convert('RGBA').resize((size, size), Image.LANCZOS)
    return _LOGO[size]

def brand(fr, x, y):
    lg = logo(52); fr.im.paste(lg, (x, y), lg)
    T(fr.d, (x + 68, y + 26), 'Hesap Çantası', F('b', 30), INK, 'lm')

def stamp(d, x, y, s=1.0):
    w, h = int(230 * s), int(64 * s)
    d.rounded_rectangle((x, y, x + w, y + h), int(12 * s), outline=STAMP, width=int(5 * s))
    T(d, (x + w // 2, y + h // 2), 'SENARYO', F('k', int(34 * s)), STAMP, 'mm')

M = 120 if L else 80
R = W - M if L else 920
TOP = 70 if L else 250
CX = W // 2 if L else (M + R) // 2

def header(fr, title, sub=None):
    brand(fr, M, TOP)
    ty = 200 if L else 370
    T(fr.d, (M, ty), title, F('k', 70 if L else 56), INK)
    if sub: T(fr.d, (M, ty + (92 if L else 78)), sub, F('s', 38 if L else 32), MUTED)

def pill(d, cx, cy, text, f, bg, fg, padx=40, h=90):
    w = d.textlength(text, font=f) + padx * 2
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), h // 2, fill=bg); T(d, (cx, cy), text, f, fg, 'mm')

# ---------------- scenes ----------------
def s_hook(fr, t, dur):
    brand(fr, M, TOP)
    if L:
        roll(fr, t, .1, (M, 330), '2027 asgari ücret', F('k', 120), INK, 'ls')
        roll(fr, t, .6, (M, 470), 'ne kadar olacak?', F('k', 110), TEAL, 'ls')
        fade(fr, t, 1.6, lambda d: (stamp(d, M, 540, 1.2), T(d, (M + 310, 578), 'Resmî rakam değil · zam oranına göre', F('s', 40), MUTED, 'lm')))
        fade(fr, t, 2.3, lambda d: pill(d, M + 420, 760, 'Bugün net: 28.075,50 ₺', F('b', 46), TEAL_S, INK))
    else:
        roll(fr, t, .1, (CX, 720), '2027', F('k', 200), TEAL, 'ms')
        roll(fr, t, .5, (CX, 860), 'asgari ücret', F('k', 100), INK, 'ms')
        roll(fr, t, .9, (CX, 970), 'ne olacak?', F('k', 100), INK, 'ms')
        fade(fr, t, 1.6, lambda d: stamp(d, CX - 160, 1040, 1.4))

def s_base(fr, t, dur):
    header(fr, 'Önce bugünü bilelim', '2026 asgari ücret')
    rows = [('Brüt', tr(BRUT26) + ' ₺'), ('− SGK %14 + işsizlik %1', '−' + tr(BRUT26 * .15) + ' ₺'), ('Vergi', '0 ₺ (istisna)'), ('Net', tr(NET26) + ' ₺')]
    for i, (a, b) in enumerate(rows):
        last = i == 3
        if L: y, x0, x1 = 390 + i * 120, M, 1300
        else: y, x0, x1 = 560 + i * 160, M, R
        h = 100 if L else 135
        fade(fr, t, .3 + i * .4, lambda d, y=y, x0=x0, x1=x1, h=h, last=last, a=a: (d.rounded_rectangle((x0, y, x1, y + h), 22, fill=TEAL if last else CARD, outline=None if last else LINE, width=3), T(d, (x0 + 32, y + h // 2), a, F('b' if last else 's', 40 if L else 34), WHITE if last else MUTED, 'lm')))
        roll(fr, t, .4 + i * .4, (x1 - 32, y + h // 2), b, F('k', 48 if L else 44), WHITE if last else INK, 'rm')
    if L: fade(fr, t, 2.4, lambda d: (d.rounded_rectangle((1360, 390, W - M, 820), 30, fill=TEAL_S), T(d, (1580, 520), 'Net =', F('b', 48), INK, 'mm'), T(d, (1580, 640), 'brüt × %85', F('k', 64), TEAL, 'mm'), T(d, (1580, 740), 'gelir ve damga vergisi yok', F('s', 30), MUTED, 'mm')))
    else: fade(fr, t, 2.2, lambda d: pill(d, CX, 1230, 'Net = brüt × %85', F('k', 48), TEAL_S, INK))

def s_slider(fr, t, dur):
    header(fr, 'Zam oranını kaydır', '2026 rakamlarına zam uygulanırsa')
    d = fr.d
    # slider position: hold at 15, 20, 25, 30
    stops = [.15, .20, .25, .30]; seg = (dur - 1.2) / 4
    k = min(3, int(max(0, t - .6) // seg)); local = (t - .6) - k * seg
    z = stops[k] if k == 0 else stops[k - 1] + (stops[k] - stops[k - 1]) * smooth(local / 0.6)
    if t < .6: z = .15
    lo, hi = .10, .35
    if L: x0, x1, y = M + 40, W - M - 40, 430
    else: x0, x1, y = M + 30, R - 30, 650
    d.rounded_rectangle((x0, y - 10, x1, y + 10), 10, fill=LINE)
    xp = x0 + (x1 - x0) * (z - lo) / (hi - lo)
    d.rounded_rectangle((x0, y - 10, xp, y + 10), 10, fill=TEAL)
    for s in stops:
        xs = x0 + (x1 - x0) * (s - lo) / (hi - lo)
        T(d, (xs, y + 50), f'%{int(s * 100)}', F('b', 34), TEAL if abs(s - z) < .003 else MUTED, 'mm')
    d.ellipse((xp - 34, y - 34, xp + 34, y + 34), fill=WHITE, outline=TEAL, width=8)
    pill(d, xp, y - 80, f'%{z * 100:.0f} zam', F('k', 40), TEAL, WHITE, 26, 70)
    b, n, dn, tes, tesyok = senaryo(z)
    vals = [('Brüt', tr(b) + ' ₺', INK), ('Net', tr(n) + ' ₺', TEAL), ('Nete artış', '+' + tr(dn) + ' ₺', INK)]
    for i, (a, v, c) in enumerate(vals):
        if L: box = (M + i * 570, 560, M + i * 570 + 530, 820)
        else: box = (M, 780 + i * 220, R, 980 + i * 220)
        big = i == 1
        d.rounded_rectangle(box, 28, fill=TEAL_S if big else CARD, outline=TEAL if big else LINE, width=4 if big else 3)
        T(d, (box[0] + 36, box[1] + 55), a, F('b', 36), MUTED, 'lm')
        T(d, (box[0] + 36, box[1] + (150 if L else 135)), v, F('k', 66 if L else 72), c, 'lm')
    stamp(d, (W - M - 230) if L else (CX - 115), 200 if L else 1460, 1.0)

def s_table(fr, t, dur):
    header(fr, 'Dört senaryo yan yana', 'Aylık, 2026 prim oranlarıyla')
    for i, z in enumerate((.15, .20, .25, .30)):
        b, n, dn, _, _ = senaryo(z)
        hl = z == .25
        if L: y, h = 380 + i * 115, 98
        else: y, h = 560 + i * 175, 150
        def rowf(d, y=y, h=h, b=b, n=n, dn=dn, z=z, hl=hl):
            d.rounded_rectangle((M, y, R, y + h), 22, fill=TEAL if hl else CARD, outline=None if hl else LINE, width=3)
            fg = WHITE if hl else INK
            if L:
                T(d, (M + 36, y + h // 2), f'%{int(z * 100)}', F('k', 48), fg if hl else TEAL, 'lm')
                T(d, (M + 260, y + h // 2), 'Brüt ' + tr(b, 0) + ' ₺', F('s', 38), fg if hl else MUTED, 'lm')
                T(d, (M + 1120, y + h // 2), 'Net ' + tr(n, 0) + ' ₺', F('k', 46), fg, 'rm')
                T(d, (R - 36, y + h // 2), '+' + tr(dn, 0) + ' ₺', F('b', 40), fg if hl else TEAL, 'rm')
            else:
                T(d, (M + 30, y + 48), f'%{int(z * 100)} zam · brüt {tr(b, 0)} ₺', F('s', 30), fg if hl else MUTED, 'lm')
                T(d, (M + 30, y + 108), tr(n, 0) + ' ₺ net', F('k', 50), fg, 'lm')
        fade(fr, t, .3 + i * .4, rowf)
    if L: fade(fr, t, 2.2, lambda d: T(d, (M, 870), 'Resmî rakam Aralık’ta açıklanınca sayfamız aynı gün güncellenir.', F('s', 36), MUTED))

def s_cost(fr, t, dur):
    header(fr, 'İşverene maliyeti', '%25 zam senaryosunda, aylık')
    b, n, dn, tes, tesyok = senaryo(.25)
    cards = [('5 puan SGK teşvikli', tes), ('Teşviksiz', tesyok)]
    for i, (a, v) in enumerate(cards):
        if L: box = (M + i * 860, 400, M + i * 860 + 800, 700)
        else: box = (M, 560 + i * 330, R, 860 + i * 330)
        fade(fr, t, .3 + i * .5, lambda d, box=box, a=a: (d.rounded_rectangle(box, 28, fill=CARD, outline=LINE, width=3), T(d, (box[0] + 40, box[1] + 70), a, F('b', 40), MUTED, 'lm')))
        roll(fr, t, .4 + i * .5, (box[0] + 40, box[1] + 180), tr(v) + ' ₺', F('k', 78 if L else 72), TEAL, 'lm')
    fade(fr, t, 1.8, lambda d: pill(d, CX, 800 if L else 1260, f'Çalışana net: {tr(n)} ₺', F('k', 44 if L else 38), TEAL_S, INK))

def s_cta(fr, t, dur):
    fr.d.rectangle((0, 0, W, H), fill=TEAL)
    lg = logo(120); fr.im.paste(lg, (CX - 60, 150 if L else 420), lg)
    roll(fr, t, .1, (CX, 360 if L else 640), 'Tüm senaryolar sitede', F('k', 76 if L else 62), WHITE, 'mm')
    def url(d):
        w2 = 520 if L else (R - M) // 2; y = 470 if L else 760
        d.rounded_rectangle((CX - w2, y, CX + w2, y + 110), 55, fill=WHITE)
        T(d, (CX, y + 55), 'hesapcantasi.com/asgari-ucret-2027' if L else 'hesapcantasi.com', F('k', 46 if L else 60), INK, 'mm')
    fade(fr, t, .8, url)
    fade(fr, t, 1.5, lambda d: T(d, (CX, 660 if L else 940), 'Resmî rakam açıklandığı gün güncellenir', F('s', 40 if L else 32), WHITE, 'mm'))
    if L: fade(fr, t, 2.2, lambda d: T(d, (CX, 760), 'Link açıklamada', F('s', 34), (200, 236, 240), 'mm'))

LONG = [(s_hook, 4.5), (s_base, 6.5), (s_slider, 9.0), (s_table, 6.5), (s_cost, 6.0), (s_cta, 6.0)]
SHORT = [(s_hook, 3.5), (s_slider, 8.0), (s_table, 5.0), (s_cta, 4.5)]
SCENES = LONG if L else SHORT

def draw(i, t):
    fn, dur = SCENES[i]; fr = Fr(); fn(fr, t, dur)
    if fn is not s_cta:
        yb = H - 12 if L else 232
        fr.d.rectangle((0, yb, int(W * min(1, t / dur)), yb + 10), fill=TEAL)
    a = min(1, t / .18, (dur - t) / .18)
    if a < 1: fr.im = Image.blend(Image.new('RGB', (W, H), TEAL) if fn is s_cta else BGIM, fr.im, max(0, a))
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
