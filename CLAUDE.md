# Hesap Çantası: rules for anyone (human or Claude) changing this repo

## Accuracy rule (from the owner; non-negotiable)
People use these calculators for decisions about their pay, taxes, rent and pensions. A wrong number can cost them money.

- **Never infer, estimate or "reason out" a rate, limit, amount, date or legal rule.** Every number in `static/assets/engine.js` PARAMS, every formula and every factual sentence in `src/content.mjs` must come from an official source (Resmî Gazete, GİB, SGK, TÜİK, TCMB, ÇSGB, the law text) or be confirmed by **at least two reliable independent sources** (Big-4 / YMM bulletins, established tax portals, major newspapers quoting the official text).
- Put the source in a code comment next to the value (tebliğ number or site).
- If a figure isn't official yet (next year's brackets, MTV, asgari ücret), don't publish a single guessed number. Show only what the law determines (e.g. the GVK 123 range) or clearly labelled scenarios, and say when the official figure comes out.
- If two sources disagree, or only one exists, don't ship the number. Leave the old value and flag it to the owner.
- Every new or changed formula gets a test in `test/engine.test.mjs` against a published worked example.
- When an official figure is published, update the page the same day and remove the "tahmini/senaryo" wording.

## Build
`npm test` then `npm run build` (output in `dist/`). Push to `main`; Cloudflare Pages deploys automatically.
