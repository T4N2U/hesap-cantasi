# YouTube upload kit: Ocak 2027 emekli ve memur zammı (Tuş & Eşittir) (publish 5 Jan 2027 or the day TÜİK publishes Aralık TÜFE; Short 2 days later)

**Status: TEMPLATE. Do not upload the ÖRNEK files.** The rates are final only when TÜİK publishes the December 2026 inflation
(early January; the exact date is in TÜİK's 2027 calendar, not out yet when this was built).
On that day (the scheduled task "Ocak zammı kesinleşiyor" does this):
1. `engine.js`: add the Kasım and Aralık TÜFE to `PARAMS.memurEmekli.aylar`, set `kalan: []`, `kesin: true` (source comment), `npm test`, push.
2. Here: `node data.mjs > data.json && python3 render_long.py && python3 render.py && python3 thumb.py`, then music
   (`python3 ../music.py <dur> long/music.wav playful-marimba`, same for short) and mux as in `../README.md`.
   With `kesin` the ÖRNEK watermark goes, "kesin değil" lines must be checked (they are tied to the 4-month preview text: remove them),
   and the thumbnail shows both rates.
3. Fill in the blanks below from data.json and upload. Note: the bubble says "Ocak 2027'de"; for another year check the suffix.

Characters: Tuş (C1, gold key; props: reading glasses + OCA calendar) and Eşittir (green "=" key). Text bubbles, no voice.
Music preset: `playful-marimba`. End screen from 30.5 s (render_long.py prints it). Topic motif: the calendar prop (this episode only).

## Long video
**Title:** Ocak 2027 Emekli ve Memur Zammı Belli Oldu: SSK, Bağ-Kur ve Memur Zam Oranı Hesaplama
**Description:**
Kendi maaşınla hesapla 👉 https://hesapcantasi.com/emekli-memur-zammi-hesaplama/?utm_source=youtube&utm_campaign=emekli

SSK ve Bağ-Kur emeklilerinin Ocak 2027 zammı: %___ (Temmuz–Aralık 2026 TÜFE, TÜİK).
Memur zammı: toplu sözleşme %5 + enflasyon farkı %___ = %___.

Örnek:
• 25.000 TL emekli aylığı → ___ TL
• 50.000 TL memur maaşı → ___ TL

• Emekli ve memur zammı hesaplama: https://hesapcantasi.com/emekli-memur-zammi-hesaplama/?utm_source=youtube&utm_campaign=emekli
• Maaş hesaplama: https://hesapcantasi.com/maas-hesaplama/?utm_source=youtube&utm_campaign=emekli

⚠️ Bilgilendirme amaçlıdır; kesin tutar için kurumunuzun bordrosunu kontrol edin.
#emeklizammı #memurzammı #ocak2027 #SSK #BağKur

**Tags:** emekli zammı 2027, ocak 2027 emekli zammı, memur zammı 2027, ssk bağkur zammı, emekli zam oranı, memur enflasyon farkı, emekli maaşı hesaplama, memur maaşı hesaplama, 6 aylık enflasyon, toplu sözleşme

**Pinned comment:** Kendi maaşınla hesapla 👉 https://hesapcantasi.com/emekli-memur-zammi-hesaplama/?utm_source=youtube&utm_campaign=emekli-comment

## Short
**Title:** Ocak 2027 emekli ve memur zammı ne kadar? #shorts
**Description:** Emekli zammı %___, memur zammı %___ (Temmuz–Aralık 2026 enflasyonu). Kendi maaşınla hesapla: https://hesapcantasi.com/emekli-memur-zammi-hesaplama/?utm_source=youtube&utm_campaign=emekli-short #emeklizammı #shorts
**Tags:** emekli zammı, memur zammı, ocak 2027, shorts
**Related video:** the long video (after it is public).
