// Figures for the Tuş & Eşittir emekli/memur Short, straight from the site's engine (PARAMS.memurEmekli).
// Until all 6 months are in (Aralık TÜFE, ~5 Jan), the render is a preview with an ÖRNEK watermark.
import * as E from '../../../static/assets/engine.js';
const M = E.PARAMS.memurEmekli;
const enf = E.kumulatifTufe(M.aylar) * 100;
const memur = E.memurEmekliZam({ maas: 100, tur: 'memur', enf });
console.log(JSON.stringify({
  donem: M.donem, kesin: M.kesin, aylar: M.aylar, kalan: M.kalan, tsOnceki: M.tsOnceki, tsYeni: M.tsYeni,
  enf, memurOran: memur.oran * 100, fark: memur.fark * 100,
}));
