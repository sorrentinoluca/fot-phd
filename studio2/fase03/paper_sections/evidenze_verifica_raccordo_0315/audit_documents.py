from pathlib import Path
import subprocess,json,re,collections,hashlib,urllib.parse,html
from bs4 import BeautifulSoup
import mistune,difflib
R=Path(__file__).resolve().parents[4];O=Path(__file__).parent;P='studio2/fase03/paper_sections/';B='e82b5a0';A='9b6bd64'
def raw(ref,p):return subprocess.check_output(['git','show',ref+':'+p],cwd=R).decode()
def norm(x):return ' '.join(x.get_text().split()).replace('letteratura.html','letteratura.md')
md=mistune.create_markdown(escape=False,plugins=['table'])
def atoms(s):return [(x.name,norm(x)) for x in s.find_all(['h1','h2','h3','h4','h5','h6','p','li','th','td']) if norm(x) and not (x.name=='p' and x.parent.name=='li')]
wm='docs/fot_walkthrough_conversazione_studio2.md';wh=wm[:-3]+'.html';tm=raw(A,wm);th=raw(A,wh);sh=BeautifulSoup(th,'html.parser');out={}
anchor='paper-sections-0315';start=tm.index('<a id="'+anchor+'"></a>');end=tm.index('### Sintesi per sezione',start);section=tm[start:end]
ma=atoms(BeautifulSoup(md(section),'html.parser'));ha=atoms(sh.find(id=anchor));out['parity_415']={'md_blocks':len(ma),'html_blocks':len(ha),'equal':ma==ha,'diff':list(difflib.unified_diff([str(x) for x in ma],[str(x) for x in ha])),'md_normalized_chars':len(' '.join(x[1] for x in ma)),'html_normalized_chars':len(' '.join(x[1] for x in ha))}
out['shared_new_unmatched_blocks']=list(((collections.Counter(atoms(BeautifulSoup(md(tm),'html.parser')))-collections.Counter(atoms(sh)))-(collections.Counter(atoms(BeautifulSoup(md(raw(B,wm)),'html.parser')))-collections.Counter(atoms(BeautifulSoup(raw(B,wh),'html.parser'))))).elements())
# Preserve every prior explicitly anchored subsection in the MD and corresponding HTML section.
old=raw(B,wm);anchors=re.findall(r'<a id="([^"]+)"',old)
out['prior_sections']=[]
def msection(t,a):
 s=t.index('<a id="'+a+'"');ends=[e for e in [t.find('<a id=',s+1),t.find('### Sintesi per sezione',s)] if e>=0];return t[s:min(ends) if ends else len(t)].rstrip()
for a in anchors:
 x,y=msection(old,a),msection(tm,a);hx=BeautifulSoup(raw(B,wh),'html.parser').find(id=a);hy=sh.find(id=a);out['prior_sections'].append({'anchor':a,'md_equal':x==y,'html_equal':str(hx)==str(hy),'md_sha256':hashlib.sha256(y.encode()).hexdigest()})
out['headings_missing']=list((collections.Counter(re.findall(r'^#{1,6} .+$',old,re.M))-collections.Counter(re.findall(r'^#{1,6} .+$',tm,re.M))).elements());out['subsection_order']=[norm(x) for x in sh.find_all('h3') if re.match(r'^4\.\d+',norm(x))]
# Local links, including fragments; MD parsed to avoid parentheses and inline-code regex errors.
def slug(t):return re.sub(r'[^\w\s-]','',t.lower().replace('`','').replace('*','')).replace(' ','-')
def target_ids(t,suffix):
 ids=[x['id'] for x in BeautifulSoup(t,'html.parser').find_all(id=True)]
 if suffix=='.md':
  seen=collections.Counter()
  for h in BeautifulSoup(md(t),'html.parser').find_all(re.compile('^h[1-6]$')):
   z=slug(norm(h));ids.append(z+('-'+str(seen[z]) if seen[z] else ''));seen[z]+=1
 return ids
cache={}
def links(ref,p):
 t=raw(ref,p);s=BeautifulSoup(md(t) if p.endswith('.md') else t,'html.parser');result=[]
 for x in s.find_all(True):
  for attr in ['href','src']:
   if not x.has_attr(attr):continue
   link=x[attr];u=urllib.parse.urlsplit(link)
   if u.scheme or u.netloc:continue
   dest=((R/p).parent/urllib.parse.unquote(u.path)).resolve() if u.path else R/p
   if not dest.is_relative_to(R):
    result.append({'source':p,'link':link,'status':'absolute_external_exists' if dest.exists() else 'absolute_external_missing'});continue
   pp=str(dest.relative_to(R));exists=subprocess.run(['git','cat-file','-e',ref+':'+pp],cwd=R,stderr=subprocess.DEVNULL).returncode==0
   status='ok' if exists else 'missing_path'
   if exists and u.fragment:
    key=(ref,pp)
    if key not in cache:cache[key]=target_ids(raw(ref,pp),dest.suffix)
    if urllib.parse.unquote(u.fragment) not in cache[key]:status='missing_anchor'
   result.append({'source':p,'link':link,'status':status})
 return result
core=[wm,wh,'studio2/PROVENIENZA.md'];out['links_base']=[x for p in core for x in links(B,p)];out['links_A']=[x for p in core for x in links(A,p)]
extra=['REPORT_DELTA_0315.md','VERIFICA_DELTA_0315.md','ACQUISIZIONE_VERIFICA_DELTA_0315.md','REPORT_ACQUISIZIONE_VERIFICA_PAPER_SECTIONS.md','ACQUISIZIONE_VERIFICA_PAPER_SECTIONS.md','CONSEGNA_0315_2026-09-14.md','CONSEGNA_INTEGRAZIONE_LOCALE_0315_2026-09-14.md']
out['links_records']=[x for p in extra for x in links(A,P+p)]
ids=[x['id'] for x in sh.find_all(id=True)];out['html_ids']={'count':len(ids),'duplicates':[x for x,c in collections.Counter(ids).items() if c>1]}
hlinks=[x for x in out['links_A'] if x['source']==wh];out['html_links']={'total_local':len(hlinks),'to_paths':sum(not x['link'].startswith('#') for x in hlinks),'to_same_page':sum(x['link'].startswith('#') for x in hlinks),'errors':[x for x in hlinks if x['status']!='ok']}
out['conflict_markers']=re.findall(r'^(?:<<<<<<<|=======|>>>>>>>)',tm+th+raw(A,'studio2/PROVENIENZA.md'),re.M)
out['old_6_12']=next(l for l in old.splitlines() if l.startswith('12. **§6.12'));out['new_6_12']=next(l for l in tm.splitlines() if l.startswith('12. **§6.12'))
(O/'documents.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
for k,v in out.items():
 if k.startswith('links_'):print(k,len(v),collections.Counter(x['status'] for x in v),[x for x in v if 'missing' in x['status']])
 else:print(k,v)
