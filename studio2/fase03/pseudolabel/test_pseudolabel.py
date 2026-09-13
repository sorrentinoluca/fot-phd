"""Test della sotto-fase 03.7: invarianti di SPECIFICA_PSEUDOLABEL.md sugli artefatti generati.

Esecuzione dalla radice del repository:
  python3 -m unittest studio2.fase03.pseudolabel.test_pseudolabel -v
Nessun dato del primo studio, nessuna chiamata a modelli, nessuna simulazione.
"""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from studio2.fase03 import protocol
from studio2.fase03.pseudolabel import pseudolabel_draw as pl

HERE = Path(__file__).resolve().parent


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def spearman(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    d2 = sum((x - y) ** 2 for x, y in zip(xs, ys))
    return 1 - 6 * d2 / (n * (n * n - 1))


class LabelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map = load(pl.ARTIFACTS["map"])
        cls.labels = {k: v for k, v in cls.map["label_by_identifier"].items() if k != pl.NORMAL_LABEL}
        cls.catalog = pl.load_catalog()

    def test_nine_unique_labels_equal_length(self):
        space = self.map["label_space"]
        self.assertEqual(len(space), 9)
        self.assertEqual(len(set(space)), 9)
        self.assertEqual(space[-1], pl.NORMAL_LABEL)
        opaque = space[:-1]
        self.assertEqual({len(label) for label in opaque}, {len(pl.PREFIX) + pl.SUFFIX_LENGTH})

    def test_regex_of_protocol(self):
        for label in self.map["label_space"][:-1]:
            self.assertRegex(label, protocol.PSEUDOLABEL)
        protocol._validate_label_space(self.map["label_space"])  # solleva ContractError se non conforme

    def test_normal_is_literal_and_last(self):
        self.assertEqual(self.map["label_by_identifier"][pl.NORMAL_LABEL], pl.NORMAL_LABEL)
        self.assertEqual(self.map["label_space"][-1], pl.NORMAL_LABEL)
        self.assertNotIn("Unknown", self.map["label_space"])

    def test_identifiers_match_frozen_catalog(self):
        self.assertEqual(list(self.labels), pl.CATALOG_IDENTIFIERS)
        self.assertEqual(self.map["idv_by_identifier"], {e["label"]: e["idv"] for e in self.catalog["faults"]})

    def test_opacity_no_fault_number_substring(self):
        # Test dichiarato: il suffisso non contiene le cifre dell'idv del proprio fault
        # né la stringa F<idv>; nessun suffisso contiene "F" seguito da cifre.
        for identifier, label in self.labels.items():
            idv = str(self.map["idv_by_identifier"][identifier])
            suffix = label[len(pl.PREFIX):]
            self.assertNotIn(idv, suffix, f"{identifier}: {label} rivela l'idv")
            self.assertNotIn(identifier, suffix)
            self.assertNotRegex(suffix, r"F[0-9]")

    def test_opacity_no_correlation_with_catalog_order(self):
        # Test dichiarato: l'ordine lessicografico delle label non coincide con l'ordine del
        # catalogo (né con il suo inverso) e la correlazione di Spearman fra rango di catalogo
        # e rango lessicografico è riportata; la costruzione per digest non trasmette ordine.
        catalog_rank = {identifier: i for i, identifier in enumerate(pl.CATALOG_IDENTIFIERS)}
        lexi = sorted(self.labels, key=lambda k: self.labels[k])
        lexi_rank = {identifier: i for i, identifier in enumerate(lexi)}
        self.assertNotEqual(lexi, pl.CATALOG_IDENTIFIERS)
        self.assertNotEqual(lexi, list(reversed(pl.CATALOG_IDENTIFIERS)))
        rho = spearman([catalog_rank[k] for k in self.labels], [lexi_rank[k] for k in self.labels])
        self.assertLess(abs(rho), 1.0)
        print(f"\n[info] Spearman(catalog order, lexicographic order) = {rho:+.3f}")

    def test_label_space_is_sorted_opaque_then_normal(self):
        self.assertEqual(self.map["label_space"], sorted(self.labels.values()) + [pl.NORMAL_LABEL])


class AssignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assignment = load(pl.ARTIFACTS["assignment"])
        cls.map = load(pl.ARTIFACTS["map"])

    def test_bijection_agents_faults(self):
        agents = self.assignment["assignment"]
        self.assertEqual(tuple(agents), protocol.AGENT_IDS)
        owned = [value["local_fault_label"] for value in agents.values()]
        self.assertEqual(sorted(owned), self.map["label_space"][:-1])
        identifiers = [value["identifier"] for value in agents.values()]
        self.assertEqual(sorted(identifiers, key=pl.CATALOG_IDENTIFIERS.index), pl.CATALOG_IDENTIFIERS)
        for value in agents.values():
            self.assertEqual(self.map["label_by_identifier"][value["identifier"]], value["local_fault_label"])

    def test_assignment_follows_digest_order(self):
        keys = {identifier: pl.assignment_key(identifier) for identifier in pl.CATALOG_IDENTIFIERS}
        expected = sorted(pl.CATALOG_IDENTIFIERS, key=lambda k: keys[k])
        actual = [value["identifier"] for value in self.assignment["assignment"].values()]
        self.assertEqual(actual, expected)

    def test_agents_block_matches_manifest_contract(self):
        agents = self.assignment["agents"]
        self.assertEqual(tuple(agents), protocol.AGENT_IDS)
        for entry in agents.values():
            self.assertEqual(set(entry), {"local_fault_label"})


class DerangementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.der = load(pl.ARTIFACTS["derangements"])
        cls.assignment = load(pl.ARTIFACTS["assignment"])["agents"]
        cls.map = load(pl.ARTIFACTS["map"])
        cls.log = load(pl.ARTIFACTS["log"])

    def test_enumeration_count_is_subfactorial_seven(self):
        table = pl.enumerate_derangements()
        self.assertEqual(len(table), 1854)
        self.assertEqual(table, sorted(table))
        self.assertTrue(all(all(p[i] != i for i in range(7)) for p in table))

    def test_zero_fixed_points_and_seven_peer_domain(self):
        der = self.der["derangements"]
        self.assertEqual(tuple(der), protocol.AGENT_IDS)
        faults = set(self.map["label_space"][:-1])
        for agent_id in protocol.AGENT_IDS:
            local = self.assignment[agent_id]["local_fault_label"]
            peers = faults - {local}
            mapping = der[agent_id]
            self.assertEqual(len(mapping), 7)
            self.assertEqual(set(mapping), peers)
            self.assertEqual(set(mapping.values()), peers)
            self.assertFalse(any(s == t for s, t in mapping.items()), f"{agent_id} ha un punto fisso")

    def test_protocol_validator_accepts_artifacts(self):
        protocol._validate_derangements(
            self.der["derangements"], agents=self.assignment, label_space=self.map["label_space"]
        )

    def test_not_the_one_step_rotation(self):
        # Almeno un agente non è la rotazione di un passo dei peer in ordine di label_space.
        rotations = 0
        for agent_id, entry in self.log["derangements"]["agents"].items():
            peers = entry["peers_in_label_space_order"]
            rotation = dict(zip(peers, peers[1:] + peers[:1]))
            rotations += self.der["derangements"][agent_id] == rotation
        self.assertLess(rotations, 8)

    def test_log_words_reproduce_indices(self):
        limit = self.log["derangements"]["acceptance_limit"]
        self.assertEqual(limit, 2**32 - (2**32 % 1854))
        for agent_id, entry in self.log["derangements"]["agents"].items():
            words = [d["word"] for d in entry["draws"]]
            self.assertTrue(all(w >= limit for w in words[:-1]))
            self.assertLess(words[-1], limit)
            self.assertEqual(words[-1] % 1854, entry["selected_index"])
            self.assertEqual(entry["rejections"], len(words) - 1)
            for draw in entry["draws"]:
                _, word = pl.derangement_word(agent_id, draw["draw_index"])
                self.assertEqual(word, draw["word"])

    def test_by_identifier_view_is_consistent(self):
        label_by_id = self.map["label_by_identifier"]
        for agent_id, mapping in self.der["derangements_by_identifier"].items():
            translated = {label_by_id[s]: label_by_id[t] for s, t in mapping.items()}
            self.assertEqual(translated, self.der["derangements"][agent_id])


class ReproducibilityTests(unittest.TestCase):
    def test_generate_is_deterministic(self):
        self.assertEqual(pl.generate(), pl.generate())

    def test_replay_matches_files_on_disk(self):
        self.assertEqual(pl.check_replay(HERE), [])

    def test_log_declares_namespace_seed_and_counters(self):
        log = load(pl.ARTIFACTS["log"])
        self.assertEqual(log["namespace"], pl.NAMESPACE)
        self.assertEqual(log["seed"], pl.SEED)
        self.assertEqual(set(log["label_counters"]), set(pl.CATALOG_IDENTIFIERS))
        self.assertEqual(set(log["derangement_rejections"]), set(protocol.AGENT_IDS))
        for attempt in log["label_attempts"]:
            digest, suffix = pl.candidate_suffix(attempt["message"])
            self.assertEqual((digest, suffix), (attempt["sha256"], attempt["suffix"]))

    def test_other_seed_changes_derangements_not_labels(self):
        catalog = pl.load_catalog()
        labels, _, _ = pl.derive_labels(catalog["faults"])
        space = pl.build_label_space(labels)
        assignment, _ = pl.assign_agents(catalog["faults"], labels)
        base, _ = pl.sample_derangements(assignment, space, seed=pl.SEED)
        other, _ = pl.sample_derangements(assignment, space, seed=pl.SEED + 1)
        self.assertNotEqual(base, other)
        other_labels, _, _ = pl.derive_labels(catalog["faults"], namespace=pl.NAMESPACE + "-x")
        self.assertNotEqual(labels, other_labels)

    def test_fails_if_catalog_differs(self):
        original = pl.CATALOG_PATH.read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            altered = Path(tmp) / "CATALOG_FREEZE.json"
            altered.write_bytes(original.replace(b'"status"', b'"status_"', 1))
            with self.assertRaises(pl.CatalogMismatch):
                pl.load_catalog(altered)
            data = json.loads(original)
            data["catalog"][0] = 4
            altered.write_bytes(json.dumps(data, indent=2, ensure_ascii=False).encode() + b"\n")
            with self.assertRaises(pl.CatalogMismatch):
                pl.load_catalog(altered)
            with self.assertRaises(pl.CatalogMismatch):
                pl.generate(catalog_path=altered)


if __name__ == "__main__":
    unittest.main()
