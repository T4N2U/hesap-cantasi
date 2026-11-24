// Every figure the MTV video shows, straight from the site's engine (PARAMS + mtv()), so the video always matches
// the website. Until engine.js holds the official 2027 tarife (mtvYil 2027), this is a preview: 2026 amounts and the
// legal range of the 2027 increase (197 s. Kanun md. 10). Re-run after the Cumhurbaşkanı kararı / tebliğ.
import * as E from '../../../static/assets/engine.js';
const P = E.PARAMS, Y = P.mtvYil;
const cars = [
  { ad: 'Yeni araç', detay: '1.0 motor · ' + Y + ' model · 900.000 ₺', cc: 999, modelYili: Y, deger: 900000, tescil2018: true },
  { ad: '4 yaşında', detay: '1.6 motor · ' + (Y - 3) + ' model · 450.000 ₺', cc: 1598, modelYili: Y - 3, deger: 450000, tescil2018: true },
  { ad: '2018 öncesi tescil', detay: '1.6 motor · 2015 model', cc: 1598, modelYili: 2015, deger: 0, tescil2018: false },
].map((c) => { const r = E.mtv(c); return { ...c, yillik: r.yillik, taksit: r.taksit, grup: r.grup }; });
const yd = P.yenidenDegerleme, nx = E.mtvSonrakiYil(0);
console.log(JSON.stringify({
  yil: Y, official: Y >= 2027, artis: P.mtvArtis,
  next: { yil: yd.uygulanacakYil, oran: yd.oran, alt: nx.altOran, ust: nx.ustOran },
  cars,
}));
