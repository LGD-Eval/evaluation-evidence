# AGENTS.md — Agent Guidance / AI 代理引导

This file helps AI agents and humans understand and use this repository autonomously. Read this first. / 本文件帮助 AI 代理与人类自主理解并使用本仓库。请先阅读本文件。

## What this repository is / 本仓库是什么

The **Evaluation Evidence** repository of LGD-Eval: the notarization layer. SHA-256 hashes, trusted timestamps, and blockchain anchors for every published claim, report version, and release artifact.

本仓库是 LGD-Eval 的**评测存证**仓库：存证层。为每条已发布结论、每个报告版本与发布产物提供 SHA-256 哈希、可信时间戳与区块链锚定。

## Quick start / 快速开始

1. Read `README.md` — anchoring process (Compute → Manifest → Timestamp → Anchor → Verify). / 阅读 `README.md`——锚定流程（计算 → 清单 → 时间戳 → 上链 → 验证）。
2. Locate the manifest for a release under `manifests/`. / 在 `manifests/` 定位某次发布的清单。
3. Verify any file: re-compute SHA-256 and compare. / 验证任一文件：复算 SHA-256 并比对。

## Key facts for agents / AI 代理须知

- **Immutability**: any mismatch between a file and its manifest entry invalidates the revision. / **不可变**：文件与清单条目不一致即宣告该版本失效。
- **Verify before cite**: always re-hash before trusting a referenced artifact. / **引用前验证**：引用产物前必须复算哈希。
- **Bilingual**: English first, Chinese complete. / **双语**：英文在前、中文完整。

## Verification command / 验证命令

```powershell
Get-FileHash <file> -Algorithm SHA256
```

## Links / 链接

- Home: `/LGD-Eval` · Protocol: `/evaluation-protocol` · Reports: `/evaluation-reports` · Skill Audit: `/skill-audit` — 主页：`/LGD-Eval` · 协议：`/evaluation-protocol` · 报告：`/evaluation-reports` · 技能审计：`/skill-audit`