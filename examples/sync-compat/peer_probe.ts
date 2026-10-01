// Synthetic, headless compatibility check; not an Obsidian device or vault test.
import { PeerCouchDB } from './PeerCouchDB.ts';
import { setGlobalLogFunction } from 'octagonal-wheels/common/logger';

const settings = JSON.parse(await Deno.readTextFile('/fixture/client.json'));
const url = settings.url;
const auth = {Authorization: 'Basic ' + btoa(settings.username + ':' + settings.password)};
const database = 'synthetic';
const peers: PeerCouchDB[] = [];
const checks: string[] = [];
setGlobalLogFunction(() => {}); // Do not retain credentials, paths or raw upstream logs.
function expect(value: unknown, message: string): asserts value {
  if (!value) throw new Error(message);
}
async function response(path: string, method='GET', body?: unknown) {
  return await fetch(url + path, {method, headers: {...auth, 'Content-Type':'application/json'},
    body: body === undefined ? undefined : JSON.stringify(body)});
}
function peer(name: string) {
  const value = new PeerCouchDB({type:'couchdb',name,database,username:settings.username,
    password:settings.password,url,passphrase:settings.contentKey,
    obfuscatePassphrase:settings.pathKey,baseDir:''},async () => {});
  peers.push(value);return value;
}
async function read(p: PeerCouchDB, path: string, expected: string) {
  const value = await p.get(path);
  expect(value !== false, 'Expected a readable synthetic note');
  expect(value.data.join('') === expected, 'Unicode text changed during round trip');
}
try {
  let ready=false;let lastFailure='not attempted';
  for(let i=0;i<60;i++) {
    try {const r=await response('/_up');await r.arrayBuffer();if(r.ok){ready=true;break;}lastFailure='HTTP '+r.status;} catch(e) {lastFailure=String(e);}
    await new Promise(r=>setTimeout(r,500));
  }
  expect(ready,'CouchDB did not become ready through trusted HTTPS: '+lastFailure);
  const denied=await fetch(url+'/'+database,{headers:{Authorization:'Basic '+btoa('invalid:invalid')}});
  expect(denied.status===401,'Invalid credentials were not denied');await denied.arrayBuffer();
  checks.push('trusted HTTPS readiness; invalid credentials denied');
  const created=await response('/'+database,'PUT');expect(created.ok,'Cannot create disposable database');await created.arrayBuffer();
  const a=peer('fixture-a'),b=peer('fixture-b');
  await a.start();await b.start();
  const path='Inbox/বাংলা café ☕.md';
  const original='# Synthetic-only\nবাংলা café ☕\nUnique marker: cali-synthetic-77f3\n';
  const file={ctime:1700000000000,mtime:1700000000000,size:new TextEncoder().encode(original).length,data:[original]};
  expect(await a.put(path,file),'Peer A write failed');await read(b,path,original);
  checks.push('A to B Unicode path and content round trip');
  const rawResponse=await response('/'+database+'/_all_docs?include_docs=true');
  expect(rawResponse.ok,'Cannot inspect synthetic encrypted storage');const raw=await rawResponse.text();
  expect(!raw.includes('cali-synthetic-77f3')&&!raw.includes(path),'Synthetic plaintext or path leaked in database documents');
  checks.push('raw database documents do not contain synthetic content marker or original path');
  const updated=original+'Update from B\n';
  expect(await b.put(path,{...file,mtime:file.mtime+10000,size:new TextEncoder().encode(updated).length,data:[updated]}),'Peer B update failed');
  await read(a,path,updated);checks.push('B to A update round trip');
  const c=peer('fixture-c');await c.start();await read(c,path,updated);
  checks.push('fresh peer can decrypt existing note');
  expect(await b.delete(path),'Delete failed');expect(await a.get(path)===false,'Deletion not visible to other peer');
  checks.push('deletion is visible to another peer');
  console.log(JSON.stringify({result:'PASS',checks,limits:'headless peers only; no filesystem mirror, client app, conflict, restart or production identity proof'}));
} finally {
  await Promise.allSettled(peers.map(p=>p.stop()));
  await Promise.allSettled(peers.map(p=>p.man?.close()));
  try {const r=await response('/'+database,'DELETE');await r.arrayBuffer();} catch {}
}
