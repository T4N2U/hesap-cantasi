// Verified facts ("doğrulanmış bilgiler") published for AI assistants via MCP resources, an MCP tool and the REST API.
// RULE (CLAUDE.md accuracy rule): a fact goes in here only if it comes from an official text or at least two reliable
// independent sources, listed in `kaynaklar`. Open questions stay out (e.g. whether the asgari ücret istisnası applies
// to an ihbar payment made alone in a month: one source only, asked to an accountant on 27 Nov 2026).
// Figures that also live in engine.js PARAMS are read from there, so the facts and the calculators never disagree.
// When PARAMS change, re-check the facts that use them and update `kontrol`.
import { PARAMS as P } from '../static/assets/engine.js';

// half-up rounding on the decimal value (27,83 × 1,5 = 41,745 → %41,75, as on the site); plain toFixed gives 41,74
const pct = (x) => '%' + (Math.round((x + 1e-9) * 100) / 100).toFixed(2).replace('.', ',').replace(/,?0+$/, '');
const SITE = 'https://hesapcantasi.com';

export const FACTS = [
  {
    id: 'ihbar-sureleri', baslik: 'İhbar (bildirim) süreleri',
    ozet: 'İş Kanunu md. 17: çalışma süresine göre 2, 4, 6 veya 8 hafta.',
    metin: [
      'Belirsiz süreli iş sözleşmesinin feshinden önce karşı tarafa bildirim yapılması gerekir (4857 sayılı İş Kanunu md. 17). Süreler:',
      '- 6 aydan az çalışmada: 2 hafta',
      '- 6 ay – 1,5 yıl: 4 hafta',
      '- 1,5 – 3 yıl: 6 hafta',
      '- 3 yıldan fazla: 8 hafta',
      'Bu süreler asgaridir; sözleşmeyle artırılabilir. Bildirim şartına uymayan taraf, bildirim süresine ilişkin ücret tutarında tazminat (ihbar tazminatı) öder.',
    ],
    kaynaklar: [{ ad: 'TÜRMOB: İş Kanunu md. 17 bildirim süreleri', url: 'https://www.turmob.org.tr/arsiv/mbs/pratikBilgiler/24-ihbar_bildirim.pdf' }, { ad: 'Paraşüt: ihbar tazminatı hesaplama', url: 'https://www.parasut.com/blog/ihbar-tazminati-hesaplama' }],
    dogrulama: 'kanun metni + ikinci kaynak', kontrol: '2026-11-27', sayfa: `${SITE}/ihbar-tazminati-hesaplama/`,
  },
  {
    id: 'ihbar-kesintileri', baslik: 'İhbar tazminatından yapılan kesintiler',
    ozet: 'Gelir vergisi ve damga vergisi kesilir; SGK primi ve işsizlik sigortası primi kesilmez.',
    metin: [
      'İhbar tazminatı ücret niteliğindedir (GVK md. 61): gelir vergisi ve damga vergisi kesilir.',
      'Sigorta primi ve işsizlik sigortası primi kesilmez.',
      `Damga vergisi oranı binde ${(P.damga * 1000).toFixed(2).replace('.', ',')}; gelir vergisi oranı ücretlinin yıl içindeki kümülatif matrahına göre %15–%40.`,
      'Not: Aynı ay başka ücret ödenmeden yalnız ihbar tazminatı ödendiğinde asgari ücret istisnasının uygulanıp uygulanmayacağı bu kaynakta doğrulanmış bilgi olarak yer almaz.',
    ],
    kaynaklar: [{ ad: 'Muhasebenews: ihbar tazminatında gelir ve damga vergisi', url: 'https://www.muhasebenews.com/2022-yili-ihbar-tazminati-hesaplamasinda-asgari-ucret-uzerinden-istisna-edilen-gelir-vergisi-ve-damga-vergisi-indirimleri-uygulanir-mi/' }, { ad: 'Av. İlker Cebeci: ihbar tazminatı brüt-net ve kesintiler', url: 'https://ilkercebeci.av.tr/ihbar-tazminati-hesaplama/' }],
    dogrulama: 'iki bağımsız kaynak', kontrol: '2026-11-27', sayfa: `${SITE}/ihbar-tazminati-hesaplama/`,
  },
  {
    id: 'mtv-odeme-zamani', baslik: 'MTV ne zaman ödenir?',
    ozet: 'Motorlu taşıtlar vergisi her yıl Ocak ve Temmuz aylarında iki eşit taksitte ödenir (197 s. Kanun md. 9).',
    metin: ['197 sayılı Motorlu Taşıtlar Vergisi Kanunu md. 9: "Motorlu taşıtlar vergisi her yıl Ocak ve Temmuz aylarında iki eşit taksitte ödenir."'],
    kaynaklar: [{ ad: '197 sayılı MTV Kanunu (güncel metin)', url: 'https://www.alomaliye.com/wp-content/uploads/2000/01/197-sk-19-12-2025.pdf' }],
    dogrulama: 'kanun metni', kontrol: '2026-11-25', sayfa: `${SITE}/mtv-hesaplama/`,
  },
  {
    id: 'mtv-artis-yetkisi', baslik: `MTV artış oranı nasıl belirlenir? (${P.yenidenDegerleme.uygulanacakYil})`,
    ozet: `MTV tutarları yeniden değerleme oranında artar; Cumhurbaşkanı bu oranın %20'si ile %150'si arasında başka bir oran belirleyebilir. ${P.yenidenDegerleme.uygulanacakYil} için aralık ${pct(P.yenidenDegerleme.oran * P.mtvYetki.alt)} – ${pct(P.yenidenDegerleme.oran * P.mtvYetki.ust)}.`,
    metin: [
      '197 sayılı Kanun md. 10: taşıt değerleri ve vergi miktarları her yıl, o yıl için ilan edilen yeniden değerleme oranında artırılır.',
      "Cumhurbaşkanı, yeniden değerleme oranının %50 fazlasını geçmemek, %20'sinden az olmamak üzere yeni oranlar tespit etmeye yetkilidir.",
      `${P.yenidenDegerleme.uygulanacakYil} için yeniden değerleme oranı ${pct(P.yenidenDegerleme.oran)}; dolayısıyla MTV artışı ${pct(P.yenidenDegerleme.oran * P.mtvYetki.alt)} ile ${pct(P.yenidenDegerleme.oran * P.mtvYetki.ust)} arasında olabilir. Yeniden değerleme oranı bir üst sınır değildir.`,
      'Örnek uygulama: 2025 için yeniden değerleme oranı %43,93 iken aralık %8,78 – %65,89 idi.',
    ],
    kaynaklar: [{ ad: '197 sayılı MTV Kanunu (güncel metin), md. 10', url: 'https://www.alomaliye.com/wp-content/uploads/2000/01/197-sk-19-12-2025.pdf' }, { ad: 'Ekonomi Gazetesi: MTV artış oranında alt ve üst sınır', url: 'https://www.ekonomigazetesi.com/ekonomi/mtv-artis-oraninda-alt-sinir-yuzde-8-78-ust-sinir-yuzde-65-89-37286' }],
    dogrulama: 'kanun metni + ikinci kaynak', kontrol: '2026-11-25', sayfa: `${SITE}/mtv-hesaplama/`,
  },
  {
    id: 'mtv-2026-artis', baslik: `${P.mtvYil} MTV artış oranı`,
    ozet: `${P.mtvYil} yılında MTV tutarları ${pct(P.mtvArtis)} artırıldı (Cumhurbaşkanı kararı; yeniden değerleme oranı %25,49 idi).`,
    metin: [`Cumhurbaşkanı kararıyla (197 s. Kanun md. 10 dayanağı) ${P.mtvYil} yılında MTV tutarlarına uygulanacak yeniden değerleme oranı ${pct(P.mtvArtis)} olarak belirlendi.`],
    kaynaklar: [{ ad: 'Alomaliye: 2026 MTV yeniden değerleme oranı kararı', url: 'https://www.alomaliye.com/2025/12/31/2026-yili-mtv-damga-vergisi-maktu-damga-vergisi-ve-harc-tutarlarinin-yeniden-degerleme-oranlari/' }, { ad: 'Bloomberg HT: MTV %18,95 artırıldı', url: 'https://www.bloomberght.com/motorlu-tasitlar-vergisi-yuzde-18-95-artirildi-3765092' }],
    dogrulama: 'iki bağımsız kaynak', kontrol: '2026-11-25', sayfa: `${SITE}/mtv-hesaplama/`,
  },
  {
    id: 'yeniden-degerleme-2027', baslik: `${P.yenidenDegerleme.uygulanacakYil} yeniden değerleme oranı`,
    ozet: `${P.yenidenDegerleme.uygulanacakYil} yılında uygulanacak yeniden değerleme oranı ${pct(P.yenidenDegerleme.oran)} (VUK mükerrer md. 298).`,
    metin: [`Maktu vergi, harç ve ceza tutarlarının ${P.yenidenDegerleme.uygulanacakYil} güncellemesinde esas alınan yeniden değerleme oranı ${pct(P.yenidenDegerleme.oran)}. Bazı tutarlarda (ör. MTV) Cumhurbaşkanı farklı oran belirleyebilir.`],
    kaynaklar: [{ ad: 'Ekonomi Gazetesi: yeniden değerleme oranı 2027 için %27,83', url: 'https://www.ekonomigazetesi.com/ekonomi/yeniden-degerleme-orani-2027-icin-2783-91275' }, { ad: 'Milliyet Uzmanpara: 2027 MTV zam oranı ve yeniden değerleme', url: 'https://uzmanpara.milliyet.com.tr/uzmanpara/2027-mtv-zam-orani-ne-kadar-olacak-yeniden-degerleme-orani-sonrasinda-mtvye-yapilacak-artis-belli-oldu-7693231' }],
    dogrulama: 'iki bağımsız kaynak', kontrol: '2026-11-25', sayfa: `${SITE}/mtv-hesaplama/`,
  },
];

export const FACT_MAP = Object.fromEntries(FACTS.map((f) => [f.id, f]));
export const factUri = (id) => `hesapcantasi://bilgi/${id}`;
export function factMarkdown(f) {
  return `# ${f.baslik}\n\n${f.ozet}\n\n${f.metin.join('\n\n')}\n\n**Doğrulama:** ${f.dogrulama} · **Son kontrol:** ${f.kontrol}\n\n**Kaynaklar:**\n${f.kaynaklar.map((k) => `- [${k.ad}](${k.url})`).join('\n')}\n\nHesaplama: ${f.sayfa}\n`;
}
