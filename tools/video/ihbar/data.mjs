// Figures for the ihbar video, from the site's engine (E.ihbar, PARAMS.damga). Notice periods: 4857 s. İş Kanunu md. 17.
// Tax: ihbar is wage income (GVK 61): gelir vergisi + damga vergisi, no SGK premium. The example uses the first bracket
// rate (%15, GVK 103), which doesn't change with the yearly bracket limits, so no re-render is needed in January.
import * as E from '../../../static/assets/engine.js';
const brut = 40000;
const ex = E.ihbar({ baslangic: '2023-01-15', bitis: '2027-01-15', brut, gvOran: 0.15 });
const sureler = [['6 aydan az', 2], ['6 ay – 1,5 yıl', 4], ['1,5 – 3 yıl', 6], ['3 yıldan fazla', 8]];
// check the engine agrees with the law table
for (const [b, h, w] of [['2026-07-01', '2026-12-01', 2], ['2026-01-01', '2026-12-01', 4], ['2025-01-01', '2026-12-01', 6], ['2022-01-01', '2026-12-01', 8]])
  if (E.ihbar({ baslangic: b, bitis: h, brut }).hafta !== w) throw new Error('engine disagrees with İş K. 17 table');
console.log(JSON.stringify({ sureler, damga: E.PARAMS.damga, ex: { maas: brut, yil: 4, ...ex } }));
