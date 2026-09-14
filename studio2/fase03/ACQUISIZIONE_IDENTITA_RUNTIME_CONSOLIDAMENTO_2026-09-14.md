# Acquisizione mirata dei metadati runtime del consolidamento

**Data:** 2026-09-14, Europe/Rome  
**Perimetro:** raccordo comune 03.6→03.12→letteratura, correzione documentale 03.15 e raccordo
metriche 03.9→03.10.  
**Esito:** riscontro positivo per l'esecutore Codex della correzione `10582798`; nessun nuovo
riscontro verificabile per l'ID sessione o il reasoning del revisore del verbale metriche E.

Questo record integra, senza modificarli, i verbali acquisiti. Riporta soltanto campi necessari a
collegare ruolo, sessione e candidato. Non acquisisce log di conversazione, configurazioni o
directory di sessione e non usa autore/committer Git o stile redazionale come prova d'identità.

## 1. Riscontri

| Ambito | Ruolo e candidato | Riscontro | Fonte | Limite |
|---|---|---|---|---|
| Raccordo comune | Esecutore di `e82b5a0` | OpenAI Codex Desktop; sessione `01a0a0b9-fc72-79b1-81b4-a4d5daa38f94`; modello `gpt-5.6-sol`; effort `high` | `studio2/fase03/evidenze_verifica_raccordo/esecutore_metadata.json` | Il metadato collega la sessione all'esecuzione registrata; non sostituisce la verifica del candidato. |
| Raccordo comune | Revisore di `e82b5a0` | OpenAI Codex Desktop; sessione `01a0a0e2-5a0b-7bc3-a111-b41f24734216`; modello `gpt-6-astra`; effort `high` | `studio2/fase03/evidenze_verifica_raccordo/runtime_metadata.json` e verbale A | Valido per il perimetro verificato dal verbale A, non per il consolidamento finale. |
| 03.15 | Esecutore del delta R1/R2 `9b6bd64..10582798` | OpenAI Codex Desktop; sessione `01a0a0e3-c3bd-7523-90ca-b5f28a40461f`; modello `gpt-5.6-sol`; effort `medium`. La chiamata runtime delle 18:07:33Z registra il commit e l'output delle 18:07:34Z restituisce l'hash completo `10582798eb5a4b52672bfbcb1cc028adcb73e9f1`. | `/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T19-07-56-01a0a0e3-c3bd-7523-90ca-b5f28a40461f.jsonl`: session meta riga 1, turn context riga 8, chiamata riga 460, output riga 463 | È un riscontro runtime locale dell'esecuzione, non una seconda review. Il log non è copiato nel repository. |
| 03.15 | Revisore correttivo C | Il verbale dichiara Claude Cowork, modello configurato `claude-opus-4-8`, sessione `session_013BLwcitiaqnqjNBLvV2mhH`; effort non esposto. | `studio2/fase03/paper_sections/VERIFICA_DELTA_RACCORDO_0315.md` | Identità e limite sono quelli dichiarati dal verbale; nessun log di sessione è stato acquisito. |
| Metriche | Esecutore e autore del controllo D su `e82b5a0..3360867` | Il verbale dichiara Claude Cowork/Agent SDK, modello configurato `claude-opus-4-8`, sessione `session_01CHTctYBYq1nnbumDuHrCsC`; reasoning non esposto. L'indice locale Claude collega esattamente tale sessione alla cartella `/Users/luker/fot-tep`. | `studio2/fase03/harness/VERIFICA_INTEGRAZIONE_RACCORDO_METRICHE_ESECUTORE.md`; `/Users/luker/Library/Application Support/Claude/local-agent-mode-sessions/19642685-93ae-4cdf-a4eb-e247e2be2c6f/7b60e72c-a2c7-4177-9ab4-ee4492b37b9f/remote-session-spaces.json` | Il collegamento alla cartella non dimostra indipendenza; D resta esplicitamente non indipendente e il modello servente può differire da quello configurato. |
| Metriche | Revisore successivo E su `e82b5a0..3360867` | Il verbale dichiara soltanto “OpenAI Codex, modello basato su GPT-5”, prodotto Codex desktop. | `studio2/fase03/harness/VERIFICA_INTEGRAZIONE_RACCORDO_METRICHE_INDIPENDENTE.md` | ID sessione/task, modello preciso ed effort restano non verificabili. Le occorrenze trovate nei log Codex locali derivano da letture successive del verbale o dal contesto orchestratore e non costituiscono prova di paternità. |

## 2. Valutazione dell'indipendenza

- A e C dichiarano verifiche in sessioni distinte dagli esecutori e conservano le proprie prove di
  perimetro; i metadati qui registrati non ampliano i relativi OK.
- D è un controllo dell'esecutore e resta non indipendente anche se sessione e progetto sono
  collegati localmente.
- E è acquisito come successivo verbale di verifica; la copia isolata descritta nel verbale è una
  misura tecnica utile, ma da sola non prova l'indipendenza dell'identità. L'assenza di un ID
  runtime verificabile resta un residuo documentale non bloccante.
- Nessuna delle identità sopra estende gli OK pregressi al merge di consolidamento
  `4ba2ad6e4a298411b4f0f7572ad3ef8e55948015` o alle acquisizioni successive.

## 3. Operazioni e limiti

La ricerca è stata limitata ai manifest/evidenze già acquisiti, ai file dei verbali e agli indici
runtime locali contenenti gli identificativi esatti. Non sono stati importati log completi, né
lette o copiate credenziali. Il riscontro mancante per E va eventualmente colmato dall'autore con
un identificativo sessione/task esportato dalla finestra che ha prodotto il verbale; non è
necessario per mantenere E byte-identico o per sottoporre a review il candidato locale.
