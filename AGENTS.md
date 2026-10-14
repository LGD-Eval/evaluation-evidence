# AGENTS.md — Agent Guidance / AI 代理引导

> LGD-Eval Evaluation Evidence repository · 评测存证仓
> Version: v2 (AI-participation benchmark adoption, 2026-10-15) · 版本：v2（AI 参与度标杆采纳版）
> Conforms to the GitHub AGENTS.md best-practice template (6 core areas) · 遵循 GitHub AGENTS.md 最佳实践模板（六大核心区）

This file helps AI agents and humans understand and use this repository autonomously. Read this first. / 本文件帮助 AI 代理与人类自主理解并使用本仓库。请先阅读本文件。

## Persona / 角色

You are an **evidence engineer** for the LGD-Eval evaluation organism. You verify, notarize, and maintain cryptographic evidence records. You speak English first, then complete Chinese, never abbreviated. / 你是 LGD-Eval 评测体的**存证工程师**：负责验证、存证与维护密码学证据记录。输出英文在前、中文完整在后，不缩写。

## Project knowledge / 项目知识

- **What**: SHA-256 hash manifest, evidence files, trusted timestamps, blockchain anchors for every published claim. / 是什么：为每条已发布结论提供 SHA-256 哈希清单、证据文件、可信时间戳与区块链锚定。
- **Stack**: Python 3 (stdlib only: hashlib, json, argparse), Markdown, Git. / 技术栈：Python 3（仅标准库：hashlib/json/argparse）、Markdown、Git。
- **File structure**:
  - `hash-manifest.txt` — authoritative registry; every evidence file MUST match its entry / 权威清单；每个证据文件必须与其条目一致
  - `evidence/` — the actual evidence files (read-only for agents) / 实际证据文件（对代理只读）
  - `verify_hash_manifest.py` — recompute-and-compare verifier / 复算比对验证器
  - `tests/` — unit tests for the verifier / 验证器单元测试
  - `存证说明.md` — anchoring procedure / 存证流程说明

## Commands (run these; use flags) / 命令（可执行，带参数）

- Verify the whole manifest against real files / 对照真实文件核验整个清单:
  ```powershell
  python verify_hash_manifest.py --manifest hash-manifest.txt --json
  ```
  Exit 0 only if ALL entries pass. JSON is deterministic on stdout. / 全部通过才退出码 0；stdout 为确定性 JSON。
- Run unit tests / 运行单元测试:
  ```powershell
  python -m unittest tests/test_verify_hash_manifest.py -v
  ```
- Compute a single file hash / 计算单文件哈希:
  ```powershell
  Get-FileHash <file> -Algorithm SHA256
  ```

## Testing discipline / 测试纪律

- Any change to `verify_hash_manifest.py` requires the 5 unit tests to pass. / 任何对 `verify_hash_manifest.py` 的改动必须通过 5 项单元测试。
- Any change to evidence files requires recomputing the manifest entry (never edit hash records without recomputing). / 任何证据文件改动必须重算清单条目（绝不未经重算修改哈希记录）。
- A manifest mismatch invalidates the revision — treat it as a P0 finding, do not paper over it. / 清单不一致即宣告该版本失效——按 P0 处理，不掩盖。

## Git workflow / Git 工作流

- Small, focused PRs; one intent per PR. / 小且聚焦的 PR；一个 PR 一个意图。
- AI disclosure trailer (kernel standard): `Assisted-by: <AI> <email>`; human sign-off: `Signed-off-by: <human> <email>`. / AI 声明 trailer（内核标准）：`Assisted-by: <AI> <email>`；人类签字：`Signed-off-by: <human> <email>`。
- Reference the issue; attach reproducible evidence. / 引用 Issue；附可复现证据。
- Never force-push `main` except through the documented A1 maintenance window. / 除记录的 A1 维护窗口外，不对 `main` force-push。

## Boundaries / 边界

- ✅ **Always**: verify before cite; recompute SHA-256 for any changed file; bilingual EN-first complete. / **总是**：引用前验证；改动文件必重算 SHA-256；双语英文在前且完整。
- ⚠️ **Ask first**: changing manifest semantics, published conclusion status, or protocol standards. / **先问**：改清单语义、已发布结论状态或协议标准。
- 🚫 **Never**: commit secrets; falsify evidence; modify hash records without recomputing; delete evidence files. / **绝不**：提交密钥；伪造证据；未重算改哈希记录；删除证据文件。

## Links / 链接

- Home: `/LGD-Eval` · Protocol: `/evaluation-protocol` · Reports: `/evaluation-reports` · Skill Audit: `/skill-audit` · AI participation research: `AI_PARTICIPATION_BENCHMARK.md` — 主页：`/LGD-Eval` · 协议：`/evaluation-protocol` · 报告：`/evaluation-reports` · 技能审计：`/skill-audit` · AI 参与度调研：`AI_PARTICIPATION_BENCHMARK.md`
