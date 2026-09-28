"""Build the self-contained proposal HTML and SVG diagrams; standard library only.

The small renderer supports this proposal's headings, paragraphs, tables, lists,
links, images and one Mermaid block. The latter uses the accompanying SVG flow.
Edit docs/proposal.md for prose; diagram layout and artwork live here.
"""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
COLORS = {'data':'#156b60','compute':'#365db0','display':'#9a6126','ai':'#7353a5','recovery':'#a34552','access':'#445669'}


def svg_start(width, height, title, description):
    tag = re.sub(r'[^a-z0-9]+', '-', title.lower())
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="{tag}-title {tag}-desc">',
            f'<title id="{tag}-title">{escape(title)}</title><desc id="{tag}-desc">{escape(description)}</desc>',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/></marker></defs>',
            f'<rect width="{width}" height="{height}" rx="24" fill="#f6f5ef"/>',
            '<style>text{font-family:Arial,sans-serif;fill:#172b36}.small{font-size:17px}.body{font-size:20px}.name{font-size:24px;font-weight:700}.eyebrow{font-size:15px;font-weight:700;letter-spacing:1px}.line{fill:none;stroke:#64748b;stroke-width:2.5;marker-end:url(#arrow)}</style>']


def text(parts, x, y, value, cls='body', fill=None):
    parts.append(f'<text x="{x}" y="{y}" class="{cls}"'+(f' style="fill:{fill}"' if fill else '')+f'>{escape(value)}</text>')


def card(parts, x, y, w, h, role, title, lines, category):
    c=COLORS[category]
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="white" stroke="#d7dfdf"/>')
    parts.append(f'<rect x="{x}" y="{y}" width="6" height="{h}" rx="3" fill="{c}"/>')
    text(parts,x+20,y+27,role.upper(),'eyebrow',c)
    text(parts,x+20,y+59,title,'name')
    for n,line in enumerate(lines):text(parts,x+20,y+87+25*n,line,'small')


def overview():
    p=svg_start(1400,930,'Calicortado architecture overview','Proposed roles: devices, private access, display, compute, data, local AI and independent recovery. All service boundaries use named HTTPS routes through destination-local Traefik.')
    text(p,45,55,'A personal library, built from replaceable parts','name')
    text(p,45,86,'PROPOSED PRODUCT • role separation does not require one new machine per box','small')
    card(p,45,120,620,115,'Your devices','Write in Obsidian',['iPhone + Mac • local notes remain editable offline'],'display')
    card(p,700,120,655,115,'Your interface','Capture · Search · Ask',['Browser + phone Shortcut • one simple experience'],'display')
    for x in [355,1025]:p.append(f'<path class="line" d="M{x} 235 V275"/>')
    p.append('<rect x="45" y="280" width="1310" height="90" rx="14" fill="#e0e9ec"/>')
    text(p,70,313,'PRIVATE ACCESS + DNS + IDENTITY','eyebrow')
    text(p,70,346,'Each receiving host: Traefik + verified HTTPS → service checks permissions','body')
    for x in [245,700,1155]:p.append(f'<path class="line" d="M{x} 370 V410"/>')
    card(p,45,415,405,180,'Display role','The front desk',['app.domain','Web experience and user session','No database credentials in browser'],'display')
    card(p,497,415,405,180,'Compute role','The working team',['capture · search · embed · answers','Indexing worker updates the catalogue','Calls data and AI through APIs'],'compute')
    card(p,950,415,405,180,'Data role','The originals + catalogue',['sync · data · index','Bridge, readable vault, note revisions','Derived index can be rebuilt'],'data')
    p.append('<path class="line" d="M450 505 H497"/><path class="line" d="M902 505 H950"/>')
    p.append('<path class="line" d="M700 595 V625 H360 V655"/><path class="line" d="M1155 595 V625 H1040 V655"/>')
    card(p,45,660,620,165,'AI role','The reading assistant',['infer.domain • local model behind an adapter','Receives permitted excerpts, not unrestricted vault access','Search and capture do not depend on generation'],'ai')
    card(p,700,660,655,165,'Independent recovery role','The recovery copy',['backup.domain • encrypted repository','Data-local worker sends a consistent backup','Restoration must be rehearsed, not merely configured'],'recovery')
    text(p,45,864,'Identity uses auth.domain. Operations cover every role: health, redacted logs, versions and restore drills.','small')
    text(p,45,895,'domain = configured DOMAIN • Initial roles may share hardware • Foundation verified; product services planned','small')
    p.append('</svg>');return ''.join(p).replace('id="arrow"', 'id="overview-arrow"').replace('url(#arrow)', 'url(#overview-arrow)')


def flow():
    p=svg_start(1600,1500,'Calicortado complete logical service flow','Eleven configurable domain endpoints plus devices and indexing worker. Solid arrows show major service requests; the shared identity and operations bands apply across the diagram. Local bridge and backup work stays inside the data boundary.')
    text(p,60,48,'How the complete product talks to itself','name')
    text(p,60,78,'PROPOSED • Every domain box means HTTPS through that destination’s Traefik','small')
    nodes={
      'obs':(90,110,'device','Obsidian',['iPhone + Mac • local editing'],'display'),
      'web':(620,110,'device','Browser',['Capture / Search / Ask'],'display'),
      'phone':(1150,110,'device','Phone Shortcut',['Receipt ID + offline fallback'],'display'),
      'sync':(90,320,'data role','Sync',['sync.domain','Encrypted sync ↔ local bridge'],'data'),
      'app':(620,320,'display role','Web interface',['app.domain','Human session; no machine keys'],'display'),
      'capture':(1150,320,'compute role','Capture',['capture.domain','Create-only ingestion'],'compute'),
      'data':(90,610,'data role','Data + local vault',['data.domain','Notes, revisions, IDs, change feed'],'data'),
      'search':(620,610,'compute role','Search',['search.domain','Current permitted results'],'compute'),
      'answers':(1150,610,'compute role','Answers',['answers.domain','Retrieval + cited response'],'compute'),
      'index':(90,920,'data role / derived','Index',['index.domain','Rebuildable lookup store'],'data'),
      'job':(620,920,'compute role','Indexing worker',['No extra public endpoint','Read changes → embed → index'],'compute'),
      'embed':(1150,920,'compute role','Embeddings',['embed.domain','Text / query → meaning vectors'],'compute'),
      'backup':(90,1220,'recovery role','Backup repository',['backup.domain','Encrypted independent copy'],'recovery'),
      'identity':(620,1220,'access role','Identity / grant broker',['auth.domain','Scoped grants; live integration due'],'access'),
      'infer':(1150,1220,'ai role','Local inference',['infer.domain','Bounded excerpts → generation'],'ai')}
    # Routes are drawn first so card backgrounds mask line crossings at boxes.
    paths=[
      'M265 235 V320','M795 235 V320','M1325 235 V320',
      'M970 382 H1150','M795 445 V610','M970 405 H1060 V660 H1150',
      'M265 445 V610','M1325 445 V520 H265 V610',
      'M620 670 H440','M1150 670 H970',
      'M705 735 V825 H265 V920','M885 735 V835 H1325 V920',
      'M620 970 H440','M970 985 H1150','M795 920 V800 H390 V735',
      'M1500 680 H1540 V1280 H1500','M155 735 H45 V1280 H90']
    for d in paths:p.append(f'<path class="line" d="{d}"/>')
    for key,(x,y,role,title,lines,category) in nodes.items():card(p,x,y,350,125,role,title,lines,category)
    for x,y,label in [(280,485,'bridge stays data-local'),(570,507,'capture saves through data API'),(455,655,'source + access'),(465,955,'index updates'),(985,969,'text to vectors'),(810,810,'change feed'),(970,815,'query vector'),(65,1140,'local snapshot worker')]:
      text(p,x,y,label,'small')
    text(p,60,1405,'Shared rules: private access + DNS; identity checked at protected destinations; operations observe all roles.','small')
    text(p,60,1435,'Only data-local code touches the vault. Other layers use domain APIs. AI has no note-write or admin authority.','small')
    text(p,60,1465,'Arrows show requests / local data operations; responses return on the same connection. No live deployment claimed.','small')
    p.append('</svg>');return ''.join(p).replace('id="arrow"', 'id="flow-arrow"').replace('url(#arrow)', 'url(#flow-arrow)')


def inline(value):
    value=escape(value)
    value=re.sub(r'`([^`]+)`',r'<code>\1</code>',value)
    value=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',value)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',value)


def render_markdown(source):
    lines=source.splitlines();out=[];i=0
    while i<len(lines):
        line=lines[i]
        if not line.strip():i+=1;continue
        if line.startswith('```mermaid'):
            i+=1
            while i<len(lines) and lines[i]!='```':i+=1
            out.append('<figure class="wide">'+flow()+'<figcaption>Full logical service flow. Each domain endpoint includes its destination’s Traefik ingress.</figcaption></figure>');i+=1;continue
        if line.startswith('!['):
            out.append('<figure class="wide">'+overview()+'</figure>');i+=1;continue
        if line.startswith('#'):
            level=len(line)-len(line.lstrip('#'));label=line[level:].strip()
            anchor=re.sub(r'[^a-z0-9 -]','',label.lower()).replace(' ','-')
            out.append(f'<h{level} id="{anchor}">{inline(label)}</h{level}>');i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[c.strip() for c in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r'[: -]+',c) for c in cells):rows.append(cells)
                i+=1
            out.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+inline(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>')
            for row in rows[1:]:out.append('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>')
            out.append('</tbody></table></div>');continue
        if line.startswith('- '):
            out.append('<ul>')
            while i<len(lines) and lines[i].startswith('- '):out.append('<li>'+inline(lines[i][2:])+'</li>');i+=1
            out.append('</ul>');continue
        paragraph=[]
        while i<len(lines) and lines[i].strip():paragraph.append(lines[i]);i+=1
        out.append('<p>'+inline(' '.join(paragraph))+'</p>')
    return '\n'.join(out)


def main():
    (DOCS/'architecture-overview.svg').write_text(overview(),encoding='utf-8')
    (DOCS/'architecture-flow.svg').write_text(flow(),encoding='utf-8')
    source=(DOCS/'proposal.md').read_text(encoding='utf-8')
    body=render_markdown(source)
    css='''
    :root{color-scheme:light;--ink:#172b36;--muted:#53646d;--paper:#fffefa;--accent:#156b60}
    *{box-sizing:border-box}body{margin:0;background:#efeee8;color:var(--ink);font:18px/1.7 system-ui,-apple-system,Segoe UI,sans-serif}
    header{background:#123e38;color:white;padding:44px max(5vw,24px);border-bottom:8px solid #d0b479}
    header span{font-size:13px;letter-spacing:2px;text-transform:uppercase}header p{max-width:860px;font-size:23px;margin:12px 0}
    nav{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px}nav a{color:#fff;padding:5px 12px;border:1px solid #92b1a7;border-radius:30px;text-decoration:none;font-size:14px}
    main{max-width:1220px;background:var(--paper);padding:52px 70px;margin:0 auto;box-shadow:0 8px 40px #243b3410}
    h1{font-size:64px;letter-spacing:-3px;line-height:1.1;margin:8px 0 20px}h2{font-size:32px;line-height:1.3;letter-spacing:-.5px;margin:65px 0 22px;border-top:1px solid #d6deda;padding-top:28px}h3{font-size:23px;margin-top:32px}
    h1+h2{border:0;margin-top:0;padding:0;color:var(--accent);font-size:36px}p{max-width:920px;margin:16px 0}strong{font-weight:650}a{color:#126d61;text-underline-offset:3px}code{background:#edf2ee;border-radius:4px;padding:2px 5px;font-size:.86em;overflow-wrap:anywhere}
    figure{margin:30px 0}figure svg{display:block;width:100%;height:auto}figcaption{font-size:14px;color:var(--muted);margin-top:12px}.wide{margin-left:-35px;margin-right:-35px}
    .table-wrap{overflow-x:auto;margin:24px 0}table{border-collapse:collapse;width:100%;font-size:15px;line-height:1.6}th{text-align:left;background:#e4ece7;color:#1d4b42;padding:14px}td{vertical-align:top;border-bottom:1px solid #dfe5e0;padding:14px}tr:nth-child(even){background:#f6f7f2}td:first-child{font-weight:550;min-width:165px}
    footer{padding:30px;text-align:center;color:var(--muted);font-size:13px}li{margin:8px 0}
    @media(max-width:700px){main{padding:30px 22px}h1{font-size:48px}h2{font-size:26px}.wide{margin:24px 0}header p{font-size:20px}table{min-width:650px}figure{overflow-x:auto}figure svg{min-width:800px}}
    @media print{body{background:white;font-size:11pt}header{padding:18px 30px;print-color-adjust:exact}nav{display:none}main{padding:20px;max-width:none;box-shadow:none}h1{font-size:36pt}h2{font-size:20pt;break-after:avoid}h3{break-after:avoid}figure{break-inside:avoid}.wide{margin:18px 0}table{font-size:9pt}tr{break-inside:avoid}a{color:inherit}footer{display:none}}
    '''
    html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Calicortado — A private second brain</title><style>'+css+'</style></head><body><header><span>Product proposal · Architecture explained · 29 September 2026</span><p>Capture quickly. Keep control. Find what matters. Ask with evidence.</p><nav><a href="#3-the-architecture-at-a-glance">Architecture</a><a href="#9-what-exists-today">Progress</a><a href="#10-the-route-to-a-usable-release">Delivery</a><a href="#12-a-small-technology-dictionary">Technology guide</a></nav></header><main>'+body+'</main><footer>Calicortado • Proposal, not a deployment claim • Generated from docs/proposal.md</footer></body></html>'
    (DOCS/'proposal.html').write_text(html,encoding='utf-8')
    print('Built proposal.html and two accessible SVG diagrams; no external rendering dependencies.')


if __name__=='__main__':main()
