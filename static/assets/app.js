import * as E from './engine.js';

const tl = E.tl, fmt = E.fmt;
const num = (v) => {
  if (v == null) return NaN;
  const s = String(v).trim().replace(/\s/g, '').replace(/₺|TL/gi, '');
  // Accept "45.000,50" (tr) and "45000.50"
  if (s.includes(',')) return parseFloat(s.replace(/\./g, '').replace(',', '.'));
  if ((s.match(/\./g) || []).length > 1 || /^\d{1,3}(\.\d{3})+$/.test(s)) return parseFloat(s.replace(/\./g, ''));
  return parseFloat(s);
};
const pct = (x) => '%' + fmt(x * 100, x * 100 % 1 ? 2 : 0);
const row = (k, v, strong) => `<div class="kv${strong ? ' strong' : ''}"><span>${k}</span><b>${v}</b></div>`;
const table = (head, rows) => `<div class="tablewrap"><table><thead><tr>${head.map((h) => `<th>${h}</th>`).join('')}</tr></thead><tbody>${rows.map((r) => `<tr>${r.map((c) => `<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
const err = (m) => `<p class="err">${m}</p>`;

const CALCS = {
  maas(f) {
    const mod = f.mod.value, tutar = num(f.tutar.value), tesvik = f.tesvik.checked;
    if (!(tutar > 0)) return err('Geçerli bir tutar girin.');
    if (mod === 'brut' && tutar < E.PARAMS.asgariBrut) return err(`Brüt maaş asgari ücretin (${tl(E.PARAMS.asgariBrut)}) altında olamaz.`);
    if (mod === 'net' && tutar < E.PARAMS.asgariNet) return err(`Net maaş asgari ücretin (${tl(E.PARAMS.asgariNet)}) altında olamaz.`);
    const r = mod === 'brut' ? E.brutNet(tutar, { tesvik }) : E.netBrut(tutar, { tesvik });
    const o = r.aylar[0];
    const head = mod === 'brut'
      ? row('Ocak ayı net maaş', tl(o.net), true) + row('Yıllık ortalama net', tl(r.ortalamaNet)) + row('Aralık ayı net', tl(r.aylar[11].net))
      : row('Ocak ayı brüt maaş', tl(o.brut), true) + row('Aralık ayı brüt', tl(r.aylar[11].brut)) + row('Yıllık toplam brüt', tl(r.toplam.brut));
    return `<div class="summary">${head}${row('SGK + işsizlik (Ocak)', tl(o.sgk + o.issizlik))}${row('İşverene maliyet (Ocak)', tl(o.maliyet))}</div>
      <h3>12 aylık bordro (${E.PARAMS.year})</h3>
      ${table(['Ay', 'Brüt', 'SGK %14', 'İşsizlik %1', 'Gelir V.', 'Damga V.', 'Net', 'Dilim'],
        r.aylar.map((a) => [a.ay, fmt(a.brut), fmt(a.sgk), fmt(a.issizlik), fmt(a.gv), fmt(a.damga), `<b>${fmt(a.net)}</b>`, pct(a.dilim)]).concat([['<b>Toplam</b>', fmt(r.toplam.brut), fmt(r.toplam.sgk), fmt(r.toplam.issizlik), fmt(r.toplam.gv), fmt(r.toplam.damga), `<b>${fmt(r.toplam.net)}</b>`, '']]))}`;
  },
  kidem(f) {
    const r = E.kidem({ baslangic: f.baslangic.value, bitis: f.bitis.value, brut: num(f.brut.value), yanHaklar: num(f.yan.value) || 0 });
    if (r.hata) return err(r.hata);
    if (!(r.giydirilmis > 0)) return err('Brüt ücreti girin.');
    return `<div class="summary">${row('Net kıdem tazminatı', tl(r.net), true)}${row('Brüt tazminat', tl(r.brut))}${row('Damga vergisi (‰7,59)', tl(r.damga))}
      ${row('Çalışma süresi', `${r.sure.yil} yıl ${r.sure.ay} ay ${r.sure.gun} gün`)}${row('Esas alınan ücret', tl(r.esas) + (r.tavanUygulandi ? ' (tavan)' : ''))}${row('Geçerli tavan', tl(r.tavan))}</div>`;
  },
  ihbar(f) {
    const r = E.ihbar({ baslangic: f.baslangic.value, bitis: f.bitis.value, brut: num(f.brut.value), yanHaklar: num(f.yan.value) || 0, gvOran: num(f.gv.value) / 100 });
    if (r.hata) return err(r.hata);
    if (!(r.brut > 0)) return err('Brüt ücreti girin.');
    return `<div class="summary">${row('Net ihbar tazminatı', tl(r.net), true)}${row('İhbar süresi', `${r.hafta} hafta (${r.gun} gün)`)}${row('Brüt tazminat', tl(r.brut))}${row('Gelir vergisi', tl(r.gv))}${row('Damga vergisi', tl(r.damga))}${row('Günlük brüt ücret', tl(r.gunluk))}</div>`;
  },
  kira(f) {
    const k = num(f.kira.value), o = num(f.oran.value);
    if (!(k > 0) || !(o >= 0)) return err('Kira bedeli ve oranı girin.');
    const r = E.kiraArtis(k, o);
    return `<div class="summary">${row('Yeni kira bedeli', tl(r.yeni), true)}${row('Aylık artış', tl(r.artis))}${row('Yıllık ek ödeme', tl(r.yillikFark))}${row('Uygulanan oran', '%' + fmt(r.oran))}</div>`;
  },
  kredi(f) {
    const tutar = num(f.tutar.value), vade = parseInt(f.vade.value, 10), faiz = num(f.faiz.value);
    if (!(tutar > 0) || !(vade > 0) || !(faiz >= 0)) return err('Tutar, vade ve faiz oranını girin.');
    const r = E.kredi({ tutar, vade, aylikFaiz: faiz, tur: f.tur.value });
    return `<div class="summary">${row('Aylık taksit', tl(r.taksit), true)}${row('Toplam geri ödeme', tl(r.toplam))}${row('Toplam faiz', tl(r.faiz))}${row('KKDF + BSMV', tl(r.kkdf + r.bsmv))}${row('Kredinin maliyeti', tl(r.maliyet))}</div>
      <details><summary>Ödeme planını göster (${vade} taksit)</summary>${table(['No', 'Taksit', 'Anapara', 'Faiz', 'KKDF', 'BSMV', 'Kalan'], r.plan.map((p) => [p.no, fmt(p.taksit), fmt(p.anapara), fmt(p.faiz), fmt(p.kkdf), fmt(p.bsmv), fmt(p.kalan)]))}</details>`;
  },
  mevduat(f) {
    const tutar = num(f.tutar.value), faiz = num(f.faiz.value), gun = parseInt(f.gun.value, 10);
    if (!(tutar > 0) || !(faiz >= 0) || !(gun > 0)) return err('Tutar, faiz ve gün sayısını girin.');
    const r = E.mevduat({ tutar, yillikFaiz: faiz, gun });
    return `<div class="summary">${row('Net faiz getirisi', tl(r.net), true)}${row('Vade sonu toplam', tl(r.vadeSonu))}${row('Brüt faiz', tl(r.brut))}${row(`Stopaj (${pct(r.stopajOran)})`, tl(r.stopaj))}${row('Net yıllık getiri', '%' + fmt(r.netYillik))}</div>`;
  },
  kdv(f) {
    const tutar = num(f.tutar.value), oran = num(f.oran.value);
    if (!(tutar > 0)) return err('Tutar girin.');
    const r = E.kdv({ tutar, oran, dahil: f.tip.value === 'dahil' });
    return `<div class="summary">${row('KDV tutarı', tl(r.kdv), true)}${row('KDV hariç', tl(r.haric))}${row('KDV dahil', tl(r.dahil))}</div>`;
  },
  yuzde(f) {
    const out = [];
    const a1 = num(f.a1.value), b1 = num(f.b1.value);
    if (isFinite(a1) && isFinite(b1)) out.push(row(`${fmt(a1, 0)} sayısının %${fmt(b1, 0)}'i`, fmt(E.yuzde('yuzdesi', a1, b1)), true));
    const a2 = num(f.a2.value), b2 = num(f.b2.value);
    if (isFinite(a2) && isFinite(b2)) out.push(row(`${fmt(a2, 0)}, ${fmt(b2, 0)} sayısının yüzde kaçı`, '%' + fmt(E.yuzde('kacyuzde', a2, b2)), true));
    const a3 = num(f.a3.value), b3 = num(f.b3.value);
    if (isFinite(a3) && isFinite(b3)) out.push(row(`${fmt(a3, 0)} → ${fmt(b3, 0)} değişim`, '%' + fmt(E.yuzde('degisim', a3, b3)), true));
    return out.length ? `<div class="summary">${out.join('')}</div>` : err('Hesaplamak için iki değer girin.');
  },
  izin(f) {
    const r = E.yillikIzin({ kidemYil: num(f.kidem.value), yas: num(f.yas.value) });
    return `<div class="summary">${row('Yıllık ücretli izin', r.gun + ' iş günü', true)}</div>${r.not ? `<p class="note">${r.not}</p>` : ''}`;
  },
  vki(f) {
    const kilo = num(f.kilo.value), boy = num(f.boy.value);
    if (!(kilo > 0) || !(boy > 50)) return err('Kilo ve boy (cm) girin.');
    const r = E.vki({ kilo, boy });
    return `<div class="summary">${row('Vücut kitle indeksi', fmt(r.vki, 1), true)}${row('Sınıf', r.sinif)}${row('Boyunuza göre normal aralık', `${fmt(r.idealMin, 1)} – ${fmt(r.idealMax, 1)} kg`)}</div>`;
  },
  tarih(f) {
    const r = E.tarihFarki(f.a.value, f.b.value);
    if (!r) return err('İkinci tarih birinciden sonra olmalı.');
    return `<div class="summary">${row('Toplam gün', fmt(r.toplamGun, 0) + ' gün', true)}${row('Yıl / ay / gün', `${r.yil} yıl ${r.ay} ay ${r.gun} gün`)}${row('Hafta', fmt(r.hafta, 0) + ' hafta')}</div>`;
  },
  issizlik(f) {
    const ort = num(f.brut.value), gun = num(f.gun.value);
    if (!(ort > 0) || !(gun >= 0)) return err('Ortalama brüt ücreti ve prim gününü girin.');
    const r = E.issizlik({ ortalamaBrut: ort, primGun: gun });
    if (!r.sureGun) return err('İşsizlik ödeneği için son 3 yılda en az 600 gün prim gerekir.');
    return `<div class="summary">${row('Aylık net işsizlik maaşı', tl(r.net), true)}${row('Ödeme süresi', `${r.sureGun} gün (${r.sureAy} ay)`)}${row('Toplam alınacak (yaklaşık)', tl(r.toplam))}${row('Aylık brüt ödenek', tl(r.brut) + (r.tavanUygulandi ? ' (tavan)' : ''))}${row('Damga vergisi', tl(r.damga))}</div>`;
  },
  mesai(f) {
    const brut = num(f.brut.value), saat = num(f.saat.value);
    if (!(brut > 0) || !(saat > 0)) return err('Brüt maaşı ve mesai saatini girin.');
    const r = E.fazlaMesai({ brut, saat, tip: f.tip.value });
    return `<div class="summary">${row('Brüt fazla mesai ücreti', tl(r.toplam), true)}${row('Saatlik brüt ücret', tl(r.saatlik))}${row(`Saatlik mesai ücreti (×${fmt(r.carpan)})`, tl(r.saatlikMesai))}</div>${saat > 270 ? '<p class="note">Yıllık fazla çalışma 270 saati geçemez.</p>' : ''}`;
  },
  tapu(f) {
    const bedel = num(f.bedel.value);
    if (!(bedel > 0)) return err('Satış bedelini girin.');
    const r = E.tapuHarci({ bedel });
    return `<div class="summary">${row('Alıcının ödeyeceği harç', tl(r.alici), true)}${row('Satıcının ödeyeceği harç', tl(r.satici))}${row('Toplam tapu harcı', tl(r.toplam))}</div><p class="note">Döner sermaye ücreti ayrıca alınır. Beyan edilen bedel emlak vergisi değerinin altında olamaz.</p>`;
  },
  zam(f) {
    const eski = num(f.eski.value), yeni = num(f.yeni.value), oran = num(f.oran.value);
    if (!(eski > 0)) return err('Mevcut tutarı girin.');
    const out = [];
    if (isFinite(yeni) && yeni > 0) { const r = E.zam({ eski, yeni }); out.push(row('Zam oranı', '%' + fmt(r.oran), true), row('Artış tutarı', tl(r.fark))); }
    if (isFinite(oran)) { const r = E.zam({ eski, oran }); out.push(row(`%${fmt(oran)} zamla yeni tutar`, tl(r.yeni), true), row('Artış tutarı', tl(r.fark))); }
    return out.length ? `<div class="summary">${out.join('')}</div>` : err('Yeni tutarı veya zam oranını girin.');
  },
  yas(f) {
    const today = new Date().toISOString().slice(0, 10);
    const r = E.tarihFarki(f.dogum.value, f.bugun.value || today);
    if (!r) return err('Doğum tarihini girin.');
    return `<div class="summary">${row('Yaşınız', `${r.yil} yıl ${r.ay} ay ${r.gun} gün`, true)}${row('Yaşanan gün', fmt(r.toplamGun, 0))}${row('Yaşanan hafta', fmt(r.hafta, 0))}</div>`;
  },
};

function bind(form) {
  const today = new Date().toISOString().slice(0, 10);
  form.querySelectorAll('input[data-today]').forEach((el) => { if (!el.value) el.value = today; });
  const fn = CALCS[form.dataset.calc];
  const out = form.parentElement.querySelector('.result');
  if (!fn || !out) return;
  // Prefill from URL (?tutar=45000&mod=net) so results are shareable
  const qs = new URLSearchParams(location.search);
  qs.forEach((v, k) => { const el = form.elements[k]; if (el && el.type !== 'checkbox') el.value = v; });
  const run = () => {
    try { out.innerHTML = fn(form.elements); } catch (e) { out.innerHTML = err('Hesaplanamadı, girdileri kontrol edin.'); console.error(e); }
  };
  form.addEventListener('input', run);
  form.addEventListener('change', run);
  form.addEventListener('submit', (e) => {
    e.preventDefault(); run();
    const p = new URLSearchParams();
    [...form.elements].forEach((el) => { if (el.name && el.type !== 'checkbox' && !(el.type === 'radio' && !el.checked) && el.value) p.set(el.name, el.value); });
    history.replaceState(null, '', '?' + p.toString());
    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
  form.querySelectorAll('[data-set]').forEach((b) => b.addEventListener('click', () => {
    const [name, val] = b.dataset.set.split('='); form.elements[name].value = val; run();
  }));
  run();
}

document.querySelectorAll('form.calc').forEach(bind);

// Mode toggle labels on maaş form
document.querySelectorAll('form[data-calc="maas"]').forEach((f) => {
  const lbl = f.querySelector('[data-tutar-label]');
  const sync = () => { if (lbl) lbl.textContent = f.mod.value === 'brut' ? 'Aylık brüt maaş (₺)' : 'Aylık net maaş (₺)'; };
  f.addEventListener('change', sync); sync();
});
