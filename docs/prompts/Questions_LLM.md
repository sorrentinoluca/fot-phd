# Modalità domande — progetto FoT-TEP

**Leggi prima `Prompt_LLM.md`, in questa stessa cartella.** Contiene le regole
comuni: instradamento per tipo di richiesta, costi, precedenze sui conflitti,
divieto di inventare riferimenti, luogo unico della letteratura. Qui ci sono
solo le regole che valgono quando si risponde a domande invece di modificare.

**Sola lettura.** Nessuna modifica ai file, nessun commit, nessun tag.

## Instradamento fine dentro il piano della nuova fase

`docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` è ~32k token: non aprirlo tutto.

| Se la domanda è | Leggi | Costo |
| --- | --- | ---: |
| Com'è disegnata la nuova fase? | §8 | ~8k |
| Cosa manca prima di partire? | §0.1 + §11 | ~2k |
| Cos'è cambiato di recente? | §0 (changelog) | ~2,2k |
| Baseline federata | §9 | ~1,6k |
| Quali decisioni sono congelate? | §10 | ~2,4k |
| Perché una strada è stata scartata? | §3, §4 | ~0,8k |
| Difficoltà per-fault, prior art federato | §12 | ~5,4k |

⚠️ **§3 e §4 descrivono disegni scartati.** Spiegano perché quelle strade sono
state chiuse, non cosa si farà.

## I tre registri, da non confondere mai

Metà dei documenti descrive cose non ancora fatte. Distingui sempre:

- **«il piano prevede»** — un'intenzione, che può ancora cambiare;
- **«gli artefatti mostrano»** — un fatto misurato e congelato;
- **«la letteratura riporta»** — il lavoro di altri.

Per ogni numero cita **l'artefatto** da cui viene, non il documento che lo
racconta. Per ogni affermazione cita file e sezione.

## Confronti fra vecchia e nuova fase

**Non sono commensurabili.** L'esperimento concluso ha 4 fault e 4 agenti; la
nuova fase ne prevede 8 e 8, con un modello diverso e uno spazio di etichette
più ampio. Un confronto diretto dei numeri è scorretto: se la domanda lo
richiede, rispondi e **segnala il limite del confronto**.

## Contraddizioni: segnalale, non appianarle

Piano, registri di decisione e walkthrough possono divergere, e in punti noti divergono per ragioni
storiche. Quando succede **dillo**, indicando le due formulazioni e quale fonte
prevale secondo le precedenze. Non mediare, non scegliere in silenzio: la
contraddizione è essa stessa un'informazione utile.

## Trappole di contenuto

- Nel piano, **`Unknown` non è una classe**: è la forma dell'astensione e sta
  fuori dallo spazio delle etichette, che ha 9 pseudolabel opache. Chiarito nella
  revisione 5; testo più vecchio può suggerire il contrario.
- In §14.1 di `docs/letteratura.md` il colore indica la vicinanza **all'esperimento per cui
  è stato assegnato**, non la qualità del lavoro: 🟢 incide sul disegno o delimita un claim, 🟡 condivide un asse,
  🔴 è sfondo.
- **Due studi, non due versioni.** `_studio2` è lo studio in corso ed è oggi uno
  **scheletro**: per il disegno vale il piano, non quel file. `_v2` e la versione senza
  suffisso sono due esposizioni del **primo** studio, che non verrà citato nel paper nuovo:
  si consultano come record, non si usano come fonte per lo studio 2.
- La letteratura non sta in nessun walkthrough: vive in `docs/letteratura.md`, vale per
  entrambi gli studi, e la numerazione §14.x è rimasta invariata dopo lo spostamento.

## Come chiudere

Se la risposta non è nei documenti, **dillo** invece di dedurla. Elenca alla fine
cosa hai letto.
