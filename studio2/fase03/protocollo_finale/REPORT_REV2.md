# Registro di consegna — candidato protocollo finale rev2

2026-09-17. Mandato: `PROMPT_7_3_REV2_CANDIDATO.md`, copia in questa cartella.
Base esatta `e0db132fc6ef477bc054d8c02b3fb62f8c39da06`, branch
`codex/studio2-freeze-protocollo-finale`. Lavoro offline documentale. Nessuna modifica a
codice, ledger, runtime o artefatti congelati; nessun push, merge o tag; nessuna lettura di
credenziali, segnali/evidence di test o predizioni. Nuovo commit, non amend.

## Decisioni e motivazioni

Copia normativa byte-identica (SHA `535939de…accb2`), con tutte le motivazioni e il testo
per il paper. D1 è sviluppata in protocollo §1.2; D2 in §3.1-bis; D3 in §7.2 e §5; D4 in
§7.3. D5 conserva swap F1/F8/F10/F13, riuso librerie e asimmetria, E5 dopo il batch con
freeze proprio. L'addendum statistico è una nuova revisione separata dal piano congelato.

L'addendum verifica l'imparzialità rispetto all'assegnazione e distingue tale risultato
finito dalla media su nuovi run. Sotto le assunzioni esplicite di indipendenza e identica
procedura entro fault, Hoeffding H1/H2 resta valido condizionando alla permutazione.
Il bootstrap per run non mantiene il bilanciamento: non è dimostrato conservativo (controesempio
algebrico della varianza attesa a medie uguali, fattore 7/8). Celle fault × posizione con una
sola osservazione non consentono un bootstrap esatto non degenere. Tango su coppie eterogenee
resta approssimato; la vecchia simulazione IID non valida automaticamente il nuovo disegno.
Appaiamento, N, m e gerarchia restano invariati; le condizioni della loro validità sono scritte.

## Raccordo puntuale alle due review del predecessore

I due verbali sono committati invariati, conservando NON OK e l'identità e0db132; non sono
review di questa rev2. Non si dichiara chiuso un rilievo di implementazione con testo normativo.

| Rilievo | Recepimento rev2 | Residuo prima del freeze |
| --- | --- | --- |
| R1 | Il runner finale è parte del freeze, protocollo §7.1; rimossa la pretesa di eseguibilità col solo harness pilot | Commit e review 7.4-FIX, test offline/dry-run |
| R2 / C3 | Coordinate complete disponibili, digest/byte degli asset e stato reale nel JSON; §2.1 distingue release dati dai tag del repository codice | Per test-v1 mancano commit/ID di release e verbale di riscaricamento: S3 PENDING. Esistenza remota soltanto riferita dal verbale Claude, non riverificata qui |
| R3 | Ordine rem6 fino al commit rivisto → candidato → tag in main | Nessuna integrazione eseguita; f0d0393 da solo non include il runner |
| B1 | Token B-noLF, G_P, diff solo DECISION POLICY, file nuovo con hash proprio, token del prompt completo | Renderer/logging/diff e SHA da 7.4-FIX; S8 PENDING |
| B2 | Una finestra/run con D1, prerequisito di estrazione test a valle dell'assegnazione; esempi/label/agenti conservati dallo sviluppo | Quattro SHA finali, prova otto finestre e manifest input, rendibilità |
| C1 | Verificati byte via git show: rev002 criteri al commit ab43f0b20f45cdb475c0caf52c6f7afcbae50891; rev005 baseline a a00605862f627710347bd63c49f79a6d0a00135f | Nessuno documentale; tag originali intatti |
| C2 | Copia byte-identica VERIFICA_PILOT_03_13.md in questa cartella, SHA 944db3…abb2 | Raggiungibilità da main solo dopo integrazione del candidato, prima del tag |
| C4 | Maschera giorno per sensibilità §10.5 distinta da intervallo ultimo PASS→fallito e unione forense; query da ledger senza scrivere record terminali | Implementazione/query 7.4-FIX rivista; nessuna sostituzione tacita del piano |
| C5 | Canary invalido generato = MARKED, no retry; trasporto zero-token recuperabile entro Q; incertezza = STOP; contabilità tentativi/slot separata e barriera dieci slot | Implementazione/review; primo giorno deve PASS, secondo giorno marcato STOP |
| C6 | D3 recepita, motivazione, prova completa zero-token, cinque consecutivi persistenti e STOP immediati | Q_max, attese/timeout e T5 completo non disponibili |
| C7 | D4, tabella esempi; primaria sempre r1, astensione per disaccordo distinta dall'invalidità | Q3: ambito aggiuntivo e meno di tre validi da accettare |
| C8 | permutation(n), versione riferimento numpy 2.2.6, tupla stringhe, library_role, tre stage e quote; SHA PREP tenuti come storia | Pin finali quattro artefatti e commit eseguibile ancora PENDING |
| N1 | Dieci righe canary e venti SHA trascritti nel JSON, hash raw solo forense | Byte pilot nel nuovo target da verificare in 7.4 |
| N2 | Rinvio al contratto tracciato e ledger.reconcile_zero_token, non handoff temporaneo | Versione finale dopo review runner |
| N3 | X=100 esplicitamente inutilizzabile senza lista identificata prima degli invii | Elenco o mantenimento della riserva non utilizzata |
| N4 | Massimo sette giorni civili distinto da finestra mobile W=168 h; STOP oltre quota/tempo | Pianificazione operativa |

7.4-PREP punti 3–10 recepiti: punti 3–5 e 7 in §7.1, punto 6 in §7.2 (X non disponibile),
punto 8 in §6 (maschere separate), punto 9 in §5.2 (overhead da misurare), punto 10 in §6
(byte esatti canary). La scelta B-noLF era già nell'inventario PREP: nessun cambio di schedule
è attribuito al solo nome del token. Gli SHA storici non sono promossi a pin finali.

## Controlli e limiti della consegna

`CONTROLLI_DOCUMENTALI_REV2.json` registra il controllo di 41 fonti documentali, di cui 35
con confronto contro il blob al commit dichiarato, copie byte-identiche, dieci canary 2/4/4,
conteggio indipendente 2.244 prompt / 6.732 chiamate scientifiche / 6.902 base, SHA Markdown
coerente col JSON e limiti algebrici. Tutte le modifiche tracciate sono in protocollo_finale/.
I 32 pin repository originari restano identici; si correggono le coordinate, non i byte.

Guardian prima e dopo: 35 test, 14 fallimenti preesistenti, 1 skipped; nessun incremento.
Il log completo è fuori repository, path/hash nel record. Non è una review indipendente
né un PASS delle dipendenze scientifiche/operative. Nessuna suite del runner è stata eseguita:
non c'è codice nuovo in questo mandato. Nessuna simulazione del processo o inferenza LLM.

Al momento della consegna documentale, rem6 è ancora a 9e0e086 e non contiene un report
7.4-FIX consegnato/rivisto. Restano quindi segnaposto espliciti per commit/review runner,
renderer B-noLF, generatore/seme/versione assegnazione e quattro SHA: assegnazione, manifest
input, inventario, schedule. Anche Q_max/backoff/timeout, nuovo massimo e T5 sono pendenti.
Il report di pubblicazione/riscaricamento test-v1 non è disponibile nelle fonti locali lette;
nessun accesso di rete è stato effettuato per supplire al mandato offline.

## Decisioni residue dell'autore (dettaglio nell'addendum)

1. Q1: bootstrap solo descrittivo approssimato con limiti Hoeffding aggiuntivi per contrasti
   medi (raccomandazione), oppure nuovo metodo da validare prima del freeze.
2. Q2: mantenere Tango approssimato con verifica sintetica indipendente pre-dati, criteri
   fissati prima della verifica (raccomandazione), oppure Hoeffding anche H3, più conservativo.
3. Q3: audit §10.4 più aggregazione descrittiva su tutti i prompt, con triplette incomplete
   invalide (raccomandazione), oppure solo audit; specificazione comunque da approvare.

La quota retry numerica sarà sottoposta all'autore con la proposta 7.4-FIX, non anticipata.
Nessuna domanda riapre D1–D5. Il candidato resta **NO-GO al freeze e all'esecuzione**.
