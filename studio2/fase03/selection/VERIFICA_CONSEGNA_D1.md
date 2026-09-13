OK

# Verifica indipendente della consegna documentale D1

Data: **2026-09-13**. Verificatore: **Codex**; modello richiesto per il sottoagente dal tool:
**gpt-5.6-sol**; autoidentificazione disponibile nel contesto: **GPT-5**. Agente/finestra separata
`/root/verifica_criteri`.

Oggetto limitato allo stato della consegna D1 dopo l'OK di `VERIFICA_CATALOGO_D1.md`, alla
corrispondenza fra manifest e documentazione e alle impronte dichiarate. In questo controllo non
sono state riaperte le fonti scientifiche, non sono stati rieseguiti il sorteggio o i test già
confermati e non sono stati consultati risultati per-fault, sonde o predizioni.

## 1. Stato e catena di attestazione

| Esito | Riscontro |
| :---: | --- |
| ✅ | `CATALOG_FREEZE.json` dichiara `status=reviewed_pending_commit_and_publication`, `independent_review_verdict=OK`, `d1_draw_executed=true` e `catalog_frozen=false`. La condizione di efficacia richiede ancora verifica OK, commit raggiungibile da `origin/main` e pubblicazione del tag annotato dedicato. Non presenta il catalogo come già congelato. |
| ✅ | `CRITERIA_FREEZE_rev002.json` usa lo stesso stato post-verifica, conserva `catalog_frozen=false` e registra l'OK della verifica D1. Il proprio `freeze_tag` è il futuro tag del catalogo; i metadati del precedente freeze dei soli criteri restano confinati sotto `criteria_origin`. Il vecchio tag non viene usato per attestare il nuovo stato D1. |
| ✅ | `catalog_freeze_manifest` nella rev. 2 punta ai **6.894 byte** correnti di `CATALOG_FREEZE.json`, SHA-256 `68b8461a6382c93e1a5dd8dc6c9def66b26b2ec865f0bc0786dd88fa95acedda`, con stato e ruolo `reviewed_catalog_candidate_pending_commit_and_publication` coerenti. Durante il controllo era rimasto il precedente ruolo `pending_D1_review`; è stato corretto prima di questo verdetto e il collegamento è stato ricontrollato. |
| ✅ | La lista `changed_fields` della rev. 2 coincide esattamente con la differenza delle chiavi di primo livello rispetto alla rev. 1, includendo per convenzione il campo autoriferito. `independent_review_verdict` non compare più fra i campi cambiati perché vale `OK` in entrambe le revisioni, pur riferendosi a verifiche diverse nei rispettivi contesti. |
| ✅ | `VERIFICA_CATALOGO_D1.md` è rimasta invariata dopo l'emissione dell'OK: **10.350 byte**, SHA-256 `e0227be49d75b8f1e680625f1ab9ba260a3d7e7967426388f2e6c84bb577a455`. |

## 2. Impronte e corrispondenza del catalogo

| Esito | Riscontro |
| :---: | --- |
| ✅ | Tutte le **7** coppie SHA-256/dimensione elencate in `CATALOG_FREEZE.json` coincidono con i file correnti: registro normativo, freeze rev. 1, snapshot dello script eseguito, log originario, fattibilità, replay corretto e test di regressione. |
| ✅ | I **4** snapshot storici sotto `criteria_origin.files` coincidono con i blob al `criteria_origin.source_commit`; il piano vivo corrente non viene confuso con quello snapshot storico. |
| ✅ | I **4** collegamenti principali della rev. 2 (`supersedes`, `d1_draw_record`, `catalog_freeze_manifest`, `validated_replay_script`) coincidono per hash e dimensione. Lo snapshot dello script originario, referenziato anche nel record D1, coincide inoltre con l'impronta già confermata nel riesame. |
| ✅ | Il catalogo nei manifest, nel piano e nelle tabelle Markdown/HTML è **F1, F2, F3, F8, F10, F13, F14, F15**; i nuovi fault sono **F2/F3/F14/F15**, la composizione è 3/2/1/2 e H={F3,F15}. Non sono emerse trascrizioni discordanti. |

## 3. Piano, walkthrough e provenienza

| Esito | Riscontro |
| :---: | --- |
| ✅ | Le modifiche al piano sono limitate allo stato D1 in §0.1, al richiamo in §6.1 e all'esito nella voce D1. Dichiarano l'estrazione verificata, il catalogo ancora in attesa di commit e pubblicazione e l'assenza di approvazione per OOD/D11. Le decisioni OOD e D11 diventano lavorabili perché il catalogo è noto, ma restano aperte. |
| ✅ | Il walkthrough conserva in §4.1 lo stato storico della chiusura dei soli criteri e aggiunge in §4.2 l'estrazione successiva. Riporta il primo NON OK, il successivo OK, la conservazione di log e script originari, i limiti scientifici e lo stato “verificato, non ancora congelato”. Non attribuisce a D1 rappresentatività, potenza o risultati diagnostici. |
| ✅ | Le sezioni §4.1 e §4.2, l'introduzione, la voce §6.1 e l'avviso sulle dipendenze hanno testo e ordine dei collegamenti equivalenti nelle versioni Markdown e HTML. Le due tabelle del catalogo corrispondono al manifest. |
| ✅ | Un controllo indipendente trova **179** collegamenti o ancore locali validi nei quattro documenti dichiarati, senza destinazioni o ancore mancanti. Gli hash dei due walkthrough e del piano coincidono con `D1_DELIVERY_CHECK.json`: rispettivamente `6c82a722…d9480d`, `60307c84…1027a` e `bcae7b97…41878`. |
| ✅ | La sezione 6 di `studio2/PROVENIENZA.md` identifica le fonti effettive di D1, distingue dati e continuità prespecificata e rinvia l'efficacia del catalogo a verifica, commit e tag dedicato. Non introduce la proposta OOD/D11 nel freeze. |

`D1_DELIVERY_CHECK.json` è quindi coerente con i riscontri ripetuti qui: stato PASS, 7 hash del
catalogo, 4 snapshot storici, 4 collegamenti della rev. 2, parità del walkthrough, tabella del
catalogo corrispondente e OOD/D11 non approvati. I valori dei test documentali
(35 eseguiti, 14 fallimenti preesistenti, 1 skipped) e dei quattro test di regressione sono quelli
già confermati nei controlli precedenti; non sono stati rieseguiti in questo passaggio.

## 4. Verdetto e limiti

**OK — la consegna D1 documentata è coerente e pronta per essere presentata all'autore come
pacchetto concreto da pubblicare.** L'esito riguarda D1 e la sua documentazione; non approva OOD,
D11, D2, il producer alternativo, la generazione di nuovi run, il protocollo scientifico o
l'esecuzione del modello.

Il pacchetto è ancora non committato e non pubblicato. `catalog_frozen=false` resta pertanto lo
stato corretto; l'efficacia e qualsiasi attestazione di disponibilità su `origin/main` richiedono
il commit finale e il tag annotato proposto. Dopo tali operazioni va controllato che commit e tag
contengano esattamente gli artefatti presentati e che le rispettive impronte coincidano. Questo
controllo non ha eseguito commit, tag o push.
