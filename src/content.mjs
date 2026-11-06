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
<p><a href="/maas-hesaplama/">Kendi maaşınızı hesaplayın →</a></p>`;
    },
    faq: [[`${Y} net asgari ücret ne kadar?`, `${tl(P.asgariNet)}.`], [`${Y} brüt asgari ücret ne kadar?`, `${tl(P.asgariBrut)}.`], ['Asgari ücretten vergi kesilir mi?', 'Hayır. Gelir vergisi ve damga vergisi istisnası nedeniyle yalnızca SGK ve işsizlik sigortası primi kesilir.']],
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
