"""End-screen-friendly closing scene for long (16:9, 1920x1080) videos.

YouTube's "1 video, 1 subscribe" end-screen template puts a video box bottom-left and a Subscribe
circle bottom-right. These zones were measured from YouTube Studio's end-screen editor (Nov 2026),
with a margin added. Keep the closing scene's content OUT of them, so the end-screen elements never
cover our text.

Usage in a render.py (long videos only; Shorts have no end screens):
    from endscreen import CTA_SEC, SAFE_BOTTOM, labels, guides
    - make the closing scene CTA_SEC seconds long
    - draw all content above SAFE_BOTTOM (y < 520)
    - call labels(draw, font, colour) to add the small "Sıradaki video" / "Abone ol" hints
    - guides(img) draws the zones in red for your own still checks (never in the final render)
In YouTube Studio: Editor → End screen → Apply template → "1 video, 1 subscribe", then set both
elements to start at the closing scene's start time (shown by render.py as 'end screen from').
"""
from PIL import ImageDraw

CTA_SEC = 10.0          # closing scene length; YouTube allows 5–20 s of end screen
SAFE_BOTTOM = 520       # all closing-scene content stays above this line
VIDEO_ZONE = (40, 540, 700, 940)       # x0, y0, x1, y1 on 1920x1080
SUB_ZONE = (1540, 540, 1880, 920)


def labels(d, font, fill):
    """Small hints right above the two zones."""
    d.text(((VIDEO_ZONE[0] + VIDEO_ZONE[2]) // 2, VIDEO_ZONE[1] - 6), 'Sıradaki video', font=font, fill=fill, anchor='md')
    d.text(((SUB_ZONE[0] + SUB_ZONE[2]) // 2, SUB_ZONE[1] - 6), 'Abone ol', font=font, fill=fill, anchor='md')


def guides(im):
    d = ImageDraw.Draw(im)
    for z in (VIDEO_ZONE, SUB_ZONE): d.rectangle(z, outline=(255, 0, 0), width=4)
    d.line((0, SAFE_BOTTOM, im.width, SAFE_BOTTOM), fill=(255, 0, 0), width=2)
    return im


def start_time(scenes):
    """Seconds from video start to the closing scene (the end-screen start to set in Studio)."""
    return sum(d for _, d in scenes[:-1])
