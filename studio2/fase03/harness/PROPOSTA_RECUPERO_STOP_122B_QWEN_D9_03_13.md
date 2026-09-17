# Proposta offline di recupero dallo STOP 122B — Qwen D9 03.13

Versione: **1**

Esito dell'artefatto: **READY_FOR_INDEPENDENT_REVIEW**

Stato operativo: **STOP — nessuna esecuzione o autorizzazione prodotta**

Questa proposta parte dal commit `0523c9279a3e760bd001daf399267c642deda02d`
(tree `814c578f48e12f95fbfa0f19fd870881ac367958`) e usa soltanto evidenza già
durevole e ispezione locale statica. Non sono stati usati rete, VPN o tunnel; non sono state
effettuate chiamate, retry o remediation; il ledger reale e i JSON privati autorizzati non sono
stati modificati.

## 1. Evidenza acquisita e limiti di lettura

La review indipendente V2 è stata copiata byte-identica in
`reviews/VERIFICA_STOP_PRIMA_CHIAMATA_PRODUCER_QWEN_D9_03_13_V2.md`. Sorgente e copia hanno
SHA-256 `f19da5e4ec332a386fad8780dbf1db44188353fc9180ba1c0eae87d073ec924f`.
Il suo verdetto è `OK`. La V1 non è stata letta né reinterpretata.

Il ledger sospeso è stato aperto con SQLite `mode=ro&immutable=1`. SHA-256 prima e dopo:
`4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb`.
L'ispezione del raw è stata limitata a struttura e metadati; il testo del reasoning non è stato
letto semanticamente, valutato o trattato come insight.

| Campo durevole | Valore osservato |
| --- | --- |
| request / stage | `0fc7a507…f684`, `producer_conformity`, `agent_1`, quota `base` |
| stato | `COMPLETED`; una risposta certa e addebitabile |
| alias | atteso e osservato `qwen3.5-122b` |
| fingerprint | atteso `null`; osservato esatto `vllm-0.27.1-934a3247`; identità invalida |
| reasoning | campo testuale presente, 8.670 caratteri e 8.670 byte UTF-8 |
| content | `null` |
| terminazione | `finish_reason=length` |
| uso | prompt 1.395, completion 2.560 = `max_tokens` 2.560, totale 3.955 |
| validazione | primo tentativo non valido, classe `structure`, `JSON value is empty or not text` |
| accounting | locale 1.395 = server 1.395, `PASS` |

Hash forensi: raw `e6489e73fff212d4fd14cb061e16712fd87c7c14ed246e820a2155a2b5518d35`;
record `0136fe479bf875c777611128903e0cf316f5f67fe987a84d334b2a78fdd2f6a7`;
commitment accounting `7d1d94b8364ac53c18e539057c915d87146b05fdbe247e8371363dba12d486c2`;
binding `413aa66f799614bd6994f28e18ac5b883021e74d6aabc243c7dae0e78c7732a7`.

## 2. Tokenizer, client e interfaccia strutturata

Snapshot: `Qwen/Qwen3.5-122B-A10B-FP8@a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9`.
Le impronte locali coincidono con il contratto: tokenizer JSON `5f9e4d49…cb42`, tokenizer config
`316230d6…4ac8`, chat template `a4aee8af…f715`. Ambiente locale ispezionato: Python `3.13.9`,
`transformers 4.57.6`, `openai 1.109.1`.

Il template pinnato supporta deterministicamente la kwarg `enable_thinking=false`: nel generation
prefix produce un blocco `<think>` vuoto e già chiuso. `apply_chat_template` accetta kwargs.
Questo dimostra una capacità del rendering **locale**, non il supporto del server.

Il builder corrente non usa quel rendering per il trasporto: invia `messages` strutturati; il
validator del provider e `generation_kwargs` non accettano `chat_template_kwargs`; nessun controllo
thinking viene trasmesso. Quindi non esiste oggi un controllo no-thinking end-to-end supportato
dal contratto locale. `extra_body.chat_template_kwargs.enable_thinking=false` è un candidato
configurativo, non una capacità attestata: non può essere eseguito senza prova non generativa del
contratto del server, implementazione harness stretta e review indipendente.

Anche l'accounting deve cambiare insieme all'interfaccia: il guard locale oggi renderizza con i
default del template. Un candidato valido deve renderizzare con la stessa kwarg trasmessa e legarla
nel binding e nel commitment; altrimenti l'uguaglianza locale/server non prova lo stesso prompt.

## 3. Supplemento candidato di qualificazione

Il JSON compagno contiene l'oggetto esatto `qualification_supplement_candidate`; il suo digest
canonico è `d180061348b15bb0322cb75ae700bb97b1328994c8d572c98741455d5b0ef579`.
Esso consente soltanto questo aggiornamento candidato:

```json
{
  "returned_model": "qwen3.5-122b",
  "system_fingerprint": "vllm-0.27.1-934a3247"
}
```

Il fingerprint è conservato come valore opaco osservato una volta. Non prova revisione o byte dei
pesi, quantizzazione, served revision, versione vLLM nonostante il testo del valore, reasoning
parser, default di sampling, cap massimo o supporto server della chat-template kwarg. Il
supplemento è `OBSERVED_NOT_REVIEWED_NOT_AUTHORIZED`; non sostituisce una qualificazione
materializzata e indipendentemente verificata.

## 4. Trattamento T9: decisione dell'autore necessaria

La classificazione non è univoca nel testo congelato. L'ordine fattuale è: binding immutabile di
`producer_conformity` → intent → risposta completa/addebito → scoperta del fingerprint non nullo e
del canale reasoning non controllato → record identità invalida → evento create-once `suspended`.
T9 disciplina difetti delle 8 chiamate di conformità, ma non stabilisce se un difetto di
qualificazione del servizio scoperto solo dopo il trasporto entri nel suo denominatore.

La raccomandazione è **fallimento antecedente di qualificazione/configurazione**. La chiamata resta
comunque in S e non diventa gratuita; è non valutabile per T9 perché la configurazione identitaria e
l'interfaccia che dovevano essere congelate prima dello stage erano incomplete. Dopo correzione e
nuova review, un pilot successore può eseguire una nuova conformità base completa di 8 casi, senza
cambiare prompt, schema, validatore, input o ordine.

Se invece l'autore decide **prima osservazione invalida T9**, non si possono completare normalmente
le sette chiamate residue. L'unica via T9 sarebbe una `REMEDIATION_T9_001.md` separata, con un diff
concreto del solo prompt, nuova review/autorizzazione e ripetizione completa degli otto casi. Questa
via è oggi bloccata: il difetto osservato è dell'interfaccia thinking, non un difetto dimostrato del
prompt; inoltre il harness richiede un outcome FAIL completo di otto casi per autorizzare la
remediation. Qui non viene creato alcun diff del prompt e la remediation non è consumata.

## 5. Vie lecite per il ledger

### Via raccomandata: pilot successore con lineage esplicita

Il ledger attuale resta predecessore forense immutabile. Il successore importa **una sola volta
S=5**: le quattro richieste storiche già riconciliate più la richiesta 122B completata. Il pacchetto
di lineage deve legare pilot id e SHA-256 del predecessore, identità/disposizione delle cinque
richieste, review indipendente e autorizzazione dell'autore. Deve rifiutare import selettivi,
duplicati e doppi conteggi transitivi.

È la via meno attaccabile perché il ledger attuale contiene simultaneamente un binding immutabile
con fingerprint atteso `null`, il record `agent_1` completato invalido e un evento `suspended`
create-once. Il successore rende esplicito il cambio di configurazione senza reinterpretare il raw.

Lavoro richiesto prima di qualunque chiamata:

1. schema/migrazione harness per import di lineage S=5, append-only e exactly-once;
2. conteggi S=5 applicati a planned max e hard stop prima di ogni intent;
3. supporto stretto del solo campo no-thinking attestato, senza pass-through generico;
4. accounting locale con la stessa chat-template kwarg e commitment aggiornato;
5. test sintetici offline su duplicati, import transitivo, resume, identity mismatch e accounting;
6. review indipendente di harness/config/lineage, nuovo ACCEPT e nuova autorizzazione scritta.

### Alternativa: disposizione revisionata nello stesso ledger

È tecnicamente concepibile solo con una modifica harness più invasiva: aggiungere un evento di
disposizione riesaminata create-once, conservare `suspended` e binding originali, e introdurre un
nuovo stage/binding con lineage invece di rivalutare `agent_1` contro la nuova identità. Vanno
modificati e riverificati prerequisiti, outcome e guardie remediation. Non è raccomandata perché
crea semantica di overlay dentro un ledger sospeso.

Sono esclusi update/cancellazione di eventi, rebinding, reset, copia selettiva di righe, azzeramento
di quote, retry della risposta completata o accettazione retroattiva sotto una nuova identità.

## 6. Diff candidato redatto, esatto nella struttura e non applicato

Il diff normativo completo è espresso come JSON Patch nel file compagno. I valori privati di URL e
credenziali non sono riprodotti. Le variazioni sostanziali sono:

```diff
--- service_122b_03_13.private.json (autorizzato, non modificato)
+++ service_122b_03_13.private.json (candidato, non creato)
- "artifact_version": "1"
+ "artifact_version": "2-candidate"
- "source": "non-generative qualification ... SHA-256 4e7e2b67..."
+ "source": "base non-generative qualification SHA-256 4e7e2b67... plus embedded qualification supplement canonical SHA-256 d1800613..."
- "serving": "NOT_EXPOSED"
+ "serving": "system_fingerprint observed once as opaque exact value vllm-0.27.1-934a3247; served revision and implementation remain NOT_EXPOSED"
- "thinking": "NOT_EXPOSED; no thinking control is sent by the 122B producer configuration"
+ "thinking": "Pinned local template supports enable_thinking=false; current structured builder did not transmit it; server acceptance remains NOT_PROVEN"
+ "qualification_supplement": {"canonical_sha256":"d180061348b15bb0322cb75ae700bb97b1328994c8d572c98741455d5b0ef579","status":"OBSERVED_NOT_REVIEWED_NOT_AUTHORIZED"}
- service.identity_sha256 = "4e7e2b67caaf64be7064fb1499b6dcdea844480a2b368ec019d03fc22f210e80"
+ service.identity_sha256 = "d180061348b15bb0322cb75ae700bb97b1328994c8d572c98741455d5b0ef579"
- service.expected_response.system_fingerprint = null
+ service.expected_response.system_fingerprint = "vllm-0.27.1-934a3247"

--- producer_122b_03_13.private.json (autorizzato, non modificato)
+++ producer_122b_03_13.private.json (candidato, non creato)
- identity_sha256 = "4e7e2b67caaf64be7064fb1499b6dcdea844480a2b368ec019d03fc22f210e80"
+ identity_sha256 = "d180061348b15bb0322cb75ae700bb97b1328994c8d572c98741455d5b0ef579"
- expected_response.system_fingerprint = null
+ expected_response.system_fingerprint = "vllm-0.27.1-934a3247"
+ extra_body = {"chat_template_kwargs":{"enable_thinking":false}}
```

`max_tokens` resta **2.560**: il singolo troncamento non è una giustificazione indipendente e
prespecificata per alzarlo. Restano invariati schema, validatore, input, otto casi, ordine e prompt.
Il campo `extra_body` non è accettato dal builder attuale ed è quindi deliberatamente
**non eseguibile**. Dopo la materializzazione vanno ricalcolati dagli effettivi byte: hash del
documento servizio, hash del provider, allowlist, hash canonico della configurazione e nuova
autorizzazione; nessun placeholder è ammesso in file eseguibili.

## 7. Contabilità con S=5

La risposta completata ha consumato 3.955 token e non è `ZERO_TOKEN_PROVEN`: non può usare quota
trasporto. Il gate non ha retry; la sonda usa solo triplette intere e al massimo 7 trasporti
cumulativi; le otto chiamate 27B sono base e non finanziano riserva.

| Voce futura | Antecedente config (raccomandata) | Prima invalidità T9 |
| --- | ---: | ---: |
| conformità primaria base | 8 | 0 |
| remediation completa | opzionale 8 | 8, ma oggi bloccata |
| alternativo 27B | 8 | 8 |
| sonda | 3–9 | 3–9 |
| gate | 120 | 120 |
| base futura con alternativo, prima della riserva | 139–145 | 131–137 |
| futuro senza trasporto, includendo remediation T9 | 139–153 secondo esito | 139–145 |
| trasporto massimo se remediation preservata/usata | 7 | 7 |
| massimo futuro con alternativo e riserva | 160 | 152 |
| massimo cumulativo includendo S=5 | **165** | **157** |
| margine rispetto a hard stop 200 | **35** | **43** |

Senza alternativo i massimi cumulativi sono rispettivamente 157 (margine 43) e 149 (margine 51).
Nel ramo antecedente, se la remediation viene esplicitamente rinunciata, fino a 15 trasporti sono
disponibili soltanto nei perimetri consentiti dalla prespecificazione; la sonda resta comunque
limitata a 7 e il gate a zero. La formula resta `8 × remediation + trasporto ≤ 15`.

Un pilot successore non ricostituisce quote: cambia il contenitore, non il consumo. Il valore 200 è
un hard stop, non autorizzazione a spendere il margine.

## 8. Blocker prima di una futura esecuzione

- decisione scritta dell'autore sulla classificazione T9;
- prova non generativa e byte-backed del supporto server per l'esatto controllo no-thinking;
- supplemento e JSON candidati materializzati, con hash derivati e review indipendente;
- harness successore/lineage/accounting implementato e verificato offline;
- review indipendente di codice, configurazione, lineage e contabilità;
- nuovo ACCEPT e nuova autorizzazione scritta sul nuovo hash canonico e sul ledger successore.

Fino alla chiusura di tutti i blocker l'unico stato operativo valido resta **STOP**.
