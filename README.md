# Hesap Çantası – Turkish calculator network

A static website: 13 calculators, 2 reference pages and 175 programmatic SEO pages (192 pages in total). It has no server, no database and no running cost beyond the domain. All calculations run in the visitor's browser.

## What's inside

| Path | What |
|---|---|
| `dist/` | **The finished website.** This folder is what you upload. |
| `static/assets/engine.js` | All formulas and **all official rates** (`PARAMS`). This is the only file you edit when rates change. |
| `src/site.mjs` | Domain, site name, e-mail, AdSense ID, analytics. |
| `src/content.mjs` | Page texts, FAQs and forms. |
| `src/build.mjs` | Generates every page, the sitemap, robots.txt and ads.txt. |
| `test/engine.test.mjs` | Checks the formulas against officially published figures. |

Rebuilding the site requires Node 18 or later: `npm run build` (output goes to `dist/`), and `npm test` runs the formula checks.

## Launch checklist (~1 hour, ~$10–15)

1. **Domain.** Buy one, for example `hesapcantasi.com`, or any name you prefer. Cloudflare Registrar sells at cost (about $10 a year). If you pick a different name, change `url` and `email` in `src/site.mjs` and rebuild.
2. **Hosting (free).** In Cloudflare, go to Workers & Pages → Create → Pages → *Upload assets* and drag in the `dist` folder. Then attach your domain under *Custom domains*.
3. **Google Search Console.** Add the domain, verify it with the DNS record Cloudflare offers, and submit `https://yourdomain/sitemap.xml`.
4. **Analytics (optional).** Turn on Cloudflare Web Analytics, which is free and needs no cookie banner, and paste its token into `cfBeacon` in `src/site.mjs`.
5. **AdSense.** Apply once the site is indexed and has some traffic, typically after 2–6 weeks. When you're approved, paste `ca-pub-…` into `adsenseClient` and rebuild. Ad slots and `ads.txt` appear automatically. The privacy page already contains Google's required cookie wording.

## Keeping it current (this is what keeps rankings)

| When | What changes | Where in `engine.js` |
|---|---|---|
| ~3rd–5th of every month | Kira artış oranı (TÜİK 12-month average CPI) | add a new row to the top of `kiraOranlari` |
| Late December / January | Asgari ücret, gelir vergisi dilimleri, SGK tavanı, kıdem tavanı (Jan–Jun) | `asgariBrut`, `asgariNet`, `gvDilim`, `sgkTavan`, `kidemTavan`, `year` |
| July | Kıdem tavanı (Jul–Dec) and, if it happens, a mid-year minimum wage raise | `kidemTavan` |
| Whenever a decree is issued | Mevduat stopajı (current rates valid until 31.12.2026), KKDF/BSMV | `stopaj`, `kkdf`, `bsmvTuketici` |

After any edit: update `updated`, run `npm test` and then `npm run build`, and re-upload `dist/`. When the year changes, also rename the URL year in `content.mjs` (asgari-ucret / gelir-vergisi pages). Better still, keep the old pages and add new ones.

## Growth ideas once it's indexed

- Add more programmatic sets: "X TL kıdem tazminatı N yıl", "X TL kredi N ay taksit", "X TL mevduat getirisi".
- Add more calculators: emeklilik/yaşlılık, enflasyon (needs a TÜFE index series), altın, araç MTV, tapu harcı, e-ticaret komisyon.
- Write one evergreen guide per calculator: "kıdem tazminatı şartları", "kira tespit davası" and similar.
- Earn a few links from forums and Ekşi/Reddit threads where people ask these questions.
