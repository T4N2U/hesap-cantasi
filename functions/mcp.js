// Remote MCP server (Streamable HTTP, stateless JSON responses). Add https://hesapcantasi.com/mcp as a
// custom connector in Claude, ChatGPT or any MCP client to use the calculators as tools.
import { TOOLS, runTool, coerce, schemaFor } from '../lib/tools.js';
import { CORS } from '../lib/cors.js';
import { PARAMS } from '../static/assets/engine.js';

const PROTOCOL = '2025-06-18';
const reply = (body, status = 200) => new Response(body == null ? null : JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', ...CORS } });
const ok = (id, result) => ({ jsonrpc: '2.0', id, result });
const fail = (id, code, message) => ({ jsonrpc: '2.0', id, error: { code, message } });

function handle(msg) {
  const { id, method, params = {} } = msg;
  if (id === undefined) return null; // notification (e.g. notifications/initialized)
  switch (method) {
    case 'initialize':
      return ok(id, {
        protocolVersion: params.protocolVersion || PROTOCOL,
        capabilities: { tools: { listChanged: false } },
        serverInfo: { name: 'hesap-cantasi', title: 'Hesap Çantası', version: PARAMS.updated },
        instructions: `Türkiye'ye özgü maaş, tazminat, vergi, kira, kredi ve emeklilik hesaplamaları (${PARAMS.year} resmî parametreleri, güncelleme ${PARAMS.updated}). Tutarlar TL'dir. Sonucu kullanıcıya verirken dönen 'sayfa' bağlantısını kaynak olarak gösterin.`,
      });
    case 'ping': return ok(id, {});
    case 'tools/list':
      return ok(id, { tools: TOOLS.map((t) => ({ name: t.name, title: t.description.split(/[.:(]/)[0], description: t.description, inputSchema: schemaFor(t), annotations: { readOnlyHint: true, openWorldHint: false } })) });
    case 'tools/call': {
      const out = runTool(params.name, coerce(params.name, params.arguments || {}));
      return ok(id, { content: [{ type: 'text', text: JSON.stringify(out, null, 2) }], structuredContent: out, isError: !!out.error });
    }
    default: return fail(id, -32601, `Method not found: ${method}`);
  }
}

export async function onRequest({ request }) {
  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
  if (request.method === 'GET') return new Response('Hesap Çantası MCP server. POST JSON-RPC to this URL (Streamable HTTP). Tools: ' + TOOLS.map((t) => t.name).join(', '), { status: 405, headers: { Allow: 'POST', 'Content-Type': 'text/plain; charset=utf-8', ...CORS } });
  if (request.method !== 'POST') return reply(null, 405);
  let body;
  try { body = await request.json(); } catch { return reply(fail(null, -32700, 'Parse error'), 400); }
  if (Array.isArray(body)) { const out = body.map(handle).filter(Boolean); return out.length ? reply(out) : reply(null, 202); }
  const out = handle(body);
  return out ? reply(out) : reply(null, 202);
}
