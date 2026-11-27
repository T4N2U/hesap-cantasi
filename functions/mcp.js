// Remote MCP server (Streamable HTTP, stateless JSON responses). Add https://hesapcantasi.com/mcp as a
// custom connector in Claude, ChatGPT or any MCP client to use the calculators as tools.
import { TOOLS, runTool, coerce, schemaFor } from '../lib/tools.js';
import { CORS, SECURITY } from '../lib/cors.js';
import { PARAMS } from '../static/assets/engine.js';
import { FACTS, FACT_MAP, factUri, factMarkdown } from '../lib/facts.js';

const PROTOCOL = '2025-06-18';
const reply = (body, status = 200) => new Response(body == null ? null : JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', ...SECURITY, ...CORS } });
const ok = (id, result) => ({ jsonrpc: '2.0', id, result });
const fail = (id, code, message) => ({ jsonrpc: '2.0', id, error: { code, message } });

function handle(msg) {
  const { id, method, params = {} } = msg;
  if (id === undefined) return null; // notification (e.g. notifications/initialized)
  switch (method) {
    case 'initialize':
      return ok(id, {
        protocolVersion: params.protocolVersion || PROTOCOL,
        capabilities: { tools: { listChanged: false }, resources: { listChanged: false } },
        serverInfo: { name: 'hesap-cantasi', title: 'Hesap Çantası', version: PARAMS.updated },
        instructions: `Türkiye'ye özgü maaş, tazminat, vergi, kira, kredi ve emeklilik hesaplamaları (${PARAMS.year} resmî parametreleri, güncelleme ${PARAMS.updated}). Tutarlar TL'dir. Sonucu kullanıcıya verirken dönen 'sayfa' bağlantısını kaynak olarak gösterin. Doğrulanmış kurallar ve oranlar kaynaklarıyla birlikte resources (hesapcantasi://bilgi/...) olarak da sunulur.`,
      });
    case 'ping': return ok(id, {});
    case 'tools/list':
      return ok(id, { tools: TOOLS.map((t) => ({ name: t.name, title: t.description.split(/[.:(]/)[0], description: t.description, inputSchema: schemaFor(t), annotations: { readOnlyHint: true, openWorldHint: false } })) });
    case 'tools/call': {
      const out = runTool(params.name, coerce(params.name, params.arguments || {}));
      return ok(id, { content: [{ type: 'text', text: JSON.stringify(out, null, 2) }], structuredContent: out, isError: !!out.error });
    }
    case 'resources/list':
      return ok(id, { resources: FACTS.map((f) => ({ uri: factUri(f.id), name: f.id, title: f.baslik, description: f.ozet, mimeType: 'text/markdown' })) });
    case 'resources/templates/list': return ok(id, { resourceTemplates: [] });
    case 'resources/read': {
      // Only exact URIs from the fixed list are served (no path parsing, nothing from the request echoed back).
      const m = typeof params.uri === 'string' && params.uri.length <= 100 ? /^hesapcantasi:\/\/bilgi\/([a-z0-9-]{1,60})$/.exec(params.uri) : null;
      const f = m && FACT_MAP[m[1]];
      if (!f) return fail(id, -32002, 'Resource not found');
      return ok(id, { contents: [{ uri: factUri(f.id), mimeType: 'text/markdown', text: factMarkdown(f) }] });
    }
    default: return fail(id, -32601, 'Method not found');
  }
}

export async function onRequest({ request }) {
  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
  if (request.method === 'GET') return new Response('Hesap Çantası MCP server. POST JSON-RPC to this URL (Streamable HTTP). Tools: ' + TOOLS.map((t) => t.name).join(', '), { status: 405, headers: { Allow: 'POST', 'Content-Type': 'text/plain; charset=utf-8', ...SECURITY, ...CORS } });
  if (request.method !== 'POST') return reply(null, 405);
  if (+(request.headers.get('content-length') || 0) > 65536) return reply(fail(null, -32600, 'Request too large'), 413);
  let body;
  try { body = await request.json(); } catch { return reply(fail(null, -32700, 'Parse error'), 400); }
  if (Array.isArray(body) && body.length > 20) return reply(fail(null, -32600, 'Batch too large'), 413);
  if (Array.isArray(body)) { const out = body.map(handle).filter(Boolean); return out.length ? reply(out) : reply(null, 202); }
  const out = handle(body);
  return out ? reply(out) : reply(null, 202);
}
