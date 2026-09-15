#!/usr/bin/env python3
"""Offline fail-closed probe for pilot_d9_decisions_received.json.
Run from an isolated archive root of candidate 3180aea. Sockets are blocked
before importing the harness, proving no network is attempted before the gate.
"""
import socket, json, sys, copy
class Blocked(Exception): pass
def _no(*a, **k): raise Blocked("network attempted")
socket.socket = _no; socket.create_connection = _no
sys.path.insert(0, ".")
from studio2.fase03.harness import d9
from studio2.fase03.harness.common import HarnessError
cfg = json.load(open("studio2/fase03/config/pilot_d9_decisions_received.json"))
def probe(c, label):
    try:
        d9.validate_config(c); print(f"[{label}] NO FAIL (config would PASS!)"); return None
    except HarnessError as e: print(f"[{label}] fail-closed: {e}"); return str(e)
    except Blocked as e: print(f"[{label}] NETWORK ATTEMPTED (!!): {e}"); return "NETWORK"
    except Exception as e: print(f"[{label}] {type(e).__name__}: {e}"); return f"OTHER:{type(e).__name__}"
probe(cfg, "as-is")
c2=copy.deepcopy(cfg); c2["d9"]["status"]="DOCUMENTED_FOR_AUTHORIZED_STAGE"; c2["d9"]["missing_requirements"]=[]
probe(c2, "prereqs-forced")
