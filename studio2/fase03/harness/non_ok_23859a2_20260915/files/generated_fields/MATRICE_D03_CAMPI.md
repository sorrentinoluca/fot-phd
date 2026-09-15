# Matrice dei campi durevoli — generata dall’inventario

Fonte: [DURABLE_FIELD_CONTRACT.json](DURABLE_FIELD_CONTRACT.json). Default per nuovi campi strutturali, incluse le chiavi nominate di evidence/approval: **DA_COPRIRE**. I payload opachi improntati ereditano la classe N per tutti i discendenti.

N = normativo; F = forense. La prova SQL altera una colonna per volta; le varianti evidence/approval sono applicate in acquisizione, antenato retry e gate riconciliato. Non si sommano metodi, sottocasi e verifiche sovrapposte.

Inventario: **69 voci**, **56** esercitate dalle nuove mutazioni generate e **13** collegate alle prove di contratto storiche. Per queste ultime non si dichiara una nuova mutazione individuale di ogni campo. **37 varianti × 3 percorsi**, 11 controlli di contenuto comuni, 33 colonne SQL, 12 campi degli involucri di riconciliazione e 14 alterazioni di contenuti/impronte apparentemente plausibili.

| Campo | Classe | Copertura |
| --- | --- | --- |
| `pilot.id` | N | generated SQL field mutation |
| `stages.stage` | N | generated SQL field mutation |
| `stages.binding_json` | N | generated SQL field mutation |
| `stages.binding_sha256` | N | generated SQL field mutation |
| `requests.request_id` | N | generated SQL field mutation |
| `requests.logical_id` | N | generated SQL field mutation |
| `requests.stage` | N | generated SQL field mutation |
| `requests.stage_run` | N | generated SQL field mutation |
| `requests.model` | N | generated SQL field mutation |
| `requests.producer` | N | generated SQL field mutation |
| `requests.quota_kind` | N | generated SQL field mutation |
| `requests.retry_of` | N | generated SQL field mutation |
| `requests.identity_json` | N | generated SQL field mutation |
| `requests.status` | N | generated SQL field mutation |
| `requests.proof_sha256` | N | generated SQL field mutation |
| `requests.intent_utc` | F | generated SQL field mutation |
| `requests.completed_utc` | F | generated SQL field mutation |
| `requests.prompt_tokens` | F | generated SQL field mutation |
| `requests.completion_tokens` | F | generated SQL field mutation |
| `requests.total_tokens` | F | generated SQL field mutation |
| `requests.latency_ms` | F | generated SQL field mutation |
| `requests.detail_json` | F | generated SQL field mutation |
| `events.event` | N | generated SQL field mutation |
| `events.created_utc` | F | generated SQL field mutation |
| `events.artifact_sha256` | N | generated SQL field mutation |
| `events.detail_json` | N | generated SQL field mutation |
| `responses.request_id` | N | generated SQL field mutation |
| `responses.raw_json` | N | generated SQL field mutation |
| `responses.raw_sha256` | N | generated SQL field mutation |
| `responses.record_json` | N | generated SQL field mutation |
| `responses.record_sha256` | N | generated SQL field mutation |
| `receipts.request_id` | F | generated SQL field mutation |
| `receipts.capture_json` | F | generated SQL field mutation |
| `reconciled.evidence.request_id` | N | generated field variants across acquisition/retry/gate |
| `reconciled.evidence.request_identity_sha256` | N | generated field variants across acquisition/retry/gate |
| `reconciled.evidence.disposition` | N | generated field variants across acquisition/retry/gate |
| `reconciled.evidence.provider_request_id` | N | generated field variants across acquisition/retry/gate |
| `reconciled.evidence.provider_evidence` | N | generated field variants across acquisition/retry/gate |
| `reconciled.evidence.prompt_tokens` | N | generated field variants across acquisition/retry/gate |
| `reconciled.evidence.completion_tokens` | N | generated field variants across acquisition/retry/gate |
| `reconciled.evidence.total_tokens` | N | generated field variants across acquisition/retry/gate |
| `reconciled.approval.author` | N | generated field variants across acquisition/retry/gate |
| `reconciled.approval.decision` | N | generated field variants across acquisition/retry/gate |
| `reconciled.approval.evidence_sha256` | N | generated field variants across acquisition/retry/gate |
| `reconciled.evidence` | N | generated envelope field deletion |
| `reconciled.approval` | N | generated envelope field deletion |
| `reconciled.approval_sha256` | N | generated envelope field deletion |
| `reconciled.previous_status` | N | generated envelope field deletion |
| `reconciled.evidence_content_sha256` | N | generated envelope field deletion |
| `reconciled.approval_content_sha256` | N | generated envelope field deletion |
| `reconciled_integrity.request_id` | N | generated envelope field deletion |
| `reconciled_integrity.evidence_file_sha256` | N | generated envelope field deletion |
| `reconciled_integrity.approval_file_sha256` | N | generated envelope field deletion |
| `reconciled_integrity.evidence_content_sha256` | N | generated envelope field deletion |
| `reconciled_integrity.approval_content_sha256` | N | generated envelope field deletion |
| `reconciled_integrity.previous_status` | N | generated envelope field deletion |
| `outcome.outcome` | N | historical contract tests; no new per-field mutation claim |
| `outcome.diagnosis` | N | historical contract tests; no new per-field mutation claim |
| `outcome.records_sha256` | N | historical contract tests; no new per-field mutation claim |
| `outcome.artifact` | N | historical contract tests; no new per-field mutation claim |
| `frozen_gate.frozen` | N | historical contract tests; no new per-field mutation claim |
| `transport_invalidity.record` | N | historical contract tests; no new per-field mutation claim |
| `remediation_authorized.diff_sha256` | N | historical contract tests; no new per-field mutation claim |
| `remediation_authorized.template_sha256` | N | historical contract tests; no new per-field mutation claim |
| `remediation_authorized.template_text` | N | historical contract tests; no new per-field mutation claim |
| `remediation_authorized.approval` | N | historical contract tests; no new per-field mutation claim |
| `remediation_waived.effect` | N | historical contract tests; no new per-field mutation claim |
| `suspended.reason` | N | historical contract tests; no new per-field mutation claim |
| `note.*` | F | historical contract tests; no new per-field mutation claim |

Il [JSON completo](MATRICE_D03_CAMPI.json) contiene gli esiti rosso/verde e le corrispondenze storiche. Matrice simmetrica e matrice SQL sono rosse su a219bd4; tutte le aspettative generate sono verdi dopo il delta. La guardia controlla anche schema e campi nuovi annidati; non è una dimostrazione di esaustività per ogni valore o combinazione di guasti.
