# Acquisizione dell'OK indipendente — pacchetto firma 03.8 rev.10

Data: 2026-09-15T15:38:43+02:00.

Copia byte-identica del verbale, senza modificare o estendere il verdetto.

- Fonte: `/Users/luker/fot-tep-verifica-pacchetto-firma-038/studio2/fase03/piano_statistico/VERIFICA_PACCHETTO_FIRMA_03_8_REV10.md`.
- Destinazione: `/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/VERIFICA_PACCHETTO_FIRMA_03_8_REV10.md`.
- Dimensione: **17.345 byte**.
- SHA-256: `37c155fb27d6e7abba6b42ff4af2cc7af6487f15af8967475f1ae46c44417de1`.
- Base del delta verificato: `8a3f7ba706570201c5b622c4e0fc79529b1c8cfd`.
- Candidato verificato: `7cf523805710633ec3b4fecd4eb8b7c9504076bf`.
- Tree del candidato: `5c8c49ff33ac01c3a778515688e5c064ccbb0be4`.
- Successore documentale: il commit che contiene questo record e la copia del
  verbale; è distinto dal candidato e non è coperto dal suo OK. Il suo hash è
  lasciato fuori dal contenuto per evitare un riferimento autoreferenziale.

## Riscontro di provenienza e acquisizione

Prima della scrittura, il worktree preparatore
`/Users/luker/fot-tep-allineamenti-038-r1-r4`, branch
`codex/studio2-allineamenti-038-r1-r4`, era pulito a `7cf5238`; i due percorsi
di acquisizione non esistevano. `origin/main` e il main del remoto effettivo
coincidevano a `a00605862f627710347bd63c49f79a6d0a00135f`; la ref `main`
locale era `4f98a2973d2e1ca7932f19c34e9dd4c0498b8b43`.

La fonte era l'unico file non tracciato nel worktree indipendente del revisore,
in detached HEAD sul candidato esatto `7cf5238`, con tree coincidente. Dimensione
e SHA-256 sono stati verificati prima e dopo la copia; `cmp` ha confermato
l'identità byte per byte. Nessuna normalizzazione o correzione è stata applicata.

Il verbale dichiara come revisore Codex, modello `gpt-6-astra`, provider OpenAI,
effort `high`, sessione `01a0a1d9-8ccd-7893-b504-4fde93380ea0`, in una finestra
indipendente dalla preparazione. Il revisore precisa che la sessione conserva il
contesto delle precedenti review R1-R4 e D9 e che non costituisce una seconda
opinione di un modello diverso.

## Fonti e byte del pacchetto giudicato idoneo

| Artefatto | Byte | SHA-256 |
|---|---:|---|
| `DECISIONI_AUTORE_03_8_DA_SOTTOSCRIVERE_REV10.md` | 4.974 | `4a0a4e1fc2797ee7a81439110e164d43159c745007136c9dda7bed7759471cc8` |
| `DECISIONI_AUTORE_03_8_COPIA_FIRMA_REV10.md` | 6.585 | `d470a6ce477f31f85951df8d877d786429a56e2f34a369407ae590494c39f605` |
| `INVENTARIO_PACCHETTO_FIRMA_03_8_REV10.json` | 6.622 | `e83420d7d151bac88dea297bc880b8dc1dcde4d3999b61c32b96f76249ce00aa` |
| `ISTRUZIONI_FIRMA_MATERIALE_REV10.md` | 3.763 | `601754706b7c590bc338021cdf51327a82beffdc4fca475451752e8cf2df2082` |
| `PIANO_STATISTICO.md` rev.10 | 81.490 | `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a` |
| `PIANO_STATISTICO_FREEZE.json` (manifest storico, non congelato) | 25.894 | `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8` |
| `VERIFICA_PIANO_STATISTICO_REV10.md` | 12.478 | `d269e26d8cb4e23370577e1e193d90d9357d66f7c739e9d0669970edf71b0066` |

Le impronte sono state ricalcolate nel candidato prima dell'acquisizione e
coincidono con il verbale. L'atto originario, la copia firma, l'inventario, le
istruzioni, il piano, il manifest e i precedenti verbali non sono stati modificati.

## Portata del verdetto e passaggio autorizzato

Il verbale reca esito **OK** esclusivamente per il pacchetto al candidato
`7cf5238` e lo giudica idoneo alla successiva firma personale di Luca. L'OK non
si estende alla copia del verbale, al presente record, a un futuro artefatto
sottoscritto o ad altri byte successivi.

Il file esatto da usare come sorgente per una copia separata da firmare è:

`/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/DECISIONI_AUTORE_03_8_COPIA_FIRMA_REV10.md`

Luca deve compilare personalmente soltanto i campi `Luogo e data effettiva` e
`Firma dell'autore`, senza modificare il restante contenuto. Il percorso previsto
per la restituzione Markdown è:

`/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.md`

Per PDF, scansione o firma digitale va conservato il formato originale usando lo
stesso stem con l'estensione effettiva; il documento non va ricostruito
artificialmente in Markdown. Alla ricezione si dovranno verificare identità del
documento, completezza dei due campi, formato nativo, acquisizione separata,
dimensione e SHA-256 dell'artefatto firmato.

Questa acquisizione non appone una firma, non approva implicitamente l'ordine
label 1a o esecuzioni, non pubblica, non integra in `main`, non crea tag o freeze
e non autorizza servizi, simulazioni o pilot. 03.8 e Fase 03 restano aperte.
