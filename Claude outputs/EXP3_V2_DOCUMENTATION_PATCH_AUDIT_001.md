# VERDICT: READY TO APPLY DOCUMENTATION PATCH

---

## 1. Identità Git della candidate

| Campo | Valore |
|---|---|
| HEAD | `7e32ea5a1249ac3549791e43f3bafcf728215389` |
| State | Detached HEAD |
| Branch | Nessuno (fatal: ref HEAD is not a symbolic ref) |

## 2. Stato Git source e candidate

### Source repository (`/Users/luker/fot-tep`)

| Controllo | Risultato |
|---|---|
| HEAD | `7e32ea5a1249ac3549791e43f3bafcf728215389` (invariato, coincide con candidate) |
| Staged diff | Vuoto |
| Tracked diff | Vuoto |
| Untracked | Identici a quelli preesistenti (file di governance EXP3_V2, schemi, test, log) |

### Candidate worktree

| Controllo | Risultato |
|---|---|
| HEAD | `7e32ea5a1249ac3549791e43f3bafcf728215389` ✓ |
| Detached | Sì ✓ |
| Staged diff | Vuoto ✓ |
| File creati o cancellati | Nessuno ✓ |
| File tracked modificati | Esattamente 2 ✓ |
| Untracked | Nessuno ✓ |

### Draft Results

| Controllo | Valore atteso | Valore osservato | Esito |
|---|---|---|---|
| Size | 5575 byte | 5575 byte | ✓ |
| SHA-256 | `fb213e17aaceccfaf4a017b884e6bfdd1606cf43bbd1db06f2b713e2db5c1e82` | identico | ✓ |

### Tag `exp3-v2-results-frozen-001`

| Campo | Valore atteso | Valore osservato | Esito |
|---|---|---|---|
| Tipo | annotated tag | `tag` | ✓ |
| Tag object | `3b66e9de8e3604e9744a10e1fcfb1fab31b6aaf4` | identico | ✓ |
| Governance commit | `3781d6801191757a47bd919f0e4e9705b5895769` | identico | ✓ |
| Payload commit (parent) | `81b0a7f61e6eaa2d229fe66d9fd768c021aaef41` | identico | ✓ |
| Governance manifest SHA-256 | `5933f2c8f9c51f11054754792dde8fd8e1890028d63e158bf8d08d213787fed7` | identico | ✓ |

## 3. Elenco esatto dei file modificati

```
M   docs/fot_walkthrough_conversazione.html
M   phase_b/README.md
```

Nessun altro file modificato, creato o cancellato.

## 4. Hash completi dei due file prima e dopo

| File | HEAD (prima) | Candidate (dopo) |
|---|---|---|
| `docs/fot_walkthrough_conversazione.html` | `bb6fb6271460ea09a15e067ee8380b4a828d2b95ae0dbe3868df13646f575139` | `5cee7594c4ff0a76ec848f2d92dcef7374138a18eee8287522d0902a444afd44` |
| `phase_b/README.md` | `67bee13dccb45be393f83d7cbc26edd46ba91f4943073c5f430344ed17a6bb89` | `386a688522ef0c896481633d3e236ab0404761a6926b5f298ed5ee832d8d1294` |

## 5. Unified diff completo

### `phase_b/README.md`

Una sola riga sostituita nella tabella degli esperimenti: la riga Experiment 3 V2 passa da stato "Completed, results pending freeze" a "Completed and frozen (tag-only)" con testo aggiornato. Nessun'altra riga toccata.

```diff
-| **Experiment 3 V2** | `exp3_v2/` | Completed, results pending freeze | Corrective revision of Exp3 with fixed technical procedure. Same scientific design, new realisations. Confirmatory results support primary B−A contrast. |
+| **Experiment 3 V2** | [`exp3_v2/`](exp3_v2/) | Completed and frozen (tag-only) | Corrective and substitutive prospective replica of Experiment 3 on new physical realisations of the same four classes. Confirmatory results are frozen under [`exp3-v2-results-frozen-001`](https://github.com/sorrentinoluca/fot-phd/tree/exp3-v2-results-frozen-001); the three evaluation outputs remain governed by that tag and are not materialized on this branch. |
```

### `docs/fot_walkthrough_conversazione.html`

Stat: 95 insertions, 2 deletions. Modifiche:

1. Contatore superiore: `/ 17` → `/ 24`
2. Fase 2 nav: placeholder rimosso, sostituito con `<ol>` contenente 7 link (`#step-18`…`#step-24`)
3. 7 nuove `<section>` (step-18…step-24) inserite dopo la chiusura di step-17 e prima di `<footer>`
4. Nessuna altra modifica (style, script, Phase 1, Phase 3, footer invariati)

## 6. Hash Fase 1 HEAD/candidate e byte-identity

| Metrica | Valore |
|---|---|
| Sequenza estratta | Da `<section id="step-1" data-step="1">` fino a `</section>\n` di step-17 (incluso LF) |
| Byte HEAD | 75118 |
| Byte candidate | 75118 |
| SHA-256 HEAD | `59c26607a4e965a15c35eec54167842d379e4c72db655d03581cb4310d235989` |
| SHA-256 candidate | `59c26607a4e965a15c35eec54167842d379e4c72db655d03581cb4310d235989` |
| Byte-identical | **Sì** ✓ |

Step 1–17: non rinumerati, kicker invariati (`Step N / 17`), id invariati, `data-step` invariati, anchor invariati, tabelle/figure/testo/whitespace invariati.

## 7. Conteggio e sequenza degli Step

| Controllo | Risultato |
|---|---|
| Totale `section[data-step]` | 24 ✓ |
| ID unici | 24 (step-1…step-24) ✓ |
| `data-step` | 1…24, senza duplicati o lacune ✓ |
| Sequenza corretta | `ids == [step-1..step-24]`, `data-steps == [1..24]` ✓ |

## 8. Verifica indice, anchor, contatore e Fase 3

| Controllo | Risultato |
|---|---|
| Contatore superiore | `/ 24` ✓ |
| Fase 2 nav | 7 link a step-18…step-24 ✓ |
| Fase 3 nav | Placeholder "Contenuti da aggiungere" invariato ✓ |
| Tutti i link `#step-N` risolvono | 0 link irrisolti ✓ |
| Nuove sezioni sorelle | Sì (non annidate), dopo step-17 e prima di footer ✓ |
| Wrapper `section id="phase-2"` | Non presente ✓ |

## 9. Verifica byte-identità CSS e JavaScript

| Blocco | HEAD SHA-256 | Candidate SHA-256 | Byte | Identico |
|---|---|---|---|---|
| `<style>` | `9814978570ebd760ab44191571ef8708dfc753956eabb86f4719dc985f5990f1` | identico | 11459 | ✓ |
| `<script>` | `c4e6b896cc0486926bf3cfa2892fbfd5294041f1dd2c2975cd11bbc5fac85b50` | identico | 62 | ✓ |

Nessun CSS, JavaScript, SVG, grafico, figura o dipendenza esterna aggiunta. Tag counts: 1 `<style>`, 2 `<script>` (invariati), 1 `<svg>` (preesistente), 0 external links, 0 nuove figure nelle sezioni 18-24.

## 10. Validazione delle tre tabelle

### Tabella Step 21 (Popolazione primaria unseen)

| Atteso | Osservato |
|---|---|
| 4 colonne (Condizione, Corretti/72, Accuratezza, Astensioni) | ✓ |
| 3 righe dati (A, B, E) | ✓ |
| A: 0/72, 0.0%, 30 abstentions | ✓ |
| B: 68/72, 94.4%, 0 abstentions | ✓ |
| E: 4/72, 5.6%, 0 abstentions | ✓ |

### Tabella Step 22 (Contrasti e bootstrap)

| Atteso | Osservato |
|---|---|
| 4 colonne (Contrasto, Stima, CI percentile 95%, Ruolo) | ✓ |
| 2 righe dati (B−A, B−E) | ✓ |
| B−A: 0.9444, [0.8611, 1.0] | ✓ |
| B−E: 0.8889, [0.7778, 0.9861] | ✓ |

### Tabella Step 23 (Risultati secondari descrittivi)

| Atteso | Osservato |
|---|---|
| 4 colonne (Condizione, Local-seen, Normal, Overall) | ✓ |
| 3 righe dati (A, B, E) | ✓ |
| A: 24/24 (100.0%), 24/24 (100.0%), 48/120 (40.0%) | ✓ |
| B: 19/24 (79.2%), 24/24 (100.0%), 111/120 (92.5%) | ✓ |
| E: 22/24 (91.7%), 24/24 (100.0%), 50/120 (41.7%) | ✓ |

Tutti i denominatori corretti. Nessun valore nuovo rispetto al draft.

## 11. Confronto di tutti i valori scientifici

Tutti i valori nel candidate corrispondono esattamente al draft frozen:

| Valore | Draft | Candidate | Match |
|---|---|---|---|
| Unseen A corretti | 0/72 (0.0%) | 0/72, 0.0% | ✓ |
| Unseen A abstentions | 30 | 30 | ✓ |
| Unseen B corretti | 68/72 (94.4%) | 68/72, 94.4% | ✓ |
| Unseen B abstentions | 0 | 0 | ✓ |
| Unseen E corretti | 4/72 (5.6%) | 4/72, 5.6% | ✓ |
| Unseen E abstentions | 0 | 0 | ✓ |
| B−A stima | 0.9444 | 0.9444 | ✓ |
| B−A CI | [0.8611, 1.0] | [0.8611, 1.0] | ✓ |
| B−E stima | 0.8889 | 0.8889 | ✓ |
| B−E CI | [0.7778, 0.9861] | [0.7778, 0.9861] | ✓ |
| Bootstrap method | paired physical-case cluster | paired physical-case cluster bootstrap | ✓ |
| Stratificazione | per pseudolabel | per pseudolabel | ✓ |
| Draw | 10.000 | 10.000 | ✓ |
| Seed | 320031 | 320031 | ✓ |
| B−A ruolo | contrasto primario | Contrasto primario | ✓ |
| Criterio replica | congiuntamente B−A > 0 e lower CI > 0 | congiuntamente, entrambi soddisfatti | ✓ |
| B−E ruolo | supporting evidence per semantic specificity | Evidenza supporting per semantic specificity | ✓ |
| B−E CI non gate | esplicito | "il CI non costituisce un gate aggiuntivo" | ✓ |
| B−E non modifica decisione primaria | implicito nel draft | "senza modificare la decisione primaria" | ✓ |
| Secondari | esclusivamente descrittivi | esclusivamente descrittivi | ✓ |

Contenuti proibiti assenti: p-value, confusion matrix, recall, helped/harmed, stability analysis, pooled, per-agent, nuove metriche, nuove CI, analisi pooled. Le sole due CI presenti sono B−A e B−E.

EXP3 descritto come "chiuso per esaurimento tecnico prima di produrre risultati scientifici" ✓. EXP3_V2 descritto come "revisione correttiva e sostitutiva" ✓. Chiusura tecnica non presentata come risultato scientifico negativo ("senza trasformare la chiusura tecnica di Experiment 3 in un risultato scientifico negativo") ✓. Nessuna causalità introdotta ✓. Generalizzazione esplicitamente negata ("non dimostra generalizzazione a nuovi fault o nuovi domini") ✓. "Nuovi fault" e "nuovi domini" compaiono esclusivamente in contesto di negazione ✓.

## 12. Valutazione della coerenza didattica

### Pattern strutturale

Tutti gli Step 18–24 seguono il pattern di Fase 1: `<section>` → `<div class="step-kicker">` → `<h2>` → contenuto esplicativo/evidenziale. Nessun redesign.

### Classi CSS

Tutte le classi utilizzate nelle nuove sezioni preesistono nello `<style>` e nella Fase 1: `callout`, `full-width`, `chain`, `example`, `panel-label`, `num`, `phase-badge`, `design`, `offline`, `scroll`, `source`, `step-kicker`. Nessuna classe nuova.

### Progressione tematica

| Step | Contenuto | Ruolo nella progressione |
|---|---|---|
| 18 | Perché una replica prospettica | Contesto |
| 19 | Da Experiment 3 a EXP3_V2 | Continuità / disegno |
| 20 | Disegno confirmatory frozen | Disegno |
| 21 | Risultati primari unseen | Risultati |
| 22 | Contrasti e bootstrap | Contrasti |
| 23 | Risultati secondari descrittivi | Secondari |
| 24 | Interpretazione, limiti e provenienza | Limiti |

La progressione contesto → disegno → risultati → contrasti → secondari → limiti è rispettata ✓.

### Tono didattico

Coerente con Fase 1: esplicativo, con callout, esempi, tabelle con caption. Nessun redesign. EXP3_V2 presentato come esperimento distinto (replica prospettica), non come appendice di EXP1 ✓.

### Duplicazione Step 17

Zero frasi di Step 17 duplicate nelle nuove sezioni ✓.

### Kicker Step 1–17

I kicker di Fase 1 mantengono il denominatore originale `/ 17` (es. "Step 1 / 17", …, "Step 17 / 17"). Questa permanenza è intenzionale per preservare l'identità degli step originali. Rischio cosmetico non bloccante: l'utente potrebbe notare la discontinuità `/ 17` → `/ 24`, ma la scelta è coerente con la policy di immutabilità della Fase 1.

## 13. Audit della riga README

La riga Experiment 3 V2 in `phase_b/README.md`:

| Requisito | Verificato |
|---|---|
| Stato "Completed and frozen (tag-only)" | ✓ |
| Descrizione: replica prospettica correttiva e sostitutiva | ✓ ("Corrective and substitutive prospective replica of Experiment 3") |
| Scope: stesse quattro classi | ✓ ("on new physical realisations of the same four classes") |
| Link a `exp3_v2/` | ✓ (`[exp3_v2/](exp3_v2/)`) |
| Link al tag `exp3-v2-results-frozen-001` | ✓ (con URL GitHub) |
| Output governati dal tag | ✓ ("remain governed by that tag") |
| Non afferma materializzazione sul branch | ✓ ("are not materialized on this branch") |
| Experiment 1, 2, 3 e altre sezioni invariate | ✓ (diff limitato alla sola riga EXP3_V2) |

## 14. Defect

### Blocking

Nessuno.

### Non-blocking

1. **Kicker denominatore (cosmetico)**: Step 1–17 conservano `/ 17` nei kicker mentre Step 18–24 usano `/ 24`. Intenzionale per preservare l'identità di Fase 1. Rischio cosmetico minimo, non bloccante come da specifica.

## 15. Conferme finali

| Conferma | Esito |
|---|---|
| Zero file modificati durante l'audit | ✓ |
| Zero output copiati | ✓ |
| Zero evaluator/verifier/RNG/bootstrap eseguiti | ✓ |
| Zero commit/tag/push | ✓ |
| `phase_b/exp3_v2/evaluation_outputs/` non creata | ✓ |
| Nessun file staged | ✓ |

### Hash finali dei file candidati (post-audit, invariati)

| File | SHA-256 pre-audit | SHA-256 post-audit | Invariato |
|---|---|---|---|
| `docs/fot_walkthrough_conversazione.html` | `5cee7594c4ff0a76ec848f2d92dcef7374138a18eee8287522d0902a444afd44` | `5cee7594c4ff0a76ec848f2d92dcef7374138a18eee8287522d0902a444afd44` | ✓ |
| `phase_b/README.md` | `386a688522ef0c896481633d3e236ab0404761a6926b5f298ed5ee832d8d1294` | `386a688522ef0c896481633d3e236ab0404761a6926b5f298ed5ee832d8d1294` | ✓ |

---

**Audit completato in modalità rigorosamente READ-ONLY. Nessun file è stato modificato, nessun output è stato copiato, nessun evaluator/verifier/RNG/bootstrap è stato eseguito, nessun commit/tag/push è stato effettuato.**
