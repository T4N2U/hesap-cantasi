"""Long (16:9) Tuş & Eşittir episode: 'Ocak 2027 emekli ve memur zammı' (publish 5 Jan 2027).
Same characters, props and text bubbles as the demo Short (render.py); figures from data.json (site engine).
Characters stand on the left, the explanation builds on the right. ÖRNEK watermark until all 6 months are in.
Ends with the 10 s end-screen closing scene (../endscreen.py). Usage: python3 render_long.py [stills]"""
import json, math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'mascot')); sys.path.insert(0, os.path.join(HERE, '..'))
import endscreen as ES
from tus_variants import keycap, face, F, GOLD, GOLD_D, GREEN_D, INK, WHITE
from PIL import Image, ImageDraw

D = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8'))
KESIN = D['kesin'] and not D['kalan']
W, H, FPS = 1920, 1080, 30
OUT = os.path.join(HERE, 'long'); os.makedirs(OUT, exist_ok=True)
BG = (246, 241, 230); MUTED = (120, 112, 100); GREEN_L = (32, 138, 104); RED = (214, 84, 64); CARD = (255, 252, 245); LINE = (226, 218, 200)

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def prog(t, s, d=.5): return ease((t - s) / d)
def tr(n, d=2): return f'{n:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def T(d, xy, s, f, fill=INK, a='la'): d.text(xy, s, font=f, fill=fill, anchor=a)
LOGO = Image.open(os.path.join(HERE, '..', 'logo.png')).convert('RGBA').resize((52, 52), Image.LANCZOS)
LOGO_L = Image.open(os.path.join(HERE, '..', 'logo.png')).convert('RGBA').resize((100, 100), Image.LANCZOS)
def blink_at(t): return 1.0 if (t % 2.6) < .12 else 0.0

def tus(d, cx, cy, s, t, talking=False, blink=0.0, mood=None):
    cy -= abs(math.sin(t * 6)) * 12 * s
    keycap(d, cx, cy, s, GOLD, GOLD_D, t)
    face(d, cx, cy - 18 * s, s, blink, 0, mood or ('open' if talking and int(t * 8) % 2 else 'smile'))
    for sx in (-1, 1): d.ellipse((cx + sx * 34 * s - 25 * s, cy - 43 * s, cx + sx * 34 * s + 25 * s, cy + 7 * s), outline=INK, width=int(5 * s))
    d.line((cx - 9 * s, cy - 18 * s, cx + 9 * s, cy - 18 * s), fill=INK, width=int(5 * s))
    x0, y0 = cx + 80 * s, cy + 30 * s
    d.rounded_rectangle((x0, y0, x0 + 70 * s, y0 + 70 * s), 10 * s, fill=WHITE, outline=INK, width=int(4 * s))
    d.rectangle((x0, y0, x0 + 70 * s, y0 + 20 * s), fill=RED); T(d, (x0 + 35 * s, y0 + 46 * s), 'OCA', F('k', 19 * s), INK, 'mm')

def esittir(d, cx, cy, s, t, talking=False, blink=0.0):
    cy -= abs(math.sin(t * 5 + 1)) * 7 * s
    keycap(d, cx, cy, s, GREEN_L, GREEN_D, t + .5, '=', WHITE)
    face(d, cx, cy - 18 * s, s, blink, 0, 'open' if talking and int(t * 8) % 2 else 'smile')

def bubble(fr, t, s0, text, x, y, w, tail_x, size=40):
    p = prog(t, s0, .25)
    if p <= 0: return
    d = fr.d; f = F('b', size); lines, cur = [], ''
    for wd in text.split():
        if d.textlength((cur + ' ' + wd).strip(), font=f) > w - 64: lines.append(cur); cur = wd
        else: cur = (cur + ' ' + wd).strip()
    lines.append(cur)
    h = 44 + len(lines) * (size + 12); yy = y - (1 - p) * 24
    d.rounded_rectangle((x, yy, x + w, yy + h), 30, fill=WHITE, outline=INK, width=4)
    ty = yy + h
    d.polygon([(tail_x - 20, ty - 2), (tail_x + 20, ty - 2), (tail_x, ty + 36)], fill=WHITE)
    d.line((tail_x - 20, ty, tail_x, ty + 36, tail_x + 20, ty), fill=INK, width=4)
    n = int(len(text) * min(1, (t - s0) / max(.6, len(text) * .035))); shown = 0
    for i, ln in enumerate(lines):
        T(d, (x + 32, yy + 24 + i * (size + 12)), ln[:max(0, n - shown)], f, INK); shown += len(ln) + 1

class Fr:
    def __init__(s):
        s.im = Image.new('RGB', (W, H), BG); s.d = ImageDraw.Draw(s.im, 'RGBA')
        s.im.paste(LOGO, (80, 60), LOGO); T(s.d, (148, 86), 'Hesap Çantası', F('b', 30), INK, 'lm')

TX, EX, CY = 240, 560, 860           # characters: bottom-left
PX0, PX1 = 820, 1820                 # right-hand panel for the explanation
def cast(fr, t, tt=False, et=False, es=True):
    tus(fr.d, TX, CY, 1.0, t, tt, blink_at(t))
    if es: esittir(fr.d, EX, CY, 1.0, t, et, blink_at(t + 1))
def panel_title(fr, t, s0, txt, sub=None):
    if prog(t, s0, .4) <= 0: return
    T(fr.d, (PX0, 170), txt, F('k', 60), INK)
    if sub: T(fr.d, (PX0, 250), sub, F('s', 34), MUTED)

# ---------------- scenes ----------------
def s_hook(fr, t, dur):
    x = TX + (1 - prog(t, 0, .6)) * -400
    tus(fr.d, x, CY, 1.2, t, 1.0 < t < 3.4, blink_at(t))
    bubble(fr, t, .8, f"{D['donem']}'de emekli ve memur zammı ne kadar olacak?", 80, 420, 720, 260, size=44)
    if prog(t, 1.6, .5) > 0:
        T(fr.d, (PX0 + 40, 380), 'Ocak 2027', F('k', 120), GREEN_D)
        T(fr.d, (PX0 + 40, 520), 'emekli & memur zammı', F('k', 76), INK)
        T(fr.d, (PX0 + 40, 630), 'SSK · Bağ-Kur · memur', F('s', 40), MUTED)

def s_rule(fr, t, dur):
    xe = EX + (1 - prog(t, 0, .6)) * 500
    tus(fr.d, TX, CY, 1.0, t, False, blink_at(t)); esittir(fr.d, xe, CY, 1.0, t, .6 < t < 3.0, blink_at(t + 1))
    bubble(fr, t, .6, 'SSK ve Bağ-Kur emeklisinin zammı = son 6 ayın enflasyonu.', 120, 420, 680, 560, size=40)
    panel_title(fr, t, 1.0, 'Temmuz–Aralık enflasyonu', 'TÜİK aylık TÜFE (%)')
    ay = [a for a, _ in D['aylar']] + [k.split(' (')[0] for k in D['kalan']]
    vals = [v for _, v in D['aylar']]; y = 820; bw, gap = 130, 30
    for i, a in enumerate(ay):
        x = PX0 + i * (bw + gap); p = prog(t, 1.8 + i * .3, .5)
        if p <= 0: continue
        if i < len(vals):
            h = 110 * vals[i] * p; fr.d.rounded_rectangle((x, y - h, x + bw, y), 16, fill=GOLD)
            T(fr.d, (x + bw / 2, y - h - 36), '%' + tr(vals[i]), F('k', 36), INK, 'mm')
        else:
            fr.d.rounded_rectangle((x, y - 160, x + bw, y), 16, outline=MUTED, width=4); T(fr.d, (x + bw / 2, y - 80), '?', F('k', 70), MUTED, 'mm')
        T(fr.d, (x + bw / 2, y + 36), a.split()[0], F('s', 32), MUTED, 'mm')

def s_total(fr, t, dur):
    cast(fr, t, 2.6 < t < 3.8, .2 < t < 2.0)
    p = prog(t, .2, 1.2)
    panel_title(fr, t, 0, f"{len(D['aylar'])} ayda toplam")
    T(fr.d, (PX0, 290), '%' + tr(D['enf'] * p), F('k', 170), INK)
    bubble(fr, t, 2.4, 'Ya kalan 2 ay?', 80, 470, 420, 240, size=44)
    if prog(t, 3.6, .4) > 0:
        for i, k in enumerate(D['kalan']):
            ay, tarih = k.rstrip(')').split(' (')
            fr.d.rounded_rectangle((PX0, 560 + i * 110, PX1, 650 + i * 110), 24, fill=CARD, outline=LINE, width=3)
            T(fr.d, (PX0 + 30, 605 + i * 110), f'{ay} enflasyonu', F('b', 38), INK, 'lm')
            T(fr.d, (PX1 - 30, 605 + i * 110), f'açıklanma: {tarih}', F('s', 34), MUTED, 'rm')

def s_memur(fr, t, dur):
    cast(fr, t, False, .3 < t < 3.0)
    bubble(fr, t, .3, f"Memura: toplu sözleşme %{D['tsYeni']} + enflasyon farkı.", 100, 440, 700, 560, size=40)
    panel_title(fr, t, .8, 'Memur zammı nasıl bulunur?')
    steps = [(f"1. Önceki dönemin zammı: %{D['tsOnceki']}", None),
             (f"2. Enflasyon farkı = (1 + 6 aylık enflasyon) ÷ (1 + %{D['tsOnceki']}) − 1", None),
             (f"3. Zam = (1 + %{D['tsYeni']}) × (1 + fark) − 1", None)]
    for i, (s, _) in enumerate(steps):
        if prog(t, 1.4 + i * .8, .4) > 0:
            fr.d.rounded_rectangle((PX0, 300 + i * 120, PX1, 390 + i * 120), 22, fill=CARD, outline=LINE, width=3)
            T(fr.d, (PX0 + 30, 345 + i * 120), s, F('b', 34), INK, 'lm')
    p = prog(t, 4.2, .8)
    if p > 0:
        T(fr.d, (PX0, 720), f"{len(D['aylar'])} aylık veriyle:  fark %{tr(D['fark'] * p)}  →  zam ≈ %{tr(D['memurOran'] * p)}", F('k', 44), GREEN_D)
        T(fr.d, (PX0, 790), 'Kesin değil: Kasım ve Aralık enflasyonuyla netleşir', F('b', 32), RED)

def s_example(fr, t, dur):
    cast(fr, t, .3 < t < 2.2, 2.6 < t < 4.0)
    bubble(fr, t, .3, 'Benim maaşım ne olur?', 80, 470, 460, 240, size=44)
    panel_title(fr, t, .6, 'Örnek: bugünkü verilerle', f"{len(D['aylar'])} aylık enflasyon %{tr(D['enf'])} · kesin değil")
    rows = [('Emekli', D['ornekEmekli']), ('Memur', D['ornekMemur'])]
    for i, (lab, r) in enumerate(rows):
        p = prog(t, 1.4 + i * 1.0, .9)
        if p <= 0: continue
        y = 340 + i * 220
        fr.d.rounded_rectangle((PX0, y, PX1, y + 180), 28, fill=CARD, outline=LINE, width=3)
        T(fr.d, (PX0 + 36, y + 50), lab, F('s', 36), MUTED, 'lm')
        T(fr.d, (PX0 + 36, y + 120), f"{tr(r['maas'], 0)} ₺  →  {tr(r['maas'] + (r['yeni'] - r['maas']) * p)} ₺", F('k', 56), INK, 'lm')
        if p >= 1: T(fr.d, (PX1 - 36, y + 120), f"+{tr(r['artis'])} ₺", F('k', 44), GREEN_D, 'rm')

def s_cta(fr, t, dur):
    fr.d.rectangle((0, 0, W, H), fill=INK)
    fr.im.paste(LOGO_L, (W // 2 - 50, 60), LOGO_L)
    if prog(t, .1, .4) > 0: T(fr.d, (W // 2, 240), 'Kendi maaşınla hesapla', F('k', 72), WHITE, 'mm')
    if prog(t, .7, .4) > 0:
        fr.d.rounded_rectangle((W // 2 - 600, 305, W // 2 + 600, 405), 50, fill=GOLD)
        T(fr.d, (W // 2, 355), 'hesapcantasi.com/emekli-memur-zammi-hesaplama', F('k', 36), INK, 'mm')
    if prog(t, 1.4, .4) > 0: T(fr.d, (W // 2, 465), 'Rakamlar açıklandığı gün güncellenir', F('s', 36), (200, 200, 200), 'mm')
    if prog(t, 2.0, .4) > 0: ES.labels(fr.d, F('b', 34), WHITE)
    # the characters wave from the empty middle, between the two end-screen zones
    tus(fr.d, 900, 760, .9, t, .3 < t < 1.6, blink_at(t), 'open' if t > 1.6 else None)
    esittir(fr.d, 1180, 770, .8, t, False, blink_at(t + 1))

SCENES = [(s_hook, 4.5), (s_rule, 7.0), (s_total, 6.0), (s_memur, 7.0), (s_example, 6.0), (s_cta, ES.CTA_SEC)]

def watermark(im):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    T(ld, (W // 2, H // 2), 'ÖRNEK', F('k', 300), (255, 80, 60, 50), 'mm')
    lay = lay.rotate(22, center=(W // 2, H // 2)); im.paste(lay, (0, 0), lay)

def draw(i, t):
    fn, dur = SCENES[i]; fr = Fr(); fn(fr, t, dur)
    if not KESIN: watermark(fr.im)
    a = min(1, t / .15, (dur - t) / .15)
    if a < 1: fr.im = Image.blend(Image.new('RGB', (W, H), INK if fn is s_cta else BG), fr.im, max(0, a))
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
    if sys.argv[1:2] == ['stills']:
        for i, (fn, dur) in enumerate(SCENES): draw(i, dur - .3).save(f'{OUT}/still{i}.jpg', quality=85)
        ES.guides(draw(len(SCENES) - 1, 3.0)).save(f'{OUT}/still-endscreen-guides.jpg', quality=85)
    else:
        for i in range(len(SCENES)): render(i)
        with open(f'{OUT}/list.txt', 'w') as f:
            for i in range(len(SCENES)): f.write(f"file 's{i:02d}.mp4'\n")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/list.txt', '-c', 'copy', f'{OUT}/silent.mp4'], check=True)
        print('done', sum(d for _, d in SCENES)); print('end screen from', ES.start_time(SCENES), 's')
