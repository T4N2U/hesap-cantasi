"""'İhbar tazminatı nasıl hesaplanır?' (publish 2 Feb 2027, Short 4 Feb). Classic style (no mascot).
Figures from data.json (site engine); notice periods from 4857 s. İş Kanunu md. 17. Evergreen: no watermark.
Visual variant: deep plum ground, mint accent, notice weeks drawn as calendar squares that fill in, wipe-in transition.
Music: lofi-piano. Long video ends with the 10 s end-screen scene (../endscreen.py). Usage: python3 render.py long|short [stills]"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
import endscreen as ES
from PIL import Image, ImageDraw, ImageFont

MODE = sys.argv[1] if len(sys.argv) > 1 else 'long'; L = MODE == 'long'
W, H = (1920, 1080) if L else (1080, 1920); FPS = 30
OUT = os.path.join(HERE, MODE); os.makedirs(OUT, exist_ok=True)
D = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8')); X = D['ex']
FD = '/usr/share/fonts/opentype/inter/'; _fc = {}
def F(w, s):
    if (w, s) not in _fc: _fc[(w, s)] = ImageFont.truetype(FD + {'b': 'InterDisplay-Bold.otf', 'k': 'InterDisplay-Black.otf', 's': 'InterDisplay-SemiBold.otf'}[w], s)
    return _fc[(w, s)]
BG = (38, 24, 52); CARD = (56, 38, 74); LINE = (84, 62, 104); INK = (246, 242, 250); MUTED = (180, 166, 196)
MINT = (110, 231, 183); MINT_D = (24, 120, 90); RED = (248, 113, 113); WHITE = (255, 255, 255); DARK = (24, 14, 34)
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def prog(t, s, d=.5): return ease((t - s) / d)
def tr(n, d=2): return f'{n:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def tl(n): return tr(n, 0 if float(n).is_integer() else 2) + ' ₺'
def T(d, xy, s, f, fill=INK, a='la'): d.text(xy, s, font=f, fill=fill, anchor=a)
_LG = {}
def logo(n):
    if n not in _LG: _LG[n] = Image.open(os.path.join(HERE, '..', 'logo.png')).convert('RGBA').resize((n, n), Image.LANCZOS)
    return _LG[n]
M = 120 if L else 80; R = W - M; CX = W // 2; TOP = 70 if L else 250
def brand(fr): lg = logo(52); fr.im.paste(lg, (M, TOP), lg); T(fr.d, (M + 68, TOP + 26), 'Hesap Çantası', F('b', 30), INK, 'lm')
class Fr:
    def __init__(s): s.im = Image.new('RGB', (W, H), BG); s.d = ImageDraw.Draw(s.im)
def wipe(fr, t, s, fn, dur=.5):
    """Content wipes in from the left (this video's transition)."""
    p = prog(t, s, dur)
    if p <= 0: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay))
    if p < 1:
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle((0, 0, int(W * p), H), fill=255)
        a = lay.getchannel('A'); lay.putalpha(Image.composite(a, Image.new('L', (W, H), 0), m))
    fr.im.paste(lay, (0, 0), lay)
def header(fr, title, sub=None):
    brand(fr); ty = 190 if L else 370
    T(fr.d, (M, ty), title, F('k', 66 if L else 54), INK)
    if sub: T(fr.d, (M, ty + (86 if L else 72)), sub, F('s', 34 if L else 30), MUTED)
def weeks(d, x, y, n, filled, sq, gap, cols=8):
    """Calendar squares: one per notice week (topic accent, this video only)."""
    for i in range(8 if L else n):
        if i >= n and not L: break
        cx, cy = x + (i % cols) * (sq + gap), y + (i // cols) * (sq + gap)
        on = i < n
        d.rounded_rectangle((cx, cy, cx + sq, cy + sq), 10, fill=(MINT if i < filled else CARD) if on else None, outline=LINE if not on else None, width=3)
        if on: d.rectangle((cx, cy, cx + sq, cy + sq * .22), fill=MINT_D if i < filled else LINE)

# ---------------- scenes ----------------
def s_hook(fr, t, dur):
    brand(fr)
    if L:
        wipe(fr, t, .1, lambda d: (T(d, (M, 300), 'İhbar tazminatı', F('k', 120), INK), T(d, (M, 440), 'nasıl hesaplanır?', F('k', 100), MINT)))
        wipe(fr, t, 1.2, lambda d: T(d, (M, 590), 'İşveren haber vermeden çıkarırsa ne alırsın?', F('s', 44), MUTED))
        n = int(8 * prog(t, 1.6, 1.6)); weeks(fr.d, 1240, 720, 8, n, 62, 14)
    else:
        wipe(fr, t, .1, lambda d: (T(d, (CX, 600), 'İhbar', F('k', 150), INK, 'mm'), T(d, (CX, 740), 'tazminatı', F('k', 120), INK, 'mm'), T(d, (CX, 870), 'nasıl hesaplanır?', F('k', 76), MINT, 'mm')))
        n = int(8 * prog(t, 1.2, 1.4))
        for i in range(8):
            cx = M + 30 + (i % 4) * 230; cy = 1020 + (i // 4) * 170
            fr.d.rounded_rectangle((cx, cy, cx + 150, cy + 150), 14, fill=MINT if i < n else CARD); fr.d.rectangle((cx, cy, cx + 150, cy + 34), fill=MINT_D if i < n else LINE)

def s_what(fr, t, dur):
    header(fr, 'İhbar tazminatı nedir?', 'İş Kanunu md. 17')
    lines = ['İşveren, kanuni bildirim süresine uymadan', 'iş sözleşmesini feshederse', 'bu sürenin ücretini öder.'] if L else ['İşveren, kanuni bildirim', 'süresine uymadan', 'sözleşmeyi feshederse', 'bu sürenin ücretini öder.']
    for i, ln in enumerate(lines):
        wipe(fr, t, .4 + i * .5, lambda d, i=i, ln=ln: T(d, (M, (380 if L else 560) + i * (90 if L else 84)), ln, F('k', 60 if L else 54), MINT if i == len(lines) - 1 else INK))
    wipe(fr, t, 2.6, lambda d: T(d, (M, 740 if L else 1000), 'Brüt ücret + düzenli yan haklar üzerinden', F('s', 38 if L else 34), MUTED))

def s_sure(fr, t, dur):
    header(fr, 'İhbar süresi kaç hafta?', 'Çalışma süresine göre')
    for i, (lab, w) in enumerate(D['sureler']):
        if L: x, y, bw, bh = M + i * 430, 360, 400, 470
        else: x, y, bw, bh = M, 520 + i * 290, R - M, 260
        def card(d, x=x, y=y, bw=bw, bh=bh, lab=lab, w=w, i=i):
            d.rounded_rectangle((x, y, x + bw, y + bh), 28, fill=CARD, outline=MINT if i == 3 else None, width=4)
            T(d, (x + 32, y + 50), lab, F('s', 34), MUTED, 'lm')
            T(d, (x + 32, y + (140 if L else 130)), f'{w} hafta', F('k', 64 if L else 60), INK, 'lm')
            T(d, (x + (32 if L else bw - 32), y + (210 if L else 130)), f'{w * 7} gün', F('b', 36), MINT, 'lm' if L else 'rm')
        wipe(fr, t, .4 + i * .45, card)
        p = prog(t, .9 + i * .45, .8)
        if p > 0 and L:
            n = int(w * p)
            for k in range(w):
                cx, cy = x + 32 + (k % 4) * 86, y + 280 + (k // 4) * 86
                fr.d.rounded_rectangle((cx, cy, cx + 70, cy + 70), 10, fill=MINT if k < n else LINE)

def s_formula(fr, t, dur):
    header(fr, 'Örnek: 4 yıl, brüt 40.000 ₺', 'İhbar süresi 8 hafta = 56 gün')
    rows = [('Günlük brüt ücret', f"{tl(X['maas'])} ÷ 30", tl(X['gunluk'])),
            ('İhbar süresi', '8 hafta × 7', f"{X['gun']} gün"),
            ('Brüt ihbar tazminatı', f"{tl(X['gunluk'])} × {X['gun']}", tl(X['brut']))]
    for i, (a, b, c) in enumerate(rows):
        y = (360 if L else 560) + i * (150 if L else 230)
        def row(d, a=a, b=b, c=c, y=y, i=i):
            d.rounded_rectangle((M, y, R, y + (120 if L else 200)), 24, fill=MINT if i == 2 else CARD)
            fg = DARK if i == 2 else INK
            if L:
                T(d, (M + 36, y + 40), a, F('s', 32), DARK if i == 2 else MUTED, 'lm'); T(d, (M + 36, y + 84), b, F('b', 34), fg, 'lm')
                T(d, (R - 36, y + 60), c, F('k', 54), fg, 'rm')
            else:
                T(d, (M + 32, y + 44), a, F('s', 32), DARK if i == 2 else MUTED, 'lm'); T(d, (M + 32, y + 100), b, F('b', 32), fg, 'lm')
                T(d, (R - 32, y + 156), c, F('k', 52), fg, 'rm')
        wipe(fr, t, .4 + i * .9, row)

def s_net(fr, t, dur):
    header(fr, 'Kesintiler ve net tutar' if L else 'Örnek: 4 yıl, brüt 40.000 ₺', 'SGK primi kesilmez' if L else 'Kesintiler · SGK primi kesilmez')
    rows = [('Brüt ihbar tazminatı', tl(X['brut']), INK), ('Gelir vergisi (%15 dilimde)', '−' + tl(X['gv']), RED), (f"Damga vergisi (binde {tr(D['damga'] * 1000)})", '−' + tl(X['damga']), RED)]
    for i, (a, b, c) in enumerate(rows):
        y = (340 if L else 540) + i * (110 if L else 150)
        wipe(fr, t, .3 + i * .5, lambda d, a=a, b=b, c=c, y=y: (d.rounded_rectangle((M, y, R, y + (90 if L else 120)), 20, fill=CARD), T(d, (M + 32, y + (45 if L else 60)), a, F('b', 36 if L else 32), MUTED, 'lm'), T(d, (R - 32, y + (45 if L else 60)), b, F('k', 44 if L else 40), c, 'rm')))
    p = prog(t, 2.0, 1.0)
    if p > 0:
        y = 700 if L else 1020
        fr.d.rounded_rectangle((M, y, R, y + (130 if L else 160)), 26, fill=MINT)
        T(fr.d, (M + 36, y + (65 if L else 80)), 'Net ihbar tazminatı', F('k', 44 if L else 40), DARK, 'lm')
        T(fr.d, (R - 36, y + (65 if L else 80)), tl(round(X['net'] * p, 2)), F('k', 60 if L else 52), DARK, 'rm')
    wipe(fr, t, 3.0, lambda d: T(d, (M, (880 if L else 1240)), 'Gelir vergisi oranı yıl içindeki matrahınıza göre %15–%40 arasıdır.', F('s', 30 if L else 26), MUTED))

def s_cta(fr, t, dur):
    fr.d.rectangle((0, 0, W, H), fill=MINT)
    if L:  # above SAFE_BOTTOM; end-screen zones left clear
        lg = logo(100); fr.im.paste(lg, (CX - 50, 70), lg)
        wipe(fr, t, .1, lambda d: T(d, (CX, 250), 'Kendi ihbar tazminatını hesapla', F('k', 70), DARK, 'mm'))
        def url(d):
            d.rounded_rectangle((CX - 500, 315, CX + 500, 415), 50, fill=DARK); T(d, (CX, 365), 'hesapcantasi.com/ihbar-tazminati-hesaplama', F('k', 38), WHITE, 'mm')
        wipe(fr, t, .7, url)
        wipe(fr, t, 1.4, lambda d: T(d, (CX, 470), 'Giriş ve çıkış tarihi · brüt ücret', F('s', 38), DARK, 'mm'))
        wipe(fr, t, 2.0, lambda d: ES.labels(d, F('b', 34), DARK))
        return
    lg = logo(120); fr.im.paste(lg, (CX - 60, 420), lg)
    wipe(fr, t, .1, lambda d: (T(d, (CX, 640), 'Kendi ihbar', F('k', 70), DARK, 'mm'), T(d, (CX, 725), 'tazminatını hesapla', F('k', 64), DARK, 'mm')))
    wipe(fr, t, .7, lambda d: (d.rounded_rectangle((M, 820, R, 930), 55, fill=DARK), T(d, (CX, 875), 'hesapcantasi.com', F('k', 60), WHITE, 'mm')))

LONG = [(s_hook, 4.5), (s_what, 6.0), (s_sure, 7.0), (s_formula, 7.0), (s_net, 7.0), (s_cta, ES.CTA_SEC)]
SHORT = [(s_hook, 3.5), (s_sure, 6.5), (s_net, 7.0), (s_cta, 4.0)]
SCENES = LONG if L else SHORT

def draw(i, t):
    fn, dur = SCENES[i]; fr = Fr(); fn(fr, t, dur)
    a = min(1, t / .18, (dur - t) / .18)
    if a < 1: fr.im = Image.blend(Image.new('RGB', (W, H), MINT if fn is s_cta else BG), fr.im, max(0, a))
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
        for i, (fn, dur) in enumerate(SCENES): draw(i, dur - .3).save(f'{OUT}/still{i}.jpg', quality=85)
        if L: ES.guides(draw(len(SCENES) - 1, 3.0)).save(f'{OUT}/still-endscreen-guides.jpg', quality=85)
    else:
        for i in range(len(SCENES)): render(i)
        with open(f'{OUT}/list.txt', 'w') as f:
            for i in range(len(SCENES)): f.write(f"file 's{i:02d}.mp4'\n")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/list.txt', '-c', 'copy', f'{OUT}/silent.mp4'], check=True)
        print('done', sum(d for _, d in SCENES))
        if L: print('end screen from', ES.start_time(SCENES), 's')
