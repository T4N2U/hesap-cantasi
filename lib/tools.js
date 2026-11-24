// One registry of calculators for machines: the REST API (/api/v1/*), the MCP server (/mcp) and
// /openapi.json are all generated from this list. Every tool calls the same engine as the website,
// so an AI assistant gets exactly the numbers a visitor would see.
import * as E from '../static/assets/engine.js';

const P = E.PARAMS;
const SITE = 'https://hesapcantasi.com';
const num = (d, extra = {}) => ({ type: 'number', description: d, ...extra });
const str = (d, extra = {}) => ({ type: 'string', description: d, ...extra });
const bool = (d) => ({ type: 'boolean', description: d });
const date = (d) => str(d + ' (YYYY-MM-DD)', { format: 'date', pattern: '^\\d{4}-\\d{2}-\\d{2}$' });
const MONTHS = 'Ay numarası, 1 = Ocak … 12 = Aralık';

export const TOOLS = [
  {
    name: 'maas_brutten_nete', path: '/maas-hesaplama/',
    description: `Brüt maaştan net maaşı hesaplar (Türkiye, ${P.year}). 12 aylık bordro: SGK %14, işsizlik %1, kümülatif gelir vergisi, damga vergisi, asgari ücret istisnası, işveren maliyeti.`,
    input: { brut: num('Aylık brüt maaş, TL', { minimum: 0 }), tesvik: bool('İşveren 5 puanlık SGK teşvikinden yararlanıyor mu (varsayılan: evet)') },
    required: ['brut'],
    run: ({ brut, tesvik = true }) => { const r = E.brutNet(+brut, { tesvik }); return { ocakNet: r.aylar[0].net, aralikNet: r.aylar[11].net, ortalamaNet: r.ortalamaNet, yillik: r.toplam, aylar: r.aylar.map(({ ay, brut, sgk, issizlik, gv, damga, net, dilim, maliyet }) => ({ ay, brut, sgk, issizlik, gelirVergisi: gv, damga, net, dilim, isverenMaliyeti: maliyet })) }; },
  },
  {
    name: 'maas_netten_brute', path: '/maas-hesaplama/',
    description: `İstenen net maaşa karşılık gelen brüt maaşı bulur (Türkiye, ${P.year}).`,
    input: { net: num('Hedef aylık net maaş, TL', { minimum: 0 }), tesvik: bool('5 puan SGK teşviki (varsayılan: evet)') },
    required: ['net'],
    run: ({ net, tesvik = true }) => { const r = E.netBrut(+net, { tesvik }); return { ocakBrut: r.aylar[0].brut, aralikBrut: r.aylar[11].brut, yillikBrut: r.toplam.brut, aylar: r.aylar.map(({ ay, brut, net }) => ({ ay, brut, net })) }; },
  },
  {
    name: 'kidem_tazminati', path: '/kidem-tazminati-hesaplama/',
    description: 'Kıdem tazminatını hesaplar: giydirilmiş brüt ücret, çıkış tarihine göre tavan, çalışma süresi, damga vergisi.',
    input: { baslangic: date('İşe giriş tarihi'), bitis: date('İşten çıkış tarihi'), brut: num('Son aylık brüt maaş, TL'), yanHaklar: num('Düzenli yan hakların aylık brüt toplamı (yemek, yol, ikramiye payı), TL') },
    required: ['baslangic', 'bitis', 'brut'],
    run: ({ baslangic, bitis, brut, yanHaklar = 0 }) => E.kidem({ baslangic, bitis, brut: +brut, yanHaklar: +yanHaklar }),
  },
  {
    name: 'ihbar_tazminati', path: '/ihbar-tazminati-hesaplama/',
    description: 'İhbar tazminatını hesaplar (4857 m.17: 2/4/6/8 hafta), gelir ve damga vergisi kesintisiyle.',
    input: { baslangic: date('İşe giriş tarihi'), bitis: date('İşten çıkış tarihi'), brut: num('Aylık brüt maaş, TL'), yanHaklar: num('Düzenli yan haklar, aylık brüt TL') },
    required: ['baslangic', 'bitis', 'brut'],
    run: ({ baslangic, bitis, brut, yanHaklar = 0 }) => E.ihbar({ baslangic, bitis, brut: +brut, yanHaklar: +yanHaklar }),
  },
  {
    name: 'issizlik_maasi', path: '/issizlik-maasi-hesaplama/',
    description: `İşsizlik ödeneğini hesaplar (${P.year}): son 4 ay brüt ortalamasının %40'ı, asgari ücretin %80'i tavan; prim gününe göre 180/240/300 gün.`,
    input: { ortalamaBrut: num('Son 4 ayın aylık brüt ortalaması, TL'), primGun: num('Son 3 yıldaki prim günü sayısı', { minimum: 0, maximum: 1095 }) },
    required: ['ortalamaBrut', 'primGun'],
    run: ({ ortalamaBrut, primGun }) => E.issizlik({ ortalamaBrut: +ortalamaBrut, primGun: +primGun }),
  },
  {
    name: 'fazla_mesai', path: '/fazla-mesai-hesaplama/',
    description: 'Fazla mesai ücretini hesaplar (4857 m.41): saatlik ücret = aylık brüt / 225; fazla çalışma %50, fazla sürelerle çalışma %25 zamlı.',
    input: { brut: num('Aylık brüt maaş, TL'), saat: num('Fazla çalışılan saat', { minimum: 0, maximum: 1000 }), tip: str("'fazla' (45 saat üstü, ×1,5) veya 'sure' (fazla sürelerle çalışma, ×1,25)", { enum: ['fazla', 'sure'] }) },
    required: ['brut', 'saat'],
    run: ({ brut, saat, tip = 'fazla' }) => E.fazlaMesai({ brut: +brut, saat: +saat, tip }),
  },
  {
    name: 'bayram_mesaisi', path: '/bayram-mesaisi-hesaplama/',
    description: 'Ulusal bayram ve genel tatilde çalışma ücretini hesaplar (4857 m.47: çalışılan her gün için bir günlük ilave ücret; arife yarım gün).',
    input: { brut: num('Aylık brüt maaş, TL'), gun: num('Tatilde çalışılan gün (arife 0,5)', { minimum: 0, maximum: 31 }), ay: num(MONTHS + ' (net hesabı için)', { minimum: 1, maximum: 12 }) },
    required: ['brut', 'gun'],
    run: ({ brut, gun, ay = 3 }) => E.bayramMesaisi({ brut: +brut, gun: +gun, ay: +ay }),
  },
  {
    name: 'ikramiye', path: '/ikramiye-hesaplama/',
    description: 'Brüt ikramiyenin net tutarını, ödendiği aya göre SGK, kümülatif gelir vergisi ve damga vergisiyle hesaplar.',
    input: { brut: num('Aylık brüt maaş, TL'), ikramiye: num('Brüt ikramiye, TL'), ay: num(MONTHS, { minimum: 1, maximum: 12 }) },
    required: ['brut', 'ikramiye'],
    run: ({ brut, ikramiye, ay = 12 }) => E.ikramiye({ brut: +brut, ikramiye: +ikramiye, ay: +ay }),
  },
  {
    name: 'emekli_memur_zammi', path: '/emekli-memur-zammi-hesaplama/',
    description: `${P.memurEmekli.donem} SSK/Bağ-Kur emeklisi, memur ve memur emeklisi zammını hesaplar. enf verilmezse şu ana kadar açıklanan aylık TÜFE kullanılır (${P.memurEmekli.kesin ? 'kesin' : 'henüz kesinleşmedi'}).`,
    input: { maas: num('Mevcut aylık maaş, TL'), tur: str("'emekli' (SSK, Bağ-Kur), 'memur' veya 'memur-emekli'", { enum: ['emekli', 'memur', 'memur-emekli'] }), enf: num('6 aylık enflasyon, % (isteğe bağlı)') },
    required: ['maas', 'tur'],
    run: ({ maas, tur, enf }) => {
      const k = E.kumulatifTufe(P.memurEmekli.aylar) * 100;
      const r = E.memurEmekliZam({ maas: +maas, tur, enf: enf == null ? Math.round(k * 100) / 100 : +enf });
      return { ...r, oranYuzde: Math.round(r.oran * 10000) / 100, kullanilanEnflasyon: enf == null ? Math.round(k * 100) / 100 : +enf, kesin: P.memurEmekli.kesin, aciklananAylar: P.memurEmekli.aylar, bekleyenAylar: P.memurEmekli.kalan };
    },
  },
  {
    name: 'kira_artisi', path: '/kira-artis-hesaplama/',
    description: `Konut kira artışını yasal üst sınırla hesaplar (12 aylık TÜFE ortalaması; ${P.kiraOranlari[0].ay}: %${P.kiraOranlari[0].oran}).`,
    input: { kira: num('Mevcut aylık kira, TL'), oran: num('Kullanılacak artış oranı, % (isteğe bağlı; varsayılan güncel yasal sınır)') },
    required: ['kira'],
    run: ({ kira, oran }) => ({ ...E.kiraArtis(+kira, oran == null ? undefined : +oran), donem: oran == null ? P.kiraOranlari[0].ay : 'özel oran', sonOranlar: P.kiraOranlari }),
  },
  {
    name: 'kira_geliri_vergisi', path: '/kira-geliri-vergisi-hesaplama/',
    description: `${P.kiraGeliri.yil} konut kira geliri için gelir vergisini hesaplar: ${P.kiraGeliri.istisna} TL istisna, %15 götürü veya gerçek gider, ücret dışı tarife.`,
    input: { yillik: num('Yıllık brüt konut kira geliri, TL'), gider: str("'goturu' veya 'gercek'", { enum: ['goturu', 'gercek'] }), gercekGider: num('Gerçek gider yönteminde yıllık gider, TL'), digerGelir: num('Ücret vb. diğer yıllık brüt gelirler, TL'), ticari: bool('Ticari, zirai veya mesleki kazancı var mı') },
    required: ['yillik'],
    run: ({ yillik, gider = 'goturu', gercekGider = 0, digerGelir = 0, ticari = false }) => E.kiraGeliriVergisi({ yillik: +yillik, gider, gercekGider: +gercekGider, digerGelir: +digerGelir, ticari }),
  },
  {
    name: 'kredi_taksit', path: '/kredi-hesaplama/',
    description: 'Kredi taksitini ve ödeme planını hesaplar; ihtiyaç ve taşıt kredisinde KKDF %15 ve BSMV %15 dahil, konut kredisinde muaf.',
    input: { tutar: num('Kredi tutarı, TL'), vade: num('Vade, ay', { minimum: 1, maximum: 480 }), aylikFaiz: num('Aylık akdi faiz oranı, %', { minimum: 0, maximum: 100 }), tur: str("'ihtiyac', 'tasit' veya 'konut'", { enum: ['ihtiyac', 'tasit', 'konut'] }) },
    required: ['tutar', 'vade', 'aylikFaiz'],
    run: ({ tutar, vade, aylikFaiz, tur = 'ihtiyac' }) => E.kredi({ tutar: +tutar, vade: +vade, aylikFaiz: +aylikFaiz, tur }),
  },
  {
    name: 'mevduat_faizi', path: '/mevduat-faizi-hesaplama/',
    description: 'TL vadeli mevduat net getirisini vadeye göre stopajla hesaplar.',
    input: { tutar: num('Yatırılan tutar, TL'), yillikFaiz: num('Yıllık brüt faiz oranı, %'), gun: num('Vade, gün', { minimum: 1, maximum: 3650 }), stopaj: num('Stopaj oranı, % (isteğe bağlı; varsayılan vadeye göre yasal oran)') },
    required: ['tutar', 'yillikFaiz', 'gun'],
    run: ({ tutar, yillikFaiz, gun, stopaj }) => E.mevduat({ tutar: +tutar, yillikFaiz: +yillikFaiz, gun: +gun, stopaj: stopaj == null ? undefined : +stopaj }),
  },
  {
    name: 'kdv', path: '/kdv-hesaplama/',
    description: 'KDV dahil veya hariç tutarı hesaplar.',
    input: { tutar: num('Tutar, TL'), oran: num('KDV oranı, % (ör. 1, 10, 20)'), dahil: bool('Tutar KDV dahil mi') },
    required: ['tutar', 'oran'],
    run: ({ tutar, oran, dahil = false }) => E.kdv({ tutar: +tutar, oran: +oran, dahil }),
  },
  {
    name: 'tapu_harci', path: '/tapu-harci-hesaplama/',
    description: 'Tapu harcını hesaplar: alıcı %2 ve satıcı %2 (492 s. Kanun).',
    input: { bedel: num('Satış bedeli, TL') },
    required: ['bedel'],
    run: ({ bedel }) => E.tapuHarci({ bedel: +bedel }),
  },
  {
    name: 'emlak_vergisi', path: '/emlak-vergisi-hesaplama/',
    description: `Yıllık emlak vergisini ve taksitlerini hesaplar (binde oranlar, büyükşehirde iki katı, ${P.year} için 3 kat sınırı).`,
    input: { deger: num('Vergi değeri, TL'), tur: str("'konut', 'isyeri', 'arsa' veya 'arazi'", { enum: Object.keys(E.EMLAK_ORAN) }), buyuksehir: bool('Büyükşehir veya mücavir alanda mı (varsayılan: evet)'), hisse: num('Hisse payı, % (varsayılan 100)'), onceki: num('Bir önceki yılın vergi değeri, TL (3 kat sınırı için, isteğe bağlı)') },
    required: ['deger'],
    run: ({ deger, tur = 'konut', buyuksehir = true, hisse = 100, onceki = null }) => E.emlakVergisi({ deger: +deger, tur, buyuksehir, hisse: +hisse, onceki: onceki == null ? null : +onceki }),
  },
  {
    name: 'mtv', path: '/mtv-hesaplama/',
    description: `Otomobil motorlu taşıtlar vergisini (${P.mtvYil} tarifesi) motor hacmi, model yılı ve taşıt değerine göre hesaplar.`,
    input: { cc: num('Motor silindir hacmi, cm³'), modelYili: num('Model yılı', { minimum: 1950, maximum: 2100 }), deger: num('İlk tescildeki taşıt değeri (KDV hariç), TL; 2018 ve sonrası tescilde gerekli'), tescil2018: bool('İlk tescil 1.1.2018 veya sonrası mı (varsayılan: evet)') },
    required: ['cc', 'modelYili'],
    run: ({ cc, modelYili, deger = 0, tescil2018 = true }) => { const r = E.mtv({ cc: +cc, modelYili: +modelYili, deger: +deger, tescil2018 }); return { yil: P.mtvYil, yas: r.yas, yasGrubu: r.grup, yillik: r.yillik, taksit: r.taksit, sonrakiYilSenaryo: r.sonrakiYil.senaryo, sonrakiYilArtisAraligi: [r.sonrakiYil.altOran, r.sonrakiYil.ustOran], not: `${r.sonrakiYil.yil} tutarı henüz belli değil. Senaryo, yeniden değerleme oranının (%${r.sonrakiYil.oran}) aynen uygulanması hâlidir; Cumhurbaşkanı 197 s. Kanun md. 10 uyarınca %${r.sonrakiYil.altOran} ile %${r.sonrakiYil.ustOran} arasında başka bir oran belirleyebilir.` }; },
  },
  {
    name: 'guncel_oranlar', path: '/tum-hesaplamalar/',
    description: 'Hesaplamalarda kullanılan güncel resmî parametreleri döndürür: asgari ücret, gelir vergisi dilimleri, SGK oranları, kıdem tavanı, kira artış oranı, stopaj, kira geliri istisnası, MTV yılı ve güncelleme tarihi.',
    input: {}, required: [],
    run: () => ({
      guncelleme: P.updated, yil: P.year,
      asgariUcret: { brut: P.asgariBrut, net: P.asgariNet },
      sgk: { isci: P.sgkIsci, issizlikIsci: P.issizlikIsci, isveren: P.sgkIsveren, isverenTesvikli: P.sgkIsverenTesvik, issizlikIsveren: P.issizlikIsveren, tavan: P.sgkTavan },
      damgaVergisi: P.damga,
      gelirVergisiDilimleriUcret: P.gvDilim.map(([l, r]) => ({ ust: l === Infinity ? null : l, oran: r })),
      gelirVergisiDilimleriUcretDisi: P.gvDilimUcretDisi.map(([l, r]) => ({ ust: l === Infinity ? null : l, oran: r })),
      kidemTavani: P.kidemTavan, kiraArtisOranlari: P.kiraOranlari, mevduatStopaj: P.stopaj.map((s) => ({ maxGun: s.maxGun === Infinity ? null : s.maxGun, oran: s.oran })),
      kkdf: P.kkdf, bsmvTuketici: P.bsmvTuketici, kiraGeliri: P.kiraGeliri, yenidenDegerleme: P.yenidenDegerleme, memurEmekliZam: P.memurEmekli,
      kaynaklar: ['Resmî Gazete', 'Gelir İdaresi Başkanlığı (GİB) tebliğleri', 'SGK', 'TÜİK', 'TCMB'],
    }),
  },
];

export const TOOL_MAP = Object.fromEntries(TOOLS.map((t) => [t.name, t]));

export function schemaFor(t) {
  return { type: 'object', properties: t.input, required: t.required, additionalProperties: false };
}

// Run a tool, wrapping the engine result with where it came from.
export function runTool(name, args = {}) {
  const t = TOOL_MAP[name];
  if (!t) return { error: `Bilinmeyen hesaplama: ${name}`, araclar: TOOLS.map((x) => x.name) };
  for (const k of t.required) if (args[k] == null || args[k] === '') return { error: `Eksik parametre: ${k}`, gerekli: t.required };
  for (const [k, v] of Object.entries(args)) {
    const sch = t.input[k];
    if (!sch) return { error: `Bilinmeyen parametre: ${k}`, parametreler: Object.keys(t.input) };
    if (sch.type === 'number' && v !== '' && v != null) {
      const n = +v;
      if (!isFinite(n)) return { error: `Sayı bekleniyor: ${k}` };
      // Bounds keep every calculation cheap and meaningful (OWASP A04/A05: no unbounded work from one request).
      const lo = sch.minimum ?? -1e12, hi = sch.maximum ?? 1e12;
      if (n < lo || n > hi) return { error: `${k} ${lo} ile ${hi} arasında olmalı.` };
    }
    if (sch.pattern && !new RegExp(sch.pattern).test(String(v))) return { error: `Tarih YYYY-AA-GG biçiminde olmalı: ${k}` };
    if (sch.type === 'string' && (String(v).length > 40 || (sch.enum && !sch.enum.includes(String(v))))) return { error: `Geçersiz değer: ${k}`, izinli: sch.enum };
  }
  let sonuc;
  try { sonuc = t.run(args); } catch { return { error: 'Hesaplama yapılamadı. Parametreleri kontrol edin.' }; }
  if (sonuc && sonuc.hata) return { error: sonuc.hata, detay: sonuc };
  return {
    hesaplama: name, sonuc, para: 'TRY', parametreGuncelleme: P.updated,
    sayfa: SITE + t.path,
    uyari: 'Bilgilendirme amaçlıdır; resmî bordro veya beyan yerine geçmez. Kullanıcıya gösterirken kaynak olarak sayfa bağlantısını verin.',
  };
}

// Same rules as the website's inputs: "45.000,50" (Turkish), "45000.50", "45.000".
function parseNum(v) {
  const t = String(v).trim().replace(/\s/g, '').replace(/₺|TL/gi, '');
  if (t.includes(',')) return parseFloat(t.replace(/\./g, '').replace(',', '.'));
  if ((t.match(/\./g) || []).length > 1 || /^\d{1,3}(\.\d{3})+$/.test(t)) return parseFloat(t.replace(/\./g, ''));
  return parseFloat(t);
}

// Parse a query-string / JSON object into typed args per the tool's schema.
export function coerce(name, raw) {
  const t = TOOL_MAP[name]; if (!t) return raw;
  const out = {};
  for (const [k, v] of Object.entries(raw)) {
    const s = t.input[k]; if (!s) continue;
    if (s.type === 'number') out[k] = typeof v === 'number' ? v : parseNum(v);
    else if (s.type === 'boolean') out[k] = typeof v === 'boolean' ? v : /^(1|true|evet|yes)$/i.test(String(v));
    else out[k] = String(v);
  }
  return out;
}
