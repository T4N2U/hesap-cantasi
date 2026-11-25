"""Tuş & Eşittir Short: 'Ocak'ta emekli ve memur zammı ne kadar?' (first mascot episode, preview for the owner).
Characters: Tuş (C1, gold key; this episode's props: reading glasses + 'OCA' calendar) and Eşittir (green '=' key).
Speech in text bubbles (works muted). Figures from data.mjs (site engine). ÖRNEK watermark until all 6 months are in.
Usage: python3 render.py [stills]"""
import json, math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'mascot'))
from tus_variants import keycap, face, F, GOLD, GOLD_D, GREEN_D, INK, WHITE, CREAM, BLUSH
from PIL import Image, ImageDraw

D = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8'))
KESIN = D['kesin'] and not D['kalan']
W, H, FPS = 1080, 1920, 30
OUT = os.path.join(HERE, 'short'); os.makedirs(OUT, exist_ok=True)
BG = (246, 241, 230); MUTED = (120, 112, 100); GREEN_L = (32, 138, 104); RED = (214, 84, 64); BAR = (240, 176, 48)

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def prog(t, s, d=.5): return ease((t - s) / d)
def tr(n, d=2): return f'{n:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def T(d, xy, s, f, fill=INK, a='la'): d.text(xy, s, font=f, fill=fill, anchor=a)

def logo(size):
    return Image.open(os.path.join(HERE, '..', 'logo.png')).convert('RGBA').resize((size, size), Image.LANCZOS)
LOGO = logo(52)

# ---------- characters ----------
def tus(d, cx, cy, s, t, talking=False, blink=0.0, mood=None):
    cy -= abs(math.sin(t * 6)) * 14 * s
    keycap(d, cx, cy, s, GOLD, GOLD_D, t)
    m = mood or ('open' if talking and int(t * 8) % 2 else 'smile')
    face(d, cx, cy - 18 * s, s, blink, 0, m)
    for sx in (-1, 1):  # reading glasses (episode prop)
        d.ellipse((cx + sx * 34 * s - 25 * s, cy - 43 * s, cx + sx * 34 * s + 25 * s, cy + 7 * s), outline=INK, width=int(5 * s))
    d.line((cx - 9 * s, cy - 18 * s, cx + 9 * s, cy - 18 * s), fill=INK, width=int(5 * s))

def calendar(d, x0, y0, s, label='OCA'):
    d.rounded_rectangle((x0, y0, x0 + 80 * s, y0 + 80 * s), 12 * s, fill=WHITE, outline=INK, width=int(4 * s))
    d.rectangle((x0, y0, x0 + 80 * s, y0 + 22 * s), fill=RED)
    T(d, (x0 + 40 * s, y0 + 52 * s), label, F('k', 22 * s), INK, 'mm')

def esittir(d, cx, cy, s, t, talking=False, blink=0.0):
    cy -= abs(math.sin(t * 5 + 1)) * 8 * s
    keycap(d, cx, cy, s, GREEN_L, GREEN_D, t + .5, '=', WHITE)
    face(d, cx, cy - 18 * s, s, blink, 0, 'open' if talking and int(t * 8) % 2 else 'smile')

def bubble(fr, t, s0, text, x, y, w, tail_x, tail_up=False, size=46):
    """Speech bubble with typewriter reveal."""
    p = prog(t, s0, .25)
    if p <= 0: return
    d = fr.d
    f = F('b', size); words = text.split(); lines, cur = [], ''
    for wd in words:
        if d.textlength((cur + ' ' + wd).strip(), font=f) > w - 70: lines.append(cur); cur = wd
        else: cur = (cur + ' ' + wd).strip()
    lines.append(cur)
    h = 50 + len(lines) * (size + 14)
    yy = y - (1 - p) * 30
    d.rounded_rectangle((x, yy, x + w, yy + h), 34, fill=WHITE, outline=INK, width=4)
    ty = yy + h if not tail_up else yy
    d.polygon([(tail_x - 22, ty - (2 if not tail_up else -2)), (tail_x + 22, ty - (2 if not tail_up else -2)), (tail_x, ty + (40 if not tail_up else -40))], fill=WHITE)
    d.line((tail_x - 22, ty, tail_x, ty + (40 if not tail_up else -40), tail_x + 22, ty), fill=INK, width=4)
    n = int(len(text) * min(1, (t - s0) / max(.6, len(text) * .035)))  # typewriter
    shown = 0
    for i, ln in enumerate(lines):
        part = ln[:max(0, n - shown)]; shown += len(ln) + 1
        T(d, (x + 35, yy + 28 + i * (size + 14)), part, f, INK)

class Fr:
    def __init__(s):
        s.im = Image.new('RGB', (W, H), BG); s.d = ImageDraw.Draw(s.im, 'RGBA')
        s.im.paste(LOGO, (80, 250), LOGO); T(s.d, (148, 276), 'Hesap Çantası', F('b', 30), INK, 'lm')

def blink_at(t): return 1.0 if (t % 2.6) < .12 else 0.0

# ---------- scenes ----------
TX, TY = 300, 1420   # Tuş home
EX, EY = 780, 1420   # Eşittir home

def s1(fr, t, dur):  # Tuş asks
    x = TX + (1 - prog(t, 0, .6)) * -500
    tus(fr.d, x, TY, 1.2, t, talking=1.0 < t < 3.2, blink=blink_at(t))
    calendar(fr.d, x + 95, TY + 40, 1.0)
    bubble(fr, t, .9, f"{D['donem']}'da emekli ve memur zammı ne kadar olacak?", 80, 520, 920, 330, size=54)

def months(fr, t, s0, y):
    d = fr.d; ay = [a.split()[0][:3] for a, _ in D['aylar']] + [k.split()[0][:3] for k in D['kalan']]
    vals = [v for _, v in D['aylar']]
    x0, bw, gap = 110, 120, 22
    for i, a in enumerate(ay):
        x = x0 + i * (bw + gap); p = prog(t, s0 + i * .25, .5)
        if p <= 0: continue
        if i < len(vals):
            h = 70 * vals[i] * p
            d.rounded_rectangle((x, y - h, x + bw, y), 14, fill=BAR)
            T(d, (x + bw / 2, y - h - 34), '%' + tr(vals[i]), F('k', 32), INK, 'mm')
        else:
            d.rounded_rectangle((x, y - 120, x + bw, y), 14, outline=MUTED, width=4)
            T(d, (x + bw / 2, y - 60), '?', F('k', 60), MUTED, 'mm')
        T(d, (x + bw / 2, y + 34), a, F('s', 30), MUTED, 'mm')

def s2(fr, t, dur):  # Eşittir explains: 6 months of inflation
    tus(fr.d, TX, TY, 1.0, t, blink=blink_at(t)); calendar(fr.d, TX + 80, TY + 34, .85)
    xe = EX + (1 - prog(t, 0, .6)) * 500
    esittir(fr.d, xe, EY, 1.2, t, talking=.8 < t < 3.0, blink=blink_at(t + 1))
    bubble(fr, t, .7, 'Emekli zammı = son 6 ayın enflasyonu.', 220, 500, 780, 790, size=50)
    months(fr, t, 1.8, 1040)

def s3(fr, t, dur):  # running total + what's left
    tus(fr.d, TX, TY, 1.0, t, talking=2.4 < t < 3.6, blink=blink_at(t)); calendar(fr.d, TX + 80, TY + 34, .85)
    esittir(fr.d, EX, EY, 1.0, t, talking=.3 < t < 2.0, blink=blink_at(t + 1))
    p = prog(t, .2, 1.2)
    T(fr.d, (540, 520), f"{len(D['aylar'])} ayda toplam", F('s', 44), MUTED, 'mm')
    T(fr.d, (540, 640), '%' + tr(D['enf'] * p), F('k', 150), INK, 'mm')
    bubble(fr, t, 2.2, 'Ya kalan 2 ay?', 120, 830, 520, 300, size=50)
    def rest(d):
        for i, k in enumerate(D['kalan']):
            ay, tarih = k.rstrip(')').split(' (')
            T(d, (540, 1070 + i * 60), f'{ay} enflasyonu · açıklanma: {tarih}', F('b', 38), INK, 'mm')
    if prog(t, 3.4, .4) > 0: rest(fr.d)

def s4(fr, t, dur):  # memur
    tus(fr.d, TX, TY, 1.0, t, blink=blink_at(t)); calendar(fr.d, TX + 80, TY + 34, .85)
    esittir(fr.d, EX, EY, 1.1, t, talking=.3 < t < 2.6, blink=blink_at(t + 1))
    bubble(fr, t, .3, f"Memura: toplu sözleşme %{D['tsYeni']} + enflasyon farkı.", 180, 500, 820, 790, size=48)
    p = prog(t, 2.2, .8)
    if p > 0:
        T(fr.d, (540, 860), f"{len(D['aylar'])} aylık veriyle memur zammı", F('s', 40), MUTED, 'mm')
        T(fr.d, (540, 970), '≈ %' + tr(D['memurOran'] * p), F('k', 120), GREEN_D, 'mm')
        T(fr.d, (540, 1070), 'Kesin değil: Aralık enflasyonuyla netleşir', F('b', 34), RED, 'mm')

def s5(fr, t, dur):  # CTA
    fr.d.rectangle((0, 0, W, H), fill=INK)
    fr.im.paste(LOGO, (80, 250), LOGO); T(fr.d, (148, 276), 'Hesap Çantası', F('b', 30), WHITE, 'lm')
    tus(fr.d, 380, 1320, 1.3, t, talking=.3 < t < 1.8, blink=blink_at(t), mood='open' if t > 1.8 else None)
    esittir(fr.d, 740, 1340, 1.0, t, blink=blink_at(t + 1))
    bubble(fr, t, .2, 'Kendi maaşınla hesapla!', 140, 560, 800, 380, size=56)
    if prog(t, 1.0, .4) > 0:
        fr.d.rounded_rectangle((90, 860, 990, 970), 55, fill=GOLD)
        T(fr.d, (540, 915), 'hesapcantasi.com', F('k', 60), INK, 'mm')

SCENES = [(s1, 4.0), (s2, 6.5), (s3, 5.5), (s4, 5.5), (s5, 4.0)]

def watermark(im):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    T(ld, (W // 2, H // 2), 'ÖRNEK', F('k', 240), (255, 80, 60, 50), 'mm')
    lay = lay.rotate(22, center=(W // 2, H // 2)); im.paste(lay, (0, 0), lay)

def draw(i, t):
    fn, dur = SCENES[i]; fr = Fr(); fn(fr, t, dur)
    if not KESIN: watermark(fr.im)
    a = min(1, t / .15, (dur - t) / .15)
    if a < 1: fr.im = Image.blend(Image.new('RGB', (W, H), INK if fn is s5 else BG), fr.im, max(0, a))
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
    else:
        for i in range(len(SCENES)): render(i)
        with open(f'{OUT}/list.txt', 'w') as f:
            for i in range(len(SCENES)): f.write(f"file 's{i:02d}.mp4'\n")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/list.txt', '-c', 'copy', f'{OUT}/silent.mp4'], check=True)
        print('done', sum(d for _, d in SCENES))
