"""Run a disposable domain/TLS headless LiveSync compatibility check.

Requires a clean pinned upstream checkout, Docker Linux containers and OpenSSL.
No live DNS, host ports, machine-wide trust or personal vault mounts are used.
"""
import argparse
import json
from pathlib import Path
import secrets
import shutil
import subprocess
import tempfile

REVISION = 'c3760beaa0851214da4860903445d7f6420ca025'
HERE = Path(__file__).resolve().parent
COUCH = 'couchdb:3.5.0@sha256:1c0a30a54535377bc9ae23f42efb1ca4e92abe796f78ec98b768ac1d5874cc1b'
TRAEFIK = 'traefik:v3.7.13@sha256:24841fe2de7304c149343d877d2923b4c8800a38ba015dea9174c23b20e344a0'


def command(args, timeout=300):
    result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        # Build/test output is synthetic, but never print resolved Compose secrets.
        raise RuntimeError('Command failed: ' + args[0] + '\n' + result.stdout[-2500:] + result.stderr[-2500:])
    return result.stdout.strip()


def run(source, openssl):
    source = source.resolve()
    if command(['git','-C',str(source),'rev-parse','HEAD']) != REVISION:
        raise ValueError('Upstream source is not the reviewed revision')
    if command(['git','-C',str(source),'status','--porcelain','--untracked-files=all']):
        raise ValueError('Upstream checkout must be clean before building')
    image = 'calicortado-sync-compat:' + REVISION[:12]
    command(['docker','build','-f',str(HERE/'Dockerfile'),'-t',image,str(source)],600)
    print('Pinned bridge built with frozen dependencies and cached runtime imports.',flush=True)
    unit = command(['docker','run','--rm','--network','none',image,'deno','test','-A','--cached-only','--no-check',
                    'Peer.test.ts','PeerStorage.test.ts','types.test.ts','util.test.ts'])
    print(unit.splitlines()[-1] if unit else 'Offline tests completed.',flush=True)
    project='cali-sync-'+secrets.token_hex(5)
    root=Path(tempfile.mkdtemp(prefix=project+'-'))
    compose=['docker','compose','-p',project,'-f',str(root/'compose.json')]
    started=False
    try:
        hostname='sync.calicortado.test'
        secret=secrets.token_urlsafe(28)
        config={'url':'https://'+hostname,'username':'fixture-admin','password':secret,
                'contentKey':secrets.token_urlsafe(28),'pathKey':secrets.token_urlsafe(28)}
        (root/'client.json').write_text(json.dumps(config),encoding='utf-8')
        command([openssl,'req','-x509','-newkey','rsa:2048','-nodes','-keyout',str(root/'ca-key.pem'),
                 '-out',str(root/'ca.pem'),'-days','1','-subj','/CN=Disposable Sync Test CA',
                 '-addext','basicConstraints=critical,CA:TRUE'])
        command([openssl,'req','-new','-newkey','rsa:2048','-nodes','-keyout',str(root/'key.pem'),
                 '-out',str(root/'server.csr'),'-subj','/CN='+hostname])
        (root/'server.ext').write_text('basicConstraints=critical,CA:FALSE\nkeyUsage=critical,digitalSignature,keyEncipherment\nextendedKeyUsage=serverAuth\nsubjectAltName=DNS:'+hostname+'\n',encoding='ascii')
        command([openssl,'x509','-req','-in',str(root/'server.csr'),'-CA',str(root/'ca.pem'),
                 '-CAkey',str(root/'ca-key.pem'),'-CAcreateserial','-out',str(root/'cert.pem'),
                 '-days','1','-extfile',str(root/'server.ext')])
        (root/'couch.ini').write_text('[couchdb]\nsingle_node = true\n[cluster]\nn = 1\nq = 1\n[chttpd]\nrequire_valid_user = true\n',encoding='utf-8')
        dynamic={'tls':{'certificates':[{'certFile':'/fixture/cert.pem','keyFile':'/fixture/key.pem'}]},
                 'http':{'routers':{'sync':{'rule':'Host(`'+hostname+'`)','entryPoints':['secure'],'tls':{},'service':'sync'}},
                         'services':{'sync':{'loadBalancer':{'servers':[{'url':'http://couch:5984'}]}}}}}
        (root/'dynamic.yml').write_text(json.dumps(dynamic),encoding='utf-8')
        def mount(src, dest):return {'type':'bind','source':str(src),'target':dest,'read_only':True}
        spec={'services':{
          'couch':{'image':COUCH,'user':'couchdb','environment':{'COUCHDB_USER':config['username'],'COUCHDB_PASSWORD':secret},
                   'volumes':[mount(root/'couch.ini','/opt/couchdb/etc/local.d/99-fixture.ini')],'networks':['backend']},
          'proxy':{'image':TRAEFIK,'command':['--entrypoints.secure.address=:443','--providers.file.filename=/fixture/dynamic.yml'],
                   'volumes':[mount(root,'/fixture')],'networks':{'backend':{},'client':{'aliases':[hostname]}}},
          'test':{'image':image,'environment':{'DENO_CERT':'/fixture/ca.pem'},
                  'volumes':[mount(root,'/fixture'),mount(HERE/'peer_probe.ts','/app/calicortado_probe.ts')],
                  'networks':['client'],'command':['deno','run','-A','--cached-only','/app/calicortado_probe.ts']}},
          'networks':{'backend':{'internal':True},'client':{'internal':True}}}
        (root/'compose.json').write_text(json.dumps(spec),encoding='utf-8')
        command(compose+['config','--quiet']);started=True
        command(compose+['up','-d','couch','proxy'])
        output=command(compose+['run','--rm','--no-deps','test'],180)
        print(output,flush=True)
    except Exception:
        if started:
            diagnostics=command(compose+['logs','--no-color','--tail','15','couch','proxy'])
            print(diagnostics.replace(secret,'[redacted]'),flush=True)
        raise
    finally:
        if started:
            command(compose+['down','--volumes','--remove-orphans','--timeout','10'])
            for kind,args in [('container',['ps','-aq']),('network',['network','ls','-q']),('volume',['volume','ls','-q'])]:
                if command(['docker']+args+['--filter','label=com.docker.compose.project='+project]):
                    raise RuntimeError('Cleanup incomplete: '+kind+' for '+project+'; retain '+str(root))
        if not root.resolve().is_relative_to(Path(tempfile.gettempdir()).resolve()):
            raise RuntimeError('Cleanup target escaped temporary directory')
        shutil.rmtree(root)
        print('Cleanup verified: project containers, networks, volumes and temporary credentials removed.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--openssl',default='openssl')
    args=parser.parse_args()
    run(args.source,args.openssl)
