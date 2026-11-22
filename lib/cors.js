export const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Accept, Mcp-Session-Id, Mcp-Protocol-Version',
};
// API responses are data only: no framing, no scripts, no sniffing (OWASP A05).
export const SECURITY = { 'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'DENY', 'Content-Security-Policy': "default-src 'none'; frame-ancestors 'none'", 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains', 'Referrer-Policy': 'no-referrer' };
export const json = (body, status = 200, extra = {}) => new Response(JSON.stringify(body, null, 2), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'public, max-age=300', ...SECURITY, ...CORS, ...extra } });
