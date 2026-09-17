# Record pre-simulazione — verifica sintetica H3

Questo record precede qualunque simulazione della griglia ufficiale. La fonte normativa è
`../SPECIFICA_VERIFICA_SINTETICA_H3.md`, revisione 1, al commit `463ea32`.

Lo script congelato ha SHA-256
`847bc294948303a1d4763cc223893eeffc167c42f4e3b1540f73ed31feb53c5f`; il manifest dei 1.620
target ha SHA-256 `51711d6e3352296f704393601a3b94cc3e2966e7b728ad13da4b12cfe6dad74f` e classifica
1.596 scenari fattibili e 24 `INFEASIBLE` per lo stress ICC.

## Provenienza Tango

- tag piano congelato: `studio2-fase03-piano-statistico-frozen-001`;
- commit puntato dal tag: `11f504b2bf45a39c1bc4746952f50d58c5022743`;
- `PIANO_STATISTICO.md`: SHA-256
  `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`;
- `design_resolution.py`: blob Git `1691e3b10d8a421eee66d69a33f612eb96b432c1`, SHA-256
  `25a648b99fcb86f8111eaaf2f712183d6c3e0a0af5960b6b84c424c38fb1e613`;
- funzioni riusate senza modifica matematica: `tango_restricted_p21`, `tango_score_z`.

La seconda via di controllo massimizza numericamente la verosimiglianza vincolata in una
dimensione e confronta MLE e score. Comprende zero discordanti, tutti i discordanti da un solo
lato e casi interni. Controlla inoltre i valori di riferimento pubblicati nel piano per zero
discordanti e per 8 perdite su 64 al bordo.

## Runtime e consumo RNG congelati

- Python 3.13.9, NumPy 2.5.2, SciPy 1.17.1;
- `Generator(PCG64(SeedSequence([20260917, scenario_index])))`;
- batch di 10.000 repliche, 100.000 repliche per scenario fattibile;
- per ogni batch, nell'ordine: uniformi gate `(batch,8)`, uniformi indipendenti
  `(batch,8,8)`, uniformi condivise `(batch,8)`; si consumano anche le uniformi non selezionate;
- checkpoint atomico dopo ogni batch con stato PCG64 e accumulatori; la ripresa richiede
  identità di SHA-256 di script, manifest e run lock.

## Test non ufficiali dichiarati

Tre scenari fuori griglia, 2.000 repliche ciascuno, seed separato `9917001`, verificano soltanto
codice, contabilità e finitezza. Non sono risultati scientifici e non entrano nel report.

Comando runtime congelato:

```bash
uv run --no-project --with numpy==2.5.2 --with scipy==1.17.1 python \
  studio2/fase03/protocollo_finale/verifica_sintetica_h3/run_verifica_sintetica_h3.py run
```
