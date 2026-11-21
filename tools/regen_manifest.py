# -*- coding: utf-8 -*-
"""重算 hash-manifest.txt 中的 SHA-256 与字节大小（保留条目顺序与说明列）。

为什么需要它：hash-manifest 是**生成物**。当清单内的文件被修改（例如修复
verify_hash_manifest.py 自身），手工合并冲突只会得到一份"哈希与文件对不上"
的清单——那比没有清单更糟。正确做法是：代码先定稿，再重算清单。

用法： python regen_manifest.py <repo_dir> [--manifest hash-manifest.txt] [--check]
  --check  只比对不写入，退出码 1 表示存在不一致
"""
import hashlib
import re
import sys
from pathlib import Path

ROW = re.compile(r"^(- `)([^`]+)(` \| `)([0-9a-fA-F]{64})(` \| )([0-9]+)( B \| )")


def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if len(sys.argv) < 2:
        print("usage: regen_manifest.py <repo_dir> [--manifest name] [--check]")
        return 2
    repo = Path(sys.argv[1]).resolve()
    name = "hash-manifest.txt"
    check = "--check" in sys.argv
    if "--manifest" in sys.argv:
        name = sys.argv[sys.argv.index("--manifest") + 1]
    mf = repo / name
    lines = mf.read_text(encoding="utf-8").splitlines()
    out, changed, missing = [], [], []
    for ln in lines:
        m = ROW.match(ln)
        if not m:
            out.append(ln)
            continue
        rel, old_hash, old_size = m.group(2), m.group(4), m.group(6)
        f = repo / rel
        if not f.is_file():
            missing.append(rel)
            out.append(ln)
            continue
        new_hash, new_size = sha256_of(f), f.stat().st_size
        if new_hash.lower() != old_hash.lower() or new_size != int(old_size):
            changed.append((rel, old_hash, new_hash, int(old_size), new_size))
        out.append(f"{m.group(1)}{rel}{m.group(3)}{new_hash}{m.group(5)}{new_size}{m.group(7)}{ln[m.end():]}")
    for rel, oh, nh, osz, nsz in changed:
        print(f"CHANGED {rel}\n  {oh} ({osz} B) -> {nh} ({nsz} B)")
    for rel in missing:
        print(f"MISSING {rel}")
    if not changed and not missing:
        print("OK — 清单与文件全部一致")
        return 0
    if check:
        return 1
    mf.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"WROTE {mf} ({len(changed)} 条更新)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
