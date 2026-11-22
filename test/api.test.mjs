// Checks every machine-facing tool returns the same figures as the engine/website, plus the MCP and REST handlers.
import assert from 'node:assert/strict';
import { TOOLS, runTool, coerce } from '../lib/tools.js';
import { onRequest as rest } from '../functions/api/v1/[[path]].js';
import { onRequest as mcp } from '../functions/mcp.js';

const SAMPLES = {
  maas_brutten_nete: { brut: 50000 }, maas_netten_brute: { net: 40000 },
  kidem_tazminati: { baslangic: '2020-01-01', bitis: '2026-05-01', brut: 65000 }, ihbar_tazminati: { baslangic: '2020-01-01', bitis: '2026-05-01', brut: 65000 },
  issizlik_maasi: { ortalamaBrut: 60000, primGun: 900 }, fazla_mesai: { brut: 33030, saat: 10 }, bayram_mesaisi: { brut: 45000, gun: 3.5 },
  ikramiye: { brut: 75000, ikramiye: 75000 }, emekli_memur_zammi: { maas: 20000, tur: 'emekli' }, kira_artisi: { kira: 20000 },
  kira_geliri_vergisi: { yillik: 240000 }, kredi_taksit: { tutar: 100000, vade: 12, aylikFaiz: 4 }, mevduat_faizi: { tutar: 100000, yillikFaiz: 40, gun: 32 },
  kdv: { tutar: 1000, oran: 20 }, tapu_harci: { bedel: 3000000 }, emlak_vergisi: { deger: 4000000 }, mtv: { cc: 1598, modelYili: 2023, deger: 450000 }, guncel_oranlar: {},
};
for (const t of TOOLS) {
  assert.ok(SAMPLES[t.name], 'sample missing for ' + t.name);
  const r = runTool(t.name, SAMPLES[t.name]);
  assert.ok(!r.error, t.name + ': ' + r.error);
  assert.ok(r.sayfa.startsWith('https://hesapcantasi.com/'), t.name);
}
assert.equal(runTool('maas_brutten_nete', { brut: 50000 }).sonuc.ocakNet, 40207.52);
assert.equal(runTool('mevduat_faizi', { tutar: 100000, yillikFaiz: 40, gun: 32 }).sonuc.net, 2893.15);
assert.equal(runTool('ikramiye', { brut: 75000, ikramiye: 75000 }).sonuc.net, 45968.25);
assert.equal(runTool('mtv', { cc: 1598, modelYili: 2023, deger: 450000 }).sonuc.yillik, 8264);
assert.ok(runTool('kdv', {}).error);
assert.ok(runTool('yok', {}).error);
assert.equal(coerce('maas_brutten_nete', { brut: '50.000' }).brut, 50000);
assert.equal(coerce('maas_brutten_nete', { brut: '50000.5' }).brut, 50000.5);

// REST
let res = await rest({ request: new Request('https://hesapcantasi.com/api/v1/maas_brutten_nete?brut=50000'), params: { path: ['maas_brutten_nete'] } });
assert.equal(res.status, 200); assert.equal((await res.json()).sonuc.ocakNet, 40207.52);
res = await rest({ request: new Request('https://hesapcantasi.com/api/v1/kdv'), params: { path: ['kdv'] } });
assert.equal(res.status, 400);
res = await rest({ request: new Request('https://hesapcantasi.com/api/v1'), params: {} });
assert.equal((await res.json()).hesaplamalar.length, TOOLS.length);

// MCP
const call = async (body) => { const r = await mcp({ request: new Request('https://hesapcantasi.com/mcp', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }) }); return [r.status, r.status === 202 ? null : await r.json()]; };
let [st, j] = await call({ jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2025-06-18', capabilities: {}, clientInfo: { name: 't', version: '1' } } });
assert.equal(st, 200); assert.equal(j.result.serverInfo.name, 'hesap-cantasi');
[st] = await call({ jsonrpc: '2.0', method: 'notifications/initialized' }); assert.equal(st, 202);
[, j] = await call({ jsonrpc: '2.0', id: 2, method: 'tools/list' }); assert.equal(j.result.tools.length, TOOLS.length);
[, j] = await call({ jsonrpc: '2.0', id: 3, method: 'tools/call', params: { name: 'kidem_tazminati', arguments: { baslangic: '2020-01-01', bitis: '2026-05-01', brut: 65000 } } });
assert.equal(j.result.isError, false); assert.ok(j.result.structuredContent.sonuc.net > 0);
[, j] = await call({ jsonrpc: '2.0', id: 4, method: 'nope' }); assert.equal(j.error.code, -32601);
console.log('API and MCP tests passed (' + TOOLS.length + ' tools)');
