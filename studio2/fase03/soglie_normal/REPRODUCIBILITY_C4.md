# Riproducibilità del completamento C4

Questo file rende il calcolo C4 riproducibile senza dipendere dal venv esterno usato nella
prima esecuzione. Non definisce una nuova analisi e non modifica soglia, score o risultato.

## Ambiente di riferimento

- CPython 3.11.5
- macOS 26.6.2 x86_64
- dipendenze Python fissate in `requirements-c4.txt`

L’ambiente e le versioni dell’esecuzione originale restano registrati anche in
`THRESHOLD_UNCERTAINTY.json`. Versioni o architetture diverse possono cambiare le ultime cifre
di somme e funzioni speciali; il verbale indipendente già quantifica questi scarti come non
sostanziali.

## Riproduzione

Da radice del repository, con un interprete CPython 3.11.5 disponibile:

```bash
c4_tmp="$(mktemp -d)"
python3.11 -m venv "$c4_tmp/venv"
"$c4_tmp/venv/bin/python" -m pip install -r studio2/fase03/soglie_normal/requirements-c4.txt
PYTHONDONTWRITEBYTECODE=1 "$c4_tmp/venv/bin/python" \
  studio2/fase03/soglie_normal/complete_threshold_uncertainty.py \
  --output "$c4_tmp/THRESHOLD_UNCERTAINTY.json"
PYTHONDONTWRITEBYTECODE=1 "$c4_tmp/venv/bin/python" -m pytest -p no:cacheprovider \
  studio2/fase03/soglie_normal/tests -q
```

Lo script verifica prima e dopo il calcolo le impronte degli input immutabili e rifiuta di
sovrascrivere un output esistente. L’output rigenerato usa una nuova marca temporale e registra
l’ambiente corrente; questi campi non devono essere confusi con i valori scientifici. Per il
confronto numerico valgono `THRESHOLD_UNCERTAINTY.json`, i test e i verbali conservati nella
cartella della sotto-fase.

Il rollout integrale dell’esecutore non è richiesto per riprodurre C4. I suoi soli metadati
pertinenti sono trascritti in `evidence/EXECUTOR_IDENTITY.json`.
