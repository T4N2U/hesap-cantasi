"""'Vergi dilimleri: maaşın hangi ayda dilim atlar?' — data-driven template (publish 2 Jan 2027, Short 4 Jan).
Every figure comes from data.mjs (the site's engine). Until engine.js holds the official 2027 tarife, the
render is a preview: it shows the 2026 tarife, the GVK 123 legal range for 2027 and an ÖRNEK watermark.
Re-render after the tebliğ: `node data.mjs > data.json && python3 render.py long && python3 render.py short`.
Visual variant: dark slate ground, amber (vergi) accent, a tax staircase, bars that grow upward. Music: rhodes-groove.
Usage: python3 render.py long|short [stills]"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import endscreen as ES
from PIL import Image, ImageDraw, ImageFont

MODE = sys.argv[1] if len(sys.argv) > 1 else 'long'
L = MODE == 'long'
W, H = (1920, 1080) if L else (1080, 1920)
FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, MODE)
os.makedirs(OUT, exist_ok=True)
D = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8'))
OFFICIAL, YEAR = D['official'], D['year']
FD = '/usr/share/fonts/opentype/inter/'
_fc = {}
def F(w, s):
    k = (w, s)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FD + {'b': 'InterDisplay-Bold.otf', 'k': 'InterDisplay-Black.otf', 's': 'InterDisplay-SemiBold.otf'}[w], s)
    return _fc[k]

BG = (21, 27, 38); CARD = (32, 40, 56); LINE = (52, 62, 82); INK = (238, 241, 246); MUTED = (150, 160, 180)
AMBER = (240, 168, 48); RATE = {0.15: (86, 150, 120), 0.2: (196, 170, 70), 0.27: (232, 134, 52), 0.35: (214, 84, 64), 0.4: (170, 60, 90)}
WHITE = (255, 255, 255)
AY = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara']

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def prog(t, s, d=0.5): return ease((t - s) / d)
def tr(n, d=0): return f'{n:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def pct(r): return '%' + (str(int(r * 100)) if (r * 100) % 1 == 0 else tr(r * 100, 1))
def T(d, xy, s, f, fill=INK, a='la'): d.text(xy, s, font=f, fill=fill, anchor=a)

_LOGO = {}
def logo(size):
    """The channel logo (briefcase with keypad), from tools/video/logo.png."""
    if size not in _LOGO:
        _LOGO[size] = Image.open(os.path.join(HERE, '..', 'logo.png')).convert('RGBA').resize((size, size), Image.LANCZOS)
    return _LOGO[size]

def brand(fr, x, y):
    lg = logo(52); fr.im.paste(lg, (x, y), lg)
    T(fr.d, (x + 68, y + 26), 'Hesap Çantası', F('b', 30), INK, 'lm')

class Fr:
    def __init__(s): s.im = Image.new('RGB', (W, H), BG); s.d = ImageDraw.Draw(s.im)

def grow(fr, t, s, box, col, dur=0.6, r=12):
    """Bars grow upward from their base (this video's transition)."""
    p = prog(t, s, dur)
    if p <= 0: return
    x0, y0, x1, y1 = box
    fr.d.rounded_rectangle((x0, y1 - (y1 - y0) * p, x1, y1), r, fill=col)

def fade(fr, t, s, fn, dur=0.4):
    p = prog(t, s, dur)
    if p <= 0: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay))
    if p < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * p)))
    fr.im.paste(lay, (0, 0), lay)

M = 120 if L else 80
R = W - M if L else 920
TOP = 70 if L else 250
CX = W // 2 if L else (M + R) // 2

def header(fr, title, sub=None):
    brand(fr, M, TOP)
    ty = 200 if L else 370
    T(fr.d, (M, ty), title, F('k', 70 if L else 54), INK)
    if sub: T(fr.d, (M, ty + (92 if L else 76)), sub, F('s', 36 if L else 30), MUTED)

def limits():
    out, prev = [], 0
    for x in D['dilimler']:
        out.append((prev, x['ust'], x['oran'])); prev = x['ust'] or prev
    return out

# ---------------- scenes ----------------
def s_hook(fr, t, dur):
    brand(fr, M, TOP)
    steps = limits()
    if L:
        fade(fr, t, .1, lambda d: (T(d, (M, 300), f'{YEAR} vergi dilimleri', F('k', 104), INK), T(d, (M, 430), 'Maaşın hangi ayda', F('k', 88), AMBER), T(d, (M, 530), 'dilim atlar?', F('k', 88), AMBER)))
        for i, (_, _, r) in enumerate(steps):
            x = 1180 + i * 130; h = 120 + i * 110
            grow(fr, t, .5 + i * .2, (x, 880 - h, x + 110, 880), RATE[r])
            if prog(t, .7 + i * .2, .3) > 0: T(fr.d, (x + 55, 880 - h - 30), pct(r), F('k', 36), INK, 'mm')
    else:
        fade(fr, t, .1, lambda d: (T(d, (CX, 470), f'{YEAR}', F('k', 150), AMBER, 'mm'), T(d, (CX, 600), 'vergi dilimleri', F('k', 86), INK, 'mm')))
        for i, (_, _, r) in enumerate(steps):
            x = M + 20 + i * 165; h = 90 + i * 85
            grow(fr, t, .4 + i * .18, (x, 1180 - h, x + 140, 1180), RATE[r])
            if prog(t, .6 + i * .18, .3) > 0: T(fr.d, (x + 70, 1180 - h - 30), pct(r), F('k', 34), INK, 'mm')
        fade(fr, t, 1.6, lambda d: T(d, (CX, 1300), 'Maaşın hangi ayda dilim atlar?', F('b', 40), INK, 'mm'))

def s_stairs(fr, t, dur):
    sub = 'Ücret gelirleri, kümülatif matrah' if OFFICIAL else f'Örnek: {YEAR} tarifesi · {D["nextYear"]} tutarları tebliğle açıklanacak'
    header(fr, f'{YEAR} ücret tarifesi', sub)
    steps = limits()
    for i, (lo, hi, r) in enumerate(steps):
        if L: y = 380 + i * 105; x0, x1 = M, R
        else: y = 520 + i * 160; x0, x1 = M, R
        h = 88 if L else 140
        def row(d, y=y, lo=lo, hi=hi, r=r):
            d.rounded_rectangle((x0, y, x1, y + h), 18, fill=CARD)
            d.rounded_rectangle((x0, y, x0 + (170 if L else 150), y + h), 18, fill=RATE[r])
            T(d, (x0 + (85 if L else 75), y + h // 2), pct(r), F('k', 46 if L else 44), WHITE, 'mm')
            label = f'{tr(hi)} ₺’ye kadar' if hi else f'{tr(lo)} ₺ üzeri'
            if L: T(d, (x0 + 210, y + h // 2), label, F('k', 46), INK, 'lm')
            else: T(d, (x0 + 180, y + h // 2), label, F('k', 40), INK, 'lm')
        fade(fr, t, .4 + i * .45, row)

def s_months(fr, t, dur):
    header(fr, 'Hangi ayda dilim atlar?', f'{YEAR} tarifesiyle, aylık brüt maaşa göre')
    ex = D['examples']
    cw = 108 if L else 64; gap = 8 if L else 5
    for i, e in enumerate(ex):
        y = (390 if L else 560) + i * (165 if L else 250)
        fade(fr, t, .3 + i * .3, lambda d, y=y, e=e: T(d, (M, y), f'Brüt {tr(e["brut"])} ₺', F('k', 40 if L else 38), INK))
        x0 = M + (360 if L else 0); yy = y + (0 if L else 60)
        for m in range(12):
            r = e['dilim'][m]
            s0 = .6 + i * .4 + m * .07
            x = x0 + m * (cw + gap)
            grow(fr, t, s0, (x, yy, x + cw, yy + (90 if L else 110)), RATE[r], .35, 10)
            if prog(t, s0 + .2, .2) > 0:
                T(fr.d, (x + cw // 2, yy + (30 if L else 35)), AY[m] if L else AY[m][:1], F('s', 24 if L else 22), WHITE, 'mm')
                T(fr.d, (x + cw // 2, yy + (66 if L else 80)), pct(r), F('k', 28 if L else 22), WHITE, 'mm')
    if L: fade(fr, t, 3.6, lambda d: T(d, (M, 900), 'Vergi yılbaşından biriken matraha göre kesilir; her Ocak sıfırlanır.', F('s', 36), MUTED))

def s_drop(fr, t, dur):
    e = D['examples'][1]
    header(fr, 'Net maaş yıl içinde düşer', f'Brüt {tr(e["brut"])} ₺ · {YEAR}')
    vals = [('Ocak net', e['ocakNet'], (86, 150, 120)), ('Aralık net', e['aralikNet'], AMBER)]
    mx = max(v for _, v, _ in vals)
    for i, (lab, v, col) in enumerate(vals):
        if L: x = 600 + i * 420; base, top = 840, 400; bw = 300
        else: x = 170 + i * 380; base, top = 1300, 640; bw = 280
        hgt = (base - top) * v / mx
        grow(fr, t, .4 + i * .5, (x, base - hgt, x + bw, base), col, .7, 18)
        if prog(t, .9 + i * .5, .3) > 0:
            T(fr.d, (x + bw // 2, base - hgt - 40), tr(v) + ' ₺', F('k', 50 if L else 44), INK, 'mm')
            T(fr.d, (x + bw // 2, base + 40), lab, F('b', 36), MUTED, 'mm')
    fade(fr, t, 2.2, lambda d: T(d, (CX, 975 if L else 1420), f'Fark: {tr(e["ocakNet"] - e["aralikNet"])} ₺', F('k', 52 if L else 46), AMBER, 'mm'))

def s_range(fr, t, dur):
    header(fr, f'{D["nextYear"]}’de dilimler ne olacak?', f'Yeniden değerleme oranı %{tr(D["yd"], 2)}')
    lo, hi = D['aralik'][0]
    fade(fr, t, .3, lambda d: T(d, (M, 420 if L else 580), 'İlk dilim sınırı, kanuna göre bu aralıkta olacak:', F('s', 40 if L else 34), MUTED))
    fade(fr, t, .8, lambda d: T(d, (M, 520 if L else 700), f'{tr(lo)} – {tr(hi)} ₺', F('k', 96 if L else 72), AMBER))
    fade(fr, t, 1.6, lambda d: T(d, (M, 680 if L else 860), 'Kesin tutarlar Aralık sonunda tebliğle açıklanır.', F('b', 40 if L else 34), INK))

def s_cta(fr, t, dur):
    fr.d.rectangle((0, 0, W, H), fill=AMBER)
    if L:  # long: everything above SAFE_BOTTOM, end-screen zones left clear (see ../endscreen.py)
        lg = logo(100); fr.im.paste(lg, (CX - 50, 70), lg)
        fade(fr, t, .1, lambda d: T(d, (CX, 250), 'Kendi bordronu hesapla', F('k', 76), BG, 'mm'))
        def url(d):
            d.rounded_rectangle((CX - 480, 315, CX + 480, 415), 50, fill=BG)
            T(d, (CX, 365), 'hesapcantasi.com/maas-hesaplama', F('k', 46), INK, 'mm')
        fade(fr, t, .7, url)
        fade(fr, t, 1.4, lambda d: T(d, (CX, 470), '12 aylık bordro · hangi ay hangi dilim', F('s', 38), BG, 'mm'))
        fade(fr, t, 2.0, lambda d: ES.labels(d, F('b', 34), BG))
        return
    lg = logo(120); fr.im.paste(lg, (CX - 60, 420), lg)
    fade(fr, t, .1, lambda d: T(d, (CX, 640), 'Kendi bordronu hesapla', F('k', 62), BG, 'mm'))
    def url(d):
        w2 = (R - M) // 2; y = 760
        d.rounded_rectangle((CX - w2, y, CX + w2, y + 110), 55, fill=BG)
        T(d, (CX, y + 55), 'hesapcantasi.com', F('k', 60), INK, 'mm')
    fade(fr, t, .7, url)
    fade(fr, t, 1.4, lambda d: T(d, (CX, 940), '12 aylık bordro · hangi ay hangi dilim', F('s', 34), BG, 'mm'))

LONG = [(s_hook, 4.5), (s_stairs, 6.5), (s_months, 8.5), (s_drop, 6.5)] + ([] if OFFICIAL else [(s_range, 5.5)]) + [(s_cta, ES.CTA_SEC)]
SHORT = [(s_hook, 3.5), (s_months, 8.0), (s_cta, 4.5)]
SCENES = LONG if L else SHORT

def watermark(im):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    T(ld, (W // 2, H // 2), 'ÖRNEK', F('k', 300 if L else 240), (255, 80, 60, 60), 'mm')
    lay = lay.rotate(22, center=(W // 2, H // 2)); im.paste(lay, (0, 0), lay)

def draw(i, t):
    fn, dur = SCENES[i]; fr = Fr(); fn(fr, t, dur)
    if fn is not s_cta:
        yb = H - 12 if L else 232
        fr.d.rectangle((0, yb, int(W * min(1, t / dur)), yb + 10), fill=AMBER)
    if not OFFICIAL: watermark(fr.im)
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
        if L: ES.guides(draw(len(SCENES) - 1, 3.0)).save(f'{OUT}/still-endscreen-guides.jpg', quality=85)
    else:
        for i in range(len(SCENES)): render(i)
        with open(f'{OUT}/list.txt', 'w') as f:
            for i in range(len(SCENES)): f.write(f"file 's{i:02d}.mp4'\n")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/list.txt', '-c', 'copy', f'{OUT}/silent.mp4'], check=True)
        print('done', sum(d for _, d in SCENES))
        if L: print('end screen from', ES.start_time(SCENES), 's')
