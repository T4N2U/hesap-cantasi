import { mkdirSync, writeFileSync, cpSync, rmSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { SITE } from './site.mjs';
import * as E from '../static/assets/engine.js';
import { CALCULATORS, INFO_PAGES, LEGAL_PAGES } from './content.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const OUT = join(ROOT, 'dist');
const P = E.PARAMS;
const fmt = E.fmt, tl = E.tl;
const VERSION = Date.now().toString(36);

rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT, { recursive: true });
cpSync(join(ROOT, 'static'), OUT, { recursive: true });

const pages = []; // for sitemap
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const trDate = (iso) => { const [y, m, d] = iso.split('-').map(Number); return `${d} ${E.AYLAR[m - 1]} ${y}`; };

function adSlot(name) {
  if (!SITE.adsenseClient) return '';
  return `<div class="ad"><ins class="adsbygoogle" style="display:block;width:100%" data-ad-client="${SITE.adsenseClient}" data-ad-format="auto" data-full-width-responsive="true" data-slot-name="${name}"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>`;
}

function layout({ path, title, description, body, schema = [], crumbs = [] }) {
  const url = SITE.url + path;
  const bc = crumbs.length ? {
    '@context': 'https://schema.org', '@type': 'BreadcrumbList',
    itemListElement: [{ name: 'Ana sayfa', path: '/' }, ...crumbs].map((c, i) => ({ '@type': 'ListItem', position: i + 1, name: c.name, item: SITE.url + c.path })),
  } : null;
  const ld = [...schema, bc].filter(Boolean).map((s) => `<script type="application/ld+json">${JSON.stringify(s)}</script>`).join('');
  const crumbHtml = crumbs.length ? `<div class="crumbs"><a href="/">Ana sayfa</a> › ${crumbs.map((c, i) => i === crumbs.length - 1 ? esc(c.name) : `<a href="${c.path}">${esc(c.name)}</a>`).join(' › ')}</div>` : '';
  const html = `<!doctype html>
<html lang="tr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(description)}">
<link rel="canonical" href="${url}">
<meta property="og:type" content="website"><meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(description)}"><meta property="og:url" content="${url}"><meta property="og:site_name" content="${SITE.name}"><meta property="og:locale" content="tr_TR">
<meta name="theme-color" content="#0f6b4f">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/style.css?v=${VERSION}">
${SITE.adsenseClient ? `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${SITE.adsenseClient}" crossorigin="anonymous"></script>` : ''}
${SITE.ga4 ? `<script async src="https://www.googletagmanager.com/gtag/js?id=${SITE.ga4}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','${SITE.ga4}');</script>` : ''}
${ld}
</head><body>
<header class="top"><div class="wrap"><a class="logo" href="/"><i>₺</i>${SITE.name}</a>
<nav class="main"><a href="/maas-hesaplama/">Maaş</a><a href="/kidem-tazminati-hesaplama/">Kıdem</a><a href="/kira-artis-hesaplama/">Kira</a><a href="/kredi-hesaplama/">Kredi</a><a href="/tum-hesaplamalar/">Tümü</a></nav></div></header>
<main class="wrap">${crumbHtml}${body}</main>
<footer><div class="wrap"><div class="fl"><a href="/hakkimizda/">Hakkımızda</a><a href="/iletisim/">İletişim</a><a href="/gizlilik-politikasi/">Gizlilik ve çerezler</a><a href="/kullanim-kosullari/">Kullanım koşulları</a><a href="/tum-hesaplamalar/">Tüm hesaplamalar</a></div>
<div>Hesaplamalar bilgilendirme amaçlıdır; resmi bordro, sözleşme veya banka teklifinin yerine geçmez. Parametreler son olarak ${trDate(P.updated)} tarihinde güncellendi.</div>
<div>© ${new Date().getFullYear()} ${SITE.name}</div></div></footer>
<script type="module" src="/assets/app.js?v=${VERSION}"></script>
${SITE.cfBeacon ? `<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token":"${SITE.cfBeacon}"}'></script>` : ''}
</body></html>`;
  const file = join(OUT, path, 'index.html');
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, html);
  pages.push(path);
}

const faqSchema = (faq) => faq?.length ? { '@context': 'https://schema.org', '@type': 'FAQPage', mainEntity: faq.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a.replace(/<[^>]+>/g, '') } })) } : null;
const faqHtml = (faq) => faq?.length ? `<section class="faq prose"><h2>Sık sorulan sorular</h2>${faq.map(([q, a]) => `<details><summary>${q}</summary><p>${a}</p></details>`).join('')}</section>` : '';
const appSchema = (c) => ({ '@context': 'https://schema.org', '@type': 'WebApplication', name: c.h1, url: SITE.url + c.path, applicationCategory: 'FinanceApplication', operatingSystem: 'Any', inLanguage: 'tr', offers: { '@type': 'Offer', price: '0', priceCurrency: 'TRY' } });

function sidebar(currentPath, extra = '') {
  const list = CALCULATORS.filter((c) => c.path !== currentPath).slice(0, 9).map((c) => `<li><a href="${c.path}">${c.short}</a></li>`).join('');
  return `<aside class="side">${extra}<div class="card"><h4>Diğer hesaplamalar</h4><ul>${list}</ul></div>${adSlot('sidebar')}</aside>`;
}

// ---------- Calculator pages ----------
for (const c of CALCULATORS) {
  const body = `<span class="stamp">Güncellendi: ${trDate(P.updated)}</span>
<h1>${c.h1}</h1><p class="lead">${c.lead}</p>
<div class="grid"><div>
<div class="card">${c.form}<div class="result" aria-live="polite"></div></div>
${adSlot('below-calc')}
<section class="prose">${c.content}</section>
${c.extra ? c.extra() : ''}
${faqHtml(c.faq)}
</div>${sidebar(c.path)}</div>`;
  layout({ path: c.path, title: c.title, description: c.description, body, schema: [appSchema(c), faqSchema(c.faq)], crumbs: [{ name: c.short, path: c.path }] });
}

// ---------- Info pages ----------
for (const p of INFO_PAGES) {
  layout({ path: p.path, title: p.title, description: p.description, body: `<span class="stamp">Güncellendi: ${trDate(P.updated)}</span><h1>${p.h1}</h1><div class="grid"><div class="prose">${p.body()}${faqHtml(p.faq)}</div>${sidebar(p.path)}</div>`, schema: [faqSchema(p.faq)], crumbs: [{ name: p.short, path: p.path }] });
}
for (const p of LEGAL_PAGES) {
  layout({ path: p.path, title: `${p.h1} | ${SITE.name}`, description: p.description, body: `<h1>${p.h1}</h1><div class="prose">${p.body}</div>`, crumbs: [{ name: p.h1, path: p.path }] });
}

// ---------- Programmatic: brütten nete ----------
const brutAmounts = [];
for (let v = 35000; v <= 150000; v += 2500) brutAmounts.push(v);
for (let v = 160000; v <= 300000; v += 10000) brutAmounts.push(v);
for (let v = 350000; v <= 500000; v += 50000) brutAmounts.push(v);
const netAmounts = [];
for (let v = 30000; v <= 120000; v += 2500) netAmounts.push(v);
for (let v = 130000; v <= 250000; v += 10000) netAmounts.push(v);

const bordroTable = (r) => `<div class="tablewrap"><table><thead><tr><th>Ay</th><th>Brüt</th><th>SGK+İşsizlik</th><th>Gelir V.</th><th>Damga V.</th><th>Net</th></tr></thead><tbody>${r.aylar.map((a) => `<tr><td>${a.ay}</td><td>${fmt(a.brut)}</td><td>${fmt(a.sgk + a.issizlik)}</td><td>${fmt(a.gv)}</td><td>${fmt(a.damga)}</td><td><b>${fmt(a.net)}</b></td></tr>`).join('')}<tr><td><b>Toplam</b></td><td>${fmt(r.toplam.brut)}</td><td>${fmt(r.toplam.sgk + r.toplam.issizlik)}</td><td>${fmt(r.toplam.gv)}</td><td>${fmt(r.toplam.damga)}</td><td><b>${fmt(r.toplam.net)}</b></td></tr></tbody></table></div>`;
const kStr = (v) => fmt(v, 0);
const nearby = (arr, v, mk) => { const i = arr.indexOf(v); return arr.slice(Math.max(0, i - 4), i + 5).filter((x) => x !== v).map((x) => `<li><a href="${mk(x)}">${kStr(x)} TL</a></li>`).join(''); };
const brutPath = (v) => `/maas/${v}-tl-brut-kac-tl-net/`;
const netPath = (v) => `/maas/${v}-tl-net-kac-tl-brut/`;

for (const v of brutAmounts) {
  const r = E.brutNet(v);
  const o = r.aylar[0], last = r.aylar[11];
  const dilimAy = r.aylar.find((a) => a.dilim > 0.15);
  const h1 = `${kStr(v)} TL brüt maaş kaç TL net? (${P.year})`;
  const faq = [
    [`${kStr(v)} TL brüt maaş Ocak ayında net kaç TL?`, `${P.year} parametreleriyle ${kStr(v)} TL brüt maaşın Ocak ayı neti ${tl(o.net)} olur.`],
    [`Yıl boyunca net maaş neden değişiyor?`, `Gelir vergisi kümülatif matraha göre hesaplanır. Matrah yükseldikçe vergi dilimi artar ve net maaş düşer. Bu maaşta Aralık ayı neti ${tl(last.net)}, yıllık ortalama net ${tl(r.ortalamaNet)} olur.`],
    [`İşverene maliyeti ne kadar?`, `5 puanlık SGK teşvikiyle aylık işveren maliyeti yaklaşık ${tl(o.maliyet)} olur.`],
  ];
  const body = `<span class="stamp">${P.year} parametreleri · Güncellendi: ${trDate(P.updated)}</span>
<h1>${h1}</h1>
<p class="lead">${kStr(v)} TL brüt maaş, ${P.year} yılı Ocak ayında <b>${tl(o.net)}</b> net olarak ele geçer. Yıllık ortalama net ${tl(r.ortalamaNet)}${dilimAy ? `; ${dilimAy.ay} ayında vergi dilimi %${Math.round(dilimAy.dilim * 100)}${({20:"'ye",27:"'ye",35:"'e",40:"'a"})[Math.round(dilimAy.dilim * 100)]} çıkar` : ''}.</p>
<div class="grid"><div>
<div class="card"><div class="summary">
<div class="kv strong"><span>Ocak net maaş</span><b>${tl(o.net)}</b></div>
<div class="kv"><span>Aralık net maaş</span><b>${tl(last.net)}</b></div>
<div class="kv"><span>Yıllık toplam net</span><b>${tl(r.toplam.net)}</b></div>
<div class="kv"><span>SGK + işsizlik kesintisi (aylık)</span><b>${tl(o.sgk + o.issizlik)}</b></div>
<div class="kv"><span>İşverene maliyet (teşvikli)</span><b>${tl(o.maliyet)}</b></div></div>
<p class="note">Farklı bir tutar mı? <a href="/maas-hesaplama/?mod=brut&tutar=${v}">Maaş hesaplama aracında düzenleyin →</a></p></div>
${adSlot('prog-top')}
<h2>${kStr(v)} TL brüt maaşın 12 aylık bordrosu</h2>
${bordroTable(r)}
<section class="prose"><h2>Nasıl hesaplandı?</h2><p>Brüt maaştan %14 SGK işçi payı ve %1 işsizlik sigortası düşülerek gelir vergisi matrahı bulunur. Gelir vergisi ${P.year} ücret tarifesine göre kümülatif matrah üzerinden hesaplanır; asgari ücrete isabet eden gelir vergisi ve damga vergisi istisna edilir. Damga vergisi brüt ücretin binde 7,59'udur. Ayrıntılar için <a href="/gelir-vergisi-dilimleri-2026/">gelir vergisi dilimleri</a> sayfasına bakın.</p></section>
${faqHtml(faq)}
<h2>Yakın tutarlar</h2><ul class="links">${nearby(brutAmounts, v, brutPath)}</ul>
</div>${sidebar('', '')}</div>`;
  layout({ path: brutPath(v), title: `${kStr(v)} TL Brüt Maaş Kaç TL Net? ${P.year} Hesaplama`, description: `${kStr(v)} TL brüt maaşın ${P.year} net karşılığı Ocak ayında ${tl(o.net)}. 12 aylık bordro, vergi dilimi ve işveren maliyeti.`, body, schema: [faqSchema(faq)], crumbs: [{ name: 'Maaş hesaplama', path: '/maas-hesaplama/' }, { name: `${kStr(v)} TL brüt`, path: brutPath(v) }] });
}

for (const v of netAmounts) {
  const r = E.netBrut(v);
  const o = r.aylar[0], last = r.aylar[11];
  const h1 = `${kStr(v)} TL net maaş kaç TL brüt? (${P.year})`;
  const faq = [
    [`${kStr(v)} TL net maaş için brüt ne olmalı?`, `${P.year} Ocak ayında ${kStr(v)} TL net için brüt maaşın ${tl(o.brut)} olması gerekir.`],
    [`Net sabitse brüt neden artıyor?`, `Kümülatif vergi matrahı yükseldikçe vergi dilimi artar. Aynı neti korumak için Aralık ayında brüt ${tl(last.brut)} olmalıdır.`],
  ];
  const body = `<span class="stamp">${P.year} parametreleri · Güncellendi: ${trDate(P.updated)}</span>
<h1>${h1}</h1>
<p class="lead">${kStr(v)} TL net maaş için ${P.year} Ocak ayında <b>${tl(o.brut)}</b> brüt ücret gerekir. Yıl boyunca aynı neti almak için toplam brüt ${tl(r.toplam.brut)} olur.</p>
<div class="grid"><div>
<div class="card"><div class="summary">
<div class="kv strong"><span>Ocak brüt maaş</span><b>${tl(o.brut)}</b></div>
<div class="kv"><span>Aralık brüt maaş</span><b>${tl(last.brut)}</b></div>
<div class="kv"><span>Yıllık toplam brüt</span><b>${tl(r.toplam.brut)}</b></div>
<div class="kv"><span>Aylık işveren maliyeti (Ocak)</span><b>${tl(o.maliyet)}</b></div></div>
<p class="note"><a href="/maas-hesaplama/?mod=net&tutar=${v}">Maaş hesaplama aracında düzenleyin →</a></p></div>
${adSlot('prog-top')}
<h2>${kStr(v)} TL net için 12 aylık brüt tablo</h2>
${bordroTable(r)}
${faqHtml(faq)}
<h2>Yakın tutarlar</h2><ul class="links">${nearby(netAmounts, v, netPath)}</ul>
</div>${sidebar('', '')}</div>`;
  layout({ path: netPath(v), title: `${kStr(v)} TL Net Maaş Kaç TL Brüt? ${P.year} Hesaplama`, description: `${kStr(v)} TL net maaş için ${P.year} Ocak brüt karşılığı ${tl(o.brut)}. 12 aylık netten brüte tablo ve işveren maliyeti.`, body, schema: [faqSchema(faq)], crumbs: [{ name: 'Maaş hesaplama', path: '/maas-hesaplama/' }, { name: `${kStr(v)} TL net`, path: netPath(v) }] });
}

// ---------- Programmatic: kira artışı ----------
const kiraAmounts = [];
for (let v = 5000; v <= 50000; v += 1000) kiraAmounts.push(v);
for (let v = 55000; v <= 100000; v += 5000) kiraAmounts.push(v);
const kiraPath = (v) => `/kira-artisi/${v}-tl-kira-ne-kadar-olur/`;
const kNow = P.kiraOranlari[0];
for (const v of kiraAmounts) {
  const r = E.kiraArtis(v, kNow.oran);
  const rows = P.kiraOranlari.map((k) => { const x = E.kiraArtis(v, k.oran); return `<tr><td>${k.ay}</td><td>%${fmt(k.oran)}</td><td>${fmt(x.artis)}</td><td><b>${fmt(x.yeni)}</b></td></tr>`; }).join('');
  const faq = [
    [`${kStr(v)} TL kira ${kNow.ay} ayında en fazla ne kadar olur?`, `${kNow.ay} için yasal üst sınır %${fmt(kNow.oran)} olduğundan ${kStr(v)} TL kira en fazla ${tl(r.yeni)} olabilir.`],
    [`Ev sahibi bu orandan fazla zam yapabilir mi?`, `Konut ve çatılı işyeri kiralarında, yenilenen kira dönemi için yapılacak artış TÜFE'nin 12 aylık ortalamasını geçemez (TBK m.344). Taraflar daha düşük bir oranda anlaşabilir. 5 yılı dolduran sözleşmelerde hâkim kira tespitinde farklı kriterler uygulanabilir.`],
  ];
  const body = `<span class="stamp">${kNow.ay} oranı · Güncellendi: ${trDate(P.updated)}</span>
<h1>${kStr(v)} TL kira ne kadar olur? (${kNow.ay})</h1>
<p class="lead">${kNow.ay} ayında yenilenen sözleşmelerde ${kStr(v)} TL kira, yasal üst sınır olan %${fmt(kNow.oran)} ile en fazla <b>${tl(r.yeni)}</b> olabilir. Aylık artış ${tl(r.artis)}.</p>
<div class="grid"><div>
<div class="card"><div class="summary"><div class="kv strong"><span>Yeni kira (en fazla)</span><b>${tl(r.yeni)}</b></div><div class="kv"><span>Aylık artış</span><b>${tl(r.artis)}</b></div><div class="kv"><span>Yıllık ek ödeme</span><b>${tl(r.yillikFark)}</b></div></div>
<p class="note"><a href="/kira-artis-hesaplama/?kira=${v}">Farklı tutar veya oranla hesaplayın →</a></p></div>
${adSlot('prog-top')}
<h2>Aylara göre ${kStr(v)} TL kira artışı</h2>
<div class="tablewrap"><table><thead><tr><th>Uygulama ayı</th><th>Oran</th><th>Artış</th><th>Yeni kira</th></tr></thead><tbody>${rows}</tbody></table></div>
${faqHtml(faq)}
<h2>Yakın tutarlar</h2><ul class="links">${nearby(kiraAmounts, v, kiraPath)}</ul>
</div>${sidebar('', '')}</div>`;
  layout({ path: kiraPath(v), title: `${kStr(v)} TL Kira Ne Kadar Olur? ${kNow.ay} Kira Artışı`, description: `${kNow.ay} kira artış oranı %${fmt(kNow.oran)} ile ${kStr(v)} TL kira en fazla ${tl(r.yeni)} olur. Önceki aylarla karşılaştırma tablosu.`, body, schema: [faqSchema(faq)], crumbs: [{ name: 'Kira artış hesaplama', path: '/kira-artis-hesaplama/' }, { name: `${kStr(v)} TL kira`, path: kiraPath(v) }] });
}

// ---------- Hubs ----------
const hubLinks = (title, arr, mk, suffix) => `<h2>${title}</h2><ul class="links">${arr.map((x) => `<li><a href="${mk(x)}">${kStr(x)} TL ${suffix}</a></li>`).join('')}</ul>`;
layout({
  path: '/tum-hesaplamalar/', title: `Tüm Hesaplama Araçları | ${SITE.name}`, description: 'Maaş, tazminat, kira, kredi, mevduat, KDV ve günlük hesaplamaların tam listesi.',
  body: `<h1>Tüm hesaplamalar</h1><div class="tiles">${CALCULATORS.map((c) => `<a class="tile" href="${c.path}"><b>${c.short}</b><span>${c.tile}</span></a>`).join('')}${INFO_PAGES.map((c) => `<a class="tile" href="${c.path}"><b>${c.short}</b><span>${c.tile}</span></a>`).join('')}</div>
${hubLinks('Brütten nete maaş tabloları', brutAmounts, brutPath, 'brüt')}${hubLinks('Netten brüte maaş tabloları', netAmounts, netPath, 'net')}${hubLinks('Kira artışı tabloları', kiraAmounts, kiraPath, 'kira')}`,
  crumbs: [{ name: 'Tüm hesaplamalar', path: '/tum-hesaplamalar/' }],
});

// ---------- Home ----------
const asg = E.brutNet(P.asgariBrut).aylar[0];
layout({
  path: '/', title: `${SITE.name} – Güncel Maaş, Tazminat, Kira ve Kredi Hesaplama ${P.year}`, description: SITE.description,
  schema: [{ '@context': 'https://schema.org', '@type': 'WebSite', name: SITE.name, url: SITE.url, inLanguage: 'tr' }],
  body: `<h1 style="margin-top:28px">Güncel hesaplamalar, tek yerde</h1>
<p class="lead">${P.year} vergi dilimleri, asgari ücret, kıdem tavanı ve kira artış oranlarıyla güncel, ücretsiz ve hızlı hesaplama araçları. Girdiğiniz bilgiler tarayıcınızdan çıkmaz.</p>
<div class="card"><div class="summary">
<div class="kv"><span>Net asgari ücret ${P.year}</span><b>${tl(asg.net)}</b></div>
<div class="kv"><span>Kira artış oranı (${kNow.ay})</span><b>%${fmt(kNow.oran)}</b></div>
<div class="kv"><span>Kıdem tazminatı tavanı</span><b>${tl(P.kidemTavan.at(-1).tutar)}</b></div>
<div class="kv"><span>Mevduat stopajı (6 aya kadar)</span><b>%17,5</b></div></div></div>
<div class="tiles">${CALCULATORS.map((c) => `<a class="tile" href="${c.path}"><b>${c.short}</b><span>${c.tile}</span></a>`).join('')}</div>
${adSlot('home')}
<h2>Popüler maaş sorguları</h2><ul class="links">${[40000, 50000, 60000, 75000, 100000, 150000].map((v) => `<li><a href="${brutPath(v)}">${kStr(v)} TL brüt kaç net?</a></li>`).join('')}${[35000, 40000, 50000, 60000, 80000, 100000].map((v) => `<li><a href="${netPath(v)}">${kStr(v)} TL net kaç brüt?</a></li>`).join('')}</ul>
<h2>Popüler kira sorguları</h2><ul class="links">${[10000, 15000, 20000, 25000, 30000, 40000].map((v) => `<li><a href="${kiraPath(v)}">${kStr(v)} TL kira ne kadar olur?</a></li>`).join('')}</ul>`,
});

// ---------- 404, sitemap, robots, headers ----------
layout({ path: '/404-sayfa/', title: 'Sayfa bulunamadı', description: 'Aradığınız sayfa bulunamadı.', body: `<h1>Sayfa bulunamadı</h1><p class="lead">Aradığınız sayfa taşınmış olabilir.</p><div class="tiles">${CALCULATORS.slice(0, 6).map((c) => `<a class="tile" href="${c.path}"><b>${c.short}</b><span>${c.tile}</span></a>`).join('')}</div>` });
cpSync(join(OUT, '404-sayfa', 'index.html'), join(OUT, '404.html'));
rmSync(join(OUT, '404-sayfa'), { recursive: true });
pages.splice(pages.indexOf('/404-sayfa/'), 1);

const today = new Date().toISOString().slice(0, 10);
writeFileSync(join(OUT, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${pages.map((p) => `<url><loc>${SITE.url}${p}</loc><lastmod>${today}</lastmod></url>`).join('\n')}\n</urlset>\n`);
writeFileSync(join(OUT, 'robots.txt'), `User-agent: *\nAllow: /\n\nSitemap: ${SITE.url}/sitemap.xml\n`);
if (SITE.adsenseClient) writeFileSync(join(OUT, 'ads.txt'), `google.com, ${SITE.adsenseClient.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n`);
writeFileSync(join(OUT, '_headers'), `/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n`);

console.log(`Built ${pages.length} pages → dist/`);
