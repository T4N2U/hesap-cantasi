# Video tools

Scripts that produce the Hesap Çantası YouTube videos. They are not part of the website build.

- `kidem/render.py`: 1920×1080 explainer (PIL frames piped to ffmpeg, one file per scene, joined with concat).
- `kidem-short/render.py`: 1080×1920 Shorts version, with content kept inside the Shorts UI safe area.
- `kidem/music.py DURATION OUT.wav`: original synthesized "playful plucks" background track (no samples).
- Add sound: `ffmpeg -i silent.mp4 -i music.wav -map 0:v -map 1:a -c:v copy -af loudnorm=I=-18:TP=-1.5:LRA=11 -c:a aac -b:a 192k -shortest out.mp4`
- Always take figures from `static/assets/engine.js` so videos match the site.
