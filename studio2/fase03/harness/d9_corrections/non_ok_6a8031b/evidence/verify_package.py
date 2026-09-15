"""Read-only integrity verification of the delivered local review package."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent.parent
manifest=json.loads((root/'MANIFEST.json').read_text())
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
for item in manifest['files']:
 p=root/item['path']
 assert p.is_file() and p.stat().st_size==item['bytes'] and digest(p)==item['sha256'],item['path']
cert=json.loads((root/'CONSEGNA.json').read_text())
for item in [cert['report'],cert['manifest']]:
 p=root/item['path'];assert p.stat().st_size==item['bytes'] and digest(p)==item['sha256']
print(f"Verified {len(manifest['files'])} files and delivery certificate")
