from pathlib import Path
import subprocess,json,re,collections,hashlib,urllib.parse,difflib
from bs4 import BeautifulSoup
import mistune
W=Path('/Users/luker/fot-tep-verifica-consolidamento-04dee86');O=Path(__file__).parent;A='04dee86';P='10582798';M='3360867';B='e82b5a0'
wm='docs/fot_walkthrough_conversazione_studio2.md';wh=wm[:-3]+'.html'
def git(*args):return subprocess.check_output(['git','-C',str(W),*args])
def raw(c,p):return git('show',c+':'+p).decode()
md=mistune.create_markdown(escape=False,plugins=['table'])
def norm(x):return ' '.join(x.get_text().split()).replace('letteratura.html','letteratura.md')
def atoms(s):return [(x.name,norm(x)) for x in s.find_all(['h1','h2','h3','h4','h5','h6','p','li','th','td']) if norm(x) and not (x.name=='p' and x.parent.name=='li')]
def msection(t,a):
 s=t.index('<a id="'+a+'"');end=[e for e in [t.find('<a id=',s+1),t.find('### Sintesi per sezione',s)] if e>=0];return t[s:min(end) if end else len(t)].rstrip()
def hsection(t,a):return str(BeautifulSoup(t,'html.parser').find(id=a))
tm=raw(A,wm);th=raw(A,wh);sh=BeautifulSoup(th,'html.parser');out={'parity':{},'section_conservation':[]}
for anchor,source in [('harness-raccordo-metriche-0310',M),('paper-sections-0315',P)]:
 ms=msection(tm,anchor);hs=sh.find(id=anchor);ma=atoms(BeautifulSoup(md(ms),'html.parser'));ha=atoms(hs)
 out['parity'][anchor]={'blocks_md':len(ma),'blocks_html':len(ha),'equal':ma==ha,'differences':list(difflib.unified_diff([str(x) for x in ma],[str(x) for x in ha])),'md_section_source_equal':ms==msection(raw(source,wm),anchor),'html_section_source_equal':str(hs)==hsection(raw(source,wh),anchor)}
for anchor in re.findall(r'<a id="([^"]+)"',raw(P,wm)):
 out['section_conservation'].append({'anchor':anchor,'md_equal':msection(tm,anchor)==msection(raw(P,wm),anchor),'html_equal':hsection(th,anchor)==hsection(raw(P,wh),anchor)})
# Exact content apart from the inserted section, status sentence, and HTML TOC.
source_m=raw(P,wm);source_h=raw(P,wh)
status_m=' il **raccordo delle metriche 03.9 → 03.10**, verificato sul solo delta, in [§4.10](#harness-raccordo-metriche-0310);'
status_h=' il <strong>raccordo delle metriche 03.9 → 03.10</strong>, verificato sul solo delta, in <a href="#harness-raccordo-metriche-0310">§4.10</a>;'
cm=tm.replace(msection(tm,'harness-raccordo-metriche-0310')+'\n\n','').replace(status_m,'')
start=th.index('<section id="harness-raccordo-metriche-0310">');end=th.index('<section id="schema-insight-0312">',start)
ch=(th[:start]+th[end:]).replace(status_h,'');toc='<li><a href="#harness-raccordo-metriche-0310"><span class="n">4.10</span>raccordo metriche 03.9 → 03.10</a></li>\n';ch=ch.replace(toc,'')
out['only_expected_insertions_vs_10582798']={'md':cm==source_m,'html':ch==source_h}
old=raw('04dee86^',wh)
needle='</code>→<code>';replacement='</code> → <code>'
s=old.index('<section id="harness-raccordo-metriche-0310">'); e=old.index('<section id="schema-insight-0312">',s)
segment=old[s:e]
out['04dee86_typography']={'mapping_sites':segment.count(needle),'added_U0020':len(th)-len(old),'only_three_arrow_spacing_replacements':old[:s]+segment.replace(needle,replacement)+old[e:]==th}
assert out['04dee86_typography']=={'mapping_sites':3,'added_U0020':6,'only_three_arrow_spacing_replacements':True}
# Raw unmodified metric section prior to the typography commit, copied from its source.
out['metric_html_before_typography_same_as_3360867']=hsection(old,'harness-raccordo-metriche-0310')==hsection(raw(M,wh),'harness-raccordo-metriche-0310')
out['order']=[norm(x) for x in sh.find_all('h3') if re.match(r'^4\.\d+',norm(x))]
ids=[x['id'] for x in sh.find_all(id=True)];out['html_ids']={'count':len(ids),'duplicates':[x for x,c in collections.Counter(ids).items() if c>1]}
def slug(t):return re.sub(r'[^\w\s-]','',t.lower().replace('`','').replace('*','')).replace(' ','-')
def target_ids(t,suffix):
 s=BeautifulSoup(t,'html.parser');ids=[x['id'] for x in s.find_all(id=True)]
 if suffix=='.md':
  seen=collections.Counter()
  for h in BeautifulSoup(md(t),'html.parser').find_all(re.compile('^h[1-6]$')):
   z=slug(norm(h));ids.append(z+('-'+str(seen[z]) if seen[z] else ''));seen[z]+=1
 return ids
cache={}
def links(p):
 t=raw(A,p);s=BeautifulSoup(md(t) if p.endswith('.md') else t,'html.parser');res=[]
 for x in s.find_all(True):
  for attr in ['href','src']:
   if not x.has_attr(attr):continue
   link=x[attr];u=urllib.parse.urlsplit(link)
   if u.scheme or u.netloc:continue
   dest=((W/p).parent/urllib.parse.unquote(u.path)).resolve() if u.path else W/p
   if not dest.is_relative_to(W):res.append({'source':p,'link':link,'status':'external_exists' if dest.exists() else 'external_missing'});continue
   pp=str(dest.relative_to(W));exists=subprocess.run(['git','-C',str(W),'cat-file','-e',A+':'+pp],stderr=subprocess.DEVNULL).returncode==0;status='ok' if exists else 'missing_path'
   if exists and u.fragment:
    if pp not in cache:cache[pp]=target_ids(raw(A,pp),dest.suffix)
    if urllib.parse.unquote(u.fragment) not in cache[pp]:status='missing_anchor'
   res.append({'source':p,'link':link,'status':status})
 return res
out['links']=[x for p in [wm,wh,'studio2/PROVENIENZA.md'] for x in links(p)]
out['conflict_markers']=re.findall(r'^(?:<<<<<<< |=======|>>>>>>> )',tm+th+raw(A,'studio2/PROVENIENZA.md'),re.M)
out['new_unmatched_atoms']=list(((collections.Counter(atoms(BeautifulSoup(md(tm),'html.parser')))-collections.Counter(atoms(sh)))-(collections.Counter(atoms(BeautifulSoup(md(raw(P,wm)),'html.parser')))-collections.Counter(atoms(BeautifulSoup(raw(P,wh),'html.parser'))))).elements())
for label,c in [('delta_P',P),('delta_M',M),('typography','04dee86^')]:
 (O/(label+'.patch')).write_bytes(git('diff',c,A,'--',wm,wh))
(O/'documents.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='links'},ensure_ascii=False,indent=2));print('links',len(out['links']),dict(collections.Counter(x['status'] for x in out['links'])))
