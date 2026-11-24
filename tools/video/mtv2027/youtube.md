# YouTube upload kit: MTV 2027 ne kadar? 1. taksitte son gün Ocak sonu (publish 19 Jan 2027, Short 21 Jan)

**Status: TEMPLATE. Do not upload the ÖRNEK files.** The 2027 MTV increase is set by Cumhurbaşkanı kararı in late December
(197 s. MTV Kanunu md. 10: between 20% and 150% of the yeniden değerleme rate, i.e. %5,57–%41,75 for 2027).
On that day:
1. Update `engine.js`: `mtvYil: 2027`, `mtvArtis` (the decided rate), the new `mtv2018` / `mtvEski` tables from the
   MTV Genel Tebliği (source comment with the tebliğ number; check every row against a second source), run `npm test`, push.
2. Here: `node data.mjs > data.json && python3 render.py long && python3 render.py short && python3 thumb.py`, then add music:
   `python3 ../music.py <long dur> long/music.wav acoustic-pluck` (same for short), mux as in `../README.md`.
   With `official: true` the ÖRNEK watermark goes, the examples show 2027 amounts and the range scene becomes "2027 MTV %X arttı".
3. Fill in the blanks below from data.json and upload.

Renderer: `render.py` (data-driven). Music preset: `acoustic-pluck`. Visual variant: asphalt, number-plate cards, road-yellow accent,
cards drive in from the right, moving lane dashes. End screen: `render.py long` prints "end screen from N s" (preview: 33.5 s).

## Long video
**Title:** MTV 2027 Ne Kadar? Motor Hacmi ve Yaşa Göre Örnekler, 1. Taksit Ocak Sonu
**Description:**
Kendi aracının MTV'sini hesapla 👉 https://hesapcantasi.com/mtv-hesaplama/?utm_source=youtube&utm_campaign=mtv

Motorlu taşıtlar vergisi otomobilde motor hacmine, aracın yaşına ve (2018 ve sonrası tescilde) taşıt değerine göre belirlenir.
2027'de MTV %___ artırıldı (Cumhurbaşkanı kararı, ___ tarihli Resmî Gazete).

Örnekler (2027, yıllık):
• 1.0 motor, 2027 model, 900.000 TL: ___ TL (2 taksit × ___ TL)
• 1.6 motor, 2024 model, 450.000 TL: ___ TL (2 taksit × ___ TL)
• 1.6 motor, 2015 model (2018 öncesi tescil): ___ TL (2 taksit × ___ TL)

Ödeme: 1. taksit Ocak sonuna, 2. taksit Temmuz sonuna kadar.

• MTV hesaplama: https://hesapcantasi.com/mtv-hesaplama/?utm_source=youtube&utm_campaign=mtv

⚠️ Bilgilendirme amaçlıdır; kesin tutar için GİB / Dijital Vergi Dairesi'ni kontrol edin.
#MTV #motorlutaşıtlarvergisi #MTV2027 #araç

**Tags:** mtv 2027, mtv ne kadar, mtv hesaplama, motorlu taşıtlar vergisi 2027, mtv zammı, mtv 2027 zam oranı, mtv taksit, araç vergisi, mtv son ödeme günü, mtv 1600 cc

**Pinned comment:** Kendi aracının MTV'sini hesapla 👉 https://hesapcantasi.com/mtv-hesaplama/?utm_source=youtube&utm_campaign=mtv-comment

## Short
**Title:** MTV 2027: aracın için ne kadar ödeyeceksin? #shorts
**Description:** 2027'de MTV %___ arttı. 1.6 motor, 2024 model araç için yıllık ___ TL. 1. taksit Ocak sonuna kadar. Kendininkini hesapla: https://hesapcantasi.com/mtv-hesaplama/?utm_source=youtube&utm_campaign=mtv-short #MTV #shorts
**Tags:** mtv 2027, mtv hesaplama, motorlu taşıtlar vergisi, shorts
**Related video:** the long MTV video (only after it is public, 19 Jan).
