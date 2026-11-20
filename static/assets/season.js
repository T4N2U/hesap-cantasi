// "Gündemde" calendar: which pages to put at the top of the homepage on a given date.
// Shared by the build (server-rendered default) and app.js (re-picked in the visitor's browser, so it
// stays right between deploys). Windows are 'MM-DD' (every year, may wrap over New Year) or 'YYYY-MM-DD'
// (one-off, e.g. bayram dates). `days: [from, to]` = those days of every month. Higher prio wins.
// {Y1} in a path is replaced with next year (asgari ücret page for the coming year).
export const GUNDEM = [
  { path: '/emlak-vergisi-hesaplama/', note: '2. taksitte son gün 30 Kasım', from: '10-20', to: '11-30', prio: 10 },
  { path: '/emlak-vergisi-hesaplama/', note: '1. taksitte son gün 31 Mayıs', from: '05-01', to: '05-31', prio: 10 },
  { path: '/emlak-vergisi-hesaplama/', note: '1. taksit dönemi başladı', from: '03-01', to: '04-30', prio: 6 },
  { path: '/asgari-ucret-{Y1}/', note: 'Yeni yıl rakamı bekleniyor: zam senaryoları', from: '11-10', to: '12-31', prio: 9 },
  { path: '/ikramiye-hesaplama/', note: 'Yıl sonu ikramiyesi net ne kalır?', from: '11-20', to: '12-31', prio: 8 },
  { path: '/maas-hesaplama/', note: 'Aralık’ta net maaş neden düşer?', from: '12-01', to: '12-31', prio: 7 },
  { path: '/maas-hesaplama/', note: 'Ocak zammıyla yeni net maaşın', from: '01-01', to: '01-31', prio: 9 },
  { path: '/maas-hesaplama/', note: 'Temmuz bordrosu ve vergi dilimi', from: '07-01', to: '07-31', prio: 8 },
  { path: '/zam-hesaplama/', note: 'Zam oranını hesapla', from: '12-20', to: '01-31', prio: 7 },
  { path: '/zam-hesaplama/', note: 'Temmuz zammı', from: '06-25', to: '07-31', prio: 7 },
  { path: '/kidem-tazminati-hesaplama/', note: 'Yeni kıdem tavanı', from: '12-28', to: '01-31', prio: 6 },
  { path: '/kidem-tazminati-hesaplama/', note: 'Temmuz kıdem tavanı', from: '06-28', to: '07-31', prio: 6 },
  { path: '/gelir-vergisi-dilimleri-{Y}/', note: 'Yeni yıl vergi dilimleri', from: '12-15', to: '01-31', prio: 6 },
  { path: '/kira-artis-hesaplama/', note: 'Bu ayın kira artış oranı açıklandı', days: [3, 10], prio: 8 },
  { path: '/fazla-mesai-hesaplama/', note: 'Ramazan Bayramı’nda çalışma ücreti', from: '2027-02-25', to: '2027-03-12', prio: 8 },
  { path: '/fazla-mesai-hesaplama/', note: 'Kurban Bayramı’nda çalışma ücreti', from: '2027-05-05', to: '2027-05-20', prio: 8 },
  { path: '/yillik-izin-hesaplama/', note: 'Tatil sezonu: kaç gün iznin var?', from: '05-15', to: '08-31', prio: 5 },
  { path: '/tapu-harci-hesaplama/', note: 'Ev alım sezonu: tapu masrafları', from: '03-01', to: '06-30', prio: 5 },
];
// Year-round favourites that fill the row when fewer than N seasonal items are active.
export const FALLBACK = ['/maas-hesaplama/', '/kidem-tazminati-hesaplama/', '/kira-artis-hesaplama/', '/tapu-harci-hesaplama/'];

const md = (d) => `${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const iso = (d) => `${d.getFullYear()}-${md(d)}`;
function active(g, d) {
  if (g.days) return d.getDate() >= g.days[0] && d.getDate() <= g.days[1];
  if (g.from.length === 10) { const t = iso(d); return t >= g.from && t <= g.to; }
  const t = md(d);
  return g.from <= g.to ? t >= g.from && t <= g.to : t >= g.from || t <= g.to;
}

// Returns [{path, note}] for date d, at most n, one per page, highest prio first.
export function pick(d = new Date(), n = 4, year = d.getFullYear()) {
  const fill = (p) => p.replace('{Y1}', String(year + 1)).replace('{Y}', String(year));
  const out = [], seen = new Set();
  for (const g of GUNDEM.filter((g) => active(g, d)).sort((a, b) => b.prio - a.prio)) {
    const path = fill(g.path);
    if (!seen.has(path)) { seen.add(path); out.push({ path, note: g.note }); }
  }
  for (const p of FALLBACK) if (out.length < n && !seen.has(p)) { seen.add(p); out.push({ path: p, note: null }); }
  return out.slice(0, n);
}
