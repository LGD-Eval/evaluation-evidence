#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for verify_hash_manifest.py.
verify_hash_manifest.py 单元测试：临时目录构造清单与文件，验证 PASS / 各 FAIL 路径。

Run / 运行:  python -m unittest tests/test_verify_hash_manifest.py -v
"""
import hashlib
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from verify_hash_manifest import parse_manifest, sha256_of, verify  # noqa: E402


def make_file(path, content=b"hello"):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(content)
    return hashlib.sha256(content).hexdigest(), len(content)


class VerifyHashManifestTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="lhdm_")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write_manifest(self, rows):
        p = os.path.join(self.tmp, "hash-manifest.txt")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("# Header comment\n")
            fh.write("| file | sha | size | note |\n")
            fh.write("|---|---|---|---|\n")
            for rel, sha, size in rows:
                fh.write("| `%s` | `%s` | %d B | note |\n" % (rel, sha, size))
        return p

    def test_all_pass(self):
        rel = "evidence/a.txt"
        sha, size = make_file(os.path.join(self.tmp, rel))
        m = self._write_manifest([(rel, sha, size)])
        results, ok = verify(m)
        self.assertTrue(ok)
        self.assertEqual([r["status"] for r in results], ["PASS"])

    def test_sha256_mismatch_fails(self):
        rel = "evidence/a.txt"
        make_file(os.path.join(self.tmp, rel), b"hello")
        bad_sha = "0" * 64
        m = self._write_manifest([(rel, bad_sha, 5)])
        results, ok = verify(m)
        self.assertFalse(ok)
        self.assertEqual(results[0]["status"], "FAIL")
        self.assertEqual(results[0]["reason"], "sha256_mismatch")

    def test_size_mismatch_fails(self):
        rel = "evidence/a.txt"
        sha, _ = make_file(os.path.join(self.tmp, rel), b"hello")
        m = self._write_manifest([(rel, sha, 999)])
        results, ok = verify(m)
        self.assertFalse(ok)
        self.assertEqual(results[0]["reason"], "size_mismatch")

    def test_missing_file_fails(self):
        m = self._write_manifest([("evidence/missing.txt", "0" * 64, 1)])
        results, ok = verify(m)
        self.assertFalse(ok)
        self.assertEqual(results[0]["reason"], "missing_file")

    def test_parse_skips_headers_and_notes(self):
        m = self._write_manifest([])
        entries = parse_manifest(m)
        self.assertEqual(entries, [])


if __name__ == "__main__":
    unittest.main()
