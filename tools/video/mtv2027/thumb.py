"""Thumbnail 1280x720. No figures until the official 2027 rate is in engine.js (then it adds the '%X zam' badge)."""
import json, os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8'))
FD = '/usr/share/fonts/opentype/inter/'
F = lambda w, s: ImageFont.truetype(FD + {'k': 'InterDisplay-Black.otf', 'b': 'InterDisplay-Bold.otf'}[w], s)
W, H = 1280, 720; BG = (34, 37, 42); YEL = (250, 204, 21); INK = (240, 242, 245); PINK = (20, 24, 30); BLUE = (0, 61, 165)
im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
d.rectangle((0, 640, W, 700), fill=(46, 50, 56))
for x in range(0, W, 130): d.rectangle((x, 664, x + 70, 676), fill=YEL)
yr = D['yil'] if D['official'] else D['next']['yil']
d.text((60, 60), f'MTV {yr}', font=F('k', 190), fill=YEL)
d.text((64, 270), 'ne kadar?', font=F('k', 120), fill=INK)
d.rounded_rectangle((60, 440, 620, 540), 50, fill=YEL); d.text((340, 490), '1. taksit: Ocak sonu', font=F('b', 46), fill=PINK, anchor='mm')
# number plate
x, y, w, h = 760, 330, 470, 150
d.rounded_rectangle((x, y, x + w, y + h), 16, fill=(248, 248, 246), outline=PINK, width=5)
d.rounded_rectangle((x + 5, y + 5, x + 68, y + h - 5), 10, fill=BLUE); d.text((x + 36, y + h - 28), 'TR', font=F('b', 32), fill=(255, 255, 255), anchor='mm')
d.text((x + 68 + (w - 68) / 2, y + h / 2), 'HESAPLA' if not D['official'] else f"%{str(D['artis']).replace('.', ',')} zam", font=F('k', 64 if not D['official'] else 58), fill=PINK, anchor='mm')
lg = Image.open(os.path.join(HERE, '..', 'logo.png')).convert('RGBA').resize((90, 90)); im.paste(lg, (1150, 40), lg)
im.save(os.path.join(HERE, 'thumbnail-mtv-2027.jpg'), quality=90)
