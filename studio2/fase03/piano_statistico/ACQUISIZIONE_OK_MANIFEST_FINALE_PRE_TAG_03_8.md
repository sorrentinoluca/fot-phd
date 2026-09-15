# Acquisizione dell'OK indipendente — manifest finale pre-tag 03.8

Data acquisizione: 2026-09-15T18:48:22+02:00.

Il verbale indipendente già presente nella sede preparatrice è acquisito senza
copiarlo, normalizzarlo o modificarlo. Questo record ne documenta provenienza,
identità e portata; non estende il verdetto e non produce un freeze.

## Artefatto acquisito

- Percorso:
  `studio2/fase03/piano_statistico/VERIFICA_MANIFEST_FINALE_PRE_TAG_03_8.md`.
- Dimensione consegnata nel mandato e ricalcolata prima della scrittura del
  presente record: **8.694 byte**.
- SHA-256 consegnato nel mandato e ricalcolato prima della scrittura:
  `5f6a600ae4c84d1eb7a82a229ca4a60589f29bc06386dee170fccd7ff2a7af8d`.
- Stato iniziale: unico file non tracciato nel worktree preparatore a HEAD
  `7a42bb6defdd69fd4ec981954ececd1f83bf5ca4`.
- Sede sorgente e destinazione: coincidono; non è stata creata una copia
  duplicata.

Dimensione e impronta vengono ricontrollate dopo staging e commit. Il valore
pregresso è attestato dal mandato di acquisizione; il verbale, per evitare
auto-riferimenti, rinvia alla propria nota di consegna e non incorpora il
proprio digest nel corpo.

## Identità e target della review

Il verbale dichiara:

- verdetto: **OK**, senza rilievi bloccanti;
- natura: review indipendente, read-only;
- base: `a5798c667dedcb85d3b745258fbc992e0c05841a`;
- candidato: `ec807dbaf2cb745ba96d397aac64a981f6fdeb7d`;
- tree candidato: `58ffd0b057dee7c1a1c399aaadd6c256d8658e34`;
- genitore unico: `a5798c667dedcb85d3b745258fbc992e0c05841a`;
- perimetro: il solo file aggiunto
  `studio2/fase03/piano_statistico/MANIFEST_FINALE_PRE_TAG_03_8.json`,
  14.768 byte, SHA-256
  `087d268d438ca6e98063346a5547849a05235a43712aebe56e007c46dcc1413d`;
- modello dichiarato: `claude-opus-4-8`, famiglia Claude Opus 4.8;
- provider e ambiente dichiarati: Anthropic, sessione Claude (Cowork);
- reasoning effort: non configurato come parametro separato e quindi non
  attestato come `high`;
- identità sessione dichiarata:
  `https://claude.ai/code/session_01H6p2273pdNzgi85fei134V`.

La divergenza dal modello suggerito nel prompt (`gpt-6-astra`, reasoning
`high`) è dichiarata dal revisore come osservazione non bloccante. Il modello
effettivamente usato resta quello riportato sopra; non viene sostituito o
reinterpretato nel record di acquisizione.

## Portata dell'OK

L'OK certifica soltanto il delta `a5798c6..ec807db`, il tree `58ffd0b` e il
singolo manifest. Non certifica:

- la consegna e il prompt nel successore `7a42bb6`;
- il verbale stesso o il presente record;
- una futura pubblicazione, il tag, il suo oggetto o il peeled;
- futuri record post-tag o dichiarazioni `freeze_effective=true`;
- harness D9, ordine label 1a, servizi, T5, controlli OOD 03.11, inferenze,
  simulazioni, pilot o run finali.

Il manifest verificato resta non efficace: `freeze_effective=false`, chiusura
03.8 e Fase 03 false, target/oggetto/peeled del tag nulli. La firma materiale
non è richiesta. 03.8 e la Fase 03 restano aperte.

## Controlli di acquisizione

- repository: `/Users/luker/fot-tep-finalizzazione-038`;
- branch: `codex/studio2-finalizzazione-038`;
- HEAD iniziale: `7a42bb6defdd69fd4ec981954ececd1f83bf5ca4`;
- remoto effettivo: `https://github.com/sorrentinoluca/fot-phd.git`;
- `refs/heads/main` remoto osservato:
  `8dbd2b49176c16f9e100e5f181c729b99d406a35`;
- tree e genitore del candidato riscontrati con Git;
- perimetro del candidato: un solo file, come dichiarato;
- tag `studio2-fase03-piano-statistico-frozen-001` assente dal remoto;
- nessuna altra modifica preesistente o attività Git concorrente rilevata.

I controlli 1–12 del verbale non sono ripetuti: il record conserva il loro
esito, inclusa la verifica 31/31 degli artefatti e il guardiano **NON PASS** su
base e candidato con 35 test, 14 fallimenti storici e 1 skip, senza
peggioramenti. L'acquisizione ricontrolla soltanto identità, byte e confine.

Il commit che contiene il verbale e il presente record è un successore
documentale e non può essere incluso nel proprio testo senza auto-riferimento.
Sarà identificato nella proposta successiva di pubblicazione e tag.
