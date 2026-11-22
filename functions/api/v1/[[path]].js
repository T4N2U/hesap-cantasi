// REST API: GET /api/v1                → list of calculators
//           GET /api/v1/{name}?a=1&b=2 → result (POST with a JSON body also works)
import { TOOLS, runTool, coerce, schemaFor } from '../../../lib/tools.js';
import { CORS, json } from '../../../lib/cors.js';

export async function onRequest({ request, params }) {
  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
  const name = (params.path || [])[0];
  if (!name) {
    return json({
      ad: 'Hesap Çantası API', aciklama: 'Türkiye için maaş, tazminat, vergi, kira ve kredi hesaplamaları. Ücretsiz, anahtar gerekmez.',
      openapi: 'https://hesapcantasi.com/openapi.json', mcp: 'https://hesapcantasi.com/mcp',
      hesaplamalar: TOOLS.map((t) => ({ ad: t.name, aciklama: t.description, url: `https://hesapcantasi.com/api/v1/${t.name}`, parametreler: schemaFor(t) })),
    });
  }
  let raw = Object.fromEntries(new URL(request.url).searchParams);
  if (!['GET', 'POST'].includes(request.method)) return json({ error: 'Yalnızca GET ve POST.' }, 405);
  if (+(request.headers.get('content-length') || 0) > 16384) return json({ error: 'İstek çok büyük.' }, 413);
  if (request.method === 'POST') { try { raw = { ...raw, ...(await request.json()) }; } catch { return json({ error: 'Gövde geçerli JSON değil.' }, 400); } }
  const out = runTool(name, coerce(name, raw));
  return json(out, out.error ? (out.araclar ? 404 : 400) : 200);
}
