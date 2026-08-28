#!/usr/bin/env python3
"""
TEP verbalizer v1 — trasforma una finestra di dati di processo in una
descrizione diagnostica TESTUALE, da dare in pasto a un agente FoT.

Principi di design (dettati dall'analisi esplorativa):
  1. Confronto sempre rispetto a una BASELINE normale (media/std per variabile).
  2. Distinguo due tipi di anomalia:
       - SPOSTAMENTO di media  -> "il livello si e' spostato" (gradino/deriva)
       - DESTABILIZZAZIONE      -> "oscilla molto piu' del normale" (varianza)
     perche' alcuni guasti (es. F10) NON spostano la media ma solo la varianza.
  3. Normalizzo tutto in "sigma" (deviazioni standard del normale), cosi'
     variabili quasi-nulle non generano falsi segnali percentuali.
  4. Descrivo per FINESTRE temporali, cosi' l'onset emerge dal testo.
  5. NON nomino MAI il tipo di guasto: la diagnosi e' cio' che l'agente
     deve dedurre. L'output e' solo la descrizione del sintomo.

Uso come libreria:
    from tep_verbalize import verbalize_case
    testo = verbalize_case(df_finestra_o_file, baseline_mean, baseline_std)

Uso da riga di comando (demo sui file gia scaricati):
    python tep_verbalize.py tep_normal.csv tep_fault10.csv
"""

import sys
import pandas as pd

XMEAS = [f"XMEAS-{i}" for i in range(1, 42)]

# Soglie (in sigma / rapporto) per qualificare l'anomalia
SHIFT_SIGMA_THR = 3.0     # |mean - base| / std_base >= 3 -> spostamento notevole
STD_RATIO_THR = 2.0       # std / std_base >= 2       -> destabilizzazione
WINDOW_MIN = 300          # ampiezza finestra (~5 h a 1 campione/min)
TOP_K = 4                 # quante variabili anomale citare al massimo


def load_normal_baseline(path):
    """Carica il file normale e ritorna (mean, std) per le 41 XMEAS.

    Gestisce l'header fuorviante del file normale del repo (xmv-*)."""
    n = pd.read_csv(path)
    if list(n.columns[:1]) == ["Time"] and "XMEAS-1" not in n.columns:
        n.columns = ["Time"] + XMEAS
    return n[XMEAS].mean(), n[XMEAS].std()


def _load_case(df_or_path):
    if isinstance(df_or_path, str):
        d = pd.read_csv(df_or_path)
    else:
        d = df_or_path.copy()
    d = d.rename(columns={"Time (h)": "Time"})
    if "XMEAS-1" not in d.columns:                    # header normale fuorviante
        d.columns = ["Time"] + XMEAS + list(d.columns[42:])
    return d


def _sigma(x):
    """Descrittore verbale dell'intensita' in sigma."""
    if x >= 30:
        return "estremo"
    if x >= 10:
        return "forte"
    if x >= 5:
        return "marcato"
    return "moderato"


def _analyze_window(w, mean_b, std_b):
    """Ritorna liste ordinate di (var, valore) per shift e destabilizzazione."""
    shift, destab = [], []
    for c in XMEAS:
        sb = std_b[c]
        if sb <= 0:
            continue
        shift_sigma = abs(w[c].mean() - mean_b[c]) / sb
        std_ratio = w[c].std() / sb
        if shift_sigma >= SHIFT_SIGMA_THR:
            direction = "sopra" if w[c].mean() > mean_b[c] else "sotto"
            shift.append((c, round(shift_sigma, 1), direction))
        if std_ratio >= STD_RATIO_THR:
            destab.append((c, round(std_ratio, 1)))
    shift.sort(key=lambda t: -t[1])
    destab.sort(key=lambda t: -t[1])
    return shift, destab


def verbalize_case(df_or_path, mean_b, std_b, window_min=WINDOW_MIN):
    """Produce la descrizione diagnostica testuale di un caso.

    Scorre il caso per finestre, riporta la prima finestra in cui compare
    un'anomalia (onset) e la firma consolidata nell'ultima finestra."""
    d = _load_case(df_or_path)
    n = len(d)
    if n < window_min:
        # file piu' corto di una finestra: analisi come finestra unica,
        # altrimenti la lista di finestre resta vuota e un guasto verrebbe
        # silenziosamente riportato come 'nessuna deviazione'
        windows = [0]
        window_min = n
    else:
        windows = list(range(0, n - window_min + 1, window_min))

    onset_idx = None
    per_window = []
    for i in windows:
        w = d.iloc[i:i + window_min]
        shift, destab = _analyze_window(w, mean_b, std_b)
        anomalous = bool(shift or destab)
        if anomalous and onset_idx is None:
            onset_idx = i
        per_window.append((i, shift, destab))

    onset_h = None if onset_idx is None else onset_idx // 60

    # Firma consolidata su TUTTA la fase post-onset (non su una singola finestra):
    # per lo shift uso mean/std calcolati sull'intero segmento anomalo, cosi'
    # l'oscillazione non si traveste da spostamento di livello in una finestra.
    if onset_idx is not None:
        seg = d.iloc[onset_idx:]
        last_shift, last_destab = _analyze_window(seg, mean_b, std_b)
    else:
        last_shift, last_destab = [], []

    lines = []
    lines.append("Registrazione di processo (misure XMEAS), confronto con "
                 "funzionamento normale di riferimento.")

    if onset_h is None:
        lines.append("Nessuna deviazione significativa rilevata su alcuna "
                     "misura: il comportamento resta entro le oscillazioni "
                     "tipiche del funzionamento normale per tutta la durata.")
        return "\n".join(lines)

    if onset_h == 0:
        lines.append("L'anomalia e' presente fin dall'inizio della finestra osservata.")
    else:
        lines.append(f"Il comportamento e' normale nelle prime ore; una "
                     f"deviazione compare a partire da circa {onset_h} ore e "
                     f"persiste fino alla fine.")

    if last_shift:
        parts = []
        for c, val, direction in last_shift[:TOP_K]:
            parts.append(f"{c} spostata {direction} del livello normale "
                         f"({_sigma(val)}, ~{val} deviazioni standard)")
        lines.append("Spostamento del livello medio su: " + "; ".join(parts) + ".")
    else:
        lines.append("Nessuno spostamento rilevante del livello medio delle misure.")

    if last_destab:
        parts = []
        for c, val in last_destab[:TOP_K]:
            parts.append(f"{c} (ampiezza ~{val}x il normale)")
        lines.append("Aumento dell'oscillazione (varianza) su: "
                     + "; ".join(parts) + ".")
    else:
        lines.append("Nessun aumento rilevante dell'oscillazione delle misure.")

    # dominanza: la misura piu' anomala sovrasta le altre o e' parte di un gruppo?
    # (discrimina firme 'a leader' da firme 'a gruppo compatto')
    dom_lines = []
    if len(last_shift) >= 2 and last_shift[1][1] > 0:
        r = last_shift[0][1] / last_shift[1][1]
        if r >= 3:
            dom_lines.append(f"Nello spostamento, {last_shift[0][0]} sovrasta "
                             f"nettamente tutte le altre (~{r:.0f} volte piu' "
                             f"intensa della seconda).")
        elif r <= 1.5:
            dom_lines.append("Nello spostamento, le misure piu' colpite hanno "
                             "intensita' simile tra loro: un gruppo compatto, "
                             "senza una misura dominante.")
    if len(last_destab) >= 2 and last_destab[1][1] > 0:
        r = last_destab[0][1] / last_destab[1][1]
        if r >= 3:
            dom_lines.append(f"Nell'oscillazione, {last_destab[0][0]} sovrasta "
                             f"nettamente le altre (~{r:.0f} volte la seconda).")
        elif r <= 1.5:
            dom_lines.append("Nell'oscillazione, le misure piu' colpite hanno "
                             "ampiezza simile tra loro, senza una dominante.")
    lines.extend(dom_lines)

    # quale effetto prevale: confronto l'intensita' massima dei due tipi
    max_shift = last_shift[0][1] if last_shift else 0.0
    max_destab = last_destab[0][1] if last_destab else 0.0
    if max_destab >= 2 * max(max_shift, 1e-9):
        lines.append("Effetto prevalente: l'INSTABILITA' (oscillazione) domina "
                     "nettamente sullo spostamento di livello.")
    elif max_shift >= 2 * max(max_destab, 1e-9):
        lines.append("Effetto prevalente: lo SPOSTAMENTO di livello domina "
                     "nettamente sull'oscillazione.")
    else:
        lines.append("Effetto prevalente: spostamento di livello e oscillazione "
                     "sono entrambi presenti e di intensita' confrontabile.")

    # sintesi qualitativa del "carattere" della firma
    n_shift, n_destab = len(last_shift), len(last_destab)
    if n_destab >= 10 or n_shift >= 8:
        character = ("Molte misure risultano coinvolte simultaneamente: "
                     "l'anomalia ha carattere diffuso sull'intero processo.")
    elif n_shift == 0 and n_destab <= 2:
        character = ("Poche misure coinvolte e senza spostamento del livello: "
                     "l'anomalia si manifesta soprattutto come instabilita' "
                     "localizzata.")
    else:
        character = ("L'anomalia coinvolge un numero limitato di misure, "
                     "con una firma localizzata e riconoscibile.")
    lines.append(character)

    return "\n".join(lines)


DIAGNOSTIC_PROMPT_TEMPLATE = """\
Sei un ingegnere di processo. Ti viene fornita la descrizione del comportamento
di un impianto chimico (processo Tennessee Eastman), ottenuta confrontando le
misure con il funzionamento normale.

Il comportamento appartiene a UNA di queste categorie:
- Normale: nessuna deviazione significativa su alcuna misura.
- Guasto A: UNA misura ha uno spostamento di livello estremo che SOVRASTA
  nettamente tutte le altre (molte volte piu' intensa della seconda); altre
  misure sono coinvolte, ma con intensita' molto minore. Lo spostamento di
  livello e' l'effetto dominante.
- Guasto B: UNA SOLA misura diventa instabile e oscilla molto; il suo livello
  medio si sposta poco e il resto del processo resta tranquillo. L'oscillazione
  e' l'effetto dominante e la firma e' localizzata.
- Guasto C: un GRUPPO di misure (tre o piu') mostra INSIEME spostamenti estremi
  E oscillazioni fortissime, con intensita' simili tra loro (nessuna misura
  sovrasta le altre). Spostamento e oscillazione sono entrambi molto forti.
- Guasto D: MOLTE misure oscillano piu' del normale (instabilita' diffusa
  sull'intero processo), ma gli spostamenti di livello restano modesti e
  NESSUNA misura singola sovrasta le altre. L'oscillazione domina, ma in modo
  diffuso, non localizzato.

Suggerimento: per distinguere le categorie considera tre aspetti:
(1) quante misure sono coinvolte (una sola / un gruppo / molte),
(2) se prevale lo spostamento di livello o l'oscillazione,
(3) se esiste UNA misura che sovrasta nettamente le altre oppure no.

Descrizione osservata:
---
{description}
---

Ragiona passo per passo sui tre aspetti indicati, poi indica la categoria
piu' probabile e spiega perche'.
"""


def build_prompt(description):
    """Avvolge la descrizione in un prompt diagnostico con le classi mascherate."""
    return DIAGNOSTIC_PROMPT_TEMPLATE.format(description=description)


def _demo(normal_path, case_path):
    mean_b, std_b = load_normal_baseline(normal_path)
    desc = verbalize_case(case_path, mean_b, std_b)
    print("=" * 70)
    print("DESCRIZIONE VERBALIZZATA:\n")
    print(desc)
    print("\n" + "=" * 70)
    print("PROMPT COMPLETO PER L'AGENTE FoT:\n")
    print(build_prompt(desc))


if __name__ == "__main__":
    if len(sys.argv) == 3:
        _demo(sys.argv[1], sys.argv[2])
    else:
        print("Uso: python tep_verbalize.py <normal.csv> <case.csv>")
        print("Esempio: python tep_verbalize.py tep_normal.csv tep_fault10.csv")
