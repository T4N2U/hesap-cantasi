# Hesap Çantası: rules for anyone (human or Claude) changing this repo

## Accuracy rule (from the owner; non-negotiable)
People use these calculators for decisions about their pay, taxes, rent and pensions. A wrong number can cost them money.

- **Never infer, estimate or "reason out" a rate, limit, amount, date or legal rule.** Every number in `static/assets/engine.js` PARAMS, every formula and every factual sentence in `src/content.mjs` must come from an official source (Resmî Gazete, GİB, SGK, TÜİK, TCMB, ÇSGB, the law text) or be confirmed by **at least two reliable independent sources** (Big-4 / YMM bulletins, established tax portals, major newspapers quoting the official text).
- Put the source in a code comment next to the value (tebliğ number or site).
- If a figure isn't official yet (next year's brackets, MTV, asgari ücret), don't publish a single guessed number. Show only what the law determines (e.g. the GVK 123 range) or clearly labelled scenarios, and say when the official figure comes out.
- If two sources disagree, or only one exists, don't ship the number. Leave the old value and flag it to the owner.
- Every new or changed formula gets a test in `test/engine.test.mjs` against a published worked example.
- When an official figure is published, update the page the same day and remove the "tahmini/senaryo" wording.

## Security rule (from the owner; non-negotiable)
Every new feature or change is reviewed against the OWASP Top 10 (and the OWASP API Security Top 10 for anything under `/api` or `/mcp`) before it ships. Don't leave an open door behind, from outside or from inside the machine.

Checklist for each change:
- **Inputs:** every value from a URL, form, API or MCP call is validated (type, range, length, enum or pattern). Unknown parameters are rejected. No unbounded loops or allocations driven by input (`lib/tools.js` enforces min/max).
- **Output:** never put user input into HTML with `innerHTML`; results render numbers we compute. JSON in `<script>` tags escapes `<`.
- **Headers:** the site CSP, HSTS, frame and permissions headers come from `src/build.mjs` (`_headers`); API/MCP responses use `SECURITY` in `lib/cors.js`. When adding a third-party script (AdSense, GA4), allow only its exact hosts in the CSP.
- **Errors:** don't expose stack traces or internal messages.
- **Edge protection (Cloudflare dashboard, not in the repo):** rate-limiting rule "Rate limit /api and /mcp" (per IP, >30 requests / 10 s → block 10 s; Free plan allows 1 rule, tested 24 Nov 2026). DMARC `p=quarantine` with Cloudflare DMARC reports; SPF + DKIM from Email Routing. Nothing sends mail as @hesapcantasi.com; if that changes, add the sender to SPF/DKIM before it sends.
- **Secrets:** none in the repo, ever. The API and MCP server are read-only, need no keys and store nothing; if that ever changes, add auth and rate limits first.
- **Dependencies:** keep vendored libraries patched. Known open item: `static/assets/vendor/xlsx.mini.min.js` is SheetJS 0.18.5 (CVE-2023-30533, CVE-2024-22363 affect *parsing* files; we only *write* exports, so exposure is low) — upgrade to 0.20.3 from cdn.sheetjs.com when reachable.
- **Tests:** add a test for each validation rule you add (`test/api.test.mjs`).

## Build
`npm test` then `npm run build` (output in `dist/`). Push to `main`; Cloudflare Pages deploys automatically.

## Machine interface
- `lib/tools.js` is the single registry of calculators for machines. `functions/api/v1/[[path]].js` (REST), `functions/mcp.js` (MCP, Streamable HTTP) and `dist/openapi.json` / `dist/llms.txt` / `/yapay-zeka/` are all generated from it.
- When you add a calculator to the site, add it to `lib/tools.js` and to `SAMPLES` in `test/api.test.mjs`.
