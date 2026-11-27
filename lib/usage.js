// Anonymous usage counting for the API and MCP server (Workers Analytics Engine, binding HC_USAGE).
// Privacy by design: we record only fixed labels — channel, tool/fact name (from our own fixed lists), a coarse client
// label, a coarse user-agent family, the 2-letter country Cloudflare already provides, and ok/error.
// We NEVER record IP addresses, raw user agents, request arguments (salaries, dates…) or anything free-form.
// If the binding is missing (local tests, preview builds) recording is a no-op; it can never break a response.
import { TOOL_MAP } from './tools.js';
import { FACT_MAP } from './facts.js';

const UA_FAMILIES = [
  ['Claude-User', 'claude-user'], ['Claude-SearchBot', 'claude-searchbot'], ['ClaudeBot', 'claudebot'], ['Anthropic', 'anthropic'],
  ['ChatGPT-User', 'chatgpt-user'], ['OAI-SearchBot', 'oai-searchbot'], ['GPTBot', 'gptbot'], ['OpenAI', 'openai'],
  ['Perplexity-User', 'perplexity-user'], ['PerplexityBot', 'perplexitybot'], ['Google-Extended', 'google-extended'],
  ['Googlebot', 'googlebot'], ['bingbot', 'bingbot'], ['YandexBot', 'yandexbot'], ['Applebot', 'applebot'],
  ['python', 'python'], ['node', 'node'], ['undici', 'node'], ['curl', 'curl'], ['Go-http-client', 'go'], ['axios', 'node'],
  ['Mozilla', 'browser'],
];
export function uaFamily(ua) {
  const s = String(ua || '').slice(0, 300);
  for (const [needle, label] of UA_FAMILIES) if (s.includes(needle)) return label;
  return s ? 'other' : 'none';
}
// MCP clients send clientInfo.name on initialize (e.g. "claude-ai", "openai-mcp"). Keep it only if it looks like a plain
// product name, lower-cased and trimmed; anything else becomes "other" so nothing free-form or personal is stored.
export function clientLabel(name) {
  const s = String(name || '').trim().toLowerCase();
  return /^[a-z0-9][a-z0-9 ._-]{0,39}$/.test(s) ? s : (s ? 'other' : 'unknown');
}
const known = (name) => (TOOL_MAP[name] || FACT_MAP[name] || ['list', 'initialize', 'resources/list', 'resources/read', 'tools/list', 'index'].includes(name)) ? name : 'unknown';

export function record(env, request, { kanal, ad, istemci = 'unknown', ok = true }) {
  try {
    const ds = env && env.HC_USAGE;
    if (!ds || typeof ds.writeDataPoint !== 'function') return;
    const country = request && request.cf && /^[A-Z]{2}$/.test(request.cf.country || '') ? request.cf.country : 'XX';
    ds.writeDataPoint({
      indexes: [kanal === 'mcp' ? 'mcp' : 'rest'],
      blobs: [kanal === 'mcp' ? 'mcp' : 'rest', known(ad), clientLabel(istemci), uaFamily(request && request.headers.get('user-agent')), country, ok ? 'ok' : 'error'],
      doubles: [1],
    });
  } catch { /* never let analytics affect the answer */ }
}
