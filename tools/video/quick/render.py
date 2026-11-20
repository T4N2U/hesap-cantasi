"""Quick-reaction Short template (1080x1920, ~15 s) for announcement days:
TÜİK kira artış oranı (each month ~3rd, 10:00) and TCMB faiz kararı (PPK days).
Only the JSON changes on the day; a full render (video + music) takes about a minute.

Look: "breaking news" — deep green band with a pulsing red date chip, white card, one huge number,
before→after strip, two or three bullets, closing URL card. Uses the channel logo.

Usage:
  python3 render.py card.json OUT.mp4 [--stills]
JSON fields:
  date        "3 Aralık 2026"            chip at the top
  kicker      "AÇIKLANDI"                word in the red chip
  headline    "Aralık kira artış oranı"  two lines max
  big         "%31,23"                   the number
  big_label   "Kira artışı üst sınırı"
  before      ["Kasım", "%31,49"]        optional: label + value
  after       ["Aralık", "%31,23"]       optional
  bullets     ["...", "..."]             2–3 short lines
  url         "hesapcantasi.com/kira-artis-hesaplama"
  preset      music.py preset (default playful-marimba)
  sample      true → big "ÖRNEK" watermark (for previews only)
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 15.0
HERE = os.path.dirname(os.path.abspath(__file__))
FD = '/usr/share/fonts/opentype/inter/'
_fc = {}
def F(w, s):
    k = (w, s)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FD + {'b': 'InterDisplay-Bold.otf', 'k': 'InterDisplay-Black.otf', 's': 'InterDisplay-SemiBold.otf'}[w], s)
    return _fc[k]

GREEN = (11, 82, 61); GREEN2 = (15, 107, 79); INK = (24, 30, 28); MUTED = (110, 120, 116); WHITE = (255, 255, 255)
RED = (214, 52, 46); PAPER = (246, 247, 244); LINE = (226, 230, 226); GOLD = (232, 176, 52)
M, R = 80, 920  # Shorts safe area: keep content left of x=920, between y≈250 and y≈1500

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def prog(t, s, d=0.4): return ease((t - s) / d)
def T(d, xy, s, f, fill=INK, a='la'): d.text(xy, s, font=f, fill=fill, anchor=a)

_LOGO = {}
def logo(size):
    if size not in _LOGO:
        _LOGO[size] = Image.open(os.path.join(HERE, '..', 'logo.png')).convert('RGBA').resize((size, size), Image.LANCZOS)
    return _LOGO[size]

def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        nxt = (cur + ' ' + w).strip()
        if d.textlength(nxt, font=f) <= width: cur = nxt
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def pop(im, t, s, fn, dur=0.35):
    """Slam-in: the element drops in at 115% and settles to 100% (this template's transition)."""
    p = prog(t, s, dur)
    if p <= 0: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay))
    if p < 1:
        k = 1.15 - .15 * p
        big = lay.resize((int(W * k), int(H * k)))
        ox, oy = (big.width - W) // 2, (big.height - H) // 2
        lay = big.crop((ox, oy, ox + W, oy + H))
        lay.putalpha(lay.getchannel('A').point(lambda v: int(v * p)))
    im.paste(lay, (0, 0), lay)

def frame(c, t):
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    # top band (sits behind the Shorts header area) + brand row
    d.rectangle((0, 0, W, 470), fill=GREEN)
    for x in range(-200, W, 60): d.line((x, 470, x + 200, 0), fill=GREEN2, width=14)
    lg = logo(56); im.paste(lg, (M, 260), lg); T(d, (M + 72, 288), 'Hesap Çantası', F('b', 32), WHITE, 'lm')
    # red chip pulses for the first seconds
    pulse = 1 + 0.06 * max(0, 1 - t / 4) * abs(((t * 2) % 2) - 1)
    kick = c.get('kicker', 'AÇIKLANDI')
    fk = F('k', int(36 * pulse)); kw = d.textlength(kick, font=fk) + 48
    d.rounded_rectangle((M, 350, M + kw, 350 + int(64 * pulse)), 14, fill=RED); T(d, (M + kw / 2, 350 + int(32 * pulse)), kick, fk, WHITE, 'mm')
    T(d, (M + kw + 24, 382), c.get('date', ''), F('b', 34), WHITE, 'lm')
    # headline card
    fh = F('k', 64); lines = wrap(d, c['headline'], fh, R - M - 60)[:2]
    pop(im, t, .2, lambda dd: (dd.rounded_rectangle((M - 20, 510, R + 20, 530 + 80 * len(lines) + 60), 30, fill=WHITE),
                                [T(dd, (M + 20, 570 + i * 80), ln, fh, INK) for i, ln in enumerate(lines)]))
    y0 = 600 + 80 * len(lines) + 40
    # big number
    bs = 230
    while d.textlength(c['big'], font=F('k', bs)) > R - M and bs > 120: bs -= 10
    def bign(dd):
        T(dd, ((M + R) // 2, y0 + 150), c['big'], F('k', bs), GREEN2, 'mm')
        T(dd, ((M + R) // 2, y0 + 300), c.get('big_label', ''), F('b', 44), MUTED, 'mm')
    pop(im, t, 1.0, bign, .45)
    y1 = y0 + 370
    if c.get('before') and c.get('after'):
        def ba(dd):
            dd.rounded_rectangle((M, y1, R, y1 + 120), 24, fill=WHITE, outline=LINE, width=3)
            T(dd, (M + 30, y1 + 60), f"{c['before'][0]}: {c['before'][1]}", F('s', 40), MUTED, 'lm')
            T(dd, ((M + R) // 2 + 40, y1 + 60), '→', F('k', 48), GOLD, 'mm')
            T(dd, (R - 30, y1 + 60), f"{c['after'][0]}: {c['after'][1]}", F('k', 42), INK, 'rm')
        pop(im, t, 2.6, ba); y1 += 150
    for i, b in enumerate(c.get('bullets', [])[:3]):
        fb = F('s', 40); bl = wrap(d, b, fb, R - M - 70)[:2]
        yy = y1 + i * 120
        pop(im, t, 4.0 + i * .8, lambda dd, bl=bl, yy=yy: (dd.ellipse((M, yy + 12, M + 28, yy + 40), fill=GOLD),
                                                            [T(dd, (M + 50, yy + j * 50), ln, fb, INK) for j, ln in enumerate(bl)]))
    # closing URL card over everything
    if t > DUR - 4.2:
        def cta(dd):
            dd.rounded_rectangle((M - 20, 1180, R + 20, 1480), 34, fill=GREEN)
            T(dd, ((M + R) // 2, 1260), 'Kendin hesapla', F('k', 58), WHITE, 'mm')
            dd.rounded_rectangle((M + 20, 1320, R - 20, 1430), 55, fill=WHITE)
            u = c['url']; fu = F('k', 44 if len(u) < 30 else 34)
            T(dd, ((M + R) // 2, 1375), u, fu, INK, 'mm')
        pop(im, t, DUR - 4.2, cta)
    if c.get('sample'):
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        T(ld, (W // 2, 1000), 'ÖRNEK', F('k', 260), (214, 52, 46, 70), 'mm'); im.paste(lay.rotate(25, center=(W // 2, 1000)), (0, 0), lay.rotate(25, center=(W // 2, 1000)))
    # progress bar under the band
    d = ImageDraw.Draw(im); d.rectangle((0, 470, int(W * t / DUR), 480), fill=GOLD)
    a = min(1, t / .2, (DUR - t) / .2)
    if a < 1: im = Image.blend(Image.new('RGB', (W, H), PAPER), im, max(0, a))
    return im

def main():
    card, out = sys.argv[1], sys.argv[2]
    c = json.load(open(card, encoding='utf-8'))
    if '--stills' in sys.argv:
        for i, t in enumerate((2.2, 7.5, DUR - 1)): frame(c, t).save(out.replace('.mp4', f'-still{i}.jpg'), quality=85)
        return
    tmp = tempfile.mkdtemp()
    silent, wav = os.path.join(tmp, 's.mp4'), os.path.join(tmp, 'm.wav')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
    for k in range(int(DUR * FPS)): p.stdin.write(frame(c, k / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0: sys.exit('render failed')
    subprocess.run([sys.executable, os.path.join(HERE, '..', 'music.py'), str(DUR), wav, c.get('preset', 'playful-marimba')], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', silent, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', f'loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=out:st={DUR - 1.5}:d=1.5', '-c:a', 'aac', '-b:a', '192k', '-shortest', out + '.tmp.mp4'], check=True)
    os.replace(out + '.tmp.mp4', out)
    print('ok', out)

if __name__ == '__main__':
    main()
