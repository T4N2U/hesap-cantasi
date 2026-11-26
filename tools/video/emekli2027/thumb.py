"""Thumbnail 1280x720 with Tuş & Eşittir. No figures until PARAMS.memurEmekli is final; then it shows both rates."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'mascot'))
from tus_variants import keycap, face, F, GOLD, GOLD_D, GREEN_D, INK, WHITE
from PIL import Image, ImageDraw
D = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8')); KESIN = D['kesin'] and not D['kalan']
tr = lambda n: f'{n:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
W, H = 1280, 720; im = Image.new('RGB', (W, H), (246, 241, 230)); d = ImageDraw.Draw(im, 'RGBA')
d.text((60, 70), 'OCAK ZAMMI', font=F('k', 120), fill=GREEN_D)
d.text((64, 210), 'Emekli & Memur', font=F('k', 84), fill=INK)
if KESIN:
    d.rounded_rectangle((60, 340, 640, 440), 50, fill=GOLD); d.text((350, 390), f"Emekli %{tr(D['enf'])}", font=F('k', 52), fill=INK, anchor='mm')
    d.rounded_rectangle((60, 460, 640, 560), 50, fill=(32, 138, 104)); d.text((350, 510), f"Memur %{tr(D['memurOran'])}", font=F('k', 52), fill=WHITE, anchor='mm')
else:
    d.rounded_rectangle((60, 350, 600, 450), 50, fill=GOLD); d.text((330, 400), 'Ne kadar olacak?', font=F('k', 52), fill=INK, anchor='mm')
keycap(d, 870, 470, 1.5, GOLD, GOLD_D, 0); face(d, 870, 443, 1.5, 0, 0, 'open')
for sx in (-1, 1): d.ellipse((870 + sx * 51 - 37, 470 - 64 - 1, 870 + sx * 51 + 37, 470 + 10), outline=INK, width=7)
keycap(d, 1110, 520, 1.1, (32, 138, 104), GREEN_D, 0, '=', WHITE); face(d, 1110, 500, 1.1, 0, 0, 'smile')
lg = Image.open(os.path.join(HERE, '..', 'logo.png')).convert('RGBA').resize((80, 80)); im.paste(lg, (1170, 30), lg)
im.save(os.path.join(HERE, 'thumbnail-emekli-memur.jpg'), quality=90)
