# FoT — Prompt di ripresa e runbook di setup (per contesto server)

> **Come usare questo file.** Incollane il contenuto all'inizio di una nuova
> conversazione con l'assistente quando avrai gli accessi al server. La prima
> parte ("Contesto e scopo") serve ad allineare l'assistente sul progetto; la
> seconda ("Runbook") è la sequenza operativa già collaudata sul Mac, da
> ripetere sul server. Le note "LEZIONE APPRESA" segnalano gli ostacoli
> realmente incontrati durante il primo setup, così non li ripeti.

---

## 1. Contesto e scopo (allineamento del nuovo contesto)

### Cos'è il progetto
Sto realizzando e testando **FoT (Federation over Text)** — il paradigma del
paper *"Federation over Text: Insight Sharing for Multi-Agent Reasoning"*
(Yao, Rabbani, Li — arXiv 2604.16778, repo `github.com/dixiyao/FoT`) — con
l'obiettivo di **applicarlo nel dominio del fotovoltaico (PV)** e valutare i
risultati che se ne ottengono.

### Cos'è FoT in una frase
È una federazione "a livello di testo": invece di condividere gradienti o pesi
(come nel federated learning classico), più agenti risolvono task localmente
con un LLM **congelato**, ne distillano **reasoning trace testuali**, e un
server centrale le aggrega in una **insight library** unica, ridistribuita
uguale a tutti gli agenti per i round successivi. Nessun gradiente, nessun
fine-tuning: si scambia solo testo (trace in salita, insight in discesa).

### Distinzione importante da tenere presente
- **FoT puro** (questo esperimento): la insight library è **unica e uguale per
  tutti** gli agenti.
- **La mia idea di ricerca** (esperimento successivo, separato): una variante
  **personalizzata** in cui il server costruisce un contesto Gᵢ **diverso per
  ogni client** in base a un profilo φᵢ, con misura del *harmed-client rate*.
  FoT puro qui serve come **baseline forte** per quell'idea.

### Perché il fotovoltaico non è banale con FoT
FoT nasce per domini già testuali (matematica, coding, QA). Il PV è fatto di
serie temporali numeriche (potenza, irraggiamento, temperatura, curve I-V).
Quindi:
- Il task deve essere **di reasoning, non di regressione**. Candidato più
  pulito: **classificazione della modalità di guasto** (soiling, ombreggiamento
  parziale, degradazione, hot-spot, guasto di stringa, anomalia MPPT) o
  root-cause / raccomandazioni diagnostiche.
- Serve un **layer di verbalizzazione** a monte che trasformi curve I-V e serie
  di potenza in **descrizioni testuali/simboliche del sintomo**. Questo layer è
  **il vero collo di bottiglia** del progetto e NON fa parte di FoT: la qualità
  di tutto l'esperimento dipende dalla sua fedeltà, e va valutato separatamente
  dal contributo di FoT.
- Rischi noti da tenere d'occhio: propagazione di allucinazioni nella library,
  eterogeneità non-IID tra impianti (una library unica può danneggiare siti
  diversi → *trasferimento negativo*), assenza di verità diagnostica
  verificabile in tempi brevi, deriva stagionale, necessità di una tassonomia
  condivisa dei guasti.

### A che punto sono (stato al termine della prima sessione)
- **Step 1 COMPLETATO sul Mac**: ho riprodotto la baseline FoT end-to-end.
  Ciclo verificato: agente → soluzione → reflection → estrazione insight →
  persistenza trace → aggregazione centrale → `insight.md` popolato.
- Prova concreta: 2 agenti su 2 task matematici distinti (17×23; velocità media
  240 km/3 h). Il server ha prodotto una library di 13 insight, **generalizzando**
  oltre i due esempi (prova che l'aggregazione/distillazione funziona).
- Costo reale della run: ~$0.005.

### Cosa manca (prossimi step, in ordine)
1. **Portare il setup sul server** (questo runbook).
2. Definire il task PV di reasoning e la metrica (accuracy / macro-F1).
3. Costruire dataset diagnostico + partizione tra N agenti + test set separato.
4. **Progettare il layer di verbalizzazione** (curve I-V / serie di potenza →
   testo diagnostico). ← passo cardine, richiede prima di sapere **quali dati
   PV ho realmente** (formato, granularità, presenza di label/esiti noti).
5. Adattare i prompt di reasoning locale e di aggregazione al vocabolario PV.
6. Baseline di confronto: agenti isolati (round 1) vs con library (round 2+),
   a parità di modello/decoding/budget token.
7. Esecuzione round-by-round (il paper osserva convergenza ~round 3), più seed.
8. Valutazione: metrica media **e per-agente** (per cogliere trasferimento
   negativo), ispezione degli insight per allucinazioni.
9. Documentazione: separare merito di FoT da merito del layer di verbalizzazione.

---

## 2. Ambiente e vincoli del server (da chiarire/verificare all'inizio)

Durante il primo setup gli **accessi da amministratore mancavano**. Sul server
questi punti vanno chiariti subito con chi lo amministra:

- **Permessi**: sul server Ubuntu l'utente non era nei sudoers. Serve
  l'amministratore per installare pacchetti di sistema. Richieste minime da
  girargli in un colpo solo:
  - `sudo snap install openclaw`   (OpenClaw non era installato; suggerito via snap)
  - `sudo apt install python3.12-venv`   (mancava il supporto venv)
- **Accesso al modello LLM**: decidere se sul server si userà
  **(A) API via OpenRouter** (come sul Mac, semplice, a consumo) oppure
  **(B) un modello locale self-hosted** (costo a token azzerato, ma richiede
  GPU/VRAM adeguata e che il modello sia open-weight — i modelli proprietari del
  paper NON sono self-hostabili). Verificare GPU/VRAM disponibili e policy sui
  modelli open-weight.
- **Nota**: se si resta su OpenRouter, il setup sotto è identico a quello del
  Mac. Se si passa a locale, cambia solo la configurazione del provider in
  OpenClaw (endpoint Ollama/vLLM/LM Studio invece di OpenRouter) — il resto di
  FoT non cambia.

---

## 3. Runbook operativo (sequenza collaudata sul Mac)

Procedere **per checkpoint**: a ogni fase, verificare prima di andare oltre.
Ambiente di riferimento della prima esecuzione: Python 3.12, OpenClaw
2026.7.x, modello `openrouter/deepseek/deepseek-v4-flash` via OpenRouter.

### Fase 0 — Chiave/accesso al modello
- Se OpenRouter: avere un account **attivo e con credito** e una **API key
  valida** (`sk-or-v1-...`).
- **LEZIONE APPRESA**: una chiave che dà errore `401 "User not found"` indica un
  account non finalizzato / chiave orfana, non un problema di OpenClaw.
  Verificare prima l'account nel browser, poi rigenerare la chiave.

### Fase 1 — Ambiente Python
```bash
python3 --version            # deve essere >= 3.11
python3 -m venv ~/fot-env
source ~/fot-env/bin/activate
python -m pip install --upgrade pip
```
- **Checkpoint**: il prompt mostra `(fot-env)`.
- **LEZIONE APPRESA (server)**: se `venv` fallisce con `ensurepip is not
  available`, manca `python3.12-venv` → serve l'amministratore (vedi §2).
  Se manca del tutto `sudo`/`conda`, l'alternativa è Miniconda nella home
  (non richiede permessi), ma sul Mac è bastato venv.

### Fase 2 — Installare OpenClaw (PRIMA di FoT)
FoT gira **sopra** OpenClaw; senza, fallisce subito.
```bash
openclaw --help              # deve rispondere
```
- Sul Mac l'installazione è avvenuta via wizard interattivo (`openclaw onboard`).
- Durante il wizard, alle schermate **"Select channel"** e **"Search provider"**
  scegliere **"Skip for now"**: non servono per FoT (sono per chatbot su
  Telegram/Slack ecc. e per la web-search degli agenti).
- **LEZIONE APPRESA**: se cade la rete durante l'onboard, la chiave può salvarsi
  troncata/corrotta nello store → causa 401 successivi (vedi Fase 3).

### Fase 3 — Collegare OpenClaw a OpenRouter
```bash
export OPENROUTER_API_KEY="sk-or-v1-...chiave-intera..."
openclaw onboard --auth-choice apiKey --token-provider openrouter --token "$OPENROUTER_API_KEY"
```
Verifica **diretta** della chiave, bypassando OpenClaw:
```bash
curl -s https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer $OPENROUTER_API_KEY"
```
- Risposta con `"data": {...}` → chiave valida.
- Risposta `401 "User not found"` → account/chiave da sistemare (vedi Fase 0).

Probe attraverso OpenClaw:
```bash
openclaw models status --probe
```
- **Checkpoint**: lo status del profilo deve essere `ok`, non `401 · auth`.
- **LEZIONE APPRESA (gestione profili auth)**: in questa versione i profili
  stanno in uno **store sqlite**, non in `auth-profiles.json`. Se convivono un
  profilo `default` (rotto) e uno `manual` (valido):
  - forzare l'uso del profilo buono:
    `openclaw models auth order set --provider openrouter openrouter:manual`
  - il profilo escluso mostrerà `Excluded by auth.order` — comportamento atteso.
  - comandi utili: `openclaw models auth list`,
    `openclaw models auth paste-api-key --provider openrouter`.

### Fase 4 — Fissare un modello economico esplicito
Non lasciare `openrouter/auto` (sceglie a caso, costo/comportamento
imprevedibili). Impostare un modello economico esplicito:
```bash
openclaw models set openrouter/deepseek/deepseek-v4-flash
openclaw models status --probe      # deve dare 'ok' sul nuovo modello
```
- **LEZIONE APPRESA**: `openclaw models list` mostra solo il catalogo locale
  (pochi modelli). Un modello non elencato si usa lo stesso indicandone il nome
  esatto con `models set`. Se dà "model not found", copiare il nome esatto dalla
  pagina OpenRouter del provider (es. openrouter.ai/deepseek).
- Alternativa economica equivalente: `openrouter/google/gemini-2.5-flash-lite`.

### Fase 5 — Installare FoT
```bash
cd ~
git clone https://github.com/dixiyao/FoT.git
cd FoT
python -m pip install -e .
fot --help                   # deve mostrare i comandi
fot list                     # lista vuota, nessun errore
```
- **LEZIONE APPRESA**: il repo è grande (~300 MB); se il clone si interrompe per
  rete (`early EOF` / `RPC failed`), rimuovere il residuo e riprovare:
  `rm -rf FoT && git clone ...`.

### Fase 6 — Configurare `setting.yaml`
Nel file `~/FoT/setting.yaml`, impostare **entrambi** i modelli sul nome
OpenRouter scelto (formato `openrouter/...`):
```yaml
default_model: "openrouter/deepseek/deepseek-v4-flash"
aggregation_model: "openrouter/deepseek/deepseek-v4-flash"
openclaw_path: openclaw
local_reasoning_class: "fot.fot_client:OpenClawFoTClient"
global_reasoning_class: "fot.fot_server:OpenClawFoTServer"
```
- **LEZIONE APPRESA**: il default del file era un modello Google non allineato
  all'auth OpenRouter → va cambiato, altrimenti le chiamate falliscono.
- Lasciare le classi di reasoning ai default per la baseline.

### Fase 7 — Primo ciclo end-to-end (verifica)
```bash
cd ~/FoT
fot agent --name test  --message "What is 17 times 23? Show your reasoning."
# attendere fine + postprocess, poi:
fot list                                   # status: finished, postprocess: finished
cat ~/FoT/.fot/reasoning_traces/problem_000001.json   # deve contenere skills_extracted / insight_book

fot agent --name test2 --message "A train travels 240 km in 3 hours. What is its average speed? Show your reasoning."
fot list                                   # attendere che ANCHE test2 sia 'finished'
```
- **LEZIONE APPRESA**: se `reasoning_traces/` sembra vuota subito dopo il run,
  è perché il `postprocess` è ancora `running` — attendere ~15 s e ricontrollare
  con `fot list` (il campo `postprocess` deve essere `finished`).

### Fase 8 — Aggregazione (chiusura del ciclo)
```bash
fot aggregate
fot show agent --name aggregate
cat ~/FoT/.fot/insight.md                  # deve contenere gli insight aggregati
```
- **Checkpoint finale**: `insight.md` popolato con insight distillati da
  entrambe le trace = ciclo FoT completo funzionante. **Questo è il traguardo
  dello step 1** (non la riproduzione esatta dei numeri del paper, che dipende
  dal modello usato).

### Note operative utili
- Stato in `./.fot/` (override con `FOT_HOME`).
- `fot clean` rimuove stato per-agente e scratch di aggregazione **ma preserva**
  la insight library persistente. Per azzerare anche la library, rimuoverla a
  parte.
- FoT esegue i task in parallelo: con OpenRouter attenzione ai rate-limit (429)
  se si lanciano molti agenti insieme → ridurre il parallelismo.
- `auto_aggregate_trace_threshold` (default 25) fa scattare l'aggregazione
  automatica: per test manuali con poche trace, usare `fot aggregate` a mano.

---

## 4. Prima domanda da affrontare nella prossima sessione
**Quali dati fotovoltaici ho concretamente a disposizione?** Formato,
granularità temporale, presenza o meno di esiti diagnostici noti (label).
Senza questa risposta il layer di verbalizzazione (passo cardine) resta teorico.
Partire da qui.
