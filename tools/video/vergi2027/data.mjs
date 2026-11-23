// Exports every figure the video shows, straight from the site's engine (PARAMS), so the video
// always matches the website. Re-run after engine.js gets the official tarife.
import * as E from '../../../static/assets/engine.js';
const P = E.PARAMS;
const examples = [40000, 75000, 120000].map((brut) => {
  const r = E.brutNet(brut);
  return { brut, dilim: r.aylar.map((a) => a.dilim), ocakNet: r.aylar[0].net, aralikNet: r.aylar[11].net, yillikGV: r.toplam.gv };
});
const official = P.year >= 2027;
console.log(JSON.stringify({
  year: P.year, official,
  dilimler: P.gvDilim.map(([l, r]) => ({ ust: l === Infinity ? null : l, oran: r })),
  aralik: official ? null : P.gvDilim.slice(0, 4).map(([l]) => E.dilimAraligi(l)),
  nextYear: P.yenidenDegerleme.uygulanacakYil, yd: P.yenidenDegerleme.oran,
  examples,
}));
