#!/usr/bin/env python3
"""03.13-REV27B: approved config revision, 27B producer requalification, suspension reconciliation.

Plan-only unless ``--execute --acknowledge REVISE_PHASE03_PILOT_CONFIG``.  Offline: no provider
call.  Writes new ``.rev2`` files next to the originals (originals stay byte-identical), replaces
the execution configuration (previous bytes kept as ``.pre_rev2``), records ``config_revision``
and ``suspension_reconciled`` in the ledger, then runs the offline preflight.  Idempotent.
"""
from __future__ import annotations

import argparse
from contextlib import closing
from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.harness.common import (HarnessError, canonical_json, load_json,  # noqa: E402
                                           sha256_file, sha256_text)

ACK = "REVISE_PHASE03_PILOT_CONFIG"
PILOT03_RUNTIME = Path("/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03")
PILOT03_SUSPENDED = "19a9b37269bede1b62799cf3ac5819557dc19a5273aa53099f04b202bb94b207"
PILOT03_FINGERPRINT = "vllm-0.28.0-5fc21ed4"
STAGE = "alternate_conformity"
ROLE = "27B"
NO_THINKING = {"chat_template_kwargs": {"enable_thinking": False}}
BACKUP = ".pre_rev2"
REVISION_APPROVAL = "config_revision_01_03_13.private.json"
SUSPENSION_APPROVAL = "suspension_reconciliation_03_13.private.json"


def rev2_path(path: Path) -> Path:
    name = path.name
    if name.endswith(".private.json"):
        return path.with_name(name[: -len(".private.json")] + ".rev2.private.json")
    return path.with_name(path.stem + ".rev2" + path.suffix)


def _dumps(value) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _sha(path: Path):
    return sha256_file(path) if path.is_file() else None


def _write_once(path: Path, data: bytes, changes, *, replace=False):
    before = _sha(path)
    if before == sha256_text(data.decode("utf-8")):
        changes.append(dict(path=str(path), before=before, after=before, action="UNCHANGED"))
        return
    if before is not None and not replace:
        raise HarnessError(f"refusing to overwrite a different existing file: {path}")
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)
    changes.append(dict(path=str(path), before=before, after=_sha(path), action="WRITTEN"))


def _ledger_view(path: Path, request_id: str):
    # Read-only; ``immutable`` only when no WAL sidecar may hold committed pages.
    wal = Path(str(path) + "-wal")
    uri = f"file:{path}?mode=ro" + ("" if wal.exists() else "&immutable=1")
    with closing(sqlite3.connect(uri, uri=True)) as c:
        c.row_factory = sqlite3.Row
        events = {r["event"]: r for r in c.execute("SELECT * FROM events")}
        binding = c.execute("SELECT binding_json FROM stages WHERE stage=?", (STAGE,)).fetchone()
        rows = list(c.execute("SELECT request_id,status,intent_utc,stage FROM requests"))
        response = c.execute("SELECT raw_json FROM responses WHERE request_id=?", (request_id,)).fetchone()
    return events, (json.loads(binding[0]) if binding else None), rows, (json.loads(response[0]) if response else None)


def plan(*, config_path: Path, ledger_path: Path, pilot_id: str, author: str, reason: str,
         fingerprint: str, suspended_request_id: str) -> dict[str, Any]:
    """Compute every target file deterministically, and refuse before any write."""
    from studio2.fase03.harness.d9 import no_thinking_template_kwargs
    from studio2.fase03.harness.guards import response_identity_valid
    from studio2.fase03.harness.ledger import (IDENTITY_SUSPENSION_REASON, PilotLedger,
                                               _diff_paths, digest)
    if not author.strip() or not reason.strip():
        raise HarnessError("author and reason are required")
    config_path = Path(config_path).resolve()
    backup = config_path.with_name(config_path.name + BACKUP)
    current = load_json(config_path)
    previous_path = backup if backup.is_file() else config_path
    previous = load_json(previous_path)
    if current != previous and not backup.is_file():
        raise HarnessError("config differs from its backup state")
    if previous.get("pilot_ledger") != {"path": str(Path(ledger_path)), "pilot_id": pilot_id} and \
            (previous.get("pilot_ledger", {}).get("pilot_id") != pilot_id
             or Path(previous.get("pilot_ledger", {}).get("path", "")).resolve() != Path(ledger_path).resolve()):
        raise HarnessError("configuration belongs to another pilot ledger")
    events, binding, rows, raw = _ledger_view(Path(ledger_path), suspended_request_id)
    if binding is None:
        raise HarnessError("the alternate stage has no durable binding")
    suspended = events.get("suspended:" + suspended_request_id)
    if suspended is None or json.loads(suspended["detail_json"]) != {"reason": IDENTITY_SUSPENSION_REASON}:
        raise HarnessError("no response-identity suspension for this request")
    created = datetime.fromisoformat(suspended["created_utc"])
    if any(datetime.fromisoformat(r["intent_utc"]) > created for r in rows):
        raise HarnessError("a request was created after the suspension; revision refused")
    if any(r["status"] == "INTENT" for r in rows):
        raise HarnessError("unresolved intent; revision refused")
    observed = {"returned_model": raw.get("model"), "system_fingerprint": raw.get("system_fingerprint")}
    old_provider_path = Path(binding["provider_reference"]["path"])
    if sha256_file(old_provider_path) != previous["d9"]["producer_configs"][ROLE]:
        raise HarnessError("27B provider file differs from the pinned producer configuration")
    provider = load_json(old_provider_path)
    new_provider = deepcopy(provider)
    new_provider.pop("thinking_token_budget", None)  # inert without thinking; not mergeable with extra_body
    new_provider["extra_body"] = deepcopy(NO_THINKING)
    no_thinking_template_kwargs(new_provider["extra_body"]["chat_template_kwargs"])
    new_provider["expected_response"]["system_fingerprint"] = fingerprint
    provider_bytes = _dumps(new_provider)
    provider_path = rev2_path(old_provider_path)
    doc_ref = previous["d9"]["services"][ROLE]["documentation"]
    doc_path = Path(doc_ref["path"])
    if sha256_file(doc_path) != doc_ref["sha256"]:
        raise HarnessError("27B service documentation differs from its pinned hash")
    doc = load_json(doc_path)
    new_doc = deepcopy(doc)
    new_doc["service"]["expected_response"]["system_fingerprint"] = fingerprint
    if _diff_paths(doc, new_doc) != [("service", "expected_response", "system_fingerprint")]:
        raise HarnessError("service documentation revision must change only the fingerprint")
    doc_bytes = _dumps(new_doc)
    new_doc_path = rev2_path(doc_path)
    new_config = deepcopy(previous)
    d9 = new_config["d9"]
    old_sha, new_sha = d9["producer_configs"][ROLE], sha256_text(provider_bytes.decode("utf-8"))
    d9["producer_configs"][ROLE] = new_sha
    new_config["approved_producer_config_sha256"] = [new_sha if v == old_sha else v
                                                     for v in previous["approved_producer_config_sha256"]]
    d9["services"][ROLE]["expected_response"]["system_fingerprint"] = fingerprint
    d9["services"][ROLE]["documentation"] = {"path": str(new_doc_path),
                                             "sha256": sha256_text(doc_bytes.decode("utf-8"))}
    if not response_identity_valid(observed, d9["services"][ROLE]["expected_response"]):
        raise HarnessError("observed identity is not accepted by the proposed config revision")
    auth_ref = previous["execution_authorization"]
    auth_path = rev2_path(Path(auth_ref["path"]))
    payload = {k: v for k, v in new_config.items() if k != "execution_authorization"}
    authorization = {"author": author.strip(), "configuration_sha256": sha256_text(canonical_json(payload)),
                     "decision": "accepted", "pilot_id": pilot_id,
                     "scope": "config revision 1 (03.13-REV27B): 27B producer requalification, "
                              "alternate resume with one requalification resend, budget probe and stability gate"}
    if auth_path.is_file():
        existing = load_json(auth_path)
        if {k: v for k, v in existing.items() if k != "created_utc"} != authorization:
            raise HarnessError(f"refusing to overwrite a different existing file: {auth_path}")
        auth_bytes = auth_path.read_bytes()
    else:
        authorization["created_utc"] = datetime.now(timezone.utc).isoformat()
        auth_bytes = _dumps(dict(sorted(authorization.items())))
    new_config["execution_authorization"] = {"path": str(auth_path),
                                             "sha256": sha256_text(auth_bytes.decode("utf-8"))}
    config_bytes = _dumps(new_config)
    previous_bytes = previous_path.read_bytes()
    approval_dir = config_path.parent
    revision_approval = {"decision": "accepted", "author": author.strip(),
                         "previous_sha256": sha256_text(previous_bytes.decode("utf-8")),
                         "new_sha256": sha256_text(config_bytes.decode("utf-8")), "reason": reason.strip()}
    suspension_approval = {"decision": "accepted", "author": author.strip(),
                           "request_id": suspended_request_id,
                           "suspension_artifact_sha256": suspended["artifact_sha256"],
                           "observed_identity": observed, "config_content_sha256": digest(new_config)}
    if current not in (previous, new_config):
        raise HarnessError("config is neither the previous nor the revised configuration")
    return dict(config_path=config_path, backup=backup, previous_bytes=previous_bytes,
                files=[(provider_path, provider_bytes), (new_doc_path, doc_bytes), (auth_path, auth_bytes),
                       (approval_dir / REVISION_APPROVAL, _dumps(revision_approval)),
                       (approval_dir / SUSPENSION_APPROVAL, _dumps(suspension_approval))],
                config_bytes=config_bytes, new_config=new_config, previous=previous,
                changed_keys=sorted(".".join(map(str, p)) for p in _diff_paths(previous, new_config)),
                observed=observed, provider_path=provider_path)


def revise(*, config_path: Path, ledger_path: Path, pilot_id: str, author: str, reason: str,
           fingerprint: str, suspended_request_id: str, execute: bool) -> dict[str, Any]:
    p = plan(config_path=config_path, ledger_path=ledger_path, pilot_id=pilot_id, author=author,
             reason=reason, fingerprint=fingerprint, suspended_request_id=suspended_request_id)
    touched = [p["config_path"], p["backup"], *(path for path, _ in p["files"])]
    result = dict(status="PLAN_ONLY", changed_keys=p["changed_keys"], observed_identity=p["observed"],
                  before={str(x): _sha(x) for x in touched}, ledger_sha256_before=_sha(Path(ledger_path)),
                  targets={str(path): sha256_text(data.decode("utf-8")) for path, data in p["files"]},
                  config_target_sha256=sha256_text(p["config_bytes"].decode("utf-8")))
    if not execute:
        return result
    from studio2.fase03.harness.d9 import validate_provider
    from studio2.fase03.harness.guards import require_execution, require_pilot_ledger
    from studio2.fase03.harness.ledger import PilotLedger
    changes: list[dict[str, Any]] = []
    for path, data in p["files"]:
        _write_once(path, data, changes)
    _write_once(p["backup"], p["previous_bytes"], changes)
    _write_once(p["config_path"], p["config_bytes"], changes, replace=True)
    new_config = load_json(p["config_path"])
    require_execution(new_config)
    validate_provider(new_config, load_json(p["provider_path"]), STAGE, file_sha256=sha256_file(p["provider_path"]))
    approval_dir = p["config_path"].parent
    ledger = PilotLedger(Path(ledger_path), pilot_id=pilot_id)
    dump_before = ledger.snapshot()
    revision = ledger.record_config_revision(previous_config_path=p["backup"], new_config_path=p["config_path"],
                                             approval_path=approval_dir / REVISION_APPROVAL)
    suspension = ledger.reconcile_suspension(suspended_request_id, approval_path=approval_dir / SUSPENSION_APPROVAL)
    for status, key in ((revision["status"], "config_revision"), (suspension["status"], "suspension_reconciled")):
        changes.append(dict(path=f"ledger:{key}", action="UNCHANGED" if status.startswith("ALREADY") else "WRITTEN"))
    require_pilot_ledger(new_config, ledger)
    for stage in sorted(s for s, n in dump_before["requests_by_stage"].items() if n):
        ledger.binding(stage)
    if ledger.unreconciled_suspensions():
        raise HarnessError("suspensions remain after reconciliation")
    result.update(status="REVISED", revision=revision, suspension=suspension, changes=changes,
                  after={str(x): _sha(x) for x in touched}, ledger_sha256_after=_sha(Path(ledger_path)),
                  snapshot=ledger.snapshot())
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runtime", type=Path, default=PILOT03_RUNTIME)
    parser.add_argument("--author", required=True)
    parser.add_argument("--reason", default="27B runtime vLLM 0.28.0 now reports system_fingerprint "
                        "vllm-0.28.0-5fc21ed4; producer requalified with enable_thinking=false "
                        "after finish_reason=length with 2047/2560 reasoning tokens")
    parser.add_argument("--fingerprint", default=PILOT03_FINGERPRINT)
    parser.add_argument("--suspended-request", default=PILOT03_SUSPENDED)
    parser.add_argument("--pilot-id", default="studio2-fase03-d9-pilot-03")
    parser.add_argument("--evidence-root", type=Path, help="optional: also print the author_acceptances plan")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge")
    args = parser.parse_args(argv)
    if args.execute and args.acknowledge != ACK:
        raise SystemExit(f"execution requires --execute --acknowledge {ACK}")
    runtime = args.runtime.resolve()
    result = revise(config_path=runtime / "execution/pilot_d9_successor_candidate_03_13.private.json",
                    ledger_path=runtime / "ledger.sqlite3", pilot_id=args.pilot_id, author=args.author,
                    reason=args.reason, fingerprint=args.fingerprint,
                    suspended_request_id=args.suspended_request, execute=args.execute)
    if args.execute and args.evidence_root is not None:
        from studio2.fase03 import author_acceptances
        census = author_acceptances.run(runtime=runtime, worktree=ROOT, author=args.author,
                                        evidence_root=args.evidence_root, execute=False)
        result["author_acceptances_blocking"] = census["blocking"]
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    return 0 if result["status"] in {"PLAN_ONLY", "REVISED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
