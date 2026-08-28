#!/usr/bin/env python3
"""
TEP — download e caratterizzazione dei guasti candidati.

Scopo: capire quali guasti hanno "firme" diagnostiche distinguibili e
complementari, per scegliere le classi del task FoT. Per ogni guasto
calcola, rispetto al file normale di riferimento:
  - variabili con SPOSTAMENTO di media (firma "a gradino/deriva")
  - variabili con DESTABILIZZAZIONE (rapporto di std elevato → oscillazione)
  - ONSET approssimativo del guasto (prima finestra in cui la firma compare)

Uso:
    python tep_characterize.py

Requisiti: pandas, openpyxl  (pip install pandas openpyxl)
"""

import io
import os
import urllib.request

import pandas as pd

BASE = "https://github.com/mv-per/tennessee-eastman-dataset/raw/main/simulations/mode_1/"
CACHE_DIR = "tep_cache"          # i file scaricati vengono salvati qui e riusati


def fetch(rel_path):
    """Scarica un file dal repo (con user-agent) e lo mette in cache locale.

    Ritorna il percorso locale del file .xlsx. Se gia presente in cache,
    non riscarica. Serve un user-agent esplicito, altrimenti GitHub risponde 403.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    local = os.path.join(CACHE_DIR, os.path.basename(rel_path))
    if os.path.exists(local):
        return local
    url = BASE + rel_path
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    with open(local, "wb") as fh:
        fh.write(data)
    return local
NORMAL_FILE = "mode1_normal_50.xlsx"
FAULTS = [1, 8, 10, 13]          # candidati: gradino / composizione / oscillazione / deriva
BATCH = 1                        # un batch basta per la caratterizzazione
WINDOW_MIN = 300                 # ampiezza finestra in righe (~5 h a 1 min/campione)

XMEAS = [f"XMEAS-{i}" for i in range(1, 42)]   # le 41 misure di processo

# Soglie per dichiarare "anomala" una variabile in una finestra
STD_RATIO_THR = 2.0     # std_guasto / std_normale >= 2  -> destabilizzazione
MEAN_SHIFT_THR = 3.0    # |mean_guasto - mean_normale| / std_normale >= 3 sigma -> shift


def load_normal():
    """Carica il normale e normalizza le colonne a XMEAS-1..41.

    Nota: nel repo il file normale ha header fuorviante (xmv-*), ma i valori
    sono le 41 misure di processo. Le rinominiamo per allinearle ai file guasto.
    """
    n = pd.read_excel(fetch(NORMAL_FILE))
    n.columns = ["Time"] + XMEAS
    return n


def load_fault(k):
    f = pd.read_excel(fetch(f"faults/mode1_{k}_{BATCH}.xlsx"))
    # i file guasto hanno 'Time (h)' + XMEAS-1..41 + XMV-1..12; teniamo le XMEAS
    f = f.rename(columns={"Time (h)": "Time"})
    return f


def baseline_stats(n):
    """Media e std di riferimento (intero file normale) per ogni XMEAS."""
    return n[XMEAS].mean(), n[XMEAS].std()


def characterize(f, mean_n, std_n):
    """Restituisce (shift_vars, destab_vars) sull'intero file guasto."""
    shift, destab = [], []
    for c in XMEAS:
        sn = std_n[c]
        if sn <= 0:
            continue
        mean_shift_sigma = abs(f[c].mean() - mean_n[c]) / sn
        std_ratio = f[c].std() / sn
        if mean_shift_sigma >= MEAN_SHIFT_THR:
            shift.append((c, round(mean_shift_sigma, 1)))
        if std_ratio >= STD_RATIO_THR:
            destab.append((c, round(std_ratio, 1)))
    shift.sort(key=lambda x: -x[1])
    destab.sort(key=lambda x: -x[1])
    return shift, destab


def find_onset(f, n, var, kind):
    """Prima finestra (in ore) in cui la firma della variabile compare.

    kind='destab': confronta std di finestra vs std normale di finestra.
    kind='shift' : confronta mean di finestra vs baseline normale in sigma.
    """
    mean_n_all = n[var].mean()
    std_n_all = n[var].std()
    for i in range(0, len(f) - WINDOW_MIN + 1, WINDOW_MIN):
        wf = f[var].iloc[i:i + WINDOW_MIN]
        wn = n[var].iloc[i:i + WINDOW_MIN]
        if kind == "destab":
            if wn.std() > 0 and wf.std() / wn.std() >= STD_RATIO_THR:
                return i // 60
        else:
            if std_n_all > 0 and abs(wf.mean() - mean_n_all) / std_n_all >= MEAN_SHIFT_THR:
                return i // 60
    return None


def main():
    print("Scarico il file normale di riferimento...")
    n = load_normal()
    mean_n, std_n = baseline_stats(n)
    print(f"  normale: {n.shape[0]} righe, {len(XMEAS)} misure\n")

    summary = []
    for k in FAULTS:
        print(f"=== Guasto {k} (batch {BATCH}) ===")
        try:
            f = load_fault(k)
        except Exception as e:
            print(f"  ERRORE nel caricamento: {e}\n")
            continue

        shift, destab = characterize(f, mean_n, std_n)

        # firma dominante e onset
        dominant = None
        if destab and (not shift or destab[0][1] >= shift[0][1]):
            var, val = destab[0]
            onset = find_onset(f, n, var, "destab")
            dominant = ("destabilizzazione", var, val, onset)
        elif shift:
            var, val = shift[0]
            onset = find_onset(f, n, var, "shift")
            dominant = ("spostamento medio", var, val, onset)

        print(f"  variabili con shift di media (>= {MEAN_SHIFT_THR}sigma): "
              f"{shift[:5] if shift else 'nessuna'}")
        print(f"  variabili destabilizzate (std ratio >= {STD_RATIO_THR}): "
              f"{destab[:5] if destab else 'nessuna'}")
        if dominant:
            tipo, var, val, onset = dominant
            onset_s = f"~{onset}h" if onset is not None else "n/d"
            print(f"  --> firma dominante: {tipo} su {var} (intensita {val}), onset {onset_s}")
        else:
            print("  --> nessuna firma netta (guasto 'difficile' o ben compensato)")
        print()

        summary.append({
            "fault": k,
            "n_shift_vars": len(shift),
            "n_destab_vars": len(destab),
            "dominant_type": dominant[0] if dominant else "nessuna",
            "dominant_var": dominant[1] if dominant else "-",
            "onset_h": dominant[3] if dominant else None,
        })

    print("=" * 60)
    print("RIEPILOGO (per scegliere classi complementari):")
    print(pd.DataFrame(summary).to_string(index=False))
    print()
    print("Criterio di scelta: preferire guasti con firme DIVERSE tra loro")
    print("(alcuni 'shift', alcuni 'destabilizzazione') e onset distinguibili,")
    print("cosi la insight library FoT ha varieta diagnostica da distillare.")


if __name__ == "__main__":
    main()
