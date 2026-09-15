# D04 — matrice generata delle decisioni negli stadi aperti

Fonte: D04_DECISION_CONTRACT.json e osservazioni degli stessi test su 23859a2 e sul corretto.

**8 metodi; 240 assertion fallite sul respinto, zero sul corretto; zero errori di setup.**
I sottocasi non sono difetti distinti né metodi aggiuntivi.

216 mutazioni quota = 9 ruoli/stadi × 4 stati × 2 ingressi × 3 valori errati.
Ogni coppia stato/ingresso ha prima un controllo positivo: 72 complessivi.
Altri 14 sottocasi alterano i campi da cui dipende il ruolo; tutti rifiutati senza scritture.
Quote e valori ammissibili non sono cambiati. Snapshot resta diagnostico, non autorizzante.

| Stadio | Ruolo | Stato | Ingresso | Quota alterata | 23859a2 | Corretto | DB invariato |
| --- | --- | --- | --- | --- | --- | --- | --- |
| alternate_conformity | base | COMPLETED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | COMPLETED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | COMPLETED | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | COMPLETED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | COMPLETED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | COMPLETED | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | FAILED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | FAILED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | FAILED | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | FAILED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | FAILED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | FAILED | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | INTENT | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | INTENT | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | INTENT | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | INTENT | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | INTENT | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | INTENT | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | ZERO_TOKEN_PROVEN | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | ZERO_TOKEN_PROVEN | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | ZERO_TOKEN_PROVEN | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | base | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | COMPLETED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | COMPLETED | bind_stage | base | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | COMPLETED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | COMPLETED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | COMPLETED | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | COMPLETED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | FAILED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | FAILED | bind_stage | base | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | FAILED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | FAILED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | FAILED | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | FAILED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | INTENT | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | INTENT | bind_stage | base | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | INTENT | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | INTENT | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | INTENT | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | INTENT | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | ZERO_TOKEN_PROVEN | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | ZERO_TOKEN_PROVEN | bind_stage | base | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | ZERO_TOKEN_PROVEN | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| alternate_conformity | transport | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | base | COMPLETED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | base | COMPLETED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | base | COMPLETED | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| budget_probe | base | COMPLETED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | base | COMPLETED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | base | COMPLETED | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| budget_probe | base | FAILED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | base | FAILED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | base | FAILED | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| budget_probe | base | FAILED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | base | FAILED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | base | FAILED | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| budget_probe | base | INTENT | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | base | INTENT | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | base | INTENT | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| budget_probe | base | INTENT | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | base | INTENT | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | base | INTENT | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| budget_probe | base | ZERO_TOKEN_PROVEN | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | base | ZERO_TOKEN_PROVEN | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | base | ZERO_TOKEN_PROVEN | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| budget_probe | base | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | base | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | base | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | COMPLETED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | COMPLETED | bind_stage | base | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | COMPLETED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | COMPLETED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | COMPLETED | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | COMPLETED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | FAILED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | FAILED | bind_stage | base | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | FAILED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | FAILED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | FAILED | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | FAILED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | INTENT | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | INTENT | bind_stage | base | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | INTENT | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | INTENT | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | INTENT | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | INTENT | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | ZERO_TOKEN_PROVEN | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | ZERO_TOKEN_PROVEN | bind_stage | base | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | ZERO_TOKEN_PROVEN | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| budget_probe | transport | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | COMPLETED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | COMPLETED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | COMPLETED | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | COMPLETED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | COMPLETED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | COMPLETED | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | FAILED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | FAILED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | FAILED | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | FAILED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | FAILED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | FAILED | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | INTENT | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | INTENT | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | INTENT | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | INTENT | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | INTENT | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | INTENT | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | ZERO_TOKEN_PROVEN | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | ZERO_TOKEN_PROVEN | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | ZERO_TOKEN_PROVEN | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | base | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | COMPLETED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | COMPLETED | bind_stage | base | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | COMPLETED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | COMPLETED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | COMPLETED | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | COMPLETED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | FAILED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | FAILED | bind_stage | base | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | FAILED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | FAILED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | FAILED | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | FAILED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | INTENT | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | INTENT | bind_stage | base | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | INTENT | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | INTENT | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | INTENT | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | INTENT | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | ZERO_TOKEN_PROVEN | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | ZERO_TOKEN_PROVEN | bind_stage | base | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | ZERO_TOKEN_PROVEN | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| producer_conformity | transport | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | COMPLETED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | COMPLETED | bind_stage | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | COMPLETED | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | COMPLETED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | COMPLETED | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | COMPLETED | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | FAILED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | FAILED | bind_stage | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | FAILED | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | FAILED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | FAILED | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | FAILED | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | INTENT | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | INTENT | bind_stage | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | INTENT | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | INTENT | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | INTENT | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | INTENT | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | ZERO_TOKEN_PROVEN | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | ZERO_TOKEN_PROVEN | bind_stage | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | ZERO_TOKEN_PROVEN | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | remediation | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | COMPLETED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | COMPLETED | bind_stage | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | COMPLETED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | COMPLETED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | COMPLETED | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | COMPLETED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | FAILED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | FAILED | bind_stage | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | FAILED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | FAILED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | FAILED | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | FAILED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | INTENT | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | INTENT | bind_stage | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | INTENT | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | INTENT | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | INTENT | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | INTENT | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | ZERO_TOKEN_PROVEN | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | ZERO_TOKEN_PROVEN | bind_stage | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | ZERO_TOKEN_PROVEN | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | base | ACCETTA | RIFIUTA | sì |
| producer_remediation | transport | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| stability_gate | base | COMPLETED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| stability_gate | base | COMPLETED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| stability_gate | base | COMPLETED | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| stability_gate | base | COMPLETED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| stability_gate | base | COMPLETED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| stability_gate | base | COMPLETED | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| stability_gate | base | FAILED | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| stability_gate | base | FAILED | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| stability_gate | base | FAILED | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| stability_gate | base | FAILED | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| stability_gate | base | FAILED | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| stability_gate | base | FAILED | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| stability_gate | base | INTENT | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| stability_gate | base | INTENT | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| stability_gate | base | INTENT | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| stability_gate | base | INTENT | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| stability_gate | base | INTENT | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| stability_gate | base | INTENT | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |
| stability_gate | base | ZERO_TOKEN_PROVEN | bind_stage | UNKNOWN | ACCETTA | RIFIUTA | sì |
| stability_gate | base | ZERO_TOKEN_PROVEN | bind_stage | remediation | ACCETTA | RIFIUTA | sì |
| stability_gate | base | ZERO_TOKEN_PROVEN | bind_stage | transport | ACCETTA | RIFIUTA | sì |
| stability_gate | base | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | UNKNOWN | ACCETTA | RIFIUTA | sì |
| stability_gate | base | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | remediation | ACCETTA | RIFIUTA | sì |
| stability_gate | base | ZERO_TOKEN_PROVEN | reserve_base_or_remediation | transport | ACCETTA | RIFIUTA | sì |

## Campi da cui dipende il ruolo

| Campo | Ingresso | Rifiuto e DB invariato |
| --- | --- | --- |
| logical_id | bind_stage | sì |
| logical_id | reserve_base_or_remediation | sì |
| stage_run | bind_stage | sì |
| stage_run | reserve_base_or_remediation | sì |
| model | bind_stage | sì |
| model | reserve_base_or_remediation | sì |
| producer | bind_stage | sì |
| producer | reserve_base_or_remediation | sì |
| identity_json | bind_stage | sì |
| identity_json | reserve_base_or_remediation | sì |
| retry_of | bind_stage | sì |
| retry_of | reserve_base_or_remediation | sì |
| stage | bind_stage | sì |
| stage | reserve_base_or_remediation | sì |

## Altre prove e limiti

Ottavo retry senza rinuncia, guasto dopo controllo sulla stessa istanza e dopo restart;
triplette senza consumo parziale; lock con scrittore reale e altro stadio aperto;
rinuncia lecita fino a 15 trasporti e rifiuto del sedicesimo;
runner e CLI con zero client/server/nuovi invii, output e database invariati.

Finite single-field faults at listed states/entries; historical closed-stage and content checks remain separate.

Il guardiano dei campi D03 rimane separato e immutato. La nuova matrice aggiunge
la dimensione delle decisioni negli stadi aperti; non prova ogni combinazione futura.
