#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for verify_hash_manifest.py.
verify_hash_manifest.py 单元测试：临时目录构造清单与文件，验证 PASS / 各 FAIL 路径。

Run / 运行:  python -m unittest tests/test_verify_hash_manifest.py -v
           python -m pytest tests

契约变更说明（2026-11-15）：`verify()` 现在返回三元组 `(results, ok, warnings)`。
第三项是为 P1-8（不可解析行不得被静默丢弃）新增的，原有断言相应改为三元解包，
并补两条新行为的用例：不可解析行 -> warning，'..' 穿越 -> path_traversal。
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

    def _write_manifest(self, rows, extra_lines=()):
        """表头一律写成 # 注释：解析器把非注释、非分隔、非数据行判为不可解析。"""
        p = os.path.join(self.tmp, "hash-manifest.txt")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("# Header comment\n")
            fh.write("# | file | sha | size | note |\n")
            fh.write("|---|---|---|---|\n")
            for rel, sha, size in rows:
                fh.write("- `%s` | `%s` | %d B | note |\n" % (rel, sha, size))
            for ln in extra_lines:
                fh.write(ln + "\n")
        return p

    def test_all_pass(self):
        rel = "evidence/a.txt"
        sha, size = make_file(os.path.join(self.tmp, rel))
        m = self._write_manifest([(rel, sha, size)])
        results, ok, warnings = verify(m)
        self.assertTrue(ok)
        self.assertEqual(warnings, [])
        self.assertEqual([r["status"] for r in results], ["PASS"])

    def test_sha256_mismatch_fails(self):
        rel = "evidence/a.txt"
        make_file(os.path.join(self.tmp, rel), b"hello")
        bad_sha = "0" * 64
        m = self._write_manifest([(rel, bad_sha, 5)])
        results, ok, warnings = verify(m)
        self.assertFalse(ok)
        self.assertEqual(results[0]["status"], "FAIL")
        self.assertEqual(results[0]["reason"], "sha256_mismatch")

    def test_size_mismatch_fails(self):
        rel = "evidence/a.txt"
        sha, _ = make_file(os.path.join(self.tmp, rel), b"hello")
        m = self._write_manifest([(rel, sha, 999)])
        results, ok, warnings = verify(m)
        self.assertFalse(ok)
        self.assertEqual(results[0]["reason"], "size_mismatch")

    def test_missing_file_fails(self):
        m = self._write_manifest([("evidence/missing.txt", "0" * 64, 1)])
        results, ok, warnings = verify(m)
        self.assertFalse(ok)
        self.assertEqual(results[0]["reason"], "missing_file")

    def test_parse_skips_headers_and_notes(self):
        m = self._write_manifest([])
        entries = parse_manifest(m)
        self.assertEqual(entries, [])

    # ---- 新增：P1-8 不可解析行不得被静默丢弃 ----
    def test_unparseable_row_is_a_warning_not_silently_dropped(self):
        rel = "evidence/a.txt"
        sha, size = make_file(os.path.join(self.tmp, rel))
        m = self._write_manifest(
            [(rel, sha, size)],
            extra_lines=["- `evidence/tampered.txt` | `not-a-hash` | 12 B | note |"],
        )
        results, ok, warnings = verify(m)
        self.assertTrue(any("unparseable" in w for w in warnings), warnings)
        self.assertFalse(ok, "存在不可解析行时必须判定失败")

    # ---- 新增：P1-9 路径穿越必须被拒绝 ----
    def test_path_traversal_is_rejected(self):
        m = self._write_manifest([("../../etc/passwd", "0" * 64, 1)])
        results, ok, warnings = verify(m)
        self.assertFalse(ok)
        self.assertEqual(results[0]["reason"], "path_traversal")

    def test_absolute_path_is_rejected(self):
        # 两道防线都可能拦住绝对路径：isabs -> path_traversal，
        # 归一化后落在 base 之外 -> path_outside_base。任一拒绝都算通过，
        # 断言写死具体标签会让用例随平台（Windows/POSIX 的 isabs 行为）漂移。
        m = self._write_manifest([("/etc/passwd", "0" * 64, 1)])
        results, ok, warnings = verify(m)
        self.assertFalse(ok)
        self.assertIn(results[0].get("reason"), ("path_traversal", "path_outside_base"))


if __name__ == "__main__":
    unittest.main()
