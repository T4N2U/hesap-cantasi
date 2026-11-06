import assert from 'node:assert/strict';
import * as E from '../static/assets/engine.js';

const near = (a, b, tol = 0.02, msg = '') => assert.ok(Math.abs(a - b) <= tol, `${msg} expected ${b}, got ${a}`);

// Asgari ücret: net 28.075,50, no GV/damga, istisna amounts per official tables
const a = E.brutNet(E.PARAMS.asgariBrut);
a.aylar.forEach((m) => { near(m.net, 28075.5, 0.01, m.ay); assert.equal(m.gv, 0); assert.equal(m.damga, 0); });
near(a.aylar[0].gvIstisna, 4211.33, 0.01, 'istisna Ocak');
near(a.aylar[6].gvIstisna, 4537.75, 0.01, 'istisna Temmuz');
near(a.aylar[7].gvIstisna, 5615.10, 0.01, 'istisna Ağustos');
near(a.toplam.gv, 0);
// Annual istisna total 57.881,23 (published)
near(a.aylar.reduce((s, m) => s + m.gvIstisna, 0), 57881.23, 0.05, 'yıllık istisna');
// Employer cost with 5-pt incentive: 39.223,13 (published)
near(a.aylar[0].maliyet, 39223.13, 0.01, 'maliyet teşvikli');
near(E.brutNet(E.PARAMS.asgariBrut, { tesvik: false }).aylar[0].maliyet, 40874.63, 0.01, 'maliyet teşviksiz');

// 50.000 brüt, Ocak
const b = E.brutNet(50000).aylar[0];
near(b.gv, 2163.67, 0.02, 'gv 50k'); near(b.damga, 128.80, 0.01, 'damga 50k'); near(b.net, 40207.52, 0.03, 'net 50k');

// SGK tavan
const c = E.brutNet(400000).aylar[0];
near(c.sgk, 297270 * 0.14, 0.01, 'sgk tavan');

// Netten brüte inverts
const n = E.netBrut(60000);
n.aylar.forEach((m) => near(m.net, 60000, 0.02, 'netBrut ' + m.ay));
assert.ok(n.aylar[11].brut > n.aylar[0].brut, 'later months need higher brüt');

// Gelir vergisi bracket totals
near(E.gelirVergisi(400000), 70500); near(E.gelirVergisi(1500000), 367500); near(E.gelirVergisi(5300000), 1697500);

// Kıdem
const k = E.kidem({ baslangic: '2020-03-15', bitis: '2026-09-15', brut: 100000 });
assert.equal(k.sure.yil, 6); assert.equal(k.sure.ay, 6); assert.ok(k.tavanUygulandi);
near(k.brut, 73729.84 * 6.5, 0.05, 'kıdem tavan');
near(k.net, k.brut * (1 - 0.00759), 0.02);
assert.ok(E.kidem({ baslangic: '2026-01-01', bitis: '2026-06-01', brut: 50000 }).hata);
const k2 = E.kidem({ baslangic: '2023-01-01', bitis: '2026-03-01', brut: 50000 });
near(k2.brut, 50000 * 3 + 50000 / 12 * 2, 0.02, 'kıdem tavan altı');

// İhbar weeks
assert.equal(E.ihbar({ baslangic: '2026-01-01', bitis: '2026-04-01', brut: 30000 }).hafta, 2);
assert.equal(E.ihbar({ baslangic: '2025-01-01', bitis: '2026-04-01', brut: 30000 }).hafta, 4);
assert.equal(E.ihbar({ baslangic: '2024-01-01', bitis: '2026-04-01', brut: 30000 }).hafta, 6);
assert.equal(E.ihbar({ baslangic: '2020-01-01', bitis: '2026-04-01', brut: 30000 }).hafta, 8);
near(E.ihbar({ baslangic: '2020-01-01', bitis: '2026-04-01', brut: 30000 }).brut, 56000);

// Kira
near(E.kiraArtis(20000, 31.23).yeni, 26246);

// Kredi: zero-tax konut annuity check and taxes add 30% to rate for ihtiyaç
const kr = E.kredi({ tutar: 100000, vade: 12, aylikFaiz: 3, tur: 'konut' });
near(kr.taksit, 100000 * 0.03 / (1 - 1.03 ** -12), 0.01);
near(kr.plan.at(-1).kalan, 0);
near(kr.toplam, kr.taksit * 12, 0.05);
const ki = E.kredi({ tutar: 100000, vade: 12, aylikFaiz: 3, tur: 'ihtiyac' });
near(ki.taksit, 100000 * 0.039 / (1 - 1.039 ** -12), 0.01);
near(ki.kkdf, ki.faiz * 0.15, 0.05); near(ki.bsmv, ki.faiz * 0.15, 0.05);

// Mevduat — published example: 100.000 TL, %40, 32 gün → net 2.893,15
const md = E.mevduat({ tutar: 100000, yillikFaiz: 40, gun: 32 });
near(md.brut, 3506.85); near(md.net, 2893.15);
assert.equal(E.stopajOrani(181), 0.175); assert.equal(E.stopajOrani(365), 0.15); assert.equal(E.stopajOrani(400), 0.10);

// KDV, yüzde
assert.deepEqual(E.kdv({ tutar: 1200, oran: 20, dahil: true }), { haric: 1000, kdv: 200, dahil: 1200 });
assert.equal(E.yuzde('yuzdesi', 250, 20), 50); assert.equal(E.yuzde('kacyuzde', 50, 200), 25); assert.equal(E.yuzde('degisim', 80, 100), 25);

// İzin, VKİ, tarih
assert.equal(E.yillikIzin({ kidemYil: 3, yas: 30 }).gun, 14);
assert.equal(E.yillikIzin({ kidemYil: 3, yas: 52 }).gun, 20);
assert.equal(E.yillikIzin({ kidemYil: 16, yas: 40 }).gun, 26);
assert.equal(E.vki({ kilo: 70, boy: 175 }).vki, 22.9);
assert.equal(E.tarihFarki('2026-01-01', '2026-12-31').toplamGun, 364);

// İşsizlik — published 2026: en düşük 13.111 TL, en yüksek 26.222 TL (net, rounded)
const is1 = E.issizlik({ ortalamaBrut: E.PARAMS.asgariBrut, primGun: 600 });
assert.equal(Math.floor(is1.net), 13111); assert.equal(is1.sureGun, 180);
assert.ok(Math.abs(is1.enCok - 26222) < 2, 'işsizlik tavan ' + is1.enCok);
const is2 = E.issizlik({ ortalamaBrut: 60000, primGun: 1100 });
near(is2.brut, 24000); assert.equal(is2.sureGun, 300);
// Published example: 60.000 TL ortalama → 23.818 TL
assert.equal(Math.round(is2.net), 23818);
assert.equal(E.issizlik({ ortalamaBrut: 40000, primGun: 500 }).sureGun, 0);
assert.ok(E.issizlik({ ortalamaBrut: 200000, primGun: 900 }).tavanUygulandi);

// Fazla mesai — published: asgari ücret 146,80 TL/saat, mesai 220,20 TL
const fm = E.fazlaMesai({ brut: 33030, saat: 10 });
near(fm.saatlik, 146.80); near(fm.saatlikMesai, 220.20); near(fm.toplam, 2202);
near(E.fazlaMesai({ brut: 33030, saat: 1, tip: 'sure' }).saatlikMesai, 183.50);

// Tapu, zam
assert.deepEqual(E.tapuHarci({ bedel: 3000000 }), { alici: 60000, satici: 60000, toplam: 120000 });
assert.equal(E.zam({ eski: 40000, yeni: 50000 }).oran, 25);
assert.equal(E.zam({ eski: 40000, oran: 30 }).yeni, 52000);

console.log('All engine tests passed');
