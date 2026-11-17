import unittest

from oif_observatory.ledger import validate_record, validate_ledger


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.record = {
            "id": "r1", "claim": "A test claim", "source_url": "https://example.org",
            "publisher": "Example", "published_at": "2026-01-01",
            "observed_at": "2026-01-02", "evidence_class": "primary",
        }

    def test_valid_record(self):
        self.assertEqual(validate_record(self.record), [])

    def test_bad_date(self):
        bad = dict(self.record, published_at="yesterday")
        self.assertIn("published_at must be an ISO-8601 date", validate_record(bad))

    def test_unknown_evidence_class(self):
        bad = dict(self.record, evidence_class="certain")
        self.assertIn("evidence_class is not recognized", validate_record(bad))

    def test_duplicate_ids(self):
        errors = validate_ledger([self.record, self.record])
        self.assertTrue(any("duplicate id" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
