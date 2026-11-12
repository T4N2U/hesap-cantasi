"""Animated explainer: 'Kıdem tazminatı nasıl hesaplanır? (2026)' — 1920x1080, 30 fps.
Each scene is drawn frame-by-frame with PIL and piped into its own ffmpeg encode; scenes are joined with concat."""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
OUT = os.path.dirname(os.path.abspath(__file__))
FD = '/usr/share/fonts/opentype/inter/'
def F(w, s): return ImageFont.truetype(FD + {'b': 'InterDisplay-Bold.otf', 'x': 'InterDisplay-ExtraBold.otf', 's': 'InterDisplay-SemiBold.otf', 'r': 'InterDisplay-Regular.otf'}[w], s)

BG = (246, 245, 241); INK = (28, 31, 29); MUTED = (95, 102, 98); ACC = (15, 107, 79); SOFT = (227, 241, 234); LINE = (227, 225, 218); CARD = (255, 255, 255); WARN = (161, 48, 31); GOLD = (214, 158, 46)

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def prog(t, start, dur=0.5): return ease((t - start) / dur)
def tr(n, d=2):
    s = f'{n:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return s

class Frame:
    def __init__(self):
        self.im = Image.new('RGB', (W, H), BG)
        self.d = ImageDraw.Draw(self.im)
    def layer(self, alpha, fn, dy=0):
        if alpha <= 0: return
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        fn(ImageDraw.Draw(lay), dy)
        if alpha < 1:
            a = lay.getchannel('A').point(lambda v: int(v * alpha)); lay.putalpha(a)
        self.im.paste(lay, (0, 0), lay)

def appear(fr, t, start, fn, dur=0.5, rise=30):
    p = prog(t, start, dur)
    fr.layer(p, fn, dy=int((1 - p) * rise))

def text(d, xy, s, font, fill=INK, anchor='la'): d.text(xy, s, font=font, fill=fill, anchor=anchor)
def card(d, box, fill=CARD, outline=LINE, r=28, w=3): d.rounded_rectangle(box, r, fill=fill, outline=outline, width=w)

def header(fr, step, title):
    d = fr.d
    d.rounded_rectangle((110, 90, 110 + 64, 154), 16, fill=ACC)
    text(d, (142, 122), '₺', F('b', 38), (255, 255, 255), 'mm')
    text(d, (196, 122), 'Hesap Çantası', F('b', 34), INK, 'lm')
    if step:
        d.rounded_rectangle((W - 330, 96, W - 110, 148), 26, fill=SOFT)
        text(d, (W - 220, 122), step, F('s', 28), ACC, 'mm')
    text(d, (110, 220), title, F('x', 76), INK)

def footer(fr, t, dur):
    d = fr.d
    d.rectangle((0, H - 14, int(W * min(1, t / dur)), H), fill=ACC)
    text(d, (W - 110, H - 50), 'hesapcantasi.com', F('s', 28), MUTED, 'rm')

# ---------------- scenes ----------------
def s_intro(fr, t, dur):
    d = fr.d
    p = prog(t, 0.1, 0.7)
    s = 0.6 + 0.4 * p
    def logo(dd, dy):
        sz = int(150 * s); cx, cy = W // 2, 330 + dy
        dd.rounded_rectangle((cx - sz // 2, cy - sz // 2, cx + sz // 2, cy + sz // 2), int(36 * s), fill=ACC)
        dd.text((cx, cy), '₺', font=F('b', int(92 * s)), fill=(255, 255, 255), anchor='mm')
    fr.layer(p, logo)
    appear(fr, t, 0.6, lambda dd, dy: text(dd, (W // 2, 520 + dy), 'Kıdem tazminatı', F('x', 120), INK, 'mm'))
    appear(fr, t, 0.9, lambda dd, dy: text(dd, (W // 2, 650 + dy), 'nasıl hesaplanır?', F('x', 120), ACC, 'mm'))
    def pill(dd, dy):
        dd.rounded_rectangle((W // 2 - 280, 770 + dy, W // 2 + 280, 850 + dy), 40, fill=SOFT)
        dd.text((W // 2, 810 + dy), '2026 · 3 adımda, örnekle', font=F('s', 38), fill=ACC, anchor='mm')
    appear(fr, t, 1.5, pill)

def s_sartlar(fr, t, dur):
    header(fr, 'Önce şartlar', 'Kimler kıdem tazminatı alır?')
    items = [('✓', 'Aynı işverende en az 1 yıl çalışmış olmak', ACC),
             ('✓', 'İşveren tarafından haklı neden olmadan çıkarılmak', ACC),
             ('✓', 'Emeklilik, askerlik, evlilik (kadın çalışan, 1 yıl içinde)', ACC),
             ('✓', 'Haklı nedenle istifa (ör. maaşın ödenmemesi)', ACC),
             ('✗', 'Normal istifada kural olarak alınmaz', WARN)]
    for i, (ic, s, col) in enumerate(items):
        y = 380 + i * 112
        def f(dd, dy, ic=ic, s=s, col=col, y=y):
            dd.ellipse((130, y - 30 + dy, 190, y + 30 + dy), fill=col)
            dd.text((160, y + dy), ic, font=F('b', 36), fill=(255, 255, 255), anchor='mm')
            dd.text((230, y + dy), s, font=F('s', 46), fill=INK, anchor='lm')
        appear(fr, t, 0.5 + i * 0.6, f)

def s_adim1(fr, t, dur):
    header(fr, 'Adım 1 / 3', 'Giydirilmiş brüt ücreti bul')
    appear(fr, t, 0.4, lambda dd, dy: text(dd, (110, 340 + dy), 'Son brüt maaşınıza düzenli ödenen yan hakları ekleyin (yemek, yol, ikramiye…).', F('r', 40), MUTED))
    rows = [('Brüt maaş', 60000, 1.2), ('+ Yemek / yol yardımı', 5000, 2.0)]
    def box(dd, dy):
        card(dd, (110, 430 + dy, 1180, 860 + dy))
    appear(fr, t, 1.0, box)
    for i, (lab, v, st) in enumerate(rows):
        y = 520 + i * 110
        appear(fr, t, st, lambda dd, dy, lab=lab, v=v, y=y: (text(dd, (170, y + dy), lab, F('s', 48), INK, 'lm'), text(dd, (1120, y + dy), tr(v) + ' ₺', F('b', 52), INK, 'rm')))
    def total(dd, dy):
        dd.line((170, 690 + dy, 1120, 690 + dy), fill=LINE, width=4)
        text(dd, (170, 775 + dy), 'Giydirilmiş ücret', F('b', 50), ACC, 'lm')
        v = 65000 * prog(t, 3.0, 1.0)
        text(dd, (1120, 775 + dy), tr(v) + ' ₺', F('x', 64), ACC, 'rm')
    appear(fr, t, 2.8, total)
    def side(dd, dy):
        card(dd, (1260, 430 + dy, 1810, 860 + dy), fill=SOFT, outline=SOFT)
        text(dd, (1310, 490 + dy), 'Neden önemli?', F('b', 40), ACC)
        for j, ln in enumerate(['Yan haklar eklenmezse', 'tazminat olduğundan', 'düşük hesaplanır.']):
            text(dd, (1310, 570 + j * 60 + dy), ln, F('r', 38), INK)
    appear(fr, t, 4.2, side)

def s_adim2(fr, t, dur):
    header(fr, 'Adım 2 / 3', 'Tavanı kontrol et')
    appear(fr, t, 0.4, lambda dd, dy: text(dd, (110, 340 + dy), 'Bir yıl için ödenebilecek en yüksek tutar yasal tavanla sınırlıdır.', F('r', 40), MUTED))
    def tav(dd, dy):
        card(dd, (110, 430 + dy, 900, 700 + dy), fill=ACC, outline=ACC)
        text(dd, (170, 500 + dy), 'Tavan · Temmuz–Aralık 2026', F('s', 38), (210, 236, 224))
        text(dd, (170, 610 + dy), tr(73729.84) + ' ₺', F('x', 84), (255, 255, 255), 'lm')
    appear(fr, t, 1.0, tav)
    # bar comparison
    base_y = 800
    def bars(dd, dy):
        p = prog(t, 2.4, 1.2)
        maxw = 820; x0 = 1000
        for j, (lab, v, col) in enumerate([('Tavan', 73729.84, ACC), ('Sizin ücretiniz', 65000, GOLD)]):
            y = 470 + j * 130 + dy
            text(dd, (x0, y), lab, F('s', 36), INK, 'la')
            wv = int(maxw * v / 73729.84 * p)
            dd.rounded_rectangle((x0, y + 50, x0 + max(wv, 12), y + 100), 18, fill=col)
            text(dd, (x0 + maxw, y), tr(v * p) + ' ₺', F('b', 36), INK, 'ra')
    appear(fr, t, 2.0, bars)
    def res(dd, dy):
        dd.rounded_rectangle((110, 760 + dy, W - 110, 880 + dy), 30, fill=SOFT)
        text(dd, (160, 820 + dy), '65.000 ₺ tavanın altında  →  hesapta 65.000 ₺ kullanılır', F('b', 48), ACC, 'lm')
    appear(fr, t, 4.2, res)

def s_adim3(fr, t, dur):
    header(fr, 'Adım 3 / 3', 'Çalışma süresiyle çarp')
    appear(fr, t, 0.4, lambda dd, dy: text(dd, (110, 340 + dy), 'Her tam yıl için 1 aylık ücret; artan aylar ve günler orantılı eklenir.', F('r', 40), MUTED))
    def sure(dd, dy):
        dd.rounded_rectangle((110, 420 + dy, 820, 500 + dy), 40, fill=SOFT)
        text(dd, (465, 460 + dy), 'Örnek süre: 6 yıl 4 ay', F('b', 42), ACC, 'mm')
    appear(fr, t, 0.9, sure)
    lines = [('6 yıl × 65.000 ₺', 390000, 1.8), ('4 ay × (65.000 ₺ ÷ 12)', 21666.67, 3.2)]
    def box(dd, dy): card(dd, (110, 540 + dy, W - 110, 940 + dy))
    appear(fr, t, 1.5, box)
    for i, (lab, v, st) in enumerate(lines):
        y = 620 + i * 105
        def f(dd, dy, lab=lab, v=v, y=y, st=st):
            text(dd, (170, y + dy), lab, F('s', 50), INK, 'lm')
            text(dd, (W - 170, y + dy), tr(v * prog(t, st, 0.9)) + ' ₺', F('b', 54), INK, 'rm')
        appear(fr, t, st, f)
    def tot(dd, dy):
        dd.line((170, 780 + dy, W - 170, 780 + dy), fill=LINE, width=4)
        text(dd, (170, 865 + dy), 'Brüt kıdem tazminatı', F('b', 54), ACC, 'lm')
        text(dd, (W - 170, 865 + dy), tr(411666.67 * prog(t, 4.8, 1.0)) + ' ₺', F('x', 70), ACC, 'rm')
    appear(fr, t, 4.6, tot)

def s_net(fr, t, dur):
    header(fr, 'Son adım', 'Damga vergisini düş')
    appear(fr, t, 0.4, lambda dd, dy: text(dd, (110, 340 + dy), 'Kıdem tazminatından gelir vergisi kesilmez; yalnızca binde 7,59 damga vergisi kesilir.', F('r', 40), MUTED))
    rows = [('Brüt tazminat', '411.666,67 ₺', INK, 1.0), ('Damga vergisi (‰7,59)', '− 3.124,55 ₺', WARN, 1.8)]
    def box(dd, dy): card(dd, (110, 430 + dy, W - 110, 650 + dy))
    appear(fr, t, 0.8, box)
    for i, (lab, v, col, st) in enumerate(rows):
        y = 490 + i * 100
        appear(fr, t, st, lambda dd, dy, lab=lab, v=v, col=col, y=y: (text(dd, (170, y + dy), lab, F('s', 48), INK, 'lm'), text(dd, (W - 170, y + dy), v, F('b', 52), col, 'rm')))
    def big(dd, dy):
        dd.rounded_rectangle((110, 700 + dy, W - 110, 920 + dy), 34, fill=ACC)
        text(dd, (W // 2, 760 + dy), 'Eline geçecek net kıdem tazminatı', F('s', 42), (210, 236, 224), 'mm')
        text(dd, (W // 2, 850 + dy), tr(408542.12 * prog(t, 3.0, 1.3)) + ' ₺', F('x', 104), (255, 255, 255), 'mm')
    appear(fr, t, 2.8, big)

def s_tavan(fr, t, dur):
    header(fr, 'Dikkat', 'Maaşınız tavanın üstündeyse?')
    def a(dd, dy):
        card(dd, (110, 380 + dy, 930, 820 + dy))
        text(dd, (160, 440 + dy), 'Brüt maaş', F('s', 40), MUTED)
        text(dd, (160, 545 + dy), '100.000 ₺', F('x', 80), INK, 'lm')
        text(dd, (160, 630 + dy), 'ama hesapta kullanılan:', F('s', 40), MUTED)
        text(dd, (160, 740 + dy), '73.729,84 ₺', F('x', 80), ACC, 'lm')
    appear(fr, t, 0.6, a)
    def b(dd, dy):
        card(dd, (990, 380 + dy, W - 110, 820 + dy), fill=SOFT, outline=SOFT)
        text(dd, (1040, 440 + dy), '6 yıl 4 ay için net', F('s', 40), ACC)
        text(dd, (1040, 530 + dy), '463.411,46 ₺', F('x', 80), ACC, 'lm')
        for j, ln in enumerate(['Tavanın üstündeki kısım', 'tazminata yansımaz.']):
            text(dd, (1040, 640 + j * 58 + dy), ln, F('r', 40), INK)
    appear(fr, t, 2.2, b)
    appear(fr, t, 3.6, lambda dd, dy: text(dd, (110, 900 + dy), 'Tavan her yıl Ocak ve Temmuz\'da memur maaş katsayısıyla güncellenir.', F('s', 40), MUTED))

def s_cta(fr, t, dur):
    d = fr.d
    d.rectangle((0, 0, W, H), fill=ACC)
    appear(fr, t, 0.2, lambda dd, dy: text(dd, (W // 2, 230 + dy), 'Kendi tazminatınızı saniyeler içinde hesaplayın', F('x', 66), (255, 255, 255), 'mm'))
    def mock(dd, dy):
        x0, y0 = 560, 330 + dy
        dd.rounded_rectangle((x0, y0, x0 + 800, y0 + 480), 30, fill=CARD)
        for j, (lab, val) in enumerate([('İşe giriş tarihi', '01.03.2020'), ('İşten çıkış tarihi', '01.07.2026'), ('Son brüt ücret', '60.000')]):
            y = y0 + 50 + j * 100
            dd.text((x0 + 50, y), lab, font=F('s', 28), fill=MUTED)
            dd.rounded_rectangle((x0 + 50, y + 36, x0 + 750, y + 86), 12, fill=BG, outline=LINE, width=2)
            dd.text((x0 + 70, y + 61), val, font=F('s', 30), fill=INK, anchor='lm')
        dd.rounded_rectangle((x0 + 50, y0 + 370, x0 + 750, y0 + 440), 14, fill=SOFT)
        dd.text((x0 + 80, y0 + 405), 'Net kıdem tazminatı', font=F('s', 32), fill=INK, anchor='lm')
        dd.text((x0 + 720, y0 + 405), '377.115,80 ₺', font=F('x', 38), fill=ACC, anchor='rm')
    appear(fr, t, 0.8, mock)
    def url(dd, dy):
        dd.rounded_rectangle((W // 2 - 620, 880 + dy, W // 2 + 620, 980 + dy), 50, fill=(255, 255, 255))
        dd.text((W // 2, 930 + dy), 'hesapcantasi.com/kidem-tazminati-hesaplama', font=F('b', 46), fill=ACC, anchor='mm')
    appear(fr, t, 1.8, url)
    p = prog(t, 3.2, 0.6)
    if p > 0:
        fr.layer(p, lambda dd, dy: dd.text((W // 2, 1035), 'Link açıklamada  ↓', font=F('s', 32), fill=(210, 236, 224), anchor='mm'))

SCENES = [(s_intro, 4.5, False), (s_sartlar, 8.0, True), (s_adim1, 8.5, True), (s_adim2, 8.0, True), (s_adim3, 8.5, True), (s_net, 7.0, True), (s_tavan, 8.0, True), (s_cta, 6.5, False)]

def draw(i, t):
    fn, dur, foot = SCENES[i]
    fr = Frame(); fn(fr, t, dur)
    if foot: footer(fr, t, dur)
    # fade in/out to bg for scene transitions
    a = min(1, t / 0.25, (dur - t) / 0.25)
    if a < 1:
        bg = Image.new('RGB', (W, H), BG if i < len(SCENES) - 1 or t < dur / 2 else ACC)
        fr.im = Image.blend(bg, fr.im, max(0, a))
    return fr.im

def render_scene(i):
    fn, dur, _ = SCENES[i]
    tmp = f'{OUT}/scene{i:02d}.tmp.mp4'; final = f'{OUT}/scene{i:02d}.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
    for k in range(int(round(dur * FPS))):
        p.stdin.write(draw(i, k / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, final)
    else: sys.exit(f'scene {i} failed')

if __name__ == '__main__':
    if sys.argv[1:2] == ['stills']:
        for i, (fn, dur, _) in enumerate(SCENES):
            draw(i, dur - 0.6).save(f'{OUT}/still{i:02d}.jpg', quality=88)
    else:
        idx = [int(a) for a in sys.argv[1:]] or range(len(SCENES))
        for i in idx: render_scene(i)
        with open(f'{OUT}/list.txt', 'w') as f:
            for i in range(len(SCENES)): f.write(f"file 'scene{i:02d}.mp4'\n")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/list.txt', '-c', 'copy', f'{OUT}/kidem-tazminati-nasil-hesaplanir.mp4'], check=True)
        print('done')
