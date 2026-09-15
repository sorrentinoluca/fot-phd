"""Generate D04 field/state/entry observations; no runtime imports or fixture writes."""
from pathlib import Path
import argparse
import hashlib
import json

p = argparse.ArgumentParser()
p.add_argument('--harness-dir', type=Path, required=True)
p.add_argument('--checks-dir', type=Path, required=True)
p.add_argument('--output-dir', type=Path, required=True)
a = p.parse_args()
contract_path = a.harness_dir / 'D04_DECISION_CONTRACT.json'
contract = json.loads(contract_path.read_text())
red = json.loads((a.checks_dir / 'red_contract.json').read_text())
green = json.loads((a.checks_dir / 'green_contract.json').read_text())
assert (red['tests'], len(red['failures']), len(red['errors'])) == (8, 240, 0)
assert (green['tests'], len(green['failures']), len(green['errors'])) == (8, 0, 0)
keys = ['stage', 'role', 'status', 'entry', 'mutation']
key = lambda row: tuple(row[k] for k in keys)
expected = {(stage, role, status, entry, value)
            for stage, roles in contract['stages'].items()
            for role in roles for status in contract['statuses']
            for entry in contract['entry_points']
            for value in contract['quota_values'] if value != role}
before = {key(row): row for row in red['observations']['quota_matrix']}
after = {key(row): row for row in green['observations']['quota_matrix']}
assert set(before) == set(after) == expected
assert len(expected) == 216
rows = []
for identity in sorted(expected):
    old, new = before[identity], after[identity]
    assert not old['refused'] and new['refused'] and new['unchanged']
    rows.append(dict(zip(keys, identity), before_refused=old['refused'], after_refused=new['refused'], after_unchanged=new['unchanged']))
deps = green['observations']['role_dependencies']
assert len(deps) == len(contract['role_dependencies']) * len(contract['entry_points'])
assert all(row['refused'] and row['unchanged'] for row in deps)
out = dict(contract_sha256=hashlib.sha256(contract_path.read_bytes()).hexdigest(),
           source='D04_DECISION_CONTRACT.json + red_contract.json + green_contract.json',
           tests=8, red_assertion_failures=240, green_failures=0, setup_errors=0,
           quota_cases=len(rows), positive_controls=72, quota_matrix=rows,
           role_dependency_cases=deps, other_observations={k: v for k, v in green['observations'].items()
                                                       if k not in {'quota_matrix', 'role_dependencies'}},
           limits=contract['coverage_limit'])
a.output_dir.mkdir(parents=True, exist_ok=True)
(a.output_dir / 'MATRICE_D04_DECISIONI.json').write_text(json.dumps(out, indent=2) + '\n')
lines = ['# D04 — matrice generata delle decisioni negli stadi aperti', '',
         'Fonte: D04_DECISION_CONTRACT.json e osservazioni degli stessi test su 23859a2 e sul corretto.', '',
         '**8 metodi; 240 assertion fallite sul respinto, zero sul corretto; zero errori di setup.**',
         'I sottocasi non sono difetti distinti né metodi aggiuntivi.', '',
         '216 mutazioni quota = 9 ruoli/stadi × 4 stati × 2 ingressi × 3 valori errati.',
         'Ogni coppia stato/ingresso ha prima un controllo positivo: 72 complessivi.',
         'Altri 14 sottocasi alterano i campi da cui dipende il ruolo; tutti rifiutati senza scritture.',
         'Quote e valori ammissibili non sono cambiati. Snapshot resta diagnostico, non autorizzante.', '',
         '| Stadio | Ruolo | Stato | Ingresso | Quota alterata | 23859a2 | Corretto | DB invariato |',
         '| --- | --- | --- | --- | --- | --- | --- | --- |']
for row in rows:
    lines.append('| ' + ' | '.join(str(row[k]) for k in keys) + ' | ACCETTA | RIFIUTA | sì |')
lines += ['', '## Campi da cui dipende il ruolo', '', '| Campo | Ingresso | Rifiuto e DB invariato |', '| --- | --- | --- |']
for row in deps:
    lines.append(f"| {row['field']} | {row['entry']} | sì |")
lines += ['', '## Altre prove e limiti', '',
          'Ottavo retry senza rinuncia, guasto dopo controllo sulla stessa istanza e dopo restart;',
          'triplette senza consumo parziale; lock con scrittore reale e altro stadio aperto;',
          'rinuncia lecita fino a 15 trasporti e rifiuto del sedicesimo;',
          'runner e CLI con zero client/server/nuovi invii, output e database invariati.', '',
          contract['coverage_limit'], '',
          'Il guardiano dei campi D03 rimane separato e immutato. La nuova matrice aggiunge',
          'la dimensione delle decisioni negli stadi aperti; non prova ogni combinazione futura.', '']
(a.output_dir / 'MATRICE_D04_DECISIONI.md').write_text('\n'.join(lines))
print(json.dumps(dict(quota_cases=len(rows), role_dependencies=len(deps), tests=8, red_failures=240, green_failures=0)))
