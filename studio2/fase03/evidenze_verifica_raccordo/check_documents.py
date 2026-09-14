from pathlib import Path
from bs4 import BeautifulSoup
import subprocess,re,json,html,collections,urllib.parse,difflib,hashlib
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent
BASE='c486eee';A='e82b5a0'
def raw(ref,p):return subprocess.check_output(['git','show',ref+':'+p],cwd=R).decode()
def norm(t):
 t=html.unescape(t);t=re.sub(r'!?\[([^\]]+)\]\([^\n]+?\)',r'\1',t);t=re.sub(r'<[^>]+>','',t);t=t.replace('**','').replace('`','').replace('*','');return ' '.join(t.split())
def slug(t):
 t=re.sub(r'<[^>]+>','',t);t=t.replace('`','').replace('*','').strip().lower();return re.sub(r'[^\w\-\s]','',t).replace(' ','-')
def ids(t,suffix):
 v=re.findall(r'(?:id|name)=["\']([^"\']+)',t)
 if suffix=='.md':
  seen=collections.Counter()
  for x in re.findall(r'^#{1,6}\s+(.+)$',t,re.M):
   s=slug(x);v.append(s+('-'+str(seen[s]) if seen[s] else ''));seen[s]+=1
 return v
cache={}
def read(ref,p):
 k=(ref,p)
 if k not in cache:
  try:cache[k]=raw(ref,p)
  except subprocess.CalledProcessError:cache[k]=None
 return cache[k]
def links(ref,p):
 t=raw(ref,p);h=BeautifulSoup(t,'html.parser') if p.endswith('.html') else None
 ll=[x[a] for x in h.find_all(True) for a in ['href','src'] if x.has_attr(a)] if h else re.findall(r'\]\(([^\n]+?)\)',t)
 result=[]
 for link in ll:
  u=urllib.parse.urlsplit(html.unescape(link.strip('<>')))
  if u.scheme or u.netloc:continue
  dest=(R/p).parent/urllib.parse.unquote(u.path) if u.path else R/p
  dest=dest.resolve()
  if not dest.is_relative_to(R):continue
  rel=str(dest.relative_to(R));exists=subprocess.run(['git','cat-file','-e',ref+':'+rel],cwd=R,stderr=subprocess.DEVNULL).returncode==0
  status='ok' if exists else 'missing_path'
  if exists and u.fragment:
   tt=read(ref,rel)
   if tt is None or urllib.parse.unquote(u.fragment) not in ids(tt,dest.suffix):status='missing_anchor'
  result.append({'source':p,'link':link,'destination':rel,'status':status})
 return result
out={};files=['docs/fot_walkthrough_conversazione_studio2.html','docs/letteratura.html','docs/paper/FoT_TEP_paper_blueprint.html','docs/fot_walkthrough_conversazione_studio2.md','docs/letteratura.md','studio2/PROVENIENZA.md']
for ref in [BASE,A]:
 out['links_'+ref]=[v for p in files for v in links(ref,p)]
out['duplicate_html_ids']={p:[x for x,c in collections.Counter(ids(raw(A,p),'.html')).items() if c>1] for p in files[:3]}
out['html_counts']={p:sum(1 for x in out['links_'+A] if x['source']==p) for p in files[:3]}
old={(x['source'],x['link'],x['status']) for x in out['links_'+BASE] if x['status']!='ok'}
out['new_link_errors']=[x for x in out['links_'+A] if x['status']!='ok' and (x['source'],x['link'],x['status']) not in old]
out['existing_link_errors']=[x for x in out['links_'+A] if x['status']!='ok' and (x['source'],x['link'],x['status']) in old]
# Match literal source sections, no scientific recalculation.
pm='studio2/PROVENIENZA.md';pbase=raw(BASE,pm);pa=raw(A,pm);p6=raw('7c99a83',pm);p12=raw('c9f83c6',pm)
out['provenienza']={'base_prefix':pa.startswith(pbase),'evidence_prefix':pa.startswith(p6),'schema_tail_equal_after_renumber':pa[pa.index('## 13.'):]==p12[p12.index('## 12.'):].replace('## 12.','## 13.',1),'headings':re.findall(r'^## .+$',pa,re.M)}
wm='docs/fot_walkthrough_conversazione_studio2.md';wh=wm[:-3]+'.html'
def mdsec(t,anchor):
 start=t.index('<a id="'+anchor+'"></a>');end=t.find('<a id=',start+1)
 # §4.12 ends before the summary, no next anchor within section.
 summary=t.find('### Sintesi per sezione',start)
 if summary>=0:end=min(end,summary) if end>=0 else summary
 return t[start:end if end>=0 else len(t)]
for anchor,ref in [('evidence-697-d','7c99a83'),('schema-insight-0312','c9f83c6')]:
 a=mdsec(raw(A,wm),anchor);b=mdsec(raw(ref,wm),anchor)
 ha=str(BeautifulSoup(raw(A,wh),'html.parser').find(id=anchor));hb=str(BeautifulSoup(raw(ref,wh),'html.parser').find(id=anchor))
 out[anchor]={'md_byte_equal':a==b,'md_sha256':hashlib.sha256(a.encode()).hexdigest(),'html_equal':ha==hb}
 # Compare ordered content blocks including headings, list items and cells.
 mdlines=[norm(re.sub(r'^(?:#{1,6}|[-*]|[0-9]+\.|>)\s*','',l)) for l in a.splitlines() if l.strip() and not l.startswith('<a ') and not l.startswith('|')]
 htext=norm(BeautifulSoup(ha,'html.parser').get_text(' ',strip=True))
 # Paragraph wrapping joins can split inline tags: normalize all Markdown prose blocks.
 blocks=[]
 for block in re.split(r'\n\s*\n',a):
  if not block.strip() or block.startswith('<a '):continue
  if block.startswith('|'):
   for l in block.splitlines():
    if re.match(r'^\|[ :|\-]+\|$',l):continue
    blocks.extend(norm(c) for c in l.strip('|').split('|') if c.strip())
  else:
   for sub in re.split(r'\n(?=\d+\. |[-*] )',block):blocks.append(norm(re.sub(r'^(?:#{1,6}|[-*]|[0-9]+\.)\s*','',sub)))
 out[anchor]['md_blocks_missing_html']=[x for x in blocks if x and x not in htext]
 out[anchor]['md_block_count']=len(blocks)
# Record all changed/deleted lines in pre-existing sections for manual review.
diff=subprocess.check_output(['git','diff',BASE,A,'--',wm,wh,pm],cwd=R).decode()
(O/'shared_removed_lines.txt').write_text('\n'.join(x for x in diff.splitlines() if x.startswith('-') and not x.startswith('---'))+'\n')
# Previous headings preserved; matching HTML sections shows exact vs changed raccordi.
for p in [wm,wh]:
 t0=raw(BASE,p);t1=raw(A,p)
 if p.endswith('.md'):
  hh0=re.findall(r'^#{1,6} .+$',t0,re.M);hh1=re.findall(r'^#{1,6} .+$',t1,re.M)
 else:
  hh0=[x.get_text(' ',strip=True) for x in BeautifulSoup(t0,'html.parser').find_all(re.compile('^h[1-6]$'))];hh1=[x.get_text(' ',strip=True) for x in BeautifulSoup(t1,'html.parser').find_all(re.compile('^h[1-6]$'))]
 out['old_headings_missing_'+Path(p).suffix]=list((collections.Counter(hh0)-collections.Counter(hh1)).elements())
# Literature table cells and card titles, independent content comparison.
lm=raw(A,'docs/letteratura.md');lh=BeautifulSoup(raw(A,'docs/letteratura.html'),'html.parser')
mdrows=[[norm(x) for x in l.strip().strip('|').split('|')] for l in lm.splitlines() if l.startswith('|') and not re.match(r'^\|[ :|\-]+\|$',l)]
htrows=[[norm(x.get_text(' ',strip=True)) for x in tr.find_all(['td','th'])] for tr in lh.find_all('tr')]
out['lit_tables']={'md_rows':len(mdrows),'html_rows':len(htrows),'equal':mdrows==htrows,'mismatches':[(i,a,b) for i,(a,b) in enumerate(zip(mdrows,htrows),1) if a!=b]}
# Text parity is handled by the Markdown parser in check_parity.py.
out.pop('lit_tables',None)
for anchor in ['evidence-697-d','schema-insight-0312']:
 out[anchor].pop('md_blocks_missing_html',None)
 out[anchor].pop('md_block_count',None)
(O/'documents.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
for k,v in out.items():
 if k.startswith('links_'):print(k, len(v),collections.Counter(x['status'] for x in v))
 elif k=='lit_tables':print(k,{z:y for z,y in v.items() if z!='mismatches'},'first_mismatch',v['mismatches'][:1])
 else:print(k,str(v)[:3000])
