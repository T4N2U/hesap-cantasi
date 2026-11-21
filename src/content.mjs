import * as E from '../static/assets/engine.js';
import { SITE } from './site.mjs';

const P = E.PARAMS, fmt = E.fmt, tl = E.tl;
const Y = P.year;
const kNow = P.kiraOranlari[0];
const tavan = P.kidemTavan.at(-1);
const asg = E.brutNet(P.asgariBrut);

const money = (name, label, value, extra = '') => `<label>${label}<input name="${name}" inputmode="decimal" autocomplete="off" value="${value}" ${extra}></label>`;
const date = (name, label, value = '', today = false) => `<label>${label}<input type="date" name="${name}" value="${value}"${today ? ' data-today' : ''}></label>`;
const go = '<button class="go" type="submit">Hesapla</button>';

export const CALCULATORS = [
  {
    path: '/maas-hesaplama/', short: 'Maaş hesaplama', tile: 'Brütten nete ve netten brüte, 12 aylık bordro',
    h1: `Maaş hesaplama ${Y}: brütten nete, netten brüte`,
    title: `Maaş Hesaplama ${Y} – Brütten Nete ve Netten Brüte (12 Aylık Bordro)`,
    description: `${Y} vergi dilimleri ve asgari ücret istisnasıyla brütten nete, netten brüte maaş hesaplama. Aylık SGK, gelir vergisi, damga vergisi ve işveren maliyeti.`,
    lead: `Brüt veya net maaşınızı girin; ${Y} yılının 12 ayı için SGK, gelir vergisi, damga vergisi ve işverene maliyeti görün.`,
    form: `<form class="calc" data-calc="maas">
<div class="seg" role="radiogroup"><label><input type="radio" name="mod" value="brut" checked>Brütten nete</label><label><input type="radio" name="mod" value="net">Netten brüte</label></div>
<label><span data-tutar-label>Aylık brüt maaş (₺)</span><input name="tutar" inputmode="decimal" autocomplete="off" value="60.000"></label>
<div class="chips">${[40000, 50000, 75000, 100000, 150000].map((v) => `<button type="button" data-set="tutar=${v}">${fmt(v, 0)}</button>`).join('')}</div>
<label class="check"><input type="checkbox" name="tesvik" checked>İşveren 5 puanlık SGK teşvikinden yararlanıyor</label>
${go}</form>`,
    content: `<h2>Brütten nete maaş nasıl hesaplanır?</h2>
<ol><li><b>SGK işçi payı (%14) ve işsizlik sigortası (%1)</b> brüt ücretten düşülür. Prime esas kazanç üst sınırı ${tl(P.sgkTavan)}'dir.</li>
<li>Kalan tutar <b>gelir vergisi matrahıdır</b>. Vergi, yılbaşından itibaren biriken (kümülatif) matraha göre <a href="/gelir-vergisi-dilimleri-2026/">${Y} ücret tarifesi</a> ile hesaplanır.</li>
<li>Asgari ücrete isabet eden gelir vergisi ve damga vergisi <b>istisna</b> edilir; bu yüzden asgari ücretin üzerindeki kısım vergilendirilir.</li>
<li><b>Damga vergisi</b> brüt ücretin binde 7,59'udur (asgari ücret kısmı hariç).</li></ol>
<p>Kümülatif matrah yükseldikçe vergi dilimi %15'ten %20'ye, ardından %27'ye çıkar. Brüt maaşınız sabit kalsa da net maaşınız yılın ikinci yarısında düşebilir. Tabloda her ayın dilimini görebilirsiniz.</p>`,
    faq: [
      [`${Y} net asgari ücret ne kadar?`, `Brüt asgari ücret ${tl(P.asgariBrut)}, net asgari ücret ${tl(P.asgariNet)}'dir. Asgari ücretten gelir vergisi ve damga vergisi kesilmez.`],
      ['Net maaşım neden yıl içinde azalıyor?', 'Gelir vergisi kümülatif matraha göre hesaplanır. Yıl içinde biriken matrah bir sonraki vergi dilimine geçtiğinde kesilen vergi artar ve net maaş azalır.'],
      ['İşverene maliyet nasıl hesaplanır?', `Brüt ücrete işveren SGK payı (%21,75; 5 puan teşvikle %16,75) ve işveren işsizlik payı (%2) eklenir.`],
      ['Bu hesaplama resmi bordro yerine geçer mi?', 'Hayır. Yemek, yol, prim, BES ve özel indirimler bordroyu değiştirebilir. Sonuçlar tahmini bilgi amaçlıdır.'],
    ],
  },
  {
    path: '/kidem-tazminati-hesaplama/', short: 'Kıdem tazminatı', tile: `Güncel tavan: ${tl(tavan.tutar)}`,
    h1: `Kıdem tazminatı hesaplama ${Y}`,
    title: `Kıdem Tazminatı Hesaplama ${Y} – Güncel Tavan ${fmt(tavan.tutar)} TL`,
    description: `${Y} kıdem tazminatı tavanı ${tl(tavan.tutar)} ile net kıdem tazminatınızı hesaplayın. Çalışma süresi, giydirilmiş ücret ve damga vergisi dahil.`,
    lead: `İşe giriş ve çıkış tarihinizi, son brüt ücretinizi girin. Hesaplama çıkış tarihindeki tavanı otomatik uygular.`,
    form: `<form class="calc" data-calc="kidem">
<div class="row2">${date('baslangic', 'İşe giriş tarihi', '2020-01-15')}${date('bitis', 'İşten çıkış tarihi', '', true)}</div>
<div class="row2">${money('brut', 'Son aylık brüt ücret (₺)', '60.000')}${money('yan', 'Düzenli yan haklar (₺/ay) <small>yemek, yol vb.</small>', '0')}</div>
${go}</form>`,
    content: `<h2>Kıdem tazminatı nasıl hesaplanır?</h2>
<p>Her tam çalışma yılı için <b>30 günlük giydirilmiş brüt ücret</b> ödenir. Yıldan artan ay ve günler orantılı olarak eklenir. Giydirilmiş ücret; brüt maaşa düzenli ödenen yemek, yol, ikramiye gibi para ve parayla ölçülebilen yan hakların eklenmesiyle bulunur.</p>
<p>Ödenecek tutar yıllık <b>tavanı</b> aşamaz. 1 Temmuz – 31 Aralık ${Y} döneminde tavan ${tl(tavan.tutar)}'dir. Kıdem tazminatından gelir vergisi kesilmez, yalnızca binde 7,59 damga vergisi kesilir.</p>
<h3>${Y} kıdem tazminatı tavanları</h3>
<div class="tablewrap"><table><thead><tr><th>Dönem</th><th>Tavan</th></tr></thead><tbody>${P.kidemTavan.map((t) => `<tr><td>${t.from.split('-').reverse().join('.')} – ${t.to.split('-').reverse().join('.')}</td><td>${tl(t.tutar)}</td></tr>`).join('')}</tbody></table></div>`,
    faq: [
      ['Kıdem tazminatı almak için kaç yıl çalışmak gerekir?', 'Aynı işverene bağlı olarak en az 1 yıl çalışmış olmak gerekir. Ayrıca fesih nedeninin kanunda sayılan hallerden biri olması gerekir (işveren feshi, emeklilik, askerlik, evlilik nedeniyle kadın çalışanın ayrılması gibi).'],
      ['İstifa eden kıdem tazminatı alabilir mi?', 'Kural olarak hayır. Ancak haklı nedenle fesih (örneğin ücretin ödenmemesi), emeklilik için yaş dışındaki şartların tamamlanması veya evlilik gibi istisnai durumlarda alınabilir.'],
      ['Kıdem tazminatından vergi kesilir mi?', 'Gelir vergisi kesilmez, yalnızca binde 7,59 damga vergisi kesilir.'],
    ],
  },
  {
    path: '/ihbar-tazminati-hesaplama/', short: 'İhbar tazminatı', tile: '2 – 8 haftalık ihbar süresi ve net tutar',
    h1: `İhbar tazminatı hesaplama ${Y}`,
    title: `İhbar Tazminatı Hesaplama ${Y} – İhbar Süresi ve Net Tutar`,
    description: 'Çalışma sürenize göre ihbar süresini (2, 4, 6, 8 hafta) ve gelir vergisi, damga vergisi düşülmüş net ihbar tazminatını hesaplayın.',
    lead: 'İş sözleşmesi bildirim süresine uyulmadan feshedildiğinde ödenen ihbar tazminatını hesaplayın.',
    form: `<form class="calc" data-calc="ihbar">
<div class="row2">${date('baslangic', 'İşe giriş tarihi', '2022-03-01')}${date('bitis', 'İşten çıkış tarihi', '', true)}</div>
<div class="row2">${money('brut', 'Son aylık brüt ücret (₺)', '60.000')}${money('yan', 'Düzenli yan haklar (₺/ay)', '0')}</div>
<label>Gelir vergisi oranı <small>yıl içindeki diliminiz</small><select name="gv"><option value="15">%15</option><option value="20">%20</option><option value="27">%27</option><option value="35">%35</option><option value="40">%40</option></select></label>
${go}</form>`,
    content: `<h2>İhbar süreleri</h2>
<div class="tablewrap"><table><thead><tr><th>Çalışma süresi</th><th>İhbar süresi</th></tr></thead><tbody><tr><td>6 aydan az</td><td>2 hafta</td></tr><tr><td>6 ay – 1,5 yıl</td><td>4 hafta</td></tr><tr><td>1,5 – 3 yıl</td><td>6 hafta</td></tr><tr><td>3 yıldan fazla</td><td>8 hafta</td></tr></tbody></table></div>
<p>İhbar tazminatı, ihbar süresine karşılık gelen <b>giydirilmiş brüt ücret</b> üzerinden hesaplanır. Kıdem tazminatından farklı olarak gelir vergisi ve damga vergisine tabidir ve tavan uygulanmaz.</p>`,
    faq: [
      ['İhbar tazminatını kim öder?', 'Bildirim süresine uymadan sözleşmeyi fesheden taraf öder. İşçi bildirim süresi vermeden istifa ederse işverene ihbar tazminatı ödemesi gerekebilir.'],
      ['İhbar tazminatında tavan var mı?', 'Hayır. Kıdem tazminatı tavanı ihbar tazminatına uygulanmaz.'],
    ],
  },
  {
    path: '/issizlik-maasi-hesaplama/', short: 'İşsizlik maaşı', tile: `${tl(E.issizlik({ ortalamaBrut: P.asgariBrut, primGun: 600 }).net)} – ${tl(E.issizlik({ ortalamaBrut: 1e9, primGun: 600 }).net)}`,
    h1: `İşsizlik maaşı hesaplama ${Y}`,
    title: `İşsizlik Maaşı Hesaplama ${Y} – Ne Kadar ve Kaç Ay Alırım?`,
    description: `${Y} işsizlik maaşı en az ${tl(E.issizlik({ ortalamaBrut: P.asgariBrut, primGun: 600 }).net)}, en çok ${tl(E.issizlik({ ortalamaBrut: 1e9, primGun: 600 }).net)}. Son 4 ay brüt ücretinize ve prim gününüze göre aylık tutarı ve süreyi hesaplayın.`,
    lead: 'Son 4 aydaki ortalama brüt ücretinizi ve son 3 yıldaki prim gün sayınızı girin.',
    form: `<form class="calc" data-calc="issizlik"><div class="row2">${money('brut', 'Son 4 ay ortalama brüt ücret (₺)', '50.000')}<label>Son 3 yıldaki prim günü<input name="gun" inputmode="numeric" value="900"></label></div>${go}</form>`,
    content: `<h2>İşsizlik maaşı nasıl hesaplanır?</h2>
<p>Günlük işsizlik ödeneği, son 4 aylık prime esas kazançların günlük ortalamasının <b>%40'ıdır</b>. Ödenek, brüt asgari ücretin <b>%80'ini</b> geçemez. Ödenekten yalnızca damga vergisi kesilir.</p>
<h3>Ödeme süreleri</h3><div class="tablewrap"><table><thead><tr><th>Son 3 yılda prim günü</th><th>Ödeme süresi</th></tr></thead><tbody><tr><td>600 gün</td><td>180 gün (6 ay)</td></tr><tr><td>900 gün</td><td>240 gün (8 ay)</td></tr><tr><td>1080 gün</td><td>300 gün (10 ay)</td></tr></tbody></table></div>
<p>Ayrıca işten ayrılmadan önceki son 120 gün kesintisiz prim ödenmiş olmalı ve iş sözleşmesi çalışanın kusuru dışında sona ermiş olmalıdır. Başvuru, işten ayrılıştan sonra 30 gün içinde İŞKUR'a yapılır.</p>`,
    faq: [
      [`${Y} en düşük işsizlik maaşı ne kadar?`, `Brüt asgari ücretin %40'ı üzerinden, damga vergisi düşülerek yaklaşık ${tl(E.issizlik({ ortalamaBrut: P.asgariBrut, primGun: 600 }).net)}.`],
      [`${Y} en yüksek işsizlik maaşı ne kadar?`, `Brüt asgari ücretin %80'i üzerinden yaklaşık ${tl(E.issizlik({ ortalamaBrut: 1e9, primGun: 600 }).net)}.`],
      ['İstifa eden işsizlik maaşı alabilir mi?', 'Kural olarak hayır. Haklı nedenle fesih (ücretin ödenmemesi gibi) halinde alınabilir.'],
    ],
  },
  {
    path: '/fazla-mesai-hesaplama/', short: 'Fazla mesai', tile: 'Saatlik mesai ücreti, %50 / %25 zam',
    h1: `Fazla mesai ücreti hesaplama ${Y}`,
    title: `Fazla Mesai Ücreti Hesaplama ${Y} – Saatlik Mesai Ne Kadar?`,
    description: 'Brüt maaşınıza göre saatlik ücreti ve %50 zamlı fazla mesai ücretini hesaplayın. Asgari ücretli için saatlik mesai ücreti dahil.',
    lead: 'Aylık brüt ücretinizi ve mesai saatinizi girin.',
    form: `<form class="calc" data-calc="mesai"><div class="row2">${money('brut', 'Aylık brüt maaş (₺)', '50.000')}<label>Mesai saati<input name="saat" inputmode="decimal" value="10"></label></div>
<label>Çalışma türü<select name="tip"><option value="fazla">Fazla çalışma (haftalık 45 saat üstü, %50)</option><option value="sure">Fazla sürelerle çalışma (45 saate kadar, %25)</option></select></label>${go}</form>`,
    content: `<h2>Fazla mesai nasıl hesaplanır?</h2><p>Saatlik brüt ücret, aylık brüt ücretin 225'e bölünmesiyle bulunur. Haftalık 45 saati aşan her saat için bu ücretin <b>%50 fazlası</b> ödenir. Sözleşmede haftalık süre 45 saatin altında belirlenmişse, 45 saate kadar olan fazla süreler için <b>%25 fazlası</b> ödenir. Yıllık fazla çalışma 270 saati geçemez.</p>
<p>Örneğin ${Y} brüt asgari ücretle saatlik ücret ${tl(E.fazlaMesai({ brut: P.asgariBrut, saat: 1 }).saatlik)}, bir saatlik fazla mesai ücreti ${tl(E.fazlaMesai({ brut: P.asgariBrut, saat: 1 }).saatlikMesai)} olur (brüt).</p>`,
    faq: [['Fazla mesai ücretinden vergi kesilir mi?', 'Evet. Fazla mesai ücreti maaşa eklenir; SGK, gelir vergisi ve damga vergisi kesintilerine tabidir.'], ['Fazla mesai yerine izin kullanılabilir mi?', 'Çalışan isterse her fazla çalışma saati için 1,5 saat, fazla süreli çalışma saati için 1,25 saat serbest zaman kullanabilir.']],
  },
  {
    path: '/tapu-harci-hesaplama/', short: 'Tapu harcı', tile: 'Alıcı %2 + satıcı %2',
    h1: `Tapu harcı hesaplama ${Y}`,
    title: `Tapu Harcı Hesaplama ${Y} – Alıcı ve Satıcı Ne Kadar Öder?`,
    description: 'Ev, arsa veya iş yeri satışında alıcı ve satıcının ödeyeceği %2 + %2 tapu harcını hesaplayın.',
    lead: 'Tapuda beyan edilecek satış bedelini girin.',
    form: `<form class="calc" data-calc="tapu">${money('bedel', 'Satış bedeli (₺)', '3.000.000')}${go}</form>`,
    content: `<h2>Tapu harcı nasıl hesaplanır?</h2><p>Gayrimenkul satışında tapu harcı, beyan edilen satış bedelinin <b>%2'si alıcıdan, %2'si satıcıdan</b> olmak üzere toplam %4'tür. Taraflar aralarında anlaşarak harcın tamamını birinin ödemesine karar verebilir.</p><p>Beyan edilen bedel, gayrimenkulün emlak vergisi değerinden düşük olamaz. Gerçek satış bedelinin altında beyan, vergi ziyaı cezasına yol açabilir. Tapu harcına ek olarak Tapu ve Kadastro Genel Müdürlüğü'nün belirlediği döner sermaye ücreti ödenir.</p>`,
    faq: [['Tapu harcını kim öder?', 'Kanuna göre alıcı ve satıcı %2\'şer öder. Uygulamada taraflar farklı paylaşım üzerinde anlaşabilir.']],
  },
  {
    path: '/ikramiye-hesaplama/', short: 'İkramiye hesaplama', tile: 'Brüt ikramiyenin neti ve vergisi',
    h1: `İkramiye hesaplama ${Y}: net ne kadar kalır?`,
    title: `İkramiye Hesaplama ${Y} – Brüt İkramiye Net Ne Kadar? Vergi ve SGK Kesintisi`,
    description: `Brüt ikramiyenizin net tutarını hesaplayın: ödendiği aya göre SGK, gelir vergisi dilimi ve damga vergisi kesintileri. ${Y} parametreleriyle.`,
    lead: 'Aylık brüt maaşınızı, brüt ikramiye tutarını ve ödeneceği ayı girin.',
    form: `<form class="calc" data-calc="ikramiye"><div class="row2">${money('brut', 'Aylık brüt maaş (₺)', '75.000')}${money('ikramiye', 'Brüt ikramiye (₺)', '75.000')}</div><label>Ödeneceği ay<select name="ay">${['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'].map((m, i) => `<option value="${i + 1}"${i === 11 ? ' selected' : ''}>${m}</option>`).join('')}</select></label>${go}</form>`,
    content: () => { const r = E.ikramiye({ brut: 75000, ikramiye: 75000, ay: 12 }); return `<h2>İkramiyeden hangi kesintiler yapılır?</h2>
<p>İkramiye ödendiği ayın maaşına eklenir ve maaş gibi vergilendirilir: <b>%14 SGK</b> ve <b>%1 işsizlik sigortası</b> primi (SGK tavanına kadar), <b>gelir vergisi</b> ve <b>binde 7,59 damga vergisi</b> kesilir.</p>
<h3>Gelir vergisi neden yüksek?</h3><p>Gelir vergisi yılbaşından beri biriken (kümülatif) matraha göre hesaplanır. Yıl sonuna doğru çoğu çalışan %20 veya %27 dilimindedir ve ikramiye bu en yüksek dilimden vergilenir. Asgari ücret istisnası aylık uygulandığı için normal maaşta zaten kullanılmıştır; ikramiyeye ek istisna gelmez.</p>
<p>Örnek: aylık ${tl(75000)} brüt maaşla Aralık'ta ${tl(75000)} brüt ikramiye alan çalışanın eline <b>${tl(r.net)}</b> geçer (%${fmt(r.oran * 100, 1)}). Kesintiler: SGK ve işsizlik ${tl(r.sgk)}, gelir vergisi ${tl(r.gv)}, damga vergisi ${tl(r.damga)}.</p>
<h3>Hangi ayda ödendiği önemli mi?</h3><p>Yıllık toplam vergi, yılın toplam matrahına göre belirlendiği için ikramiye hangi ayda ödenirse ödensin yıl sonundaki toplam net gelir hemen hemen aynıdır. Değişen, o ayın netidir: yılın başında ödenen ikramiye düşük dilimde vergilenir ama sonraki aylarda daha erken dilim atlarsınız.</p>
<p>Aylık maaşınızın 12 aylık dökümü için <a href="/maas-hesaplama/">maaş hesaplama</a> aracını kullanın.</p>`; },
    faq: [
      ['İkramiyeden vergi kesilir mi?', 'Evet. İkramiye ücret sayılır; SGK primi, işsizlik sigortası primi, gelir vergisi ve damga vergisi kesilir.'],
      ['Brüt ikramiyenin yüzde kaçı net kalır?', `Yıl sonunda %27 dilimindeki bir çalışan için yaklaşık %61'i. Dilim düştükçe oran yükselir.`],
      ['İkramiye SGK tavanını aşarsa ne olur?', `Aylık prime esas kazanç ${tl(P.sgkTavan)} tavanını aşarsa, aşan kısımdan SGK primi kesilmez; gelir vergisi ve damga vergisi kesilmeye devam eder.`],
    ],
  },
  {
    path: '/emekli-memur-zammi-hesaplama/', short: 'Emekli ve memur zammı', tile: `${P.memurEmekli.donem} zam oranı ve yeni maaş`,
    h1: `Emekli ve memur zammı hesaplama (${P.memurEmekli.donem})`,
    title: `Emekli ve Memur Zammı Hesaplama ${P.memurEmekli.donem} – SSK, Bağ-Kur, Memur Yeni Maaş`,
    description: `${P.memurEmekli.donem} SSK, Bağ-Kur ve memur zammını hesaplayın: 6 aylık enflasyon, toplu sözleşme zammı ve enflasyon farkıyla yeni maaşınız. Aylık TÜFE verileriyle güncellenir.`,
    lead: 'Maaşınızı ve grubunuzu seçin. 6 aylık enflasyon kutusu, şu ana kadar açıklanan aylarla doldurulmuştur; kesinleşen rakamla değiştirebilirsiniz.',
    form: (() => { const k = E.kumulatifTufe(P.memurEmekli.aylar) * 100; return `<form class="calc" data-calc="memur"><label>Grup<select name="tur"><option value="emekli">SSK veya Bağ-Kur emeklisi</option><option value="memur">Memur</option><option value="memur-emekli">Memur emeklisi</option></select></label><div class="row2">${money('maas', 'Mevcut aylık net maaş (₺)', '20.000')}<label>6 aylık enflasyon (%)<input name="enf" inputmode="decimal" value="${fmt(k)}"></label></div><div class="row2" data-memur>${money('tso', 'Önceki dönem toplu sözleşme zammı (%)', String(P.memurEmekli.tsOnceki))}${money('tsy', 'Yeni dönem toplu sözleşme zammı (%)', String(P.memurEmekli.tsYeni))}</div>${go}</form>`; })(),
    content: () => {
      const M = P.memurEmekli, k = Math.round(E.kumulatifTufe(M.aylar) * 10000) / 10000;
      const memur = E.memurEmekliZam({ maas: 1, tur: 'memur', enf: k * 100 });
      let cum = 1;
      const rows = M.aylar.map(([ay, o]) => { cum *= 1 + o / 100; return `<tr><td>${ay}</td><td>%${fmt(o)}</td><td>%${fmt((cum - 1) * 100)}</td></tr>`; }).join('') + M.kalan.map((a) => `<tr><td>${a}</td><td colspan="2">Henüz açıklanmadı</td></tr>`).join('');
      const ex = [15000, 20000, 25000, 30000].map((v) => `<tr><td>${tl(v)}</td><td>${tl(v * (1 + k))}</td></tr>`).join('');
      const exm = [50000, 60000, 75000, 90000].map((v) => `<tr><td>${tl(v)}</td><td>${tl(v * (1 + memur.oran))}</td></tr>`).join('');
      return `<h2>${M.donem} zammı nasıl hesaplanır?</h2>
<p><b>SSK ve Bağ-Kur emeklileri</b>, önceki 6 ayın (Temmuz–Aralık veya Ocak–Haziran) TÜFE artışı kadar zam alır. <b>Memurlar ve memur emeklileri</b> ise toplu sözleşmeyle belirlenen zammı alır; önceki 6 aydaki enflasyon, o dönemin toplu sözleşme zammını aşarsa aradaki fark (enflasyon farkı) da eklenir.</p>
<h3>Şu ana kadar açıklanan aylık enflasyon</h3><div class="tablewrap"><table><thead><tr><th>Ay</th><th>Aylık TÜFE</th><th>Kümülatif</th></tr></thead><tbody>${rows}</tbody></table></div>
<p>${M.kesin ? 'Oranlar kesinleşmiştir.' : `<b>Rakamlar henüz kesinleşmedi.</b> ${M.kalan.length} aylık veri daha açıklanınca bu sayfa aynı gün güncellenir. Şimdiye kadarki ${M.aylar.length} aylık enflasyon %${fmt(k * 100)}.`}</p>
<h3>Şu ana kadarki verilerle emekli maaşı</h3><div class="tablewrap"><table><thead><tr><th>Mevcut maaş</th><th>Yeni maaş (%${fmt(k * 100)})</th></tr></thead><tbody>${ex}</tbody></table></div>
<h3>Şu ana kadarki verilerle memur maaşı</h3><p>Toplu sözleşme zammı %${fmt(M.tsYeni)}, enflasyon farkı %${fmt(memur.fark * 100)}: toplam %${fmt(memur.oran * 100)}.</p><div class="tablewrap"><table><thead><tr><th>Mevcut maaş</th><th>Yeni maaş</th></tr></thead><tbody>${exm}</tbody></table></div>
<p>En düşük emekli aylığı ve bayram ikramiyesi ayrıca kanunla belirlenir; otomatik olarak artmaz. Kendi maaş artışınızı yorumlamak için <a href="/zam-hesaplama/">zam hesaplama</a> aracını kullanabilirsiniz.</p>`;
    },
    faq: [
      ['Emekli zammı ne zaman belli olur?', 'Ocak zammı, TÜİK’in Aralık enflasyonunu açıkladığı 3 Ocak civarında; Temmuz zammı ise Haziran enflasyonunun açıklandığı 3 Temmuz civarında kesinleşir.'],
      ['SSK ve Bağ-Kur emeklisi aynı zammı mı alır?', 'Evet. İkisi de önceki 6 ayın TÜFE artışı kadar zam alır.'],
      ['Memur enflasyon farkı nasıl hesaplanır?', '(1 + 6 aylık enflasyon) ÷ (1 + o dönemin toplu sözleşme zammı) − 1. Sonuç sıfırdan büyükse yeni dönem toplu sözleşme zammıyla çarpılarak eklenir.'],
    ],
  },
  {
    path: '/mtv-hesaplama/', short: 'MTV hesaplama', tile: `${P.mtvYil} motorlu taşıtlar vergisi`,
    h1: `MTV hesaplama ${P.mtvYil}: otomobil motorlu taşıtlar vergisi`,
    title: `MTV Hesaplama ${P.mtvYil} – Motor Hacmi, Yaş ve Taşıt Değerine Göre Motorlu Taşıtlar Vergisi`,
    description: `${P.mtvYil} otomobil MTV tutarını motor hacmi, model yılı ve taşıt değerine göre hesaplayın. Ocak ve Temmuz taksitleri ile ${P.mtvYil + 1} tahmini.`,
    lead: 'Aracınızın motor hacmini, model yılını ve (2018 ve sonrası tescilde) ilk tescildeki taşıt değerini girin.',
    form: `<form class="calc" data-calc="mtv"><label>İlk tescil tarihi<select name="tescil"><option value="yeni">1 Ocak 2018 ve sonrası</option><option value="eski">31 Aralık 2017 ve öncesi</option></select></label><div class="row2"><label>Motor silindir hacmi (cm³)<input name="cc" inputmode="numeric" value="1598"></label><label>Model yılı<input name="yil" inputmode="numeric" value="2023"></label></div><div data-yeni>${money('deger', 'Taşıt değeri (ilk tescil, KDV hariç ₺)', '450.000')}</div>${go}</form>`,
    content: () => {
      const yd = P.yenidenDegerleme;
      const rows = P.mtvEski.map(([lim, a], i) => { const lo = i ? P.mtvEski[i - 1][0] + 1 : 0; return `<tr><td>${lim === Infinity ? `${fmt(lo, 0)} ve üzeri` : i ? `${fmt(lo, 0)}–${fmt(lim, 0)}` : `${fmt(lim, 0)} ve altı`}</td>${a.map((v) => `<td>${fmt(v, 0)}</td>`).join('')}</tr>`; }).join('');
      return `<h2>MTV nasıl hesaplanır?</h2>
<p>Otomobillerde motorlu taşıtlar vergisi; <b>motor silindir hacmine</b>, <b>aracın yaşına</b> ve 1 Ocak 2018'den sonra ilk kez tescil edilen araçlarda <b>taşıt değerine</b> (ilk tescildeki KDV hariç bedel) göre (I) sayılı tarifeden bulunur. Yaş, model yılından hesaplanır: ${P.mtvYil} için ${P.mtvYil - 2}–${P.mtvYil} model araçlar 1-3 yaş grubundadır.</p>
<p>Yıllık vergi iki eşit taksitte ödenir: <b>Ocak</b> ve <b>Temmuz</b> ayları sonuna kadar.</p>
<h3>${P.mtvYil} tarifesi (31.12.2017 ve öncesi tescilli otomobiller, yıllık TL)</h3><div class="tablewrap"><table><thead><tr><th>Motor hacmi (cm³)</th><th>1-3</th><th>4-6</th><th>7-11</th><th>12-15</th><th>16+</th></tr></thead><tbody>${rows}</tbody></table></div>
<p>2018 ve sonrası tescilli araçlarda her motor hacmi diliminde taşıt değerine göre 2–3 ayrı satır vardır; hesaplama aracı doğru satırı seçer.</p>
<h3>${yd.uygulanacakYil} MTV ne kadar olacak?</h3><p>MTV tutarları her yıl yeniden değerleme oranı kadar artırılır. ${yd.uygulanacakYil} için oran <b>%${fmt(yd.oran)}</b> olarak açıklandı. Hesaplama aracındaki ${yd.uygulanacakYil} tutarı bu oranla bulunmuş bir <b>tahmindir</b>; kesin tarife Aralık sonunda yayımlanacak tebliğle belli olur ve bu sayfa güncellenir.</p>`;
    },
    faq: [
      ['MTV ne zaman ödenir?', 'Yılda iki eşit taksitte: Ocak ve Temmuz ayları sonuna kadar.'],
      ['Taşıt değeri nedir?', '1 Ocak 2018 ve sonrası ilk kez tescil edilen araçlarda, ilk tescildeki KDV hariç satış bedelidir (faturada yazan tutar). Sonraki yıllarda bu sınırlar yeniden değerleme oranıyla güncellenir.'],
      [`${P.yenidenDegerleme.uygulanacakYil} MTV zammı ne kadar?`, `Yeniden değerleme oranı kadar, yani %${fmt(P.yenidenDegerleme.oran)}.`],
    ],
  },
  {
    path: '/zam-hesaplama/', short: 'Zam hesaplama', tile: 'Maaş zammı oranı ve yeni maaş',
    h1: 'Maaş zammı hesaplama',
    title: 'Zam Hesaplama – Maaş Zammı Yüzde Kaç? Yeni Maaş Ne Kadar?',
    description: 'Eski ve yeni maaşınıza göre zam oranını veya zam oranına göre yeni maaşınızı hesaplayın.',
    lead: 'Zam oranını bulmak için yeni tutarı, yeni maaşı bulmak için zam oranını girin.',
    form: `<form class="calc" data-calc="zam">${money('eski', 'Mevcut maaş (₺)', '40.000')}<div class="row2">${money('yeni', 'Yeni maaş (₺)', '50.000')}${money('oran', 'veya zam oranı (%)', '')}</div>${go}</form>`,
    content: `<h2>Zam oranı nasıl hesaplanır?</h2><p>Zam oranı = (yeni maaş − eski maaş) ÷ eski maaş × 100. Zammın enflasyonu karşılayıp karşılamadığını görmek için oranı yıllık enflasyonla karşılaştırın.</p><p>Brüt zammın net maaşa etkisini görmek için <a href="/maas-hesaplama/">maaş hesaplama</a> aracını kullanın.</p>`,
    faq: [],
  },
  {
    path: '/emlak-vergisi-hesaplama/', short: 'Emlak vergisi', tile: 'Konut, işyeri, arsa · taksitler',
    h1: `Emlak vergisi hesaplama ${Y}`,
    title: `Emlak Vergisi Hesaplama ${Y} – Konut, İşyeri, Arsa ve Taksit Tutarları`,
    description: `${Y} emlak vergisini vergi değerinden hesaplayın: konut binde 1 (büyükşehirde binde 2), işyeri, arsa ve arazi oranları, hisse payı ve iki taksit tutarı.`,
    lead: 'Taşınmazın vergi değerini, türünü ve bulunduğu yeri seçin. Yıllık vergiyi ve iki taksiti görün.',
    form: `<form class="calc" data-calc="emlak">
${money('deger', 'Bu yılın vergi değeri (₺) <small>e-Devlet veya belediye beyanı</small>', '4.000.000')}
<div class="row2"><label>Taşınmaz türü<select name="tur"><option value="konut">Konut (mesken)</option><option value="isyeri">İşyeri / diğer bina</option><option value="arsa">Arsa</option><option value="arazi">Arazi (tarla, bahçe)</option></select></label>
<label>Bulunduğu yer<select name="yer"><option value="buyuksehir">Büyükşehir / mücavir alan</option><option value="normal">Diğer yerler</option></select></label></div>
<div class="row2">${money('hisse', 'Hisse payınız (%)', '100')}${money('onceki', 'Geçen yılın vergi değeri (₺) <small>isteğe bağlı, 3 kat sınırı için</small>', '')}</div>
<label class="check"><input type="checkbox" name="muaf">Muafiyet şartlarını taşıyorum (tek konut, 200 m² altı, emekli/geliri yok vb.)</label>
${go}</form>`,
    content: `<h2>Emlak vergisi nasıl hesaplanır?</h2>
<p>Emlak vergisi = vergi değeri × vergi oranı × hisse payınız. Vergi değeri; binanın metrekare inşaat maliyeti ve bulunduğu yerin arsa (arsa payı) değeri birlikte dikkate alınarak belirlenir. Kendi taşınmazınızın değerini e-Devlet'teki emlak vergisi borç sorgulama ekranından veya belediyenizden öğrenebilirsiniz.</p>
<h3>Emlak vergisi oranları</h3>
<div class="tablewrap"><table><thead><tr><th>Taşınmaz</th><th>Diğer yerler</th><th>Büyükşehir / mücavir alan</th></tr></thead><tbody>
<tr><td>Konut</td><td>binde 1</td><td>binde 2</td></tr><tr><td>İşyeri / diğer bina</td><td>binde 2</td><td>binde 4</td></tr><tr><td>Arsa</td><td>binde 3</td><td>binde 6</td></tr><tr><td>Arazi</td><td>binde 1</td><td>binde 2</td></tr></tbody></table></div>
<h3>${Y} için 3 kat sınırı</h3>
<p>2026–2029 dönemi için belirlenen yeni değerlerde, ${Y} yılı vergi değeri 2025 yılı vergi değerinin iki katından fazla artamaz; yani en fazla 3 katı olabilir. Geçen yılın değerini girerseniz araç bu sınırı otomatik uygular. Sonraki yıllarda değer, yeniden değerleme oranına göre güncellenir.</p>
<h3>Ödeme tarihleri</h3>
<p>Vergi iki eşit taksitte ödenir: 1. taksit Mart–Mayıs, 2. taksit Kasım ayı sonuna kadar. Geç ödemede aylık gecikme zammı uygulanır. Tapuda satış yapılabilmesi için o yılın vergisinin tamamının ödenmiş olması gerekir.</p>
<h3>Kimler muaf?</h3>
<p>Brüt 200 m²'yi geçmeyen tek konutu bulunan ve geliri olmayan, yalnızca emekli aylığı alan, gazi, engelli veya şehit dul ve yetimleri için konut vergisi oranı sıfır uygulanır. Hisseli de olsa başka konutu olanlar yararlanamaz. Muafiyet için belediyeye dilekçe verilmesi gerekir.</p>`,
    faq: [
      ['Emlak vergisi değerimi nereden öğrenirim?', 'e-Devlet\'te belediyenizin "Emlak Vergisi Borç Sorgulama" hizmetinden veya belediyenin emlak servisinden öğrenebilirsiniz.'],
      [`${Y} emlak vergisi 2. taksit ne zaman ödenir?`, 'İkinci taksit Kasım ayının sonuna kadar ödenir.'],
      ['Büyükşehirde emlak vergisi oranı neden iki kat?', 'Kanuna göre büyükşehir belediye sınırları ve mücavir alanlarda oranlar %100 artırımlı uygulanır.'],
    ],
  },
  {
    path: '/kira-artis-hesaplama/', short: 'Kira artışı', tile: `${kNow.ay} oranı: %${fmt(kNow.oran)}`,
    h1: `Kira artış hesaplama (${kNow.ay}: %${fmt(kNow.oran)})`,
    title: `Kira Artış Hesaplama ${kNow.ay} – Yasal Oran %${fmt(kNow.oran)}`,
    description: `${kNow.ay} kira artış oranı %${fmt(kNow.oran)} (TÜFE 12 aylık ortalama). Mevcut kiranızı girin, yasal üst sınıra göre yeni kirayı hesaplayın.`,
    lead: `Konut ve çatılı işyeri kiralarında yasal artış sınırı TÜFE'nin 12 aylık ortalamasıdır. ${kNow.ay} ayında yenilenen sözleşmeler için oran %${fmt(kNow.oran)}.`,
    form: `<form class="calc" data-calc="kira">
<div class="row2">${money('kira', 'Mevcut aylık kira (₺)', '20.000')}
<label>Artış oranı (%)<select name="oran">${P.kiraOranlari.map((k) => `<option value="${k.oran}">${k.ay} – %${fmt(k.oran)}</option>`).join('')}</select></label></div>
${go}</form>`,
    content: `<h2>Kira artışı nasıl hesaplanır?</h2>
<p>Yeni kira = mevcut kira × (1 + 12 aylık ortalama TÜFE). Kullanılacak oran, kira yılının yenilendiği aydan bir önceki ayın TÜİK verisiyle açıklanan orandır. Örneğin ${kNow.ay} ayında yenilenen bir sözleşmede %${fmt(kNow.oran)} uygulanır.</p>
<h3>Son aylarda açıklanan oranlar</h3>
<div class="tablewrap"><table><thead><tr><th>Uygulama ayı</th><th>Oran</th></tr></thead><tbody>${P.kiraOranlari.map((k) => `<tr><td>${k.ay}</td><td>%${fmt(k.oran)}</td></tr>`).join('')}</tbody></table></div>`,
    faq: [
      ['Ev sahibi yasal orandan fazla zam yapabilir mi?', 'Yenilenen kira dönemlerinde artış, TÜFE 12 aylık ortalamasını geçemez (TBK m.344). Daha düşük bir oranda anlaşmak mümkündür.'],
      ['%25 kira artış sınırı hâlâ geçerli mi?', 'Hayır. Konut kiralarında geçici olarak uygulanan %25 sınırı sona ermiştir; artışlarda TÜFE 12 aylık ortalaması esas alınır.'],
      ['5 yılı dolan sözleşmelerde ne olur?', '5 yıldan uzun süren kira ilişkilerinde, yeni kira yılında kira bedeli hâkim tarafından emsal kiralar dikkate alınarak yeniden belirlenebilir (kira tespit davası).'],
    ],
  },
  {
    path: '/kredi-hesaplama/', short: 'Kredi hesaplama', tile: 'KKDF/BSMV dahil taksit ve ödeme planı',
    h1: `Kredi hesaplama ${Y}: taksit ve ödeme planı`,
    title: `Kredi Hesaplama ${Y} – KKDF ve BSMV Dahil Taksit ve Ödeme Planı`,
    description: 'İhtiyaç, taşıt ve konut kredisi için aylık taksit, toplam geri ödeme ve vergiler dahil ödeme planını hesaplayın.',
    lead: 'Bankanın verdiği aylık faiz oranını girin. İhtiyaç ve taşıt kredilerinde %15 KKDF ve %15 BSMV otomatik eklenir.',
    form: `<form class="calc" data-calc="kredi">
<label>Kredi türü<select name="tur"><option value="ihtiyac">İhtiyaç kredisi (KKDF %15 + BSMV %15)</option><option value="tasit">Taşıt kredisi (KKDF %15 + BSMV %15)</option><option value="konut">Konut kredisi (vergisiz)</option></select></label>
<div class="row2">${money('tutar', 'Kredi tutarı (₺)', '200.000')}<label>Vade (ay)<input name="vade" inputmode="numeric" value="24"></label></div>
${money('faiz', 'Aylık faiz oranı (%) <small>bankanın ilan ettiği akdi faiz</small>', '3,50')}
${go}</form>`,
    content: `<h2>Kredi taksiti nasıl hesaplanır?</h2>
<p>Eşit taksitli kredilerde taksit, vergiler eklenmiş efektif faiz oranıyla anüite formülüyle hesaplanır. İhtiyaç ve taşıt kredilerinde her ay ödenen faizin %15'i kadar KKDF ve %15'i kadar BSMV alınır; bu, faiz yükünü yaklaşık %30 artırır. Konut kredileri bu vergilerden muaftır.</p>
<p>Bankalar ayrıca kredi tahsis ücreti (en fazla anaparanın binde 5'i) ve sigorta primi alabilir. Bunlar burada dahil değildir; teklifleri karşılaştırırken yıllık maliyet oranına bakın.</p>`,
    faq: [
      ['KKDF ve BSMV nedir?', 'KKDF (Kaynak Kullanımını Destekleme Fonu) ve BSMV (Banka ve Sigorta Muameleleri Vergisi), tüketici kredilerinde faiz tutarı üzerinden alınan yasal kesintilerdir. İhtiyaç ve taşıt kredisinde her biri %15\'tir.'],
      ['Konut kredisinde vergi var mı?', 'Konut kredileri KKDF ve BSMV\'den muaftır.'],
    ],
  },
  {
    path: '/mevduat-faizi-hesaplama/', short: 'Mevduat faizi', tile: 'Stopaj sonrası net getiri',
    h1: `Mevduat faizi hesaplama ${Y}`,
    title: `Mevduat Faizi Hesaplama ${Y} – Stopaj Sonrası Net Getiri`,
    description: 'Vadeli mevduatın brüt ve net getirisini güncel stopaj oranlarıyla (%17,5 / %15 / %10) hesaplayın.',
    lead: 'Anapara, yıllık faiz ve vade gününü girin. Stopaj oranı vadeye göre otomatik seçilir.',
    form: `<form class="calc" data-calc="mevduat">
${money('tutar', 'Anapara (₺)', '100.000')}
<div class="row2">${money('faiz', 'Yıllık brüt faiz (%)', '38')}<label>Vade (gün)<input name="gun" inputmode="numeric" value="32"></label></div>
<div class="chips">${[32, 46, 92, 181, 365].map((g) => `<button type="button" data-set="gun=${g}">${g} gün</button>`).join('')}</div>
${go}</form>`,
    content: `<h2>Mevduat getirisi nasıl hesaplanır?</h2>
<p>Brüt faiz = anapara × yıllık faiz × gün / 365. Brüt faizden stopaj (gelir vergisi kesintisi) düşülerek net getiri bulunur.</p>
<h3>TL mevduat stopaj oranları</h3>
<div class="tablewrap"><table><thead><tr><th>Vade</th><th>Stopaj</th></tr></thead><tbody><tr><td>Vadesiz ve 6 aya kadar</td><td>%17,5</td></tr><tr><td>6 ay – 1 yıl</td><td>%15</td></tr><tr><td>1 yıldan uzun</td><td>%10</td></tr></tbody></table></div>
<p class="note">Oranlar 31 Aralık ${Y}'ya kadar geçerli olmak üzere uzatılmıştır; Cumhurbaşkanı kararıyla değişebilir.</p>`,
    faq: [['Stopaj anaparadan mı kesilir?', 'Hayır, yalnızca faiz kazancından kesilir.'], ['Banka faizini nasıl seçmeliyim?', 'Brüt faiz yerine stopaj sonrası net getiriyi karşılaştırın; kampanya oranlarının tutar ve yeni müşteri koşullarını kontrol edin.']],
  },
  {
    path: '/kdv-hesaplama/', short: 'KDV hesaplama', tile: 'KDV dahil / hariç, %1 %10 %20',
    h1: 'KDV hesaplama: dahil ve hariç',
    title: 'KDV Hesaplama – KDV Dahil ve Hariç Tutar (%1, %10, %20)',
    description: 'KDV dahil fiyattan KDV\'yi ayırın veya KDV hariç tutara KDV ekleyin. %1, %10 ve %20 oranları.',
    lead: 'Tutarı ve oranı seçin; KDV tutarını, dahil ve hariç fiyatı anında görün.',
    form: `<form class="calc" data-calc="kdv">
<div class="seg"><label><input type="radio" name="tip" value="haric" checked>KDV hariç tutar</label><label><input type="radio" name="tip" value="dahil">KDV dahil tutar</label></div>
<div class="row2">${money('tutar', 'Tutar (₺)', '1.000')}<label>KDV oranı<select name="oran"><option value="20">%20 (genel)</option><option value="10">%10</option><option value="1">%1</option></select></label></div>
${go}</form>`,
    content: `<h2>KDV formülleri</h2><p><b>KDV hariçten dahile:</b> dahil tutar = tutar × (1 + oran).<br><b>KDV dahilden hariçe:</b> hariç tutar = tutar ÷ (1 + oran). Örneğin %20 KDV dahil 1.200 TL'nin hariç tutarı 1.000 TL, KDV'si 200 TL'dir.</p>
<p>Genel oran %20'dir. Bazı temel gıda ürünleri, kitaplar ve konut teslimleri gibi mal ve hizmetlerde %10 veya %1 oranı uygulanır.</p>`,
    faq: [['KDV dahil fiyattan KDV nasıl çıkarılır?', 'Tutarı 1 + KDV oranına bölün. %20 için 1,20\'ye bölmek gerekir; tutarı %20 azaltmak yanlış sonuç verir.']],
  },
  {
    path: '/yuzde-hesaplama/', short: 'Yüzde hesaplama', tile: 'Yüzdesi, yüzde kaçı, değişim oranı',
    h1: 'Yüzde hesaplama',
    title: 'Yüzde Hesaplama – Yüzdesi, Yüzde Kaçı ve Yüzde Değişim',
    description: 'Bir sayının yüzdesini, bir sayının diğerinin yüzde kaçı olduğunu ve iki sayı arasındaki yüzde değişimi hesaplayın.',
    lead: 'Üç yaygın yüzde hesabı tek sayfada. Doldurduğunuz satır anında hesaplanır.',
    form: `<form class="calc" data-calc="yuzde">
<div class="row2">${money('a1', 'Sayı', '250')}${money('b1', 'Yüzde (%)', '20')}</div>
<div class="row2">${money('a2', 'Bu sayı', '50')}${money('b2', 'Şu sayının yüzde kaçı?', '200')}</div>
<div class="row2">${money('a3', 'Eski değer', '80')}${money('b3', 'Yeni değer', '100')}</div>
${go}</form>`,
    content: `<h2>Formüller</h2><ul><li>A'nın %B'si = A × B ÷ 100</li><li>A, B'nin yüzde kaçı = A ÷ B × 100</li><li>Yüzde değişim = (yeni − eski) ÷ eski × 100</li></ul>`,
    faq: [['Zam oranı nasıl hesaplanır?', 'Yeni ücretten eski ücreti çıkarıp eski ücrete bölün ve 100 ile çarpın.']],
  },
  {
    path: '/yillik-izin-hesaplama/', short: 'Yıllık izin', tile: '14 / 20 / 26 gün kuralı',
    h1: 'Yıllık izin hesaplama',
    title: 'Yıllık İzin Hesaplama – Kaç Gün İzin Hakkım Var?',
    description: 'İş Kanunu\'na göre kıdeminize ve yaşınıza göre yıllık ücretli izin gününüzü hesaplayın.',
    lead: 'Hizmet sürenize ve yaşınıza göre yasal asgari yıllık ücretli izin hakkınızı öğrenin.',
    form: `<form class="calc" data-calc="izin"><div class="row2"><label>Kıdem (yıl)<input name="kidem" inputmode="numeric" value="3"></label><label>Yaşınız<input name="yas" inputmode="numeric" value="30"></label></div>${go}</form>`,
    content: `<h2>Yasal izin süreleri (4857 s. Kanun m.53)</h2><div class="tablewrap"><table><thead><tr><th>Hizmet süresi</th><th>İzin</th></tr></thead><tbody><tr><td>1 – 5 yıl (5 dahil)</td><td>14 gün</td></tr><tr><td>5 – 15 yıl</td><td>20 gün</td></tr><tr><td>15 yıl ve üzeri</td><td>26 gün</td></tr></tbody></table></div><p>18 yaş ve altındaki ile 50 yaş ve üzerindeki çalışanlara verilecek izin 20 günden az olamaz. Sözleşmeyle bu süreler artırılabilir.</p>`,
    faq: [['Hafta sonu ve resmi tatiller izinden sayılır mı?', 'Hayır. İzin süresine rastlayan hafta tatili ve resmi tatil günleri izin süresinden sayılmaz.']],
  },
  {
    path: '/iki-tarih-arasindaki-gun-hesaplama/', short: 'Gün hesaplama', tile: 'İki tarih arası gün, hafta, ay',
    h1: 'İki tarih arasındaki gün sayısı',
    title: 'İki Tarih Arasındaki Gün Hesaplama – Gün, Hafta, Ay',
    description: 'İki tarih arasında kaç gün, hafta, ay ve yıl olduğunu hesaplayın.',
    lead: 'Başlangıç ve bitiş tarihini seçin.',
    form: `<form class="calc" data-calc="tarih"><div class="row2">${date('a', 'Başlangıç', `${Y}-01-01`)}${date('b', 'Bitiş', '', true)}</div>${go}</form>`,
    content: '<h2>Nasıl hesaplanır?</h2><p>Bitiş günü dahil edilmez; iki tarih arasındaki tam gün farkı gösterilir. Başlangıç gününü de saymak isterseniz sonuca 1 ekleyin.</p>',
    faq: [],
  },
  {
    path: '/yas-hesaplama/', short: 'Yaş hesaplama', tile: 'Yıl, ay ve gün olarak yaş',
    h1: 'Yaş hesaplama',
    title: 'Yaş Hesaplama – Kaç Yaşındayım? (Yıl, Ay, Gün)',
    description: 'Doğum tarihinize göre yaşınızı yıl, ay, gün ve toplam gün olarak hesaplayın.',
    lead: 'Doğum tarihinizi girin.',
    form: `<form class="calc" data-calc="yas"><div class="row2">${date('dogum', 'Doğum tarihi', '1990-06-15')}${date('bugun', 'Hesap tarihi', '', true)}</div>${go}</form>`,
    content: '<h2>Yaş nasıl hesaplanır?</h2><p>Doğum tarihinden bugüne kadar geçen tam yıllar yaşı verir; kalan ay ve günler ayrıca gösterilir.</p>',
    faq: [],
  },
  {
    path: '/vucut-kitle-indeksi-hesaplama/', short: 'Vücut kitle indeksi', tile: 'VKİ ve normal kilo aralığı',
    h1: 'Vücut kitle indeksi (VKİ) hesaplama',
    title: 'Vücut Kitle İndeksi Hesaplama – VKİ ve İdeal Kilo Aralığı',
    description: 'Kilo ve boyunuza göre vücut kitle indeksinizi (VKİ) ve Dünya Sağlık Örgütü sınıflamasını hesaplayın.',
    lead: 'Kilonuzu ve boyunuzu girin.',
    form: `<form class="calc" data-calc="vki"><div class="row2">${money('kilo', 'Kilo (kg)', '70')}${money('boy', 'Boy (cm)', '175')}</div>${go}</form>`,
    content: '<h2>VKİ sınıfları</h2><div class="tablewrap"><table><thead><tr><th>VKİ</th><th>Sınıf</th></tr></thead><tbody><tr><td>&lt; 18,5</td><td>Zayıf</td></tr><tr><td>18,5 – 24,9</td><td>Normal</td></tr><tr><td>25 – 29,9</td><td>Fazla kilolu</td></tr><tr><td>30 ve üzeri</td><td>Obez</td></tr></tbody></table></div><p class="note">VKİ kas kütlesini ve vücut yapısını dikkate almaz; sağlıkla ilgili kararlar için hekiminize danışın.</p>',
    faq: [],
  },
];

const dilimRows = () => {
  let prev = 0;
  return P.gvDilim.map(([lim, rate]) => {
    const r = `<tr><td>${lim === Infinity ? `${fmt(prev, 0)} TL üzeri` : `${fmt(prev, 0)} – ${fmt(lim, 0)} TL`}</td><td>%${rate * 100}</td><td>${lim === Infinity ? '' : tl(E.gelirVergisi(lim))}</td></tr>`;
    prev = lim; return r;
  }).join('');
};

export const INFO_PAGES = [
  {
    path: `/asgari-ucret-${Y}/`, short: `Asgari ücret ${Y}`, tile: `Net ${tl(P.asgariNet)}`,
    h1: `Asgari ücret ${Y}: net ${tl(P.asgariNet)}`,
    title: `Asgari Ücret ${Y} – Net ${fmt(P.asgariNet)} TL, Brüt ${fmt(P.asgariBrut)} TL ve İşveren Maliyeti`,
    description: `${Y} asgari ücret: brüt ${tl(P.asgariBrut)}, net ${tl(P.asgariNet)}. Kesintiler, vergi istisnası ve işverene maliyet tablosu.`,
    body: () => {
      const a = asg.aylar[0];
      return `<p class="lead">${Y} yılında brüt asgari ücret <b>${tl(P.asgariBrut)}</b>, net asgari ücret <b>${tl(P.asgariNet)}</b>'dir. Günlük brüt asgari ücret ${tl(P.asgariBrut / 30)}.</p>
<h2>Kesintiler</h2><div class="tablewrap"><table><tbody>
<tr><td>Brüt asgari ücret</td><td>${tl(P.asgariBrut)}</td></tr><tr><td>SGK işçi payı (%14)</td><td>${tl(a.sgk)}</td></tr><tr><td>İşsizlik sigortası işçi payı (%1)</td><td>${tl(a.issizlik)}</td></tr><tr><td>Gelir vergisi</td><td>0,00 ₺ (istisna)</td></tr><tr><td>Damga vergisi</td><td>0,00 ₺ (istisna)</td></tr><tr><td><b>Net asgari ücret</b></td><td><b>${tl(a.net)}</b></td></tr></tbody></table></div>
<h2>İşverene maliyeti</h2><div class="tablewrap"><table><tbody><tr><td>5 puan SGK teşvikli</td><td>${tl(a.maliyet)}</td></tr><tr><td>Teşviksiz</td><td>${tl(E.brutNet(P.asgariBrut, { tesvik: false }).aylar[0].maliyet)}</td></tr></tbody></table></div>
<h2>Asgari ücret vergi istisnası</h2><p>Tüm çalışanların ücretlerinin asgari ücrete isabet eden kısmı gelir vergisi ve damga vergisinden istisnadır. Aylık gelir vergisi istisnası Ocak–Haziran ${tl(asg.aylar[0].gvIstisna)}, Temmuz ${tl(asg.aylar[6].gvIstisna)}, Ağustos–Aralık ${tl(asg.aylar[7].gvIstisna)}'dir. Aylık damga vergisi istisnası ${tl(P.asgariBrut * P.damga)}'dir.</p>
<p><a href="/maas-hesaplama/">Kendi maaşınızı hesaplayın →</a> · <a href="/asgari-ucret-${Y + 1}/">${Y + 1} zam senaryoları →</a></p>`;
    },
    faq: [[`${Y} net asgari ücret ne kadar?`, `${tl(P.asgariNet)}.`], [`${Y} brüt asgari ücret ne kadar?`, `${tl(P.asgariBrut)}.`], ['Asgari ücretten vergi kesilir mi?', 'Hayır. Gelir vergisi ve damga vergisi istisnası nedeniyle yalnızca SGK ve işsizlik sigortası primi kesilir.']],
  },
  {
    path: `/asgari-ucret-${Y + 1}/`, short: `Asgari ücret ${Y + 1}`, tile: 'Zam senaryoları: net, brüt, maliyet',
    h1: `Asgari ücret ${Y + 1}: zam senaryoları`,
    title: `Asgari Ücret ${Y + 1} – Zam Oranına Göre Net, Brüt ve İşveren Maliyeti`,
    description: `${Y + 1} asgari ücret ne kadar olur? %15, %20, %25 ve %30 zam senaryolarında net ve brüt asgari ücret ile işverene maliyet tablosu. Resmî rakam açıklanınca güncellenir.`,
    body: () => {
      const oranlar = [0.15, 0.20, 0.25, 0.30];
      const kesinti = P.sgkIsci + P.issizlikIsci;
      const tes = 1 + P.sgkIsverenTesvik + P.issizlikIsveren, tesYok = 1 + P.sgkIsveren + P.issizlikIsveren;
      const rows = oranlar.map((o) => { const b = P.asgariBrut * (1 + o); return `<tr><td>%${fmt(o * 100, 0)}</td><td>${tl(b)}</td><td><b>${tl(b * (1 - kesinti))}</b></td><td>+${tl(b * (1 - kesinti) - P.asgariNet)}</td><td>${tl(b * tes)}</td><td>${tl(b * tesYok)}</td></tr>`; }).join('');
      return `<p class="lead">${Y + 1} asgari ücreti henüz açıklanmadı. Aşağıdaki tablo, ${Y} rakamlarına (brüt ${tl(P.asgariBrut)}, net ${tl(P.asgariNet)}) farklı zam oranları uygulandığında ortaya çıkacak tutarları gösterir. <b>Bunlar senaryodur, resmî rakam değildir.</b> Resmî tutar açıklandığı gün bu sayfa güncellenecektir.</p>
<h2>Zam oranına göre ${Y + 1} asgari ücret</h2><div class="tablewrap"><table><thead><tr><th>Zam</th><th>Brüt</th><th>Net</th><th>Nete artış</th><th>İşverene maliyet (teşvikli)</th><th>İşverene maliyet (teşviksiz)</th></tr></thead><tbody>${rows}</tbody></table></div>
<p>Hesaplama ${Y} oranlarıyla yapılmıştır: işçiden SGK %14 ve işsizlik sigortası %1 kesilir; asgari ücret gelir vergisi ve damga vergisinden istisna olduğu için net, brütün %85'idir. İşveren maliyetinde SGK işveren payı (%${fmt(P.sgkIsverenTesvik * 100, 2)} teşvikli, %${fmt(P.sgkIsveren * 100, 2)} teşviksiz) ve %2 işsizlik sigortası işveren payı eklenir. Prim oranları veya teşvikler değişirse tutarlar da değişir.</p>
<h2>Asgari ücret nasıl belirlenir?</h2><p>Asgari ücret; işçi, işveren ve hükümet temsilcilerinden oluşan Asgari Ücret Tespit Komisyonu tarafından belirlenir ve Resmî Gazete'de yayımlanır. Yeni yıl asgari ücreti genellikle Aralık ayında açıklanır ve 1 Ocak'tan itibaren uygulanır.</p>
<h2>Asgari ücret zammı maaşımı nasıl etkiler?</h2><p>Asgari ücretin üzerinde maaş alanlarda da vergi istisnası asgari ücretle birlikte artar; bu nedenle brüt maaşınız aynı kalsa bile netiniz bir miktar yükselebilir. Kendi durumunuz için <a href="/maas-hesaplama/">maaş hesaplama</a> ve <a href="/zam-hesaplama/">zam hesaplama</a> araçlarını kullanabilirsiniz. Güncel rakamlar: <a href="/asgari-ucret-${Y}/">asgari ücret ${Y}</a>.</p>`;
    },
    faq: [
      [`${Y + 1} asgari ücret açıklandı mı?`, `Henüz açıklanmadı. Bu sayfadaki tutarlar zam senaryolarıdır; resmî rakam açıklandığında güncellenecektir.`],
      [`${Y + 1} asgari ücret %25 zamla ne kadar olur?`, `${Y} oranlarıyla brüt ${tl(P.asgariBrut * 1.25)}, net ${tl(P.asgariBrut * 1.25 * (1 - P.sgkIsci - P.issizlikIsci))} olur.`],
      ['Asgari ücret ne zaman açıklanır?', 'Genellikle Aralık ayında Asgari Ücret Tespit Komisyonu tarafından açıklanır ve 1 Ocak\'tan itibaren geçerli olur.'],
    ],
  },
  {
    path: `/gelir-vergisi-dilimleri-${Y}/`, short: `Vergi dilimleri ${Y}`, tile: '%15 – %40 ücret tarifesi',
    h1: `Gelir vergisi dilimleri ${Y}`,
    title: `Gelir Vergisi Dilimleri ${Y} – Ücret Gelirleri Tarifesi (%15–%40)`,
    description: `${Y} ücret gelirleri gelir vergisi tarifesi: 190.000 TL'ye kadar %15, 400.000 TL'ye kadar %20, 1.500.000 TL'ye kadar %27, 5.300.000 TL'ye kadar %35, üzeri %40.`,
    body: () => `<p class="lead">${Y} yılında ücret gelirlerine 332 Seri No.lu Gelir Vergisi Genel Tebliği ile belirlenen beş dilimli tarife uygulanır.</p>
<h2>Ücret gelirleri tarifesi</h2><div class="tablewrap"><table><thead><tr><th>Kümülatif matrah</th><th>Oran</th><th>Dilim sonuna kadar toplam vergi</th></tr></thead><tbody>${dilimRows()}</tbody></table></div>
<p>Ücret dışı gelirlerde (kira, serbest meslek, ticari kazanç) üçüncü dilim 1.000.000 TL'de biter; ücretlilerde bu sınır 1.500.000 TL'dir.</p>
<h2>Maaşınız hangi ayda dilim atlar?</h2><p>Bordroda vergi, yılbaşından itibaren biriken matraha göre hesaplanır. <a href="/maas-hesaplama/">Maaş hesaplama</a> aracındaki 12 aylık tablo, hangi ayda %20 veya %27 dilimine geçeceğinizi gösterir.</p>`,
    faq: [['İlk vergi dilimi sınırı ne kadar?', '190.000 TL.'], ['Asgari ücretli vergi dilimine girer mi?', 'Asgari ücretin vergisi istisna olduğundan, asgari ücretli çalışan gelir vergisi ödemez.']],
  },
  {
    path: `/gelir-vergisi-dilimleri-${P.yenidenDegerleme.uygulanacakYil}/`, short: `Vergi dilimleri ${P.yenidenDegerleme.uygulanacakYil}`, tile: P.yenidenDegerleme.uygulanacakYil > Y ? 'Tahmini tarife (yeniden değerleme ile)' : 'Ücret gelirleri tarifesi',
    h1: `Gelir vergisi dilimleri ${P.yenidenDegerleme.uygulanacakYil} (tahmini)`,
    title: `Gelir Vergisi Dilimleri ${P.yenidenDegerleme.uygulanacakYil} – Tahmini Tarife (%${fmt(P.yenidenDegerleme.oran)} Yeniden Değerleme)`,
    description: `${P.yenidenDegerleme.uygulanacakYil} gelir vergisi dilimleri ne olacak? ${Y} tarifesinin %${fmt(P.yenidenDegerleme.oran)} yeniden değerleme oranıyla güncellenmiş tahmini hali; ücret ve ücret dışı gelirler için.`,
    body: () => {
      const yd = P.yenidenDegerleme, N = yd.uygulanacakYil;
      const tab = (now, est) => { let pa = 0, pb = 0; return now.map(([lim, r], i) => { const [l2] = est[i]; const row = `<tr><td>%${r * 100}</td><td>${lim === Infinity ? `${fmt(pa, 0)} TL üzeri` : `${fmt(pa, 0)} – ${fmt(lim, 0)} TL`}</td><td><b>${l2 === Infinity ? `${fmt(pb, 0)} TL üzeri` : `${fmt(pb, 0)} – ${fmt(l2, 0)} TL`}</b></td></tr>`; pa = lim; pb = l2; return row; }).join(''); };
      return `<p class="lead">${N} gelir vergisi tarifesi henüz yayımlanmadı. Tarifedeki dilim tutarları her yıl yeniden değerleme oranıyla artırılır; ${N} için oran <b>%${fmt(yd.oran)}</b> olarak açıklandı. Aşağıdaki ${N} dilimleri bu oranla hesaplanmış <b>tahmindir</b> (1.000 TL'yi aşmayan kesirler atılmıştır). Resmî tebliğ Aralık sonunda yayımlanınca sayfa aynı gün güncellenir.</p>
<h2>Ücret gelirleri</h2><div class="tablewrap"><table><thead><tr><th>Oran</th><th>${Y}</th><th>${N} (tahmini)</th></tr></thead><tbody>${tab(P.gvDilim, E.tahminiDilim(P.gvDilim))}</tbody></table></div>
<h2>Ücret dışı gelirler (kira, serbest meslek, ticari kazanç)</h2><div class="tablewrap"><table><thead><tr><th>Oran</th><th>${Y}</th><th>${N} (tahmini)</th></tr></thead><tbody>${tab(P.gvDilimUcretDisi, E.tahminiDilim(P.gvDilimUcretDisi))}</tbody></table></div>
<h2>Ne değişir?</h2><p>Dilimler genişlediği için aynı brüt maaşla bir üst dilime daha geç geçilir. Örneğin ${Y}'da %20 dilimi 190.000 TL'de başlarken, ${N}'de tahminen ${fmt(E.tahminiDilim(P.gvDilim)[0][0], 0)} TL'de başlayacak. Kendi bordronuz için <a href="/maas-hesaplama/">maaş hesaplama</a> aracını kullanın; güncel tarife: <a href="/gelir-vergisi-dilimleri-${Y}/">gelir vergisi dilimleri ${Y}</a>.</p>`;
    },
    faq: [
      [`${P.yenidenDegerleme.uygulanacakYil} vergi dilimleri açıklandı mı?`, 'Henüz resmî tebliğ yayımlanmadı. Bu sayfadaki tutarlar yeniden değerleme oranıyla hesaplanmış tahminlerdir; tebliğ Aralık sonunda yayımlanır.'],
      [`${P.yenidenDegerleme.uygulanacakYil} ilk vergi dilimi ne kadar olacak?`, `Tahminen ${fmt(E.tahminiDilim(P.gvDilim)[0][0], 0)} TL (${Y}: 190.000 TL).`],
      ['Yeniden değerleme oranı nedir?', 'Yurt içi üretici fiyat endeksindeki (Yİ-ÜFE) son 12 aylık artıştır. Vergi, harç ve ceza tutarları bir sonraki yıl bu oranla güncellenir.'],
    ],
  },
];

export const LEGAL_PAGES = [
  { path: '/hakkimizda/', h1: 'Hakkımızda', description: `${SITE.name} hakkında.`, body: `<p>${SITE.name}, Türkiye'de sık ihtiyaç duyulan maaş, tazminat, kira, kredi ve vergi hesaplamalarını güncel resmi parametrelerle, ücretsiz ve hızlı bir şekilde sunmak için hazırlanmıştır.</p><p>Parametreler Resmî Gazete, Gelir İdaresi Başkanlığı, SGK ve TÜİK tarafından yayımlanan verilere göre güncellenir. Son güncelleme: ${P.updated}.</p><p>Hesaplamalar bilgilendirme amaçlıdır; hukuki, mali veya tıbbi tavsiye değildir.</p>` },
  { path: '/iletisim/', h1: 'İletişim', description: `${SITE.name} iletişim.`, body: `<p>Hata bildirimi, öneri ve iş birlikleri için: <a href="mailto:${SITE.email}">${SITE.email}</a></p>` },
  { path: '/kullanim-kosullari/', h1: 'Kullanım koşulları', description: 'Kullanım koşulları.', body: `<p>Bu sitedeki hesaplama araçları ve içerikler genel bilgilendirme amacıyla sunulur. Sonuçların doğruluğu için azami özen gösterilse de mevzuat değişiklikleri, kişisel durumlar ve yuvarlama farkları nedeniyle gerçek tutarlar farklı olabilir. Önemli kararlar için uzman görüşü alınız.</p><p>${SITE.name}, sonuçların kullanımından doğabilecek zararlardan sorumlu tutulamaz.</p>` },
  { path: '/gizlilik-politikasi/', h1: 'Gizlilik ve çerez politikası', description: 'Gizlilik ve çerez politikası.', body: `<p>Hesaplama araçlarına girdiğiniz değerler yalnızca tarayıcınızda işlenir; sunucularımıza gönderilmez veya saklanmaz.</p>
<h2>Reklamlar ve çerezler</h2><p>Bu site, Google AdSense dahil üçüncü taraf reklam hizmetleri kullanabilir. Google gibi üçüncü taraf sağlayıcılar, bu siteye ve diğer sitelere yaptığınız ziyaretlere dayalı reklamlar sunmak için çerez kullanır. Google'ın reklam çerezlerini kullanması, Google ve iş ortaklarının size bu siteye ve/veya internetteki diğer sitelere yaptığınız ziyaretlere dayalı reklamlar sunmasına olanak tanır. Kişiselleştirilmiş reklamları <a href="https://adssettings.google.com" rel="nofollow">Google Reklam Ayarları</a> üzerinden devre dışı bırakabilirsiniz.</p>
<h2>Analitik</h2><p>Site trafiğini anonim olarak ölçmek için analitik araçlar kullanılabilir.</p>
<h2>KVKK</h2><p>6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamındaki talepleriniz için <a href="mailto:${SITE.email}">${SITE.email}</a> adresine yazabilirsiniz.</p>` },
];
