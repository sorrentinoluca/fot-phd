# 7.3 rev2 — candidato del protocollo finale aggiornato alle decisioni dell'autore

Stessa worktree e branch del candidato (`e0db132`,
`/Users/luker/fot-tep-pubblicazione-consolidamento-0315-metriche`,
`codex/studio2-freeze-protocollo-finale`). `gpt-6-astra`, reasoning high. Offline, documentale;
nessuna modifica a codice, ledger, runtime o artefatti congelati; nessun push/merge/tag. Commit
nuovo, non amend.

**Normativo**: `/Users/luker/fot-tep/studio2/fase03/DECISIONI_AUTORE_7_3_REV2_2026-09-17.md`
(SHA-256 `535939de1d8c1e6f8185fd838a6bd20caca85b5f09c7908f679f251761aaccb2`). Copialo
byte-identico in `protocollo_finale/` e committalo: decisioni **e motivazioni** devono entrare nel
protocollo (l'autore lo chiede espressamente) e restare riusabili per i metodi del paper.
Rilievi da chiudere: `VERIFICA_PROTOCOLLO_FINALE.md` (R1–R3) e
`VERIFICA_PROTOCOLLO_FINALE_claude.md` (B1, B2, C1–C8), entrambi in `protocollo_finale/`.
L'implementazione corrispondente è in corso in parallelo (7.4-FIX, worktree rem6, da `9e0e086`):
gli SHA di assegnazione finestre, manifest di input, inventario e schedule restano segnaposto
espliciti finché quel lavoro non è consegnato e rivisto.

## Mandato

1. **D1 nel protocollo**: regola di assegnazione run→finestra, nome corretto («assegnazione
   casuale bilanciata per posizione, separatamente per fault»), quantità stimata (media uniforme
   sulle otto posizioni), condizioni di validità (indipendenza dai risultati, nessuna sostituzione
   selettiva), analisi per posizione secondaria e descrittiva con il limite delle otto unità
   indipendenti, appoggi in letteratura **con i limiti indicati dall'autore**, testo per il paper.
2. **Addendum al piano statistico 03.8** (`protocollo_finale/ADDENDUM_PIANO_STATISTICO_FINESTRE.md`,
   nuova revisione tracciata, il piano congelato non si tocca): verifica — non assumere — che
   bootstrap a cluster, appaiamento fra condizioni, gatekeeping H1→H2→H3 e margine *m* restino
   validi con campionamento bilanciato senza reinserimento; dì esplicitamente se il ricampionamento
   deve rispettare il bilanciamento per posizione o se il bootstrap per run resta corretto (e
   conservativo o no), con argomento. Se serve una scelta dell'autore, formulala con opzioni e
   raccomandazione.
3. **D2** `B-noLF`: definizione, token, renderer come file nuovo; S8 aggiornato.
4. **D3** al posto di `Q=0` assoluto: tabella a quattro esiti, definizione di «zero token»,
   STOP operativo (5 consecutivi per servizio, persistente, attesa crescente, tetto cumulativo
   separato), STOP immediati, motivazione. Aggiorna conteggio massimo e T5 con il tetto dei retry
   proposto da 7.4-FIX (segnaposto se non ancora disponibile).
5. **D4**: ripetizione 1 sempre primaria; aggregatore 2 su 3 altrimenti astensione per
   disaccordo; tre categorie registrate separatamente; tabella di esempi; caso con meno di tre
   esiti validi; ambito della sensibilità (solo audit 10 % come §10.4 oppure anche tutti i prompt
   come descrittiva aggiuntiva): proponi, con rinvio esatto al piano, e segnala se richiede
   l'addendum del punto 2.
6. **Correzioni delle review**: R1 (togliere «nessun meccanismo nuovo»: il runner finale è parte
   del freeze e va citato per commit dopo la sua review); R2/C3 coordinate immutabili e stato di
   pubblicazione delle release `evidence-v2` e `test-v1`; C1 coppie tag↔file; C2 verbale
   `VERIFICA_PILOT_03_13.md` da rendere raggiungibile da `main`; C4–C5 canary; C7 = D4; C8
   schedule (chiamata numpy `Generator.permutation(n)`, ordinamento sulla tupla, `library_role`,
   tre stage) come da `REPORT_7_4_PREP.md` punti 3–10, confermati dall'autore.
7. Checklist §8 e deviazioni §9 aggiornate (nuove: assegnazione delle finestre, retry zero-token,
   aggregatore; E5 rinviata a dopo il batch). Ordine di integrazione: rem6 fino al commit rivisto
   → candidato → tag `studio2-fase03-protocollo-finale-frozen-001`.

## Consegna

In chat: SHA del commit, domande che richiedono l'autore (numerate, con raccomandazione),
segnaposto ancora aperti. Niente altro.
