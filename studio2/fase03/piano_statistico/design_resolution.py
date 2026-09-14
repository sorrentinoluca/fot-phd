#!/usr/bin/env python3
"""Risoluzione del disegno per il piano statistico della Fase 03 (sotto-fase 03.8).

Calcola, **senza alcun dato reale**, potenza e semiampiezza attese per le tre ipotesi
H1–H3 del piano §8.5 con 48 cluster (6 run per fault) e 64 cluster (8 run per fault):

* H1  B-LF > E-LF sui local-unseen   (superiorità, 7 osservazioni per cluster)
* H2  B-LF > A    sui local-unseen   (superiorità, 7 osservazioni per cluster)
* H3  B-LF non inferiore ad A sui local-seen, margine m (1 osservazione per cluster)

Due strade, che devono dare numeri coerenti:

1. **analitica** — errore standard della differenza appaiata fra proporzioni con
   effetto di disegno per i cluster, e potenza normale;
2. **simulazione su dati sintetici nulli** — esiti binari appaiati generati da un
   modello dichiarato, analizzati con il bootstrap a cluster stratificato per pseudolabel
   (8 strati, intervalli), con il test score di Tango (H3), con il test di Hoeffding sulla
   media delle medie di cluster (H1/H2, decisione primaria: valido per qualunque distribuzione
   limitata) e con il test di permutazione per inversione di segno (H1/H2, esatto solo sotto
   la nulla forte di scambiabilità), per misurare ampiezza dell'intervallo, potenza e
   **dimensione del test al bordo**, anche sotto una nulla debole asimmetrica.

I float del JSON sono arrotondati a 12 cifre decimali (`canonical`) perché l'impronta non
dipenda dall'ultima cifra di `erf`/`sqrt` della libreria matematica.

Guardia esplicita sui dati: builtins.open e io.open (anche pathlib) rifiutano
letture e modalità di aggiornamento durante main(). È una guardia contro letture
accidentali, non una sandbox per os.open, estensioni native o processi esterni.
Lo script scrive soltanto i due artefatti nella cartella di output.

Uso:
    python3 design_resolution.py --out . [--reps 400] [--boot 2000] [--seed 20260913]
    python3 design_resolution.py --quick      # griglia ridotta, per i test

Il modello generativo è dichiarato in `simulate_h3` e `simulate_h12`. I parametri di
scenario (tasso di discordanza d, correlazione intra-cluster rho, effetto vero) sono
ipotesi di progetto, non stime: non esiste alcun dato dello studio 2 da cui stimarli
prima dei run di test, ed è voluto.
"""

from __future__ import annotations

import argparse
import builtins
import io
import json
import math
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

import numpy as np

# --------------------------------------------------------------------------- guardia dati

FORBIDDEN_PATH_FRAGMENTS = (
    "fault_runs/runs",
    "soglie_normal/runs",
    "phase_b/",
    "evidence",
    "tep_exp3_v2",
    "icl/",
    "ablation/",
)


class DataAccessError(RuntimeError):
    """Sollevata se lo script prova a leggere un file: qui non servono dati."""


_ORIGINAL_OPEN = builtins.open
_ORIGINAL_IO_OPEN = io.open


def _guarded_open(file: Any, mode: str = "r", *args: Any, **kwargs: Any):  # type: ignore[no-untyped-def]
    text = str(file)
    if any(fragment in text.replace("\\", "/") for fragment in FORBIDDEN_PATH_FRAGMENTS):
        raise DataAccessError(f"accesso vietato a un percorso di dati: {text}")
    if "r" in mode or "+" in mode:
        raise DataAccessError(f"lettura di file non ammessa in questo script: {text}")
    return _ORIGINAL_OPEN(file, mode, *args, **kwargs)


def install_data_guard() -> None:
    """Blocca letture e update via builtins.open e io.open, incluso pathlib."""
    builtins.open = _guarded_open  # type: ignore[assignment]
    io.open = _guarded_open  # type: ignore[assignment]


def remove_data_guard() -> None:
    builtins.open = _ORIGINAL_OPEN  # type: ignore[assignment]
    io.open = _ORIGINAL_IO_OPEN  # type: ignore[assignment]


def assert_no_forbidden_argv(argv: list[str]) -> None:
    for token in argv:
        norm = token.replace("\\", "/")
        if any(fragment in norm for fragment in FORBIDDEN_PATH_FRAGMENTS):
            raise DataAccessError(f"argomento vietato: {token}")


# --------------------------------------------------------------------------- analitico

SQRT2 = math.sqrt(2.0)


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / SQRT2))


def norm_ppf(p: float) -> float:
    """Inversa della normale standard (Acklam), errore relativo < 1.2e-9."""
    if not 0.0 < p < 1.0:
        raise ValueError("p deve stare in (0, 1)")
    a = (-3.969683028665376e01, 2.209460984245205e02, -2.759285104469687e02,
         1.383577518672690e02, -3.066479806614716e01, 2.506628277459239e00)
    b = (-5.447609879822406e01, 1.615858368580409e02, -1.556989798598866e02,
         6.680131188771972e01, -1.328068155288572e01)
    c = (-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e00,
         -2.549732539343734e00, 4.374664141464968e00, 2.938163982698783e00)
    d = (7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e00,
         3.754408661907416e00)
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (
        ((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)


def se_paired_delta(n_clusters: int, discordance: float, obs_per_cluster: int = 1,
                    icc: float = 0.0) -> float:
    """Errore standard della differenza appaiata di accuratezza.

    Ogni osservazione contribuisce delta in {-1, 0, +1}; sotto l'ipotesi nulla
    Var(delta) = d, dove d è la probabilità di discordanza fra le due condizioni.
    Con k osservazioni per cluster e correlazione intra-cluster rho l'effetto di
    disegno è 1 + (k-1) rho (Kish).
    """
    if not 0.0 < discordance <= 1.0:
        raise ValueError("discordanza in (0, 1]")
    if not 0.0 <= icc <= 1.0:
        raise ValueError("icc in [0, 1]")
    design_effect = 1.0 + (obs_per_cluster - 1) * icc
    return math.sqrt(discordance * design_effect / (obs_per_cluster * n_clusters))


def power_one_sided(se: float, effect_above_bound: float, alpha: float = 0.05) -> float:
    """Potenza del test unilaterale: P(limite inferiore > bordo) se l'effetto vero
    sta `effect_above_bound` sopra il bordo (0 per superiorità, -m per non inferiorità)."""
    return norm_cdf(effect_above_bound / se - norm_ppf(1.0 - alpha))


def minimum_detectable(se: float, power: float = 0.80, alpha: float = 0.05) -> float:
    """Distanza minima dal bordo rilevabile con la potenza data."""
    return (norm_ppf(1.0 - alpha) + norm_ppf(power)) * se


def hoeffding_threshold(n_clusters: int, alpha: float = 0.05, range_width: float = 2.0) -> float:
    """Soglia del test di Hoeffding (1963) per la media di n variabili indipendenti limitate in un
    intervallo di ampiezza `range_width`: P(media - E[media] >= t) <= exp(-2 n t^2 / range^2).
    Le medie di cluster della differenza di accuratezza stanno in [-1, 1] (ampiezza 2). Rifiuto di
    H0: E[D] <= 0 se la media osservata è >= t; livello garantito alpha per **qualunque**
    distribuzione limitata, senza ipotesi di simmetria o di forma."""
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha in (0, 1)")
    return range_width * math.sqrt(math.log(1.0 / alpha) / (2.0 * n_clusters))


def hoeffding_power(se: float, effect: float, n_clusters: int, alpha: float = 0.05) -> float:
    """Potenza (approssimazione normale) del test di Hoeffding: P(media >= t) con media vera `effect`."""
    return norm_cdf((effect - hoeffding_threshold(n_clusters, alpha)) / se)


@dataclass
class AnalyticRow:
    """one_sided_bound_distance = z_(1-alpha) * SE.

    Il livello unilaterale è 1 - alpha_one_sided del payload JSON;
    two_sided_halfwidth_95 resta invece la semiampiezza bilaterale al 95%.
    """

    hypothesis: str
    n_clusters: int
    obs_per_cluster: int
    discordance: float
    icc: float
    margin_or_effect: float
    se: float
    one_sided_bound_distance: float
    two_sided_halfwidth_95: float
    power_at_null_or_effect: float
    mde_80: float
    hoeffding_threshold: float | None = None
    hoeffding_power: float | None = None
    hoeffding_mde_80: float | None = None
    hoeffding_mde_80_feasible: bool | None = None


def analytic_grid(n_clusters_list: tuple[int, ...], h3_discordance: tuple[float, ...],
                  h3_margins: tuple[float, ...], h12_discordance: tuple[float, ...],
                  h12_icc: tuple[float, ...], h12_effects: tuple[float, ...],
                  alpha: float = 0.05) -> list[AnalyticRow]:
    rows: list[AnalyticRow] = []
    z = norm_ppf(1.0 - alpha)
    z2 = norm_ppf(0.975)
    for n in n_clusters_list:
        for d in h3_discordance:
            se = se_paired_delta(n, d, 1, 0.0)
            for m in h3_margins:
                rows.append(AnalyticRow("H3", n, 1, d, 0.0, m, se, z * se, z2 * se,
                                        power_one_sided(se, m, alpha), minimum_detectable(se, alpha=alpha)))
        for d in h12_discordance:
            for icc in h12_icc:
                se = se_paired_delta(n, d, 7, icc)
                for eff in h12_effects:
                    if abs(eff) > d:
                        continue
                    mde_h = hoeffding_threshold(n, alpha) + norm_ppf(0.80) * se
                    rows.append(AnalyticRow("H1/H2", n, 7, d, icc, eff, se, z * se, z2 * se,
                                            power_one_sided(se, eff, alpha), minimum_detectable(se, alpha=alpha),
                                            hoeffding_threshold(n, alpha), hoeffding_power(se, eff, n, alpha),
                                            mde_h, mde_h <= d))
    return rows


# --------------------------------------------------------------------------- simulazione

N_STRATA = 8  # otto pseudolabel di fault; Normal non entra nella popolazione primaria
CHUNK = 25    # repliche Monte Carlo elaborate insieme (limite di memoria, non di risultato)


def stratified_cluster_bootstrap_quantiles(
    cluster_sums: np.ndarray, cluster_sizes: np.ndarray, boot: int, rng: np.random.Generator,
    probs: tuple[float, ...] = (0.05, 0.95),
) -> np.ndarray:
    """Bootstrap a cluster stratificato: `cluster_sums` ha forma (strati, cluster per strato)
    e contiene la somma dei delta del cluster; `cluster_sizes` le numerosità. Ricampiona con
    reinserimento i cluster **dentro** ogni strato, stessa numerosità dello strato, e
    restituisce i quantili della media dei delta sulle osservazioni ricampionate."""
    return stratified_cluster_bootstrap_quantiles_batch(
        cluster_sums[None, ...], cluster_sizes[None, ...], boot, rng, probs)[0]


def stratified_cluster_bootstrap_quantiles_batch(
    cluster_sums: np.ndarray, cluster_sizes: np.ndarray, boot: int, rng: np.random.Generator,
    probs: tuple[float, ...] = (0.05, 0.95),
) -> np.ndarray:
    """Versione vettoriale su più repliche: input di forma (repliche, strati, cluster per strato),
    output di forma (repliche, len(probs)). Stessa procedura di ricampionamento per replica."""
    reps, strata, per_stratum = cluster_sums.shape
    idx = rng.integers(0, per_stratum, size=(reps, boot, strata, per_stratum))
    sums = np.take_along_axis(np.broadcast_to(cluster_sums[:, None], idx.shape), idx, axis=3)
    sizes = np.take_along_axis(np.broadcast_to(cluster_sizes[:, None], idx.shape), idx, axis=3)
    means = sums.sum(axis=(2, 3)) / sizes.sum(axis=(2, 3))
    return np.quantile(means, probs, axis=1).T


def tango_restricted_p21(b: np.ndarray, c: np.ndarray, n: int, delta0: float) -> np.ndarray:
    """MLE vincolata di p21 = P(B errato, A corretto) sotto p12 - p21 = delta0 (Tango 1998).

    Radice positiva di 2N p21^2 - [(b+c) - delta0 (2N - b + c)] p21 - c delta0 (1 - delta0) = 0,
    con b = coppie (B corretto, A errato) e c = coppie (B errato, A corretto)."""
    A = 2.0 * n
    B = -(b + c) + delta0 * (2.0 * n - b + c)
    C = -c * delta0 * (1.0 - delta0)
    disc = np.maximum(B * B - 4.0 * A * C, 0.0)
    return (-B + np.sqrt(disc)) / (2.0 * A)


def tango_score_z(b: np.ndarray, c: np.ndarray, n: int, delta0: float) -> np.ndarray:
    """Statistica score di Tango per H0: p12 - p21 = delta0 su coppie indipendenti.
    Per la non inferiorità con margine m si pone delta0 = -m e si rifiuta se Z > z_(1-alpha)."""
    p21 = tango_restricted_p21(b, c, n, delta0)
    var = n * (2.0 * p21 + delta0 * (1.0 - delta0))
    var = np.where(var <= 0.0, np.nan, var)
    return (b - c - n * delta0) / np.sqrt(var)


def sign_flip_pvalues(cluster_means: np.ndarray, flips: int, rng: np.random.Generator) -> np.ndarray:
    """Test di permutazione per inversione di segno a livello di cluster (unilaterale, H1: media > 0).
    `cluster_means` ha forma (repliche, cluster). p = P(media permutata >= media osservata)."""
    reps, n = cluster_means.shape
    observed = cluster_means.mean(axis=1)
    signs = rng.choice(np.array([-1.0, 1.0]), size=(reps, flips, n))
    permuted = (cluster_means[:, None, :] * signs).mean(axis=2)
    return (1.0 + (permuted >= observed[:, None]).sum(axis=1)) / (flips + 1.0)


def sign_flip_exact_two_point(n: int, k: int, a: float, b: float) -> float:
    """p-value esatto del test di inversione di segno (unilaterale, media > 0) per un campione di
    n medie di cluster di cui k valgono `a` e n-k valgono `b`: enumera le 2^n inversioni per
    conteggi (j inversioni fra le `a`, i fra le `b`)."""
    observed = k * a + (n - k) * b
    total = 0
    for j in range(k + 1):
        for i in range(n - k + 1):
            s = (k - 2 * j) * a + (n - k - 2 * i) * b
            if s >= observed - 1e-12:
                total += math.comb(k, j) * math.comb(n - k, i)
    return total / 2.0 ** n


def weak_null_counterexample(n_clusters: int, alpha: float = 0.05,
                             a: float = 1.0 / 7.0, b: float = -1.0, prob_a: float = 7.0 / 8.0) -> dict[str, float]:
    """Errore di primo tipo esatto dei test di inversione di segno e di Hoeffding sotto una nulla **debole**
    asimmetrica: medie di cluster pari ad `a` con probabilità `prob_a` e a `b` altrimenti, con
    E[D] = prob_a·a + (1-prob_a)·b (= 0 per i valori di default: +1/7 con 7/8, -1 con 1/8).
    È il controesempio del secondo verbale di verifica: la nulla debole «media ≤ 0» non implica
    la simmetria dei segni, quindi il sign-flip non è di livello alpha su quella classe; il test di
    Hoeffding lo è, perché usa solo la limitatezza di D in [-1, 1]."""
    mean = prob_a * a + (1.0 - prob_a) * b
    size = 0.0
    size_h = 0.0
    threshold = hoeffding_threshold(n_clusters, alpha)
    for k in range(n_clusters + 1):
        pk = math.comb(n_clusters, k) * prob_a ** k * (1.0 - prob_a) ** (n_clusters - k)
        if pk < 1e-12:
            continue
        if sign_flip_exact_two_point(n_clusters, k, a, b) <= alpha:
            size += pk
        if (k * a + (n_clusters - k) * b) / n_clusters >= threshold - 1e-12:
            size_h += pk
    return {"n_clusters": n_clusters, "a": a, "b": b, "prob_a": prob_a, "mean_under_null": mean,
            "exact_size_sign_flip": size, "hoeffding_threshold": threshold,
            "exact_size_hoeffding": size_h}


def draw_paired_deltas(rng: np.random.Generator, size: tuple[int, ...], discordance: float,
                       effect: float) -> np.ndarray:
    """delta per osservazione: +1 con prob (d+eff)/2, -1 con prob (d-eff)/2, 0 altrimenti."""
    if abs(effect) > discordance:
        raise ValueError("|effetto| non può superare la discordanza")
    u = rng.random(size)
    p_plus = (discordance + effect) / 2.0
    p_minus = (discordance - effect) / 2.0
    return np.where(u < p_plus, 1, np.where(u < p_plus + p_minus, -1, 0)).astype(np.int8)


def simulate_h3(n_per_fault: int, discordance: float, true_delta: float, margin: float,
                reps: int, boot: int, seed: int, alpha: float = 0.05) -> dict[str, float]:
    """H3: una osservazione local-seen per cluster, 8 strati × n_per_fault cluster.
    Riporta il tasso con cui il quantile alpha del bootstrap supera -margin (intervallo, non
    decisione) e il tasso di rifiuto del test score di Tango, che è la decisione di H3."""
    rng = np.random.default_rng(seed)
    lows: list[np.ndarray] = []
    highs: list[np.ndarray] = []
    halfwidths_90: list[np.ndarray] = []
    tango: list[np.ndarray] = []
    n_pairs = N_STRATA * n_per_fault
    z_crit = norm_ppf(1.0 - alpha)
    for start in range(0, reps, CHUNK):
        chunk = min(CHUNK, reps - start)
        deltas = draw_paired_deltas(rng, (chunk, N_STRATA, n_per_fault), discordance, true_delta)
        sizes = np.ones(deltas.shape, dtype=np.int64)
        q = stratified_cluster_bootstrap_quantiles_batch(deltas.astype(np.int64), sizes, boot, rng,
                                                         (alpha, 1.0 - alpha, 0.05, 0.95))
        halfwidths_90.append((q[:, 3] - q[:, 2]) / 2.0)
        lows.append(q[:, 0])
        highs.append(q[:, 1])
        b = (deltas == 1).sum(axis=(1, 2)).astype(float)
        c = (deltas == -1).sum(axis=(1, 2)).astype(float)
        z = tango_score_z(b, c, n_pairs, -margin)
        tango.append(np.nan_to_num(z, nan=-np.inf) > z_crit)
    lower = np.concatenate(lows)
    upper = np.concatenate(highs)
    return {
        "rejection_rate": float((lower > -margin).mean()),
        "rejection_rate_tango": float(np.concatenate(tango).mean()),
        "mean_halfwidth_90": float(np.concatenate(halfwidths_90).mean()),
        "mean_lower_bound": float(lower.mean()),
    }


def simulate_h12(n_per_fault: int, discordance: float, true_delta: float, icc: float,
                 reps: int, boot: int, seed: int, obs_per_cluster: int = 7,
                 alpha: float = 0.05) -> dict[str, float]:
    """H1/H2: 7 osservazioni local-unseen per cluster. Correlazione intra-cluster per
    mescolanza: con probabilità icc le 7 osservazioni del cluster copiano un solo delta
    comune, altrimenti sono indipendenti; la correlazione fra due osservazioni dello stesso
    cluster è esattamente icc e la distribuzione marginale è invariata.
    Riporta il tasso con cui il quantile alpha del bootstrap supera 0 (intervallo, non decisione),
    il tasso di rifiuto del sign-flip (supplementare) e quello del test di Hoeffding, che è la
    decisione di H1/H2."""
    rng = np.random.default_rng(seed)
    lows: list[np.ndarray] = []
    highs: list[np.ndarray] = []
    halfwidths_90: list[np.ndarray] = []
    flips: list[np.ndarray] = []
    hoeff: list[np.ndarray] = []
    threshold = hoeffding_threshold(N_STRATA * n_per_fault, alpha)
    for start in range(0, reps, CHUNK):
        chunk = min(CHUNK, reps - start)
        shape = (chunk, N_STRATA, n_per_fault, obs_per_cluster)
        indep = draw_paired_deltas(rng, shape, discordance, true_delta)
        shared = draw_paired_deltas(rng, shape[:-1] + (1,), discordance, true_delta)
        use_shared = rng.random(shape[:-1] + (1,)) < icc
        deltas = np.where(use_shared, shared, indep)
        sums = deltas.sum(axis=3).astype(np.int64)
        sizes = np.full(sums.shape, obs_per_cluster, dtype=np.int64)
        q = stratified_cluster_bootstrap_quantiles_batch(sums, sizes, boot, rng, (alpha, 1.0 - alpha, 0.05, 0.95))
        halfwidths_90.append((q[:, 3] - q[:, 2]) / 2.0)
        lows.append(q[:, 0])
        highs.append(q[:, 1])
        cluster_means = (sums / obs_per_cluster).reshape(chunk, -1)
        flips.append(sign_flip_pvalues(cluster_means, boot, rng) <= alpha)
        hoeff.append(cluster_means.mean(axis=1) >= threshold)
    lower = np.concatenate(lows)
    upper = np.concatenate(highs)
    return {"rejection_rate": float((lower > 0.0).mean()),
            "rejection_rate_signflip": float(np.concatenate(flips).mean()),
            "rejection_rate_hoeffding": float(np.concatenate(hoeff).mean()),
            "hoeffding_threshold": threshold,
            "mean_halfwidth_90": float(np.concatenate(halfwidths_90).mean())}


# --------------------------------------------------------------------------- griglie

FULL_GRID: dict[str, Any] = {
    "n_per_fault": (6, 8),
    "h3_discordance": (0.05, 0.10, 0.20, 0.30),
    "h3_margins": (0.10, 0.125, 0.15),
    "h12_discordance": (0.30, 0.50, 0.80),
    "h12_icc": (0.0, 0.25, 0.50, 1.0),
    "h12_effects": (0.10, 0.20, 0.30, 0.50, 0.70),
}

QUICK_GRID: dict[str, Any] = {
    "n_per_fault": (6, 8),
    "h3_discordance": (0.10, 0.20),
    "h3_margins": (0.125,),
    "h12_discordance": (0.50,),
    "h12_icc": (0.0, 0.50),
    "h12_effects": (0.20,),
}


def run_simulations(grid: dict[str, Any], reps: int, boot: int, seed: int,
                    progress: Callable[[str], None] | None = None,
                    alpha: float = 0.05) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    counter = 0
    for n in grid["n_per_fault"]:
        for d in grid["h3_discordance"]:
            for m in grid["h3_margins"]:
                for label, true_delta in (("power_at_zero_delta", 0.0), ("size_at_margin", -m)):
                    if abs(true_delta) > d:
                        continue  # scenario impossibile: l'effetto non può superare la discordanza
                    counter += 1
                    res = simulate_h3(n, d, true_delta, m, reps, boot, seed + counter, alpha=alpha)
                    out.append({"hypothesis": "H3", "n_per_fault": n, "n_clusters": N_STRATA * n,
                                "discordance": d, "margin": m, "scenario": label,
                                "true_delta": true_delta, **res})
                    if progress:
                        progress(f"H3 n={n} d={d} m={m} {label}: {res}")
        for d in grid["h12_discordance"]:
            for icc in grid["h12_icc"]:
                for label, eff in [("size_at_zero_delta", 0.0)] + [
                        (f"power_at_delta_{e}", e) for e in grid["h12_effects"]]:
                    if eff > d:
                        continue
                    counter += 1
                    res = simulate_h12(n, d, eff, icc, reps, boot, seed + counter, alpha=alpha)
                    out.append({"hypothesis": "H1/H2", "n_per_fault": n, "n_clusters": N_STRATA * n,
                                "discordance": d, "icc": icc, "scenario": label,
                                "true_delta": eff, **res})
                    if progress:
                        progress(f"H1/H2 n={n} d={d} icc={icc} {label}: {res}")
    return out


FLOAT_DIGITS = 12


def canonical(obj: Any) -> Any:
    """Arrotonda ogni float a FLOAT_DIGITS cifre decimali prima della serializzazione, così che
    differenze di ultima cifra fra librerie matematiche (erf, sqrt) non cambino l'impronta del JSON."""
    if isinstance(obj, float):
        return round(obj, FLOAT_DIGITS)
    if isinstance(obj, dict):
        return {k: canonical(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [canonical(v) for v in obj]
    return obj


def markdown_tables(analytic: list[AnalyticRow], simulated: list[dict[str, Any]],
                    alpha: float = 0.05, reps: int = 400) -> str:
    lines = ["# Risoluzione del disegno — tabelle generate", "",
             "Generato da `design_resolution.py` su dati sintetici nulli; nessun dato reale.", "",
             f"Livello unilaterale α = {alpha:g}; limite unilaterale {(1-alpha)*100:g}%. "
             "Potenza e MDE analitici usano Var(δ)=d (approssimazione a varianza nulla); "
             "non sono potenze esatte di Tango o garanzie di potenza. Scenari |Δ|>d esclusi.", "",
             "## Analitico — H3 (local-seen, 1 osservazione per cluster)", "",
             "| cluster | d | m | SE | distanza del limite unilaterale | semiampiezza 95% bilaterale | potenza NI normale a δ=0 | m minimo normale (potenza 80%) |",
             "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for r in analytic:
        if r.hypothesis == "H3":
            lines.append(f"| {r.n_clusters} | {r.discordance:.2f} | {r.margin_or_effect:.3f} | {r.se:.4f} | "
                         f"{r.one_sided_bound_distance:.3f} | {r.two_sided_halfwidth_95:.3f} | "
                         f"{r.power_at_null_or_effect:.2f} | {r.mde_80:.3f} |")
    lines += ["", "## Analitico — H1/H2 (local-unseen, 7 osservazioni per cluster)", "",
              "«potenza» è quella di un test normale al livello α (riferimento); «soglia/potenza Hoeffding» "
              "è il test primario del piano per H1/H2: rifiuto se la media delle medie di cluster è ≥ soglia.", "",
              "MDE Hoeffding = soglia + z(0,80) SE; se supera d, l'80% non è raggiungibile "
              "nell'approssimazione. L'asterisco identifica tali valori non ammissibili.", "",
              "| cluster | d | rho | Δ | SE | distanza del limite unilaterale | potenza normale | MDE normale 80% | soglia Hoeffding | potenza Hoeffding | MDE Hoeffding 80% |",
              "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for r in analytic:
        if r.hypothesis != "H3":
            lines.append(f"| {r.n_clusters} | {r.discordance:.2f} | {r.icc:.2f} | {r.margin_or_effect:.2f} | "
                         f"{r.se:.4f} | {r.one_sided_bound_distance:.3f} | {r.power_at_null_or_effect:.2f} | "
                         f"{r.mde_80:.3f} | {r.hoeffding_threshold:.3f} | {r.hoeffding_power:.2f} | "
                         f"{r.hoeffding_mde_80:.3f}{'' if r.hoeffding_mde_80_feasible else '*'} |")
    lines += ["", "## Simulazione — bootstrap a cluster stratificato (8 strati)", "",
              f"Tasso di rifiuto «bootstrap»: quantile {alpha*100:g}% del bootstrap percentile sopra il bordo (riportato "
              "come intervallo, non usato come decisione). «Score/sign-flip»: per H3 il test score di Tango "
              "(1998) al bordo −m, che è la decisione di H3; per H1/H2 il test di permutazione per inversione "
              "di segno sulle medie di cluster, che è solo supplementare. «Hoeffding» è la decisione di H1/H2. "
              "Negli scenari `size_*` il tasso di rifiuto è "
              f"l'errore di primo tipo realizzato e va confrontato con {alpha:g}; con {reps} repliche "
              f"il MCSE massimo è {0.5 / math.sqrt(reps):.4f} (semiampiezza normale 95% "
              f"≈ {norm_ppf(0.975)*0.5/math.sqrt(reps):.4f}).", "",
              "| ipotesi | cluster | d | rho | m | scenario | δ vero | rifiuto bootstrap | rifiuto score/sign-flip | rifiuto Hoeffding | semiampiezza 90% media |",
              "| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |"]
    for s in simulated:
        alt = s.get("rejection_rate_tango", s.get("rejection_rate_signflip", float("nan")))
        hoe = s.get("rejection_rate_hoeffding")
        hoe_txt = "—" if hoe is None else f"{hoe:.3f}"
        lines.append(f"| {s['hypothesis']} | {s['n_clusters']} | {s['discordance']:.2f} | "
                     f"{s.get('icc', '—') if 'icc' in s else '—'} | {s.get('margin', '—')} | {s['scenario']} | "
                     f"{s['true_delta']:.3f} | {s['rejection_rate']:.3f} | {alt:.3f} | {hoe_txt} | {s['mean_halfwidth_90']:.3f} |")
    return "\n".join(lines) + "\n"


def weak_null_markdown(rows: list[dict[str, float]], alpha: float = 0.05) -> str:
    lines = ["", "## Nulla debole asimmetrica — controesempio esatto (secondo verbale di verifica)", "",
             "Medie di cluster +1/7 con probabilità 7/8 e −1 con probabilità 1/8: E[D] = 0, distribuzione "
             "non simmetrica. Errore di primo tipo esatto del test di inversione di segno (unilaterale, "
             f"α = {alpha:g}), calcolato per enumerazione. Mostra perché la garanzia sotto la nulla "
             "**forte** di scambiabilità (simmetria dei segni) non si estende alla nulla debole «media ≤ 0». Il test di "
             "Hoeffding, che usa medie di cluster indipendenti e limitate in [−1, 1], controlla il livello "
             "anche qui: è la decisione primaria del piano per H1/H2.", "",
             "| cluster | E[D] sotto la nulla | errore di primo tipo esatto, sign-flip | soglia Hoeffding | errore di primo tipo esatto, Hoeffding |",
             "| ---: | ---: | ---: | ---: | ---: |"]
    for r in rows:
        lines.append(f"| {r['n_clusters']} | {r['mean_under_null']:.3f} | {r['exact_size_sign_flip']:.4f} | "
                     f"{r['hoeffding_threshold']:.3f} | {r['exact_size_hoeffding']:.4f} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    assert_no_forbidden_argv(argv)
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default=".", help="cartella di output (unica scrittura ammessa)")
    parser.add_argument("--reps", type=int, default=400, help="repliche Monte Carlo per scenario")
    parser.add_argument("--boot", type=int, default=2000, help="ricampionamenti bootstrap per replica")
    parser.add_argument("--seed", type=int, default=20260913)
    parser.add_argument("--quick", action="store_true", help="griglia ridotta")
    parser.add_argument("--alpha", type=float, default=0.05)
    args = parser.parse_args(argv)
    if not 0 < args.alpha < 0.5 or args.reps < 1 or args.boot < 1:
        parser.error("richiesti 0 < alpha < 0.5, reps >= 1 e boot >= 1")

    install_data_guard()
    try:
        grid = QUICK_GRID if args.quick else FULL_GRID
        analytic = analytic_grid(tuple(N_STRATA * n for n in grid["n_per_fault"]), grid["h3_discordance"],
                                 grid["h3_margins"], grid["h12_discordance"], grid["h12_icc"],
                                 grid["h12_effects"], args.alpha)
        simulated = run_simulations(grid, args.reps, args.boot, args.seed,
                                    progress=lambda s: print(s, file=sys.stderr), alpha=args.alpha)
        out_dir = Path(args.out)
        out_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "generator": "studio2/fase03/piano_statistico/design_resolution.py",
            "no_real_data": True,
            "data_guard": "builtins.open e io.open (pathlib incluso) rifiutano letture e update durante main; non è una sandbox",
            "alpha_one_sided": args.alpha,
            "reps": args.reps, "boot": args.boot, "seed": args.seed, "quick": args.quick,
            "grid": {k: list(v) for k, v in grid.items()},
            "float_digits": FLOAT_DIGITS,
            "analytic": [asdict(r) for r in analytic],
            "simulated": simulated,
            "weak_null_counterexample": [weak_null_counterexample(N_STRATA * n, args.alpha)
                                         for n in grid["n_per_fault"]],
        }
        with open(out_dir / "DESIGN_RESOLUTION.json", "w", encoding="utf-8") as fh:
            json.dump(canonical(payload), fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        with open(out_dir / "DESIGN_RESOLUTION.md", "w", encoding="utf-8") as fh:
            fh.write(markdown_tables(analytic, simulated, args.alpha, args.reps))
            fh.write(weak_null_markdown(payload["weak_null_counterexample"], args.alpha))
    finally:
        remove_data_guard()
    print(f"scritti {out_dir / 'DESIGN_RESOLUTION.json'} e {out_dir / 'DESIGN_RESOLUTION.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
