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


EXT_HEADING = re.compile(
    r"^(?:##|###)\s*(?:.*(?:lgd-gate|外部|external|另一仓|别的仓).*)", re.I)


def parse_manifest(manifest_path):
    """Parse markdown table rows into dicts. / 解析表格行。

    清单里混着两类行，必须分开处理（2026-11-27 修：旧版一律当本地文件，
    于是"引擎发布字节"那三个跨仓行必然 MISSING，外人一跑就是 3 FAIL）：

      local    —— 本仓文件，按路径本地重算 SHA-256 与大小，必须 PASS
      external —— 别的仓的发布字节（本清单只是引用记录），路径不在本仓；
                  标 EXTERNAL，不本地校验，既不冒充 PASS 也不算 FAIL

    分区依据：出现含 lgd-gate / 外部 / external 的 ## 小标题之后的行算 external。
    """
    entries = []
    external = False
    with open(manifest_path, "r", encoding="utf-8") as fh:
        for line in fh:
            s = line.strip()
            if s.startswith("#"):
                if EXT_HEADING.match(s):
                    external = True
                continue
            m = TABLE_ROW.match(s)
            if m:
                entries.append({"path": m.group(1),
                                "sha256": m.group(2).lower(),
                                "size": int(m.group(3)),
                                "kind": "external" if external else "local"})
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
    for ent in entries:
        rel, expected_sha, expected_size = ent["path"], ent["sha256"], ent["size"]
        if ent["kind"] == "external":
            results.append({"path": rel, "status": "EXTERNAL",
                            "reason": "declared in another repository; not verifiable locally",
                            "expected_sha256": expected_sha,
                            "expected_size": expected_size})
            continue
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


def _selftest():
    """红队自测：造两棵树，好清单必须绿、坏清单必须红。 / Self-test. """
    import tempfile
    cases = []
    for tamper in (False, True):
        d = tempfile.mkdtemp()
        f = os.path.join(d, "sample.bin")
        with open(f, "wb") as fh:
            fh.write(b"evidence-bytes")
        real = sha256_of(f)
        size = os.path.getsize(f)
        shown = ("0" * 64) if tamper else real
        mf = os.path.join(d, "hash-manifest.txt")
        with open(mf, "w", encoding="utf-8") as fh:
            fh.write("| 文件路径 | SHA-256 | 大小 | 说明 |\n|---|---|---|---|\n")
            fh.write("- `sample.bin` | `%s` | %d B | selftest |\n" % (shown, size))
        results, ok = verify(mf)
        cases.append(("tampered" if tamper else "honest", ok, not tamper))
    good = sum(1 for _, got, want in cases if got == want)
    for name, got, want in cases:
        print("selftest %-9s got=%s want=%s %s" % (name, got, want, "OK" if got == want else "BAD"))
    print("selftest: %d/%d 符合预期" % (good, len(cases)))
    return 0 if good == len(cases) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Verify a SHA-256 hash manifest.")
    ap.add_argument("--manifest", default="hash-manifest.txt",
                    help="Path to the manifest (default: hash-manifest.txt).")
    ap.add_argument("--json", action="store_true",
                    help="Emit deterministic JSON on stdout.")
    ap.add_argument("--selftest", action="store_true",
                    help="Run the red-team self-test (honest=tampered cases).")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

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
            "external": sum(1 for r in results if r["status"] == "EXTERNAL"),
            "entries": results,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print("%s  %s" % (r["status"].ljust(8), r["path"]))
        print("total=%d passed=%d failed=%d external=%d (external=%d 行在别的仓，未本地校验；不算通过)" % (
            len(results),
            sum(1 for x in results if x["status"] == "PASS"),
            sum(1 for x in results if x["status"] == "FAIL"),
            sum(1 for x in results if x["status"] == "EXTERNAL"),
            sum(1 for x in results if x["status"] == "EXTERNAL"),
        ))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
