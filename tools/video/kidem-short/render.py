"""Vertical Shorts version: 'Kıdem tazminatın ne kadar?' — 1080x1920, 30 fps, ~37 s.
Content kept inside the Shorts safe area (top 220 px, bottom 420 px and right 160 px are covered by YouTube UI)."""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
OUT = os.path.dirname(os.path.abspath(__file__))
FD = '/usr/share/fonts/opentype/inter/'
_fc = {}
def F(w, s):
    k = (w, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(FD + {'b': 'InterDisplay-Bold.otf', 'x': 'InterDisplay-ExtraBold.otf', 'k': 'InterDisplay-Black.otf', 's': 'InterDisplay-SemiBold.otf', 'r': 'InterDisplay-Regular.otf'}[w], s)
    return _fc[k]

BG = (246, 245, 241); INK = (28, 31, 29); MUTED = (95, 102, 98); ACC = (15, 107, 79); SOFT = (227, 241, 234); LINE = (227, 225, 218); CARD = (255, 255, 255); WARN = (161, 48, 31); GOLD = (232, 176, 52); LIGHT = (210, 236, 224)
L, R = 80, 920  # safe horizontal bounds

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def prog(t, s, d=0.5): return ease((t - s) / d)
def tr(n, d=2): return f'{n:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

class Frame:
    def __init__(self, bg=BG):
        self.im = Image.new('RGB', (W, H), bg); self.d = ImageDraw.Draw(self.im)
    def layer(self, a, fn, dy=0):
        if a <= 0: return
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay), dy)
        if a < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * a)))
        self.im.paste(lay, (0, 0), lay)

def appear(fr, t, s, fn, dur=0.45, rise=40):
    p = prog(t, s, dur); fr.layer(p, fn, int((1 - p) * rise))

def T(d, xy, s, f, fill=INK, a='la'): d.text(xy, s, font=f, fill=fill, anchor=a)

def head(fr, step, title1, title2=None):
    d = fr.d
    d.rounded_rectangle((L, 250, L + 56, 306), 14, fill=ACC); T(d, (L + 28, 278), '₺', F('b', 34), (255, 255, 255), 'mm')
    T(d, (L + 76, 278), 'Hesap Çantası', F('b', 32), INK, 'lm')
    if step:
        d.rounded_rectangle((L, 350, L + 250, 410), 30, fill=SOFT); T(d, (L + 125, 380), step, F('b', 32), ACC, 'mm')
    T(d, (L, 450), title1, F('k', 84), INK)
    if title2: T(d, (L, 550), title2, F('k', 84), ACC)

def s_hook(fr, t, dur):
    fr.d.rectangle((0, 0, W, H), fill=ACC)
    appear(fr, t, 0.05, lambda d, dy: T(d, (W // 2 - 40, 640 + dy), 'Kıdem', F('k', 190), (255, 255, 255), 'mm'))
    appear(fr, t, 0.25, lambda d, dy: T(d, (W // 2 - 40, 830 + dy), 'tazminatın', F('k', 132), (255, 255, 255), 'mm'))
    appear(fr, t, 0.45, lambda d, dy: T(d, (W // 2 - 40, 1000 + dy), 'ne kadar?', F('k', 136), GOLD, 'mm'))
    def pill(d, dy):
        d.rounded_rectangle((W // 2 - 360, 1150 + dy, W // 2 + 280, 1250 + dy), 50, fill=(255, 255, 255))
        T(d, (W // 2 - 40, 1200 + dy), '3 adımda hesapla', F('b', 52), ACC, 'mm')
    appear(fr, t, 1.1, pill)
    # bouncing arrow hint
    if t > 1.6:
        import math
        y = 1330 + int(14 * math.sin((t - 1.6) * 7))
        fr.d.polygon([(W // 2 - 70, y), (W // 2 - 10, y), (W // 2 - 40, y + 40)], fill=LIGHT)

def s_a1(fr, t, dur):
    head(fr, 'Adım 1', 'Giydirilmiş', 'ücreti bul')
    appear(fr, t, 0.3, lambda d, dy: T(d, (L, 680 + dy), 'Brüt maaş + düzenli yan haklar', F('s', 46), MUTED))
    appear(fr, t, 0.6, lambda d, dy: d.rounded_rectangle((L, 780 + dy, R, 1300 + dy), 34, fill=CARD, outline=LINE, width=3))
    for i, (lab, v, s) in enumerate([('Brüt maaş', '60.000 ₺', 1.0), ('+ Yemek / yol', '5.000 ₺', 1.7)]):
        y = 880 + i * 120
        appear(fr, t, s, lambda d, dy, lab=lab, v=v, y=y: (T(d, (L + 50, y + dy), lab, F('s', 54), INK, 'lm'), T(d, (R - 50, y + dy), v, F('x', 60), INK, 'rm')))
    def tot(d, dy):
        d.line((L + 50, 1060 + dy, R - 50, 1060 + dy), fill=LINE, width=5)
        T(d, (L + 50, 1170 + dy), '=', F('k', 90), ACC, 'lm')
        T(d, (R - 50, 1170 + dy), tr(65000 * prog(t, 2.6, 0.9), 0) + ' ₺', F('k', 104), ACC, 'rm')
    appear(fr, t, 2.4, tot)
    appear(fr, t, 4.0, lambda d, dy: T(d, (L, 1360 + dy), 'Yan hakları eklemezsen tazminat düşük çıkar.', F('s', 40), MUTED))

def s_a2(fr, t, dur):
    head(fr, 'Adım 2', 'Tavanı', 'kontrol et')
    def tav(d, dy):
        d.rounded_rectangle((L, 700 + dy, R, 940 + dy), 34, fill=ACC)
        T(d, (L + 50, 760 + dy), 'Tavan · Temmuz–Aralık 2026', F('s', 40), LIGHT)
        T(d, (L + 50, 870 + dy), '73.729,84 ₺', F('k', 104), (255, 255, 255), 'lm')
    appear(fr, t, 0.4, tav)
    def bars(d, dy):
        p = prog(t, 1.6, 1.1); mw = R - L
        for j, (lab, v, col) in enumerate([('Tavan', 73729.84, ACC), ('Senin ücretin', 65000, GOLD)]):
            y = 1010 + j * 150 + dy
            T(d, (L, y), lab, F('s', 42), INK)
            T(d, (R, y), tr(v * p, 0) + ' ₺', F('b', 42), INK, 'ra')
            d.rounded_rectangle((L, y + 60, L + max(16, int(mw * v / 73729.84 * p)), y + 115), 22, fill=col)
    appear(fr, t, 1.3, bars)
    def res(d, dy):
        d.rounded_rectangle((L, 1340 + dy, R, 1470 + dy), 34, fill=SOFT)
        T(d, ((L + R) // 2, 1405 + dy), 'Altında → 65.000 ₺ kullanılır', F('x', 50), ACC, 'mm')
    appear(fr, t, 3.4, res)

def s_a3(fr, t, dur):
    head(fr, 'Adım 3', 'Süreyle çarp')
    def sure(d, dy):
        d.rounded_rectangle((L, 590 + dy, L + 520, 680 + dy), 45, fill=SOFT); T(d, (L + 260, 635 + dy), 'Örnek: 6 yıl 4 ay', F('b', 46), ACC, 'mm')
    appear(fr, t, 0.3, sure)
    appear(fr, t, 0.6, lambda d, dy: d.rounded_rectangle((L, 740 + dy, R, 1400 + dy), 34, fill=CARD, outline=LINE, width=3))
    rows = [('6 yıl × 65.000', 390000, 1.0), ('4 ay × 65.000 ÷ 12', 21666.67, 2.2)]
    for i, (lab, v, s) in enumerate(rows):
        y = 830 + i * 170
        def f(d, dy, lab=lab, v=v, y=y, s=s):
            T(d, (L + 50, y + dy), lab, F('s', 48), MUTED, 'lm')
            T(d, (R - 50, y + 70 + dy), tr(v * prog(t, s, 0.8)) + ' ₺', F('x', 64), INK, 'rm')
        appear(fr, t, s, f)
    def tot(d, dy):
        d.line((L + 50, 1180 + dy, R - 50, 1180 + dy), fill=LINE, width=5)
        T(d, (L + 50, 1240 + dy), 'Brüt tazminat', F('b', 48), ACC, 'lm')
        T(d, (R - 50, 1325 + dy), tr(411666.67 * prog(t, 3.8, 1.0)) + ' ₺', F('k', 78), ACC, 'rm')
    appear(fr, t, 3.6, tot)

def s_net(fr, t, dur):
    head(fr, 'Son adım', 'Damga vergisini', 'düş')
    appear(fr, t, 0.3, lambda d, dy: T(d, (L, 690 + dy), 'Gelir vergisi yok, sadece binde 7,59', F('s', 44), MUTED))
    def r1(d, dy):
        d.rounded_rectangle((L, 780 + dy, R, 1000 + dy), 34, fill=CARD, outline=LINE, width=3)
        T(d, (L + 50, 840 + dy), 'Brüt', F('s', 48), INK, 'lm'); T(d, (R - 50, 840 + dy), '411.666,67 ₺', F('b', 52), INK, 'rm')
        T(d, (L + 50, 940 + dy), 'Damga', F('s', 48), INK, 'lm'); T(d, (R - 50, 940 + dy), '− 3.124,55 ₺', F('b', 52), WARN, 'rm')
    appear(fr, t, 0.7, r1)
    def big(d, dy):
        d.rounded_rectangle((L, 1060 + dy, R, 1420 + dy), 40, fill=ACC)
        T(d, ((L + R) // 2, 1140 + dy), 'Eline geçecek net', F('s', 48), LIGHT, 'mm')
        T(d, ((L + R) // 2, 1290 + dy), tr(408542.12 * prog(t, 2.0, 1.4)) + ' ₺', F('k', 110), (255, 255, 255), 'mm')
    appear(fr, t, 1.8, big)

def s_cta(fr, t, dur):
    fr.d.rectangle((0, 0, W, H), fill=ACC)
    appear(fr, t, 0.1, lambda d, dy: T(d, (W // 2 - 40, 520 + dy), 'Kendi tazminatını', F('k', 80), (255, 255, 255), 'mm'))
    appear(fr, t, 0.3, lambda d, dy: T(d, (W // 2 - 40, 630 + dy), '5 saniyede hesapla', F('k', 80), GOLD, 'mm'))
    def mock(d, dy):
        x0, y0 = L + 40, 760 + dy; x1 = R - 40
        d.rounded_rectangle((x0, y0, x1, y0 + 470), 34, fill=CARD)
        for j, (lab, val) in enumerate([('İşe giriş', '01.03.2020'), ('Çıkış', '01.07.2026'), ('Brüt ücret', '60.000')]):
            y = y0 + 40 + j * 105
            T(d, (x0 + 40, y), lab, F('s', 30), MUTED)
            d.rounded_rectangle((x0 + 40, y + 38, x1 - 40, y + 90), 12, fill=BG, outline=LINE, width=2)
            T(d, (x0 + 60, y + 64), val, F('s', 32), INK, 'lm')
        d.rounded_rectangle((x0 + 40, y0 + 370, x1 - 40, y0 + 440), 14, fill=SOFT)
        T(d, (x0 + 65, y0 + 405), 'Net', F('b', 36), INK, 'lm'); T(d, (x1 - 65, y0 + 405), '377.115,80 ₺', F('k', 40), ACC, 'rm')
    appear(fr, t, 0.8, mock)
    def url(d, dy):
        d.rounded_rectangle((L, 1300 + dy, R, 1410 + dy), 55, fill=(255, 255, 255))
        T(d, ((L + R) // 2, 1355 + dy), 'hesapcantasi.com', F('k', 64), ACC, 'mm')
    appear(fr, t, 1.8, url)
    appear(fr, t, 2.6, lambda d, dy: T(d, ((L + R) // 2, 1460 + dy), 'Google’da “Hesap Çantası” yaz', F('s', 40), LIGHT, 'mm'))

SCENES = [(s_hook, 3.5), (s_a1, 7.0), (s_a2, 6.5), (s_a3, 8.0), (s_net, 6.0), (s_cta, 6.5)]

def draw(i, t):
    fn, dur = SCENES[i]
    fr = Frame(); fn(fr, t, dur)
    if fn not in (s_hook, s_cta):
        fr.d.rectangle((0, 214, int(W * min(1, t / dur)), 222), fill=ACC)  # progress line under the top UI
    a = min(1, t / 0.2, (dur - t) / 0.2)
    if a < 1: fr.im = Image.blend(Image.new('RGB', (W, H), ACC if fn in (s_hook, s_cta) else BG), fr.im, max(0, a))
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
        for i, (fn, dur) in enumerate(SCENES): draw(i, dur - 0.5).save(f'{OUT}/still{i}.jpg', quality=88)
    else:
        for i in range(len(SCENES)): render(i)
        with open(f'{OUT}/list.txt', 'w') as f:
            for i in range(len(SCENES)): f.write(f"file 's{i:02d}.mp4'\n")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/list.txt', '-c', 'copy', f'{OUT}/silent.mp4'], check=True)
        print('done', sum(d for _, d in SCENES))
