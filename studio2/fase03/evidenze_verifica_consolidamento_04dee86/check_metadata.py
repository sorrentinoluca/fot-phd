from pathlib import Path
import json
O=Path(__file__).parent;root=Path('/Users/luker/.codex/sessions/2026/09/14');out={}
for role,name,lines in [('reviewer','rollout-2026-09-14T19-06-23-01a0a0e2-5a0b-7bc3-a111-b41f24734216.jsonl',[]),('executor_R1_R2','rollout-2026-09-14T19-07-56-01a0a0e3-c3bd-7523-90ca-b5f28a40461f.jsonl',[1,8,421,460,463]),('executor_consolidation','rollout-2026-09-14T18-22-18-01a0a0b9-fc72-79b1-81b4-a4d5daa38f94.jsonl',[1,466,569,572,873,876])]:
 p=root/name;allrows=[json.loads(l) for l in p.open()];rows=[]
 if role=='reviewer':lines=[1,max(i for i,d in enumerate(allrows,1) if d['type']=='turn_context')]
 for i in lines:
  d=allrows[i-1];v=d.get('payload',{});row={'path':str(p),'line':i,'timestamp':d.get('timestamp'),'type':d['type'],'payload_type':v.get('type')}
  if d['type']=='session_meta':row.update({k:v.get(k) for k in ['id','session_id','model_provider','cwd','originator']})
  elif d['type']=='turn_context':row.update({k:v.get(k) for k in ['model','effort','cwd']})
  elif v.get('type') in ['custom_tool_call','function_call']:row.update({'call_id':v.get('call_id'),'name':v.get('name'),'input':v.get('input',v.get('arguments'))})
  elif v.get('type') in ['custom_tool_call_output','function_call_output']:row.update({'call_id':v.get('call_id'),'output':v.get('output')})
  rows.append(row)
 out[role]=rows
# Only exact project linkage from the named Claude index; no session transcript is read.
p=Path('/Users/luker/Library/Application Support/Claude/local-agent-mode-sessions/19642685-93ae-4cdf-a4eb-e247e2be2c6f/7b60e72c-a2c7-4177-9ab4-ee4492b37b9f/remote-session-spaces.json')
d=json.loads(p.read_text());hits=[]
def walk(x,path='$'):
 if isinstance(x,dict):
  for k,v in x.items():
   if '01CHTctYBYq1nnbumDuHrCsC' in k or (not isinstance(v,(dict,list)) and '01CHTctYBYq1nnbumDuHrCsC' in str(v)):hits.append({'json_path':path+'.'+k,'value':v})
   else:walk(v,path+'.'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,path+'['+str(i)+']')
walk(d);out['Claude_D_index']={'path':str(p),'exact_session_matches':hits}
(O/'metadata.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
for k,rows in out.items():
 if isinstance(rows,list):print(k,[{x:r.get(x) for x in ['line','timestamp','type','payload_type','model','effort','id','model_provider','call_id']} for r in rows])
 else:print(k,rows)
