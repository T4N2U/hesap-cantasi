// Hesap engine — all calculations, shared by the browser and the build script.
// Update PARAMS when official rates change (January / July, monthly for kira).

export const PARAMS = {
  year: 2026,
  updated: '2026-11-05',
  asgariBrut: 33030.00,
  asgariNet: 28075.50,
  sgkIsci: 0.14,
  issizlikIsci: 0.01,
  sgkIsveren: 0.2175,      // 5 puan teşviksiz
  sgkIsverenTesvik: 0.1675, // 5 puan teşvikli
  issizlikIsveren: 0.02,
  sgkTavan: 297270.00,
  damga: 0.00759,
  // Ücret gelirleri tarifesi (GVK 103, 332 Seri No.lu Tebliğ)
  gvDilim: [
    [190000, 0.15],
    [400000, 0.20],
    [1500000, 0.27],
    [5300000, 0.35],
    [Infinity, 0.40],
  ],
  kidemTavan: [
    { from: '2026-01-01', to: '2026-06-30', tutar: 64948.77 },
    { from: '2026-07-01', to: '2026-12-31', tutar: 73729.84 },
  ],
  stopaj: [ // TL mevduat, gün sınırına göre
    { maxGun: 182, oran: 0.175 },
    { maxGun: 365, oran: 0.15 },
    { maxGun: Infinity, oran: 0.10 },
  ],
  kkdf: 0.15,
  bsmvTuketici: 0.15,
  kiraOranlari: [ // 12 aylık ortalama TÜFE — uygulandığı ay
    { ay: 'Kasım 2026', oran: 31.23 },
    { ay: 'Ekim 2026', oran: 31.49 },
    { ay: 'Eylül 2026', oran: 31.79 },
  ],
};

export const r2 = (x) => Math.round((x + Number.EPSILON) * 100) / 100;

export function gelirVergisi(matrah, dilim = PARAMS.gvDilim) {
  let tax = 0, prev = 0;
  for (const [limit, rate] of dilim) {
    if (matrah <= prev) break;
    tax += (Math.min(matrah, limit) - prev) * rate;
    prev = limit;
  }
  return tax;
}

export function marjinalOran(matrah) {
  for (const [limit, rate] of PARAMS.gvDilim) if (matrah < limit) return rate;
  return 0.40;
}

export const AYLAR = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];

// One month of payroll given gross and cumulative bases before this month.
function bordroAy(brut, cum, cumAsgari, tesvik) {
  const P = PARAMS;
  const sgkMatrah = Math.min(brut, P.sgkTavan);
  const sgk = sgkMatrah * P.sgkIsci;
  const issizlik = sgkMatrah * P.issizlikIsci;
  const gvMatrah = brut - sgk - issizlik;
  const gvHam = gelirVergisi(cum + gvMatrah) - gelirVergisi(cum);
  const aMatrah = P.asgariBrut * (1 - P.sgkIsci - P.issizlikIsci);
  const gvIstisna = gelirVergisi(cumAsgari + aMatrah) - gelirVergisi(cumAsgari);
  const gv = Math.max(0, gvHam - gvIstisna);
  const damga = Math.max(0, brut * P.damga - P.asgariBrut * P.damga);
  const net = brut - sgk - issizlik - gv - damga;
  const isverenOran = (tesvik ? P.sgkIsverenTesvik : P.sgkIsveren) + P.issizlikIsveren;
  const maliyet = brut + sgkMatrah * isverenOran;
  return {
    brut: r2(brut), sgk: r2(sgk), issizlik: r2(issizlik), gvMatrah: r2(gvMatrah),
    kumulatif: r2(cum + gvMatrah), gv: r2(gv), gvIstisna: r2(Math.min(gvIstisna, gvHam)),
    damga: r2(damga), net: r2(net), maliyet: r2(maliyet),
    dilim: marjinalOran(cum + gvMatrah),
    _gvMatrah: gvMatrah, _aMatrah: aMatrah,
  };
}

// Brütten nete: brut can be a number (same every month) or array of 12.
export function brutNet(brut, { tesvik = true } = {}) {
  const list = Array.isArray(brut) ? brut : Array(12).fill(brut);
  let cum = 0, cumA = 0;
  const aylar = list.map((b, i) => {
    const row = bordroAy(b, cum, cumA, tesvik);
    cum += row._gvMatrah; cumA += row._aMatrah;
    delete row._gvMatrah; delete row._aMatrah;
    return { ay: AYLAR[i], ...row };
  });
  const toplam = {};
  for (const k of ['brut','sgk','issizlik','gv','damga','net','maliyet'])
    toplam[k] = r2(aylar.reduce((s, a) => s + a[k], 0));
  return { aylar, toplam, ortalamaNet: r2(toplam.net / 12) };
}

// Netten brüte: find the gross for each month that yields the target net.
export function netBrut(net, { tesvik = true } = {}) {
  const targets = Array.isArray(net) ? net : Array(12).fill(net);
  let cum = 0, cumA = 0;
  const brutler = [];
  targets.forEach((t) => {
    let lo = t, hi = t * 2.5 + 10000;
    for (let i = 0; i < 80; i++) {
      const mid = (lo + hi) / 2;
      if (bordroAy(mid, cum, cumA, tesvik).net < t) lo = mid; else hi = mid;
    }
    const b = r2(hi);
    const row = bordroAy(b, cum, cumA, tesvik);
    cum += row._gvMatrah; cumA += row._aMatrah;
    brutler.push(b);
  });
  return brutNet(brutler, { tesvik });
}

function tavanFor(dateStr) {
  const t = PARAMS.kidemTavan.find((x) => dateStr >= x.from && dateStr <= x.to);
  return t ? t.tutar : PARAMS.kidemTavan[PARAMS.kidemTavan.length - 1].tutar;
}

export function sureHesapla(baslangic, bitis) {
  const a = new Date(baslangic + 'T00:00:00Z'), b = new Date(bitis + 'T00:00:00Z');
  if (!(b > a)) return null;
  let y = b.getUTCFullYear() - a.getUTCFullYear();
  let m = b.getUTCMonth() - a.getUTCMonth();
  let d = b.getUTCDate() - a.getUTCDate();
  if (d < 0) { m -= 1; d += new Date(Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), 0)).getUTCDate(); }
  if (m < 0) { y -= 1; m += 12; }
  const toplamGun = Math.round((b - a) / 86400000);
  return { yil: y, ay: m, gun: d, toplamGun };
}

// Kıdem tazminatı: giydirilmiş brüt ücret, tavanla sınırlı; yalnız damga vergisi kesilir.
export function kidem({ baslangic, bitis, brut, yanHaklar = 0 }) {
  const s = sureHesapla(baslangic, bitis);
  if (!s) return { hata: 'Çıkış tarihi giriş tarihinden sonra olmalı.' };
  if (s.yil < 1) return { hata: 'Kıdem tazminatı için en az 1 yıl çalışmış olmak gerekir.', sure: s };
  const giydirilmis = brut + yanHaklar;
  const tavan = tavanFor(bitis);
  const esas = Math.min(giydirilmis, tavan);
  const brutTaz = esas * s.yil + (esas / 12) * s.ay + (esas / 365) * s.gun;
  const damga = brutTaz * PARAMS.damga;
  return {
    sure: s, giydirilmis: r2(giydirilmis), tavan, esas: r2(esas), tavanUygulandi: giydirilmis > tavan,
    brut: r2(brutTaz), damga: r2(damga), net: r2(brutTaz - damga),
  };
}

// İhbar tazminatı: 4857/17 — süreye göre 2/4/6/8 hafta; GV + damga kesilir.
export function ihbar({ baslangic, bitis, brut, yanHaklar = 0, gvOran = 0.15 }) {
  const s = sureHesapla(baslangic, bitis);
  if (!s) return { hata: 'Çıkış tarihi giriş tarihinden sonra olmalı.' };
  const aylar = s.yil * 12 + s.ay + s.gun / 30;
  const hafta = aylar < 6 ? 2 : aylar < 18 ? 4 : aylar < 36 ? 6 : 8;
  const gunluk = (brut + yanHaklar) / 30;
  const brutTaz = gunluk * hafta * 7;
  const gv = brutTaz * gvOran, damga = brutTaz * PARAMS.damga;
  return { sure: s, hafta, gun: hafta * 7, gunluk: r2(gunluk), brut: r2(brutTaz), gv: r2(gv), damga: r2(damga), net: r2(brutTaz - gv - damga) };
}

export function kiraArtis(kira, oran = PARAMS.kiraOranlari[0].oran) {
  const artis = kira * oran / 100;
  return { kira: r2(kira), oran, artis: r2(artis), yeni: r2(kira + artis), yillikFark: r2(artis * 12) };
}

// Kredi: aylık akdi faiz + KKDF/BSMV (konutta yok). Eşit taksitli ödeme planı.
export const KREDI_TURLERI = {
  ihtiyac: { ad: 'İhtiyaç kredisi', kkdf: PARAMS.kkdf, bsmv: PARAMS.bsmvTuketici },
  tasit: { ad: 'Taşıt kredisi', kkdf: PARAMS.kkdf, bsmv: PARAMS.bsmvTuketici },
  konut: { ad: 'Konut kredisi', kkdf: 0, bsmv: 0 },
};
export function kredi({ tutar, vade, aylikFaiz, tur = 'ihtiyac' }) {
  const t = KREDI_TURLERI[tur] || KREDI_TURLERI.ihtiyac;
  const f = aylikFaiz / 100;
  const r = f * (1 + t.kkdf + t.bsmv);
  const taksit = r === 0 ? tutar / vade : tutar * r / (1 - Math.pow(1 + r, -vade));
  let kalan = tutar; const plan = [];
  let topFaiz = 0, topKkdf = 0, topBsmv = 0;
  for (let i = 1; i <= vade; i++) {
    const faiz = kalan * f, kkdf = faiz * t.kkdf, bsmv = faiz * t.bsmv;
    let anapara = taksit - faiz - kkdf - bsmv;
    if (i === vade) anapara = kalan;
    kalan = Math.max(0, kalan - anapara);
    topFaiz += faiz; topKkdf += kkdf; topBsmv += bsmv;
    plan.push({ no: i, taksit: r2(i === vade ? anapara + faiz + kkdf + bsmv : taksit), anapara: r2(anapara), faiz: r2(faiz), kkdf: r2(kkdf), bsmv: r2(bsmv), kalan: r2(kalan) });
  }
  const toplam = plan.reduce((s, p) => s + p.taksit, 0);
  return { tur: t.ad, taksit: r2(taksit), toplam: r2(toplam), faiz: r2(topFaiz), kkdf: r2(topKkdf), bsmv: r2(topBsmv), maliyet: r2(toplam - tutar), plan };
}

export function stopajOrani(gun) {
  return PARAMS.stopaj.find((s) => gun <= s.maxGun).oran;
}
export function mevduat({ tutar, yillikFaiz, gun, stopaj }) {
  const st = stopaj == null ? stopajOrani(gun) : stopaj / 100;
  const brut = tutar * (yillikFaiz / 100) * gun / 365;
  const kesinti = brut * st;
  const net = brut - kesinti;
  return { brut: r2(brut), stopajOran: st, stopaj: r2(kesinti), net: r2(net), vadeSonu: r2(tutar + net), netYillik: r2((net / tutar) * (365 / gun) * 100) };
}

export function kdv({ tutar, oran, dahil }) {
  if (dahil) {
    const haric = tutar / (1 + oran / 100);
    return { haric: r2(haric), kdv: r2(tutar - haric), dahil: r2(tutar) };
  }
  const k = tutar * oran / 100;
  return { haric: r2(tutar), kdv: r2(k), dahil: r2(tutar + k) };
}

export function yuzde(mod, a, b) {
  if (mod === 'yuzdesi') return r2(a * b / 100);             // a sayısının %b'si
  if (mod === 'kacyuzde') return b === 0 ? NaN : r2(a / b * 100); // a, b'nin yüzde kaçı
  if (mod === 'degisim') return a === 0 ? NaN : r2((b - a) / a * 100); // a'dan b'ye değişim
  return NaN;
}

export function yillikIzin({ kidemYil, yas }) {
  if (kidemYil < 1) return { gun: 0, not: 'Yıllık izin hakkı 1 yıllık çalışmadan sonra doğar.' };
  let gun = kidemYil < 5 ? 14 : kidemYil < 15 ? 20 : 26;
  let not = '';
  if ((yas <= 18 || yas >= 50) && gun < 20) { gun = 20; not = '18 yaş ve altı ile 50 yaş ve üstü çalışanlara en az 20 gün izin verilir.'; }
  return { gun, not };
}

export function vki({ kilo, boy }) {
  const m = boy / 100; const v = kilo / (m * m);
  const sinif = v < 18.5 ? 'Zayıf' : v < 25 ? 'Normal' : v < 30 ? 'Fazla kilolu' : v < 35 ? 'Obez (1. derece)' : v < 40 ? 'Obez (2. derece)' : 'Obez (3. derece)';
  return { vki: Math.round(v * 10) / 10, sinif, idealMin: r2(18.5 * m * m), idealMax: r2(24.9 * m * m) };
}

export function tarihFarki(a, b) {
  const s = sureHesapla(a, b);
  if (!s) return null;
  return { ...s, hafta: Math.floor(s.toplamGun / 7) };
}

// İşsizlik ödeneği (4447 m.50): son 4 ay brüt ortalamasının %40'ı, brüt asgari ücretin %80'ini geçemez; yalnız damga vergisi.
export function issizlik({ ortalamaBrut, primGun }) {
  const P = PARAMS;
  const brut = Math.min(ortalamaBrut * 0.4, P.asgariBrut * 0.8);
  const damga = brut * P.damga;
  const sure = primGun >= 1080 ? 300 : primGun >= 900 ? 240 : primGun >= 600 ? 180 : 0;
  return {
    brut: r2(brut), damga: r2(damga), net: r2(brut - damga), sureGun: sure, sureAy: sure / 30,
    toplam: r2((brut - damga) * sure / 30), tavanUygulandi: ortalamaBrut * 0.4 > P.asgariBrut * 0.8,
    enAz: r2(P.asgariBrut * 0.4 * (1 - P.damga)), enCok: r2(P.asgariBrut * 0.8 * (1 - P.damga)),
  };
}

// Fazla mesai (4857 m.41): saatlik brüt = aylık brüt / 225; fazla çalışma %50, fazla sürelerle çalışma %25 zamlı.
export function fazlaMesai({ brut, saat, tip = 'fazla' }) {
  const saatlik = brut / 225;
  const carpan = tip === 'sure' ? 1.25 : 1.5;
  const saatlikMesai = saatlik * carpan;
  return { saatlik: r2(saatlik), carpan, saatlikMesai: r2(saatlikMesai), toplam: r2(saatlikMesai * saat), yillikSinir: 270 };
}

// Tapu harcı (492 s. Kanun): alıcı ve satıcı ayrı ayrı %2.
export function tapuHarci({ bedel }) {
  const h = bedel * 0.02;
  return { alici: r2(h), satici: r2(h), toplam: r2(h * 2) };
}

export function zam({ eski, yeni, oran }) {
  if (oran != null && isFinite(oran)) { const y = eski * (1 + oran / 100); return { eski: r2(eski), yeni: r2(y), fark: r2(y - eski), oran: r2(oran) }; }
  return { eski: r2(eski), yeni: r2(yeni), fark: r2(yeni - eski), oran: r2((yeni - eski) / eski * 100) };
}

export const fmt = (n, d = 2) => (isFinite(n) ? n.toLocaleString('tr-TR', { minimumFractionDigits: d, maximumFractionDigits: d }) : '—');
export const tl = (n) => fmt(n) + ' ₺';
