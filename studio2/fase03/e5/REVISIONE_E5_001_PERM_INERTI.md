# REVISIONE_E5_001 — coppie PERM inerti (2026-09-19, decisione dell'autore)

Revisione dichiarata **dopo** il tag `exp5-protocol-frozen-001`, che non viene toccato.

**Rilievo (G3, lotto test).** In 8 coppie PERM su 96 lo scambio della colonna della famiglia
non cambia il testo verbalizzato: il blocco `CASE TO DIAGNOSE` di PERM è identico a quello di
FULL, quindi il prompt PERM è byte-identico al portante B-LF. Per famiglia: `diff` 6/24,
`level` 1/32, `residual` 1/24, `trend` 0/16. OMIT: 0/96. Il builder congelato
`build_e5_prompts.py` si ferma («S18: the case block did not change»).

**Decisione.** Le coppie restano. Niente rigenerazione del derangement (PROTOCOLLO_E5 §7, §9):
il derangement è quello realizzato e la corruzione è definita sulla colonna, non sul testo.
Le 8 coppie si inviano come le altre (R=3) e portano `inert: true` in manifest, schedule e
punteggi.

**Analisi.** Il primario usa tutte le 96 coppie PERM: è l'effetto dello scambio così come è
stato realizzato, e una corruzione che non arriva al testo fa parte di quell'effetto. La
sensibilità esclude le coppie inerti e riporta il contrasto condizionato a una corruzione
visibile nel testo. Nelle coppie inerti FULL e PERM differiscono solo per il rumore di decoding.
OMIT non è toccato: un OMIT inerte resta un errore.

**Codice.** Gli 8 attesi sono fissati in `INERTI_ATTESI_E5.json`: G3 e la materializzazione rifiutano qualunque altro insieme. `build_e5_prompts_rev1.py` è il builder congelato con questa sola regola cambiata:
un blocco PERM invariato viene registrato come inerte invece di fermare la build. Sui dati
reali: 192 prompt, 8 inerti, 576 chiamate. `run_e5_execute.py` e `verifica_e5_g3.py`
accettano un inerte solo se il flag corrisponde ai byte, e solo nel braccio PERM.
