#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_hash_manifest.py — Verify a SHA-256 hash manifest against real files.
哈希存证清单验证器 — 对照真实文件逐项核验 SHA-256 与大小。

Usage / 用法:
    python verify_hash_manifest.py [--manifest hash-manifest.txt] [--json]

Behavior / 行为:
  * Parses the markdown table in the manifest (path | SHA-256 | size | note).
  * Recomputes SHA-256 of every listed file, relative to the manifest's directory.
  * Reports pass/fail per entry; exits 0 only if ALL entries pass.
  * --json emits deterministic machine-readable JSON on stdout.
  * 解析清单内的 Markdown 表格（路径 | SHA-256 | 大小 | 说明），
    以清单所在目录为基准重算每个文件的 SHA-256 与大小，
    逐项输出通过/失败；全部通过才退出码 0；--json 输出确定性 JSON。

This is the AI sample contribution for LGD-Eval/evaluation-evidence issue #1
(add SHA-256 verification script). Apache-2.0. Assisted-by: LGD-Eval (AI agent).
"""
import argparse
import hashlib
import json
import os
import re
import sys

TABLE_ROW = re.compile(r"^(?:-\s*)?(?:\|\s*)?`([^`]+)`\s*\|\s*`([0-9a-fA-F]{64})`\s*\|\s*([0-9]+)\s*B?\s*\|")


def parse_manifest(manifest_path):
    """Parse the markdown table rows into (rel_path, sha256, size). / 解析表格行。"""
    entries = []
    with open(manifest_path, "r", encoding="utf-8") as fh:
        for line in fh:
            m = TABLE_ROW.match(line.strip())
            if m:
                entries.append((m.group(1), m.group(2).lower(), int(m.group(3))))
    return entries


def sha256_of(path, chunk=1 << 16):
    """Compute SHA-256 of a file. / 计算文件 SHA-256。"""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def verify(manifest_path):
    """Verify every entry; return (results, ok). / 逐项核验，返回结果与是否全部通过。"""
    base = os.path.dirname(os.path.abspath(manifest_path))
    entries = parse_manifest(manifest_path)
    results = []
    ok = True
    for rel, expected_sha, expected_size in entries:
        full = os.path.join(base, rel)
        item = {
            "path": rel,
            "expected_sha256": expected_sha,
            "expected_size": expected_size,
            "status": "pending",
            "actual_sha256": None,
            "actual_size": None,
        }
        if not os.path.isfile(full):
            item["status"] = "FAIL"
            item["reason"] = "missing_file"
            ok = False
        else:
            actual_sha = sha256_of(full)
            actual_size = os.path.getsize(full)
            item["actual_sha256"] = actual_sha
            item["actual_size"] = actual_size
            if actual_sha != expected_sha:
                item["status"] = "FAIL"
                item["reason"] = "sha256_mismatch"
                ok = False
            elif actual_size != expected_size:
                item["status"] = "FAIL"
                item["reason"] = "size_mismatch"
                ok = False
            else:
                item["status"] = "PASS"
        results.append(item)
    return results, ok


def main(argv=None):
    ap = argparse.ArgumentParser(description="Verify a SHA-256 hash manifest.")
    ap.add_argument("--manifest", default="hash-manifest.txt",
                    help="Path to the manifest (default: hash-manifest.txt).")
    ap.add_argument("--json", action="store_true",
                    help="Emit deterministic JSON on stdout.")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.manifest):
        print("ERROR: manifest not found: %s" % args.manifest, file=sys.stderr)
        return 2

    results, ok = verify(args.manifest)
    if args.json:
        payload = {
            "manifest": os.path.basename(args.manifest),
            "schema": "lgd-eval/hash-manifest-verify/v1",
            "total": len(results),
            "passed": sum(1 for r in results if r["status"] == "PASS"),
            "failed": sum(1 for r in results if r["status"] == "FAIL"),
            "entries": results,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print("%s  %s" % (r["status"].ljust(4), r["path"]))
        print("total=%d passed=%d failed=%d" % (
            len(results),
            sum(1 for x in results if x["status"] == "PASS"),
            sum(1 for x in results if x["status"] == "FAIL"),
        ))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
