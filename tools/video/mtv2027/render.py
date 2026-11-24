"""'MTV 2027 ne kadar? 1. taksitte son gün Ocak sonu' — data-driven template (publish 19 Jan 2027, Short 21 Jan).
Every figure comes from data.mjs (the site's engine). Until engine.js holds the official 2027 MTV tarife, the render is a
preview: 2026 amounts, the legal range of the 2027 increase (197 s. Kanun md. 10) and an ÖRNEK watermark.
Re-render after the Cumhurbaşkanı kararı / tebliğ: `node data.mjs > data.json && python3 render.py long && python3 render.py short`.
Visual variant: asphalt ground, number-plate cards (blue TR strip), road-yellow accent, cards drive in from the right,
moving lane dashes. Music: acoustic-pluck. Long video ends with the 10 s end-screen scene (../endscreen.py).
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
OFFICIAL, YIL, NX = D['official'], D['yil'], D['next']
SHOW = YIL if OFFICIAL else NX['yil']     # the year in the title
FD = '/usr/share/fonts/opentype/inter/'
_fc = {}
def F(w, s):
    k = (w, s)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FD + {'b': 'InterDisplay-Bold.otf', 'k': 'InterDisplay-Black.otf', 's': 'InterDisplay-SemiBold.otf'}[w], s)
    return _fc[k]

BG = (34, 37, 42); ROAD = (46, 50, 56); INK = (240, 242, 245); MUTED = (156, 163, 175)
YEL = (250, 204, 21); PLATE = (248, 248, 246); PINK = (20, 24, 30); BLUE = (0, 61, 165); WHITE = (255, 255, 255)
BAR = [(250, 204, 21), (96, 165, 250), (163, 230, 53)]

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def prog(t, s, d=0.5): return ease((t - s) / d)
def tr(n, d=0): return f'{n:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def tl(n): return tr(n, 0 if float(n).is_integer() else 2) + ' ₺'
from decimal import Decimal, ROUND_HALF_UP
def r2(x): return float(Decimal(str(x)).quantize(Decimal('0.01'), ROUND_HALF_UP))
def pc(x): return '%' + tr(r2(x), 2).rstrip('0').rstrip(',')
def T(d, xy, s, f, fill=INK, a='la'): d.text(xy, s, font=f, fill=fill, anchor=a)

_LOGO = {}
def logo(size):
    if size not in _LOGO:
        _LOGO[size] = Image.open(os.path.join(HERE, '..', 'logo.png')).convert('RGBA').resize((size, size), Image.LANCZOS)
    return _LOGO[size]

def brand(fr, x, y):
    lg = logo(52); fr.im.paste(lg, (x, y), lg)
    T(fr.d, (x + 68, y + 26), 'Hesap Çantası', F('b', 30), INK, 'lm')

class Fr:
    def __init__(s): s.im = Image.new('RGB', (W, H), BG); s.d = ImageDraw.Draw(s.im)

def lanes(fr, t, y):
    """Moving lane dashes along the bottom: the road under every scene."""
    fr.d.rectangle((0, y - 30, W, y + 30), fill=ROAD)
    off = int(t * 260) % 160
    for x in range(-160 + off, W, 160): fr.d.rectangle((x, y - 5, x + 80, y + 5), fill=YEL)

def drive(fr, t, s, fn, dur=0.55):
    """Content drives in from the right (this video's transition)."""
    p = prog(t, s, dur)
    if p <= 0: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay))
    if p < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * p)))
    fr.im.paste(lay, (int((1 - p) * 260), 0), lay)

def fade(fr, t, s, fn, dur=0.4):
    p = prog(t, s, dur)
    if p <= 0: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay))
    if p < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * p)))
    fr.im.paste(lay, (0, 0), lay)

def plate(d, x, y, w, h, text, f):
    """A Turkish number plate: white card, blue TR strip on the left."""
    d.rounded_rectangle((x, y, x + w, y + h), 14, fill=PLATE, outline=PINK, width=4)
    sw = int(h * 0.42)
    d.rounded_rectangle((x + 4, y + 4, x + 4 + sw, y + h - 4), 10, fill=BLUE)
    T(d, (x + 4 + sw / 2, y + h - 22), 'TR', F('b', int(h * 0.22)), WHITE, 'mm')
    T(d, (x + sw + (w - sw) / 2, y + h / 2), text, f, PINK, 'mm')

M = 120 if L else 80
R = W - M
TOP = 70 if L else 250
CX = W // 2
ROADY = H - 70 if L else H - 330

def header(fr, title, sub=None):
    brand(fr, M, TOP)
    ty = 190 if L else 370
    T(fr.d, (M, ty), title, F('k', 68 if L else 56), INK)
    if sub: T(fr.d, (M, ty + (88 if L else 76)), sub, F('s', 36 if L else 32), MUTED)

# ---------------- scenes ----------------
def s_hook(fr, t, dur):
    brand(fr, M, TOP); lanes(fr, t, ROADY)
    if L:
        fade(fr, t, .1, lambda d: (T(d, (M, 330), f'MTV {SHOW}', F('k', 150), YEL), T(d, (M, 500), 'ne kadar ödeyeceğim?', F('k', 84), INK)))
        fade(fr, t, 1.4, lambda d: T(d, (M, 630), '1. taksitte son gün: Ocak sonu', F('s', 46), MUTED))
        drive(fr, t, .6, lambda d: plate(d, 1180, 640, 600, 150, f'MTV {SHOW}', F('k', 72)))
    else:
        fade(fr, t, .1, lambda d: (T(d, (CX, 600), f'MTV {SHOW}', F('k', 150), YEL, 'mm'), T(d, (CX, 740), 'ne kadar', F('k', 96), INK, 'mm'), T(d, (CX, 850), 'ödeyeceğim?', F('k', 96), INK, 'mm')))
        drive(fr, t, .6, lambda d: plate(d, M + 40, 1000, R - M - 80, 150, f'MTV {SHOW}', F('k', 72)))
        fade(fr, t, 1.3, lambda d: T(d, (CX, 1260), '1. taksit: Ocak sonu', F('s', 46), MUTED, 'mm'))

def s_how(fr, t, dur):
    header(fr, 'MTV neye göre hesaplanır?', 'Otomobil, (I) sayılı tarife'); lanes(fr, t, ROADY)
    items = [('Motor hacmi', 'cm³ dilimi'), ('Aracın yaşı', 'model yılından'), ('Taşıt değeri', '2018 ve sonrası tescilde')]
    for i, (a, b) in enumerate(items):
        if L: x, y, w, h = M + i * 570, 420, 520, 300
        else: x, y, w, h = M, 560 + i * 300, R - M, 250
        def card(d, x=x, y=y, w=w, h=h, a=a, b=b, i=i):
            d.rounded_rectangle((x, y, x + w, y + h), 28, fill=ROAD, outline=YEL if i == 2 else None, width=4)
            d.ellipse((x + 36, y + 40, x + 116, y + 120), fill=YEL); T(d, (x + 76, y + 80), str(i + 1), F('k', 46), PINK, 'mm')
            T(d, (x + 36, y + (190 if L else 160)), a, F('k', 54 if L else 50), INK, 'lm')
            T(d, (x + 36, y + (250 if L else 212)), b, F('s', 34 if L else 32), MUTED, 'lm')
        drive(fr, t, .4 + i * .5, card)
    fade(fr, t, 2.6, lambda d: T(d, (CX, 820 if L else 1500), 'Yıllık tutar iki eşit taksitte ödenir', F('b', 42), YEL, 'mm'))

def s_cars(fr, t, dur):
    header(fr, f'{YIL} MTV: 3 örnek', 'Yıllık tutar ve taksit'); lanes(fr, t, ROADY)
    cars = D['cars']; mx = max(c['yillik'] for c in cars)
    for i, c in enumerate(cars):
        if L: y, x0, bx0, bx1 = 390 + i * 190, M, M + 620, R - 330
        else: y, x0, bx0, bx1 = 560 + i * 330, M, M, R - 40
        def row(d, c=c, y=y, i=i):
            if L:
                plate(d, x0, y, 560, 120, c['ad'], F('k', 40))
                T(d, (x0, y + 150), c['detay'], F('s', 28), MUTED, 'lm')
            else:
                plate(d, x0, y, R - M, 110, c['ad'], F('k', 44))
                T(d, (x0, y + 140), c['detay'], F('s', 30), MUTED, 'lm')
        drive(fr, t, .3 + i * .6, row)
        p = prog(t, .8 + i * .6, .7)
        if p > 0:
            by = y + 30 if L else y + 175
            bw = (bx1 - bx0) * c['yillik'] / mx * p
            fr.d.rounded_rectangle((bx0, by, bx0 + max(bw, 12), by + 60), 12, fill=BAR[i])
            if L:
                T(fr.d, (bx0 + bw + 24, by + 18), tl(round(c['yillik'] * p)), F('k', 46), INK, 'lm')
                if p >= 1: T(fr.d, (bx0 + bw + 24, by + 66), f"taksit {tl(c['taksit'])}", F('s', 30), MUTED, 'lm')
            else:
                T(fr.d, (bx0 + 20, by + 30), tl(round(c['yillik'] * p)), F('k', 40), PINK, 'lm')
                if p >= 1: T(fr.d, (bx0, by + 100), f"2 taksit × {tl(c['taksit'])}", F('s', 30), MUTED, 'lm')

def s_next(fr, t, dur):
    lanes(fr, t, ROADY)
    if OFFICIAL:
        header(fr, f'{YIL} MTV %{tr(D["artis"], 2)} arttı', 'Cumhurbaşkanı kararıyla')
        return
    header(fr, f'{NX["yil"]} artışı henüz belli değil', 'Kanun sadece aralığı belirliyor')
    lo, hi, rv = NX['alt'], NX['ust'], NX['oran']
    x0, x1 = (M, R) if L else (M, R)
    y = 560 if L else 820
    sc = lambda v: x0 + (x1 - x0) * v / 45
    fr.d.rounded_rectangle((x0, y, x1, y + 40), 20, fill=ROAD)
    p = prog(t, .4, .9)
    if p > 0:
        a, b = sc(lo), sc(lo + (hi - lo) * p)
        fr.d.rounded_rectangle((a, y, b, y + 40), 20, fill=YEL)
    for v, lab, s in ((lo, pc(lo), 1.2), (hi, pc(hi), 1.4)):
        fade(fr, t, s, lambda d, v=v, lab=lab: (d.rectangle((sc(v) - 3, y - 30, sc(v) + 3, y + 70), fill=INK), T(d, (sc(v), y - 50), lab, F('k', 44 if L else 38), INK, 'ms')))
    fade(fr, t, 2.0, lambda d: (d.polygon([(sc(rv), y + 50), (sc(rv) - 18, y + 82), (sc(rv) + 18, y + 82)], fill=WHITE),
                                T(d, (sc(rv), y + 130), f'{pc(rv)} yeniden değerleme', F('b', 38 if L else 32), WHITE, 'mm')))
    if L:
        fade(fr, t, 3.0, lambda d: T(d, (M, 820), f"Cumhurbaşkanı bu oranın %20'si ile %150'si arasında karar verir.  {YIL}'da {pc(D['artis'])} uygulandı.", F('s', 34), MUTED))
    else:
        fade(fr, t, 3.0, lambda d: (T(d, (CX, 1080), "Cumhurbaşkanı oranın %20'si ile", F('s', 36), MUTED, 'mm'), T(d, (CX, 1130), "%150'si arasında karar verir.", F('s', 36), MUTED, 'mm'),
                                    T(d, (CX, 1220), f"{YIL}'da {pc(D['artis'])} uygulandı.", F('b', 40), INK, 'mm')))

def s_dates(fr, t, dur):
    header(fr, 'Ne zaman ödenir?'); lanes(fr, t, ROADY)
    for i, (a, b) in enumerate((('1. taksit', 'Ocak sonuna kadar'), ('2. taksit', 'Temmuz sonuna kadar'))):
        if L: x, y, w, h = M + i * 860, 400, 800, 300
        else: x, y, w, h = M, 600 + i * 360, R - M, 300
        def card(d, x=x, y=y, w=w, h=h, a=a, b=b, i=i):
            d.rounded_rectangle((x, y, x + w, y + h), 28, fill=YEL if i == 0 else ROAD)
            T(d, (x + 50, y + 90), a, F('s', 44), PINK if i == 0 else MUTED, 'lm')
            T(d, (x + 50, y + 190), b, F('k', 64 if L else 60), PINK if i == 0 else INK, 'lm')
        drive(fr, t, .3 + i * .6, card)

def s_cta(fr, t, dur):
    fr.d.rectangle((0, 0, W, H), fill=YEL)
    if L:  # everything above SAFE_BOTTOM; end-screen zones stay clear (../endscreen.py)
        lg = logo(100); fr.im.paste(lg, (CX - 50, 70), lg)
        fade(fr, t, .1, lambda d: T(d, (CX, 250), 'Kendi aracının MTV’sini hesapla', F('k', 72), PINK, 'mm'))
        def url(d):
            d.rounded_rectangle((CX - 460, 315, CX + 460, 415), 50, fill=PINK)
            T(d, (CX, 365), 'hesapcantasi.com/mtv-hesaplama', F('k', 46), WHITE, 'mm')
        fade(fr, t, .7, url)
        fade(fr, t, 1.4, lambda d: T(d, (CX, 470), 'Motor hacmi · model yılı · taşıt değeri', F('s', 38), PINK, 'mm'))
        fade(fr, t, 2.0, lambda d: ES.labels(d, F('b', 34), PINK))
        return
    lg = logo(120); fr.im.paste(lg, (CX - 60, 420), lg)
    fade(fr, t, .1, lambda d: (T(d, (CX, 640), 'Kendi aracının', F('k', 66), PINK, 'mm'), T(d, (CX, 720), 'MTV’sini hesapla', F('k', 66), PINK, 'mm')))
    def url(d):
        d.rounded_rectangle((M, 820, R, 930), 55, fill=PINK); T(d, (CX, 875), 'hesapcantasi.com', F('k', 60), WHITE, 'mm')
    fade(fr, t, .7, url)
    fade(fr, t, 1.4, lambda d: T(d, (CX, 1010), 'Motor hacmi · model yılı · taşıt değeri', F('s', 34), PINK, 'mm'))

LONG = [(s_hook, 4.5), (s_how, 7.0), (s_cars, 9.0), (s_next, 7.5 if not OFFICIAL else 4.0), (s_dates, 5.5), (s_cta, ES.CTA_SEC)]
SHORT = [(s_hook, 3.5), (s_cars, 8.0), (s_next, 6.5 if not OFFICIAL else 3.5), (s_cta, 4.5)]
SCENES = LONG if L else SHORT

def watermark(im):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    T(ld, (W // 2, H // 2), 'ÖRNEK', F('k', 300 if L else 240), (255, 80, 60, 60), 'mm')
    lay = lay.rotate(22, center=(W // 2, H // 2)); im.paste(lay, (0, 0), lay)

def draw(i, t):
    fn, dur = SCENES[i]; fr = Fr(); fn(fr, t, dur)
    if not OFFICIAL: watermark(fr.im)
    a = min(1, t / .18, (dur - t) / .18)
    if a < 1: fr.im = Image.blend(Image.new('RGB', (W, H), YEL if fn is s_cta else BG), fr.im, max(0, a))
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
