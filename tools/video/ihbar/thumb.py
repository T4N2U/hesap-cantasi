"""Thumbnail 1280x720: question + the 2/4/6/8 weeks ladder (figures from the law, not year-dependent)."""
import json, os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8'))
FD = '/usr/share/fonts/opentype/inter/'; F = lambda w, s: ImageFont.truetype(FD + {'k': 'InterDisplay-Black.otf', 'b': 'InterDisplay-Bold.otf'}[w], s)
BG = (38, 24, 52); MINT = (110, 231, 183); MINT_D = (24, 120, 90); INK = (246, 242, 250); CARD = (56, 38, 74); DARK = (24, 14, 34)
im = Image.new('RGB', (1280, 720), BG); d = ImageDraw.Draw(im)
d.text((60, 60), 'İHBAR', font=F('k', 170), fill=INK); d.text((64, 240), 'TAZMİNATI', font=F('k', 110), fill=MINT)
d.rounded_rectangle((60, 410, 560, 500), 45, fill=MINT); d.text((310, 455), 'Kaç hafta, ne kadar?', font=F('b', 44), fill=DARK, anchor='mm')
for i, (lab, w) in enumerate(D['sureler']):
    x = 700 + i * 140; h = 90 + w * 45; y0 = 640 - h
    d.rounded_rectangle((x, y0, x + 110, 640), 16, fill=MINT if i == 3 else CARD); d.rectangle((x, y0, x + 110, y0 + 24), fill=MINT_D if i == 3 else (84, 62, 104))
    d.text((x + 55, y0 - 30), f'{w} hafta', font=F('k', 30), fill=INK, anchor='mm')
lg = Image.open(os.path.join(HERE, '..', 'logo.png')).convert('RGBA').resize((80, 80)); im.paste(lg, (1170, 30), lg)
im.save(os.path.join(HERE, 'thumbnail-ihbar.jpg'), quality=90)
