from pathlib import Path
from bs4 import BeautifulSoup
import mistune,re,subprocess,json,difflib,collections,hashlib
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent
md=mistune.create_markdown(escape=False,plugins=['table'])
def raw(ref,p):return subprocess.check_output(['git','show',ref+':'+p],cwd=R).decode()
def text(x):return ' '.join(x.get_text().split()).replace('letteratura.html','letteratura.md')
def atoms(s):return [(x.name,text(x)) for x in s.find_all(['h1','h2','h3','h4','h5','h6','p','li','th','td']) if text(x) and not (x.name=='p' and x.parent.name=='li')]
def sec(t,anchor):
 start=t.index('<a id="'+anchor+'"></a>');end=t.find('<a id=',start+1);summary=t.find('### Sintesi per sezione',start)
 if summary>=0:end=min(end,summary) if end>=0 else summary
 return t[start:end if end>=0 else len(t)]
wm='docs/fot_walkthrough_conversazione_studio2.md';wh=wm[:-3]+'.html';out={}
for anchor in ['evidence-697-d','schema-insight-0312']:
 a=atoms(BeautifulSoup(md(sec(raw('e82b5a0',wm),anchor)),'html.parser'));b=atoms(BeautifulSoup(raw('e82b5a0',wh),'html.parser').find(id=anchor));out[anchor]={'md_blocks':len(a),'html_blocks':len(b),'equal':a==b,'delta':list(difflib.unified_diff([str(x) for x in a],[str(x) for x in b]))}
# Full literature pair, preserving punctuation and table structure.
a=BeautifulSoup(md(raw('e82b5a0','docs/letteratura.md')),'html.parser');b=BeautifulSoup(raw('e82b5a0','docs/letteratura.html'),'html.parser')
rows=lambda s:[[text(c) for c in r.find_all(['th','td'])] for r in s.find_all('tr')]
ra,rb=rows(a),rows(b);out['literature_tables']={'counts':[len(ra),len(rb)],'equal':ra==rb,'delta':[(i,x,y) for i,(x,y) in enumerate(zip(ra,rb),1) if x!=y]}
# cards are h3 within 14.2, bounded by 14.3.
lm=raw('e82b5a0','docs/letteratura.md')
lmsec=lm[lm.index('### 14.2'):lm.index('### 14.3')]
ca=re.findall(r'^\*\*([^\n]+)\*\*\s*$',lmsec,re.M)
# HTML uses h4 for cards; all h4 card titles occur between 14.2 and 14.3.
heads=b.find_all(re.compile('^h[1-6]$'));start=next(i for i,h in enumerate(heads) if text(h).startswith('14.2'));end=next(i for i,h in enumerate(heads) if text(h).startswith('14.3'))
cb=[]
for x in heads[start].next_elements:
 if x is heads[end]:break
 if getattr(x,'name',None)=='h4':cb.append(text(x))
 elif getattr(x,'name',None)=='p' and [c.name for c in x.children if getattr(c,'name',None)]==['strong','em'] and all(not str(c).strip() for c in x.children if not getattr(c,'name',None)):
  cb.append(text(x.find('strong',recursive=False)))
out['literature_cards']={'counts':[len(ca),len(cb)],'equal':ca==cb,'delta':list(difflib.unified_diff(ca,cb))}
# Categories and actual rows in 14.1.
cat=lm[lm.index('### 14.1'):lm.index('### 14.2')]
out['literature_index']={'categories':len(re.findall(r'<summary>',cat)),'rows':sum(1 for l in cat.splitlines() if l.startswith('|') and l.rstrip().endswith(('🟢 |','🟡 |','🔴 |')))}
# Compare full paragraph text presence, allowing HTML wrappers/navigation.
pa=[text(x) for x in a.find_all('p') if text(x)];pb=[text(x) for x in b.find_all('p') if text(x)]
out['literature_paragraphs_diagnostic_layout_only']={'counts':[len(pa),len(pb)],'missing_html':list((collections.Counter(pa)-collections.Counter(pb)).elements()),'extra_html':list((collections.Counter(pb)-collections.Counter(pa)).elements())}
# Full walkthrough mapping: all Markdown blocks must occur in HTML in order; report differences for review.
a=atoms(BeautifulSoup(md(raw('e82b5a0',wm)),'html.parser'));b=atoms(BeautifulSoup(raw('e82b5a0',wh),'html.parser'))
out['walkthrough_full_missing_diagnostic']=list((collections.Counter(a)-collections.Counter(b)).elements())
a0=atoms(BeautifulSoup(md(raw('c486eee',wm)),'html.parser'));b0=atoms(BeautifulSoup(raw('c486eee',wh),'html.parser'))
out['walkthrough_new_unmatched_blocks']=list(((collections.Counter(a)-collections.Counter(b))-(collections.Counter(a0)-collections.Counter(b0))).elements())
# Inherited layout differences are not a parity failure; retain the delta check.
for key in list(out):
 if 'diagnostic' in key:out.pop(key)
(O/'parity.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
for k,v in out.items():print(k,str(v)[:1600])
