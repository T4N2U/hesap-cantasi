# Video tools

Scripts that produce the Hesap Çantası YouTube videos. They are not part of the website build.

- `kidem/render.py`: 1920×1080 explainer (PIL frames piped to ffmpeg, one file per scene, joined with concat).
- `kidem-short/render.py`: 1080×1920 Shorts version, with content kept inside the Shorts UI safe area.
- `music.py DURATION OUT.wav PRESET`: original synthesized background music (no samples, no copyright).
- Add sound: `ffmpeg -i silent.mp4 -i music.wav -map 0:v -map 1:a -c:v copy -af loudnorm=I=-18:TP=-1.5:LRA=11 -c:a aac -b:a 192k -shortest out.mp4` (use `I=-16` for Shorts).
- Always take figures from `static/assets/engine.js` so videos match the site.

## Music: same melody, different arrangement for each video

Every video uses the channel's signature chord progression and melody (`CHORDS`, `MELODY` in `music.py`).
Only the arrangement changes. Keep it safe: calm tempo, soft attacks, gentle or no drums.

| Preset | Feel | Used by |
|---|---|---|
| `playful-marimba` | bouncy marimba arpeggio, shaker | kıdem tazminatı (long + Short) |
| `lofi-piano` | slow swung piano chords, soft kick/snare, light vinyl | |
| `acoustic-pluck` | nylon-guitar arpeggio, shaker | maaş: Aralık'ta maaşım neden düşüyor? (long + Short) |
| `rhodes-groove` | warm electric piano, soft pop beat | |
| `musicbox-light` | music box over a pad, no drums | |
| `soft-pad` | sustained pads, music-box melody, heartbeat kick | |

Rotate presets so neighbouring videos in the schedule never share one. A long video and its Short use the same preset.
Record the preset in the table above when a video is made.

## Visual style: familiar, not identical

**Always the same (the brand):**
- the ₺ logo chip and "Hesap Çantası" wordmark, `hesapcantasi.com` on the closing card
- Inter Display typography and type scale; numbers in Turkish format (`408.542,12 ₺`)
- green `#0f6b4f` as the brand color; a closing card with the page URL
- numbers that count up, with figures taken from the site's engine

**Changes from video to video (pick a different combination each time):**
- *topic accent*: a second color for the series (e.g. maaş = blue, vergi = amber, kira = terracotta, kredi = purple, tazminat = gold), used for highlights, bars and the thumbnail band
- *background*: light paper, dark green, a soft tinted gradient, or a faint grid/pattern of the topic's symbols
- *layout*: cards in a column, a split screen (formula left, result right), a single big number, a timeline/month strip (for bordro videos), a receipt/bordro-style document
- *transitions*: fade, slide, wipe, card flip, zoom on the number
- *a topic visual*: a payslip for maaş, a calendar for kira, a house for emlak/tapu, a car for MTV, a bank card for kredi
- *thumbnail layout*: big question, a big number, or a before/after comparison

## Scheduling rule (from the owner)

Build blocks are offered at 22:00 Istanbul time with a phone notification ("evet / atla").
- "evet": build now.
- "atla", or no reply: build the same job at **03:00 the next night** without asking again, and report the result in the morning.
