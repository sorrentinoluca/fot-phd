# EXP3_V2 Documentation Integration — Structured VERDICT

---

## 0 · VERDICT

**CONDITIONALLY VIABLE.**

The patch is structurally feasible. The walkthrough HTML can accommodate Steps 18–24 under Fase 2 using the existing `section[data-step]` pattern, and the JavaScript will discover them without modification to Fase 1 body content. Seven specific amendments are required (detailed below) compared to the prior proposal that incorrectly used a monolithic `<section id="phase-2">` with internal `<h3>` headings and no `data-step` attributes.

**Conditions for viability:**

1. Every new step must be a top-level `<section id="step-N" data-step="N">` — not nested inside a wrapper section.
2. The topbar progress denominator ("/ 17") must be updated to reflect the new total — either hardcoded to "/ 24" or computed dynamically by JavaScript.
3. Fase 1 body sections (step-1 through step-17) must remain **byte-identical**: no kicker text changes, no content edits, no attribute modifications.
4. Fase 2 nav placeholder must be replaced with an `<ol>` of step links following the Fase 1 pattern.
5. New CSS rules must use `#step-N`-prefixed selectors (N ≥ 18) to avoid any cascade interference with Fase 1 styling.
6. All numerical results must come exclusively from the frozen draft `EXP3_V2_CONFIRMATORY_RESULTS_SECTION_001.md` (SHA-256: `fb213e17aaceccfaf4a017b884e6bfdd1606cf43bbd1db06f2b713e2db5c1e82`).
7. References to frozen outputs must cite tag `exp3-v2-results-frozen-001`; no frozen output file may be copied into the current branch.

---

## 1 · SOURCE IDENTITY VERIFICATION

| Property | Expected | Observed | Match |
|---|---|---|---|
| File | `EXP3_V2_CONFIRMATORY_RESULTS_SECTION_001.md` | Present at staged path | ✓ |
| Size | 5575 bytes | 5575 bytes | ✓ |
| SHA-256 | `fb213e17...db5c1e82` | `fb213e17aaceccfaf4a017b884e6bfdd1606cf43bbd1db06f2b713e2db5c1e82` | ✓ |
| Lines | 50 | 50 | ✓ |

The draft is the authoritative source for all Exp3v2 numerical values in this review. No additional computation has been performed.

---

## 2 · FROZEN DRAFT — KEY VALUES EXTRACTION

All values below are taken verbatim from the frozen draft.

### Primary unseen population (n = 72 per condition)

| Condition | Correct | Incorrect | Abstentions | Total | Accuracy |
|---|---:|---:|---:|---:|---:|
| A | 0 | 72 | 30 | 72 | 0.000 (0.0%) |
| B | 68 | 4 | 0 | 72 | 0.944 (94.4%) |
| E | 4 | 68 | 0 | 72 | 0.056 (5.6%) |

Abstentions treated as errors in all cells.

### Confirmatory contrasts

| Contrast | Observed | 95% percentile CI | Interpretation |
|---|---:|---|---|
| B−A | 0.9444 (94.4 pp) | [0.8611, 1.0] | Supported: B−A > 0 AND lower CI bound > 0 |
| B−E | 0.8889 (88.9 pp) | [0.7778, 0.9861] | Supporting evidence for semantic specificity |

B−A is the **primary contrast** (not "gate primary"). `replication_supported` requires conjointly B−A > 0 AND lower CI bound > 0; both are satisfied. B−E is **supporting evidence** for semantic specificity — it is not a gate and its CI is not a pre-specified gating criterion.

### Bootstrap parameters

- 10,000 draws
- Seed: 320031
- Bootstrap unit: physical-case cluster, stratified by pseudolabel

### Secondary populations (descriptive only)

| Condition | Local-seen (24) | Normal (24) | Overall (120) |
|---|---|---|---|
| A | 24/24 (100%) | 24/24 (100%) | 48/120 (40.0%) |
| B | 19/24 (79.2%) | 24/24 (100%) | 111/120 (92.5%) |
| E | 22/24 (91.7%) | 24/24 (100%) | 50/120 (41.7%) |

No confirmatory inference specified for secondary populations.

### Design parameters (from draft Limitations)

- 4 faults, 6 physical cases per fault → 24 physical runs
- 4 agents → 3 unseen agents per run → 72 agent-case per condition
- Single frozen model
- Scope limited to EXP3_V2 perimeter

---

## 3 · STRUCTURAL ANALYSIS — CURRENT HTML

### Document skeleton

```
<!doctype html>
<html lang="it">
<head>  ...meta, title, <style> (lines 1–74)
<body>
  <a class="skip">                              (line 77)
  <div class="topbar">                          (lines 78–81)
    progress-label: "Step <#current-step> / 17"
  <button#nav-backdrop>                         (line 82)
  <div class="layout">                          (line 83)
    <nav#guide-nav>                             (lines 84–95)
      <ol class="nav-root">
        <li> Step 1 link
        <li> <details "Fase 1" open> → <ol> Steps 2–17
        <li> <details "Fase 2">      → <p> "Contenuti da aggiungere."
        <li> <details "Fase 3">      → <p> "Contenuti da aggiungere."
    <main#main>                                 (line 96)
      <header>                                  (lines 97–99)
      <section#step-1  data-step="1">           (line 100)
      ...
      <section#step-16 data-step="16">          (line 323)
      <section#step-17 data-step="17">          (line 334)
      <footer>                                  (line 478)
  </div> <!-- .layout -->
  <script>                                      (lines 480–494)
</body>
</html>
```

### Section pattern (invariant for every step)

```html
<section id="step-N" data-step="N">
  <div class="step-kicker">Step N / TOTAL <span class="phase-badge CLASS">LABEL</span></div>
  <h2>TITLE</h2>
  ...content...
</section>
```

### Phase badges used in Fase 1

| CSS class | Colour | Used for |
|---|---|---|
| `.design` | amber | Methodology / Phase A design steps |
| `.runtime` | teal | Phase B inference / execution steps |
| `.offline` | blue | Ground-truth evaluation steps |

### Nav index structure

```html
<ol class="nav-root">
  <li><a href="#step-1">1. Introduzione</a></li>
  <li><details class="nav-phase" open><summary>Fase 1</summary>
    <ol> <!-- 16 links: step-2 through step-17 --> </ol>
  </details></li>
  <li><details class="nav-phase"><summary>Fase 2</summary>
    <p class="nav-phase-empty">Contenuti da aggiungere.</p>
  </details></li>
  <li><details class="nav-phase"><summary>Fase 3</summary>
    <p class="nav-phase-empty">Contenuti da aggiungere.</p>
  </details></li>
</ol>
```

### CSS scoping for Step 17

Lines 36–70 define 25+ CSS rules all prefixed with `#step-17 .s17*`. These rules are scoped to Step 17's section element and will not interfere with new Fase 2 sections. New custom visualisations in Steps 18–24 must follow the same scoping pattern: `#step-21 .s21bars`, `#step-22 .s22ci`, etc.

---

## 4 · JAVASCRIPT ANALYSIS

### Source (lines 480–494)

The single IIFE at the end of the document manages: nav toggle (mobile/desktop), scroll-based progress tracking, and IntersectionObserver highlighting.

### Critical selectors

```javascript
const links = [...nav.querySelectorAll('a[href^="#step-"]')];
const sections = [...document.querySelectorAll('section[data-step]')];
```

**Both selectors are open-ended**: they will automatically discover any new `<section data-step="18">` through `<section data-step="24">` and any new `<a href="#step-18">` through `<a href="#step-24">` in the nav — no JS modification required for discovery.

### Progress label update

```javascript
function updateCurrent() {
  ...
  current.textContent = step;
  ...
}
```

The JS updates `#current-step` with the active step's `data-step` value. It does **not** touch the denominator. The denominator "17" is hardcoded in HTML at line 80:

```html
<span class="progress-label" aria-live="polite">
  Step <span id="current-step">1</span> / 17
</span>
```

### IntersectionObserver

```javascript
const observer = new IntersectionObserver(updateCurrent,
  { rootMargin: '-18% 0px -62% 0px', threshold: [0, .1] });
sections.forEach(section => observer.observe(section));
```

The observer iterates over `sections` (all `section[data-step]`), so new sections are automatically observed. No code change needed.

### Link highlighting

```javascript
links.forEach(link =>
  link.getAttribute('href') === `#step-${step}`
    ? link.setAttribute('aria-current', 'step')
    : link.removeAttribute('aria-current')
);
```

This matches links by `href="#step-N"`, so new nav links in the Fase 2 `<ol>` will receive `aria-current` highlighting automatically.

### JS MODIFICATIONS REQUIRED

Only **one** modification:

**Option A (minimal):** Change the hardcoded "17" in the topbar to "24":
```html
Step <span id="current-step">1</span> / 24
```

**Option B (robust, recommended):** Add a `<span id="total-steps">` and compute dynamically:
```html
Step <span id="current-step">1</span> / <span id="total-steps">24</span>
```
Add one line to the IIFE, after `sections` is defined:
```javascript
document.getElementById('total-steps').textContent = sections.length;
```

Option B is preferred because it remains correct if Fase 3 steps are added later.

### JS VERDICT

The JavaScript is fully compatible with the proposed patch. No Fase 1 logic changes. One topbar denominator fix (outside Fase 1 body).

---

## 5 · BYTE-IDENTITY ANALYSIS — FASE 1

### Scope of the byte-identity constraint

"Il contenuto attuale di Fase 1 deve restare byte-identico."

**Elements inside Fase 1 body** (must NOT change):
- `<section id="step-1" data-step="1">` through `<section id="step-17" data-step="17">` — all section tags, attributes, kicker text, headings, paragraphs, tables, SVGs, and every byte within.
- Specifically: the kicker text "Step N / 17" inside each section remains as-is.

**Elements outside Fase 1 body** (may change):
- `<head>`: `<style>` block — additions of new `#step-18`+ rules at the end are permitted.
- Topbar: progress label denominator — outside any Fase 1 section.
- Nav index: the Fase 2 `<details>` placeholder — structural navigation, not Fase 1 body content.
- Footer: link text, if needed.
- `<script>`: one-line addition for dynamic total, if Option B chosen.
- New `<section>` elements inserted **after** `</section>` of step-17 and **before** `<footer>`.

### Kicker text inconsistency

After the patch, Fase 1 kickers will read "Step N / 17" while Fase 2 kickers will read "Step N / 24" and the topbar will show "Step N / 24". This creates a visible inconsistency.

**Assessment:** This is cosmetically imperfect but scientifically harmless. The "/ 17" in Fase 1 kickers is historically accurate — Fase 1 comprised 17 steps when it was written. The topbar always shows the true document-wide total via JS. The alternative — modifying all 17 existing kickers — would violate byte-identity. **Recommendation:** Accept the inconsistency. Optionally, add a one-line CSS rule to visually hide the "/ 17" portion of kickers in Fase 1 and replace it with a JS-injected value, but this is an aesthetic refinement, not a structural requirement.

### FASE 1 BODY MODIFICATIONS = 0 ✓

---

## 6 · PROPOSED STEP STRUCTURE FOR FASE 2

### Step allocation

| data-step | Section ID | Title (proposed) | Phase badge | Content scope |
|---:|---|---|---|---|
| 18 | `step-18` | Perché una replica prospettica | `.design` | Motivation: why replicate Exp1 with new physical realisations; what a confirmatory replica adds to a PoC |
| 19 | `step-19` | Da Exp 3 a EXP3_V2: correzione e revisione | `.design` | Exp3's technical closure; what EXP3_V2 changed (procedure, not science); link to `phase_b/exp3/` and `phase_b/exp3_v2/` |
| 20 | `step-20` | Disegno confirmatory frozen | `.design` | Pre-specified contrasts, scoring rule, population definitions; 4 faults × 6 physical cases × 4 agents; paired cluster bootstrap (10,000 draws, seed 320031); reference to tag `exp3-v2-results-frozen-001` |
| 21 | `step-21` | Risultati primari: popolazione unseen | `.offline` | Primary unseen table (A=0/72, B=68/72, E=4/72); abstention behaviour (A: 30 abstentions, B/E: 0); bar chart analogous to Step 17 Figure 1 |
| 22 | `step-22` | Contrasti e bootstrap | `.offline` | B−A = 0.9444 CI [0.8611, 1.0]; B−E = 0.8889 CI [0.7778, 0.9861]; forest-plot SVG analogous to Step 17 Figure 2; interpretation of each contrast |
| 23 | `step-23` | Risultati secondari descrittivi | `.offline` | Local-seen (A 100%, B 79.2%, E 91.7%), Normal (all 100%), Overall; descriptive only — no confirmatory inference; note B < A in local-seen |
| 24 | `step-24` | Interpretazione, limiti e provenienza frozen | `.offline` | Claim: B−A supported, B−E supports semantic specificity; limitations (4 faults, single model, EXP3_V2 perimeter); provenance: tag `exp3-v2-results-frozen-001`; no cross-experiment meta-analytic claims |

### Design rationale

The seven steps mirror the didactic structure of Step 17 (which presented Exp1 results), adapted for the EXP3_V2 confirmatory design:

- **Steps 18–20** establish context and design before any numbers appear — paralleling how Steps 12–15 established Phase B design before Step 17's results.
- **Steps 21–22** present the primary quantitative findings — parallel to Step 17 subsections 1–3.
- **Step 23** covers secondary/descriptive analyses — parallel to Step 17 subsection 5.
- **Step 24** consolidates interpretation and limitations — parallel to Step 17 subsections 6–7.

Each step is self-contained within a `<section>` with its own `data-step`, following the corrected pattern (not the prior monolithic `<section id="phase-2">` with `<h3>` subheadings).

---

## 7 · PROPOSED HTML SKELETON (FASE 2 SECTIONS)

### Nav index patch

**Replace** (line 91):
```html
<li><details class="nav-phase"><summary>Fase 2</summary>
  <p class="nav-phase-empty">Contenuti da aggiungere.</p>
</details></li>
```

**With:**
```html
<li><details class="nav-phase" open><summary>Fase 2 — Replica confirmatory (Experiment 3 V2)</summary><ol>
  <li><a href="#step-18">18. Perché una replica prospettica</a></li>
  <li><a href="#step-19">19. Da Exp 3 a EXP3_V2</a></li>
  <li><a href="#step-20">20. Disegno confirmatory frozen</a></li>
  <li><a href="#step-21">21. Risultati primari unseen</a></li>
  <li><a href="#step-22">22. Contrasti e bootstrap</a></li>
  <li><a href="#step-23">23. Risultati secondari descrittivi</a></li>
  <li><a href="#step-24">24. Interpretazione, limiti e provenienza</a></li>
</ol></details></li>
```

### Section skeleton (one per step, inserted between `</section>` of step-17 and `<footer>`)

```html
<!-- ═══════════════════════════════════════════════════════ -->
<!-- FASE 2 — Replica confirmatory (Experiment 3 V2)        -->
<!-- Source: EXP3_V2_CONFIRMATORY_RESULTS_SECTION_001.md    -->
<!-- Frozen outputs: tag exp3-v2-results-frozen-001          -->
<!-- ═══════════════════════════════════════════════════════ -->

<section id="step-18" data-step="18">
  <div class="step-kicker">Step 18 / 24 <span class="phase-badge design">Fase 2 / replica design</span></div>
  <h2>Perché una replica prospettica</h2>
  <!-- Content: motivazione scientifica per replicare Exp1 su nuove
       realizzazioni fisiche; cosa aggiunge la replica al PoC;
       struttura 4 fault × 6 casi × 4 agenti vs Exp1's 4 × 3 × 4 -->
</section>

<section id="step-19" data-step="19">
  <div class="step-kicker">Step 19 / 24 <span class="phase-badge design">Fase 2 / revisione tecnica</span></div>
  <h2>Da Exp 3 a EXP3_V2: correzione e revisione</h2>
  <!-- Content: chiusura tecnica di Exp3 (attempt exhaustion, nessun
       dato scientifico); cosa EXP3_V2 ha corretto nella procedura;
       stesso disegno scientifico, nuove realizzazioni;
       link a phase_b/exp3/ e phase_b/exp3_v2/ -->
</section>

<section id="step-20" data-step="20">
  <div class="step-kicker">Step 20 / 24 <span class="phase-badge design">Fase 2 / disegno frozen</span></div>
  <h2>Disegno confirmatory frozen</h2>
  <!-- Content:
       - Contrasti pre-specificati: B−A (primario), B−E (supporto)
       - Scoring: astensione = errore
       - Popolazione primaria: unseen (n=72 per condizione)
       - 4 fault, 6 casi fisici per fault, 4 agenti
         → 24 run fisici × 3 unseen agents = 72 agent-case
       - Bootstrap: cluster paired sui 24 run fisici,
         stratificato per pseudolabel, 10.000 draws, seed 320031
       - Provenienza: tag exp3-v2-results-frozen-001
       - Nessun output frozen copiato nel branch corrente -->
</section>

<section id="step-21" data-step="21">
  <div class="step-kicker">Step 21 / 24 <span class="phase-badge offline">Fase 2 / risultati primari</span></div>
  <h2>Risultati primari: popolazione unseen</h2>
  <!-- Content:
       - Tabella: A=0/72 (0.0%), B=68/72 (94.4%), E=4/72 (5.6%)
       - Astensioni: A=30, B=0, E=0 (tutte contate come errore)
       - Barra composizione esiti (CSS classes: s21bars, s21row, etc.)
         Stile analogo a Step 17 Figure 1 ma con valori Exp3v2
       - Callout: interpretazione del floor di A e dell'assenza
         di astensioni in B/E -->
</section>

<section id="step-22" data-step="22">
  <div class="step-kicker">Step 22 / 24 <span class="phase-badge offline">Fase 2 / contrasti</span></div>
  <h2>Contrasti e bootstrap</h2>
  <!-- Content:
       - B−A = 0.9444 (94.4 pp), CI [0.8611, 1.0]
         → "contrasto primario", non "gate primary"
         → Supportato: B−A > 0 AND lower CI > 0
       - B−E = 0.8889 (88.9 pp), CI [0.7778, 0.9861]
         → "supporting evidence for semantic specificity"
         → NON un gate; CI non usata come criterio aggiuntivo
       - Forest-plot SVG analogo a Step 17 Figure 2
         (aggiornare i valori e le posizioni dei punti/segmenti)
       - Nota: con 24 cluster indipendenti (vs 12 di Exp1),
         la granularità bootstrap è più fine ma va comunque
         interpretata nel contesto del PoC -->
</section>

<section id="step-23" data-step="23">
  <div class="step-kicker">Step 23 / 24 <span class="phase-badge offline">Fase 2 / secondari</span></div>
  <h2>Risultati secondari descrittivi</h2>
  <!-- Content:
       - Tabella: Local-seen (A=100%, B=79.2%, E=91.7%),
         Normal (tutti 100%), Overall (A=40.0%, B=92.5%, E=41.7%)
       - Normal: tutti 24/24 corretti in ogni condizione
       - Osservazione critica: B (79.2%) < A (100%) in local-seen
         → B non domina in local-seen
       - Queste analisi sono DESCRITTIVE;
         nessuna inferenza confirmatory per popolazioni secondarie
       - Nessuna nuova claim inferenziale -->
</section>

<section id="step-24" data-step="24">
  <div class="step-kicker">Step 24 / 24 <span class="phase-badge offline">Fase 2 / interpretazione</span></div>
  <h2>Interpretazione, limiti e provenienza frozen</h2>
  <!-- Content:
       - Claim: B−A supportato; B−E allineato con specificità semantica
       - replication_supported = (B−A > 0) AND (lower CI bound > 0)
       - Limiti: 4 fault, 6 casi fisici/fault, 4 agenti; singolo
         modello frozen; scope limitato al perimetro EXP3_V2;
         nessuna inferenza confirmatory per secondari
       - NON effettuare claim cross-experiment meta-analitiche
         combinando Exp1 e Exp3v2
       - Provenienza: tag exp3-v2-results-frozen-001
         → citare il tag, non copiare gli output frozen
       - "Questi risultati forniscono evidenza confirmatory forte
         all'interno di EXP3_V2 che la condizione B supera la
         condizione A sui casi unseen" -->
</section>
```

---

## 8 · PROPOSED CSS ADDITIONS

All new rules must be appended **after** line 70 (end of `#step-17` rules) and **before** the `@media` queries at line 71. All rules must be scoped with `#step-N` prefix (N ≥ 18).

```css
/* ── Fase 2: Step 21 — composition bars ── */
#step-21 .s21bars{margin:14px 0}
#step-21 .s21row{display:flex;align-items:center;gap:12px;margin:8px 0}
#step-21 .s21lab{width:22px;font-weight:850;color:var(--navy)}
#step-21 .s21track{flex:1;display:flex;height:32px;border-radius:6px;overflow:hidden;border:1px solid var(--line)}
#step-21 .s21seg{display:flex;align-items:center;justify-content:center;color:#fff;font-size:13px;font-weight:800;min-width:0}
#step-21 .s21seg.ok{background:#087367}
#step-21 .s21seg.wr{background:#a03932}
#step-21 .s21seg.ab{background:#8a99a3}
#step-21 .s21legend{display:flex;gap:16px;flex-wrap:wrap;font-size:13px;margin:8px 0 0;color:var(--muted)}
#step-21 .s21legend span{display:inline-flex;align-items:center;gap:6px}
#step-21 .s21legend i{width:13px;height:13px;border-radius:3px;display:inline-block}
/* ── Fase 2: Step 22 — forest plot caption ── */
#step-22 .fig-cap{font-size:13px;color:var(--muted);max-width:90ch;margin:8px 0 0}
/* ── Fase 2: Step 23 — tags ── */
#step-23 .s23tag{display:inline-block;font-size:10.5px;font-weight:850;letter-spacing:.04em;text-transform:uppercase;padding:1px 7px;border-radius:999px;margin-left:4px}
#step-23 .s23tag.desc{background:#eef0f2;color:#5a6b76}
```

This mirrors the Step 17 pattern exactly. Additional rules (for the forest-plot SVG in Step 22, for example) would follow the same scoping convention.

---

## 9 · PROPOSED phase_b/README.md PATCH

### Target line: Experiment 3 V2 row in the Experiments table

**Current:**
```markdown
| **Experiment 3 V2** | `exp3_v2/` | Completed, results pending freeze | Corrective revision of Exp3 with fixed technical procedure. Same scientific design, new realisations. Confirmatory results support primary B−A contrast. |
```

**Proposed:**
```markdown
| **Experiment 3 V2** | `exp3_v2/` | Completed and frozen | Corrective revision of Exp3 with fixed technical procedure. Same scientific design, new realisations. Primary unseen B−A = +0.9444 [0.8611, 1.0], n = 72 per condition. Frozen outputs under tag `exp3-v2-results-frozen-001`. |
```

### Changes

1. Status: `Completed, results pending freeze` → `Completed and frozen`
2. Description: add the primary contrast value and tag reference
3. No other rows or sections of the README are modified

### Scope

This is the **only** change to `phase_b/README.md`. The architecture, pseudolabel, conditions, metrics, and execution sections remain untouched.

---

## 10 · PSEUDO-DIFF SUMMARY

### `docs/fot_walkthrough_conversazione.html`

```
LOCATION                        ACTION               FASE 1 BODY IMPACT
───────────────────────────────────────────────────────────────────────
<style> (after line 70)         ADD ~20 CSS rules     None (head, not body)
Topbar progress (line 80)       EDIT "/ 17" → "/ 24" None (topbar, not body)
Nav Fase 2 placeholder (l. 91)  REPLACE placeholder   None (nav, not body)
After </section> step-17 (l.476) INSERT 7 sections    None (new content only)
<script> (line 492)             ADD 1 line (opt. B)   None (script, not body)
───────────────────────────────────────────────────────────────────────
TOTAL edits to Fase 1 body:     0
```

### `phase_b/README.md`

```
LOCATION                           ACTION
────────────────────────────────────────────
Experiments table, Exp3v2 row      EDIT status + description
────────────────────────────────────────────
TOTAL lines modified:              1
```

---

## 11 · MODIFICATION COUNTER

| Scope | Insertions | Edits | Deletions | Body bytes changed |
|---|---:|---:|---:|---:|
| **Fase 1 body** (step-1 … step-17) | 0 | 0 | 0 | **0** |
| `<head>/<style>` | ~20 rules | 0 | 0 | — |
| Topbar | 0 | 1 | 0 | — |
| Nav index | 1 block | 1 (replace placeholder) | 1 (placeholder) | — |
| New Fase 2 sections | 7 sections | 0 | 0 | — |
| `<script>` | 0–1 line | 0 | 0 | — |
| `phase_b/README.md` | 0 | 1 row | 0 | — |

### **PHASE 1 BODY MODIFICATIONS = 0** ✓

---

## 12 · DIFFERENCES FROM EXP1 (STEP 17) THAT THE PATCH MUST REFLECT

The Fase 2 content must not be a copy-paste of Step 17 with swapped numbers. Key structural differences between Exp1 and EXP3_V2:

| Dimension | Exp1 (Step 17) | EXP3_V2 (Fase 2) |
|---|---|---|
| Physical runs | 12 (3 per fault) | 24 (6 per fault) |
| Agent-case per condition | 36 | 72 |
| Bootstrap clusters | 12 | 24 |
| Bootstrap seed | 20260829 | 320031 |
| B accuracy (unseen) | 31/36 (86.1%) | 68/72 (94.4%) |
| A accuracy (unseen) | 0/36 (0.0%) | 0/72 (0.0%) |
| E accuracy (unseen) | 3/36 (8.3%) | 4/72 (5.6%) |
| A abstentions | 14/36 | 30/72 |
| B−A observed | +0.8611 | +0.9444 |
| B−A CI | [0.8333, 0.9167] | [0.8611, 1.0] |
| B−E observed | +0.7778 | +0.8889 |
| B−E CI | [0.7222, 0.8333] | [0.7778, 0.9861] |
| Pre-specified criteria | 4 support criteria | B−A > 0 AND lower CI > 0 |
| Local-seen (B) | 12/12 (100%) | 19/24 (79.2%) |
| Normal | 12/12 (100%) | 24/24 (100%) |
| Heatmap detail | Per-run × per-agent | Not included in draft (24 runs too large for visual) |
| F8 heterogeneity | Reported | Not applicable (different fault allocation) |
| R=3 stability | 33/36 unanimous | Not reported in draft |

### Critical differences for content authoring

1. **B does not dominate local-seen in EXP3_V2** (79.2% < A's 100%). Step 23 must note this without dramatising it — it is a descriptive observation, not a failure of the primary contrast.
2. **No per-run heatmap** in the frozen draft. Step 21 should present the composition-bar figure but not fabricate a run-level heatmap. If the heatmap is desired, it must come from a separate frozen artifact, not from the draft.
3. **Pre-specified criteria differ**: Exp1 had 4 named support criteria; EXP3_V2 specifies B−A > 0 AND lower CI > 0 as the pre-specified criterion, with B−E reported only as supporting evidence. Step 20 must use the EXP3_V2 criterion language, not Exp1's.
4. **Bootstrap cluster count** is 24, not 12. The callout about small-sample uncertainty (Step 17's "Con soli 12 cluster…") should be adapted to "Con 24 cluster…" — still cautious, still a PoC, but acknowledging the doubled cluster count.

---

## 13 · SCIENTIFIC PRECISION CHECKLIST

| Claim/term | Required phrasing | Forbidden phrasing |
|---|---|---|
| B−A role | "contrasto primario" | "gate primary", "primary gate" |
| B−A interpretation | "Supportato sotto il criterio pre-specificato" | "Statisticamente significativo" |
| replication_supported | Requires conjointly B−A > 0 AND lower CI bound > 0 | Either condition alone |
| B−E role | "Supporting evidence for semantic specificity" | "Secondary gate", "second primary endpoint" |
| B−E CI | "Non è un criterio gating pre-specificato" | Treating B−E CI as an additional decision rule |
| Abstentions | "Contate come errore" | "Excluded", "filtered" |
| Secondary populations | "Descrittive, nessuna inferenza confirmatory" | "Confirm", "prove" |
| Cross-experiment | Must NOT combine Exp1 and Exp3v2 meta-analytically | "Combined evidence from both experiments shows…" |
| Scope | "All'interno di EXP3_V2" / "nel perimetro EXP3_V2" | Generalisation claims |
| Frozen provenance | "Tag `exp3-v2-results-frozen-001`" | Copying frozen files into the branch |

---

## 14 · RISKS AND OPEN QUESTIONS

### Risk 1: Kicker denominator inconsistency
**Severity:** Cosmetic (low).
Fase 1 kickers show "/ 17"; Fase 2 kickers show "/ 24". The topbar shows "/ 24". A reader scrolling through may notice the jump. Mitigation: a brief `<!-- note -->` comment at the boundary, or a CSS/JS fix that updates kicker denominators without touching the HTML source text of Fase 1 sections.

### Risk 2: No per-run heatmap in the frozen draft
**Severity:** Content gap (medium).
Step 17 includes a detailed 12-row heatmap. The EXP3_V2 draft does not provide per-run breakdown. Step 21 should not fabricate one. If desired, a separate frozen artifact must be produced and tagged. The walkthrough can reference it or leave it for a future patch.

### Risk 3: Fase 2 `<summary>` text
**Severity:** Naming (low).
The `<summary>` text "Fase 2 — Replica confirmatory (Experiment 3 V2)" is descriptive but long. It must fit the nav panel width (280px). At 13.5px font, this is approximately 48 characters — likely to wrap to two lines. Consider shortening to "Fase 2 — EXP3_V2 Confirmatory" (32 characters).

### Risk 4: Tag `exp3-v2-results-frozen-001` must exist before the patch is applied
**Severity:** Blocking (high).
The walkthrough and README will reference this tag. If the tag does not yet exist in the repository, the patch should be staged but not merged until the tag is created. The review cannot verify tag existence (REVIEW-ONLY).

### Open question: Fase 2 `<details open>` or closed?
Fase 1 uses `<details ... open>` (expanded by default). Should Fase 2 also start expanded? If the walkthrough is meant to be read sequentially, both phases expanded is appropriate. If Fase 2 is supplementary, it could start collapsed. **Recommendation:** `open`, matching Fase 1.

---

## 15 · SUMMARY OF REQUIRED ACTIONS (post-review)

When this review is approved and implementation begins:

1. **Create tag** `exp3-v2-results-frozen-001` on the commit containing the frozen EXP3_V2 outputs (prerequisite).
2. **Edit `docs/fot_walkthrough_conversazione.html`:**
   - Append CSS rules (after line 70, before `@media`).
   - Update topbar progress denominator (line 80).
   - Replace Fase 2 nav placeholder (line 91).
   - Insert 7 `<section>` elements between step-17's `</section>` and `<footer>`.
   - Optionally add 1 JS line for dynamic total.
3. **Edit `phase_b/README.md`:**
   - Update Experiment 3 V2 table row (status + description).
4. **Verify:** `git diff` on the committed patch must show zero modifications inside `<section id="step-1">` through `<section id="step-17">`.
5. **Do NOT** copy frozen output files into the working branch.
6. **Do NOT** perform any bootstrap, evaluator, or RNG computation.
7. **Do NOT** create cross-experiment meta-analytic claims.

---

*This review is REVIEW-ONLY. No files have been modified, no files have been created in the repository, no frozen outputs have been copied, no computation has been performed. The review examines the structural feasibility of the proposed documentation patch and provides a concrete implementation blueprint.*
