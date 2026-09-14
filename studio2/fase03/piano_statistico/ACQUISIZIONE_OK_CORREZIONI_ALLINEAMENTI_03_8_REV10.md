# Acquisizione dell'OK indipendente — correzioni R1–R4, 03.8

Data: 2026-09-15T00:34:19.999795+02:00.
Copia byte-identica, senza modificare o estendere il verdetto.

- Fonte: `/Users/luker/fot-tep-verifica-correzioni-allineamenti-03-8-rev10/studio2/fase03/piano_statistico/VERIFICA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md`.
- Destinazione: `/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/VERIFICA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md`.
- Dimensione: **20.816 byte**.
- SHA-256: `9248c42572a20388ddf5af976840e68fdc908e545312a63234167778ce53a256`.
- Candidato verificato: `9a56d12d0633a0c9790c48792182f26fc6eb424a`.
- Tree: `e35e5ca661325657715dce6723e4e8ec09540101`.
- Base del delta verificato: `1a21fd260ad2df6a3b04ffb6fa5e2d642a3f63b1`.
- Consegna successiva distinta: `16f227439357b07b7dc945f67ab5a4368c12b684`.

## Revisore e perimetro

Come documentato dal verbale: Codex, modello `gpt-6-astra`, provider `openai`,
effort `high`; task/sessione `01a0a1d9-8ccd-7893-b504-4fde93380ea0`.
Identità letta dal revisore nei record session_meta/turn_context indicati nella fonte;
non è stata ricostruita o nuovamente attestata dal preparatore.
Worktree revisore: `/Users/luker/fot-tep-verifica-correzioni-allineamenti-03-8-rev10`,
detached sul candidato, con il solo verbale non tracciato al riscontro.

È indipendente dal preparatore. **Limite dichiarato:** stessa sessione che aveva
emesso il precedente NON OK, proseguita per incarico dell'autore; non è una nuova
task senza contesto né una seconda opinione di modello diverso. Nessun sottoagente.
L'OK copre le correzioni R1–R4 e la coerenza documentale risultante del candidato,
non il futuro recepimento D9, che richiede review del proprio delta.

Il verbale identifica anche il record D9 esterno `aaba893dff8c62f9f9281eec7423eee020235e03`:
ruoli approvati e registrati localmente; al candidato verificato manca l'acquisizione
nel ramo 03.8. Tale acquisizione avviene successivamente, non viene retrodatata.

## Preflight e preservazione

Worktree preparatore `/Users/luker/fot-tep-allineamenti-038-r1-r4`, branch `codex/studio2-allineamenti-038-r1-r4`,
pulito prima di scrivere, HEAD 16f2274. Origin/main e main remoto effettivo
coincidono a `a00605862f627710347bd63c49f79a6d0a00135f`. Main locale resta
`4f98a2973d2e1ca7932f19c34e9dd4c0498b8b43`. Copia principale a
`819b12e97fb94d501032655ec2f226139e6c5ca5`, con non tracciati preesistenti,
non usata per checkout o integrazione. Worktree e file delle altre finestre intatti.

Catena conservata: 4503cb6 NON OK → 2520e7a consegna → 1a21fd2 acquisizione
NON OK → 9a56d12 correzioni → 16f2274 consegna → presente acquisizione OK.
Il precedente verbale NON OK e tutti gli artefatti statistici/review restano
byte-identici. L'acquisizione è separata dal successivo commit di acquisizione
D9 e dal recepimento documentale. Controllo iniziale del guardiano: 35 test,
14 fallimenti storici, 1 skip, 0 errori, exit 1, stessi identificativi/subtest
nei controlli di 9a56d12; **non PASS**.

Nessuna firma, freeze, pubblicazione, chiusura 03.8/Fase 03, qualifica servizi,
approvazione ordine label o autorizzazione al pilot deriva dall'OK acquisito.
Nessun push, merge, tag, inferenza, API o simulazione.
