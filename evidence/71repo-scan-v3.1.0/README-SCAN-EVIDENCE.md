# 71 仓全量扫描证据（skillgate v3.1.0 口径）

> 本目录为 Muse 外审 P1-4 整改产物：派单头条数字（71 仓 / 753 findings / CRITICAL 1 / HIGH 8 / 误报 0）的原始可对账证据。
> 登记时间：2026-11-04（本地）｜ 录入：workbuddy 整改流程。

## 一、数字来源与口径

| 指标 | 数值 | 证据文件 |
|---|---|---|
| 扫描仓数 | 71 | `fullrun_71repos.json`（acct/name/lang/updated/structure 逐仓可查） |
| findings 总数 | 753 | `skillgate_fp_survey.clean.json`（逐条 severity/category/file/line/text 可查） |
| CRITICAL | 1 | 同上 |
| HIGH | 8 | 同上 |
| MEDIUM | 62 | 同上 |
| LOW | 101 | 同上 |
| INFO | 581 | 同上 |
| 高危真阳性率 | 9/9 | 1+8 条高危逐条人工复核（描述+文件+行号可查），误报 0 |

- **工具**：skillgate 安全扫描器（同源引擎，`skillgate/scripts/skillgate.py`）。
- **版本锚**：本证据基于 **rule_version v3.1.0** 全量扫描；公开仓当前版本 v3.1.1（P0 注入规则整改版，规则 40 条 / 模式 101 个，自检与 12/12 对抗回归 PASS）。对外引用本组数字时，须注明「v3.1.0 全量扫描口径」，并引用本目录登记哈希。
- **降幅 44.5%**：相对 v2.x 基线的 findings 总量降幅（基线口径见 `.skillgate-audit.jsonl` 工作记录；如需基线全量明细可另行补入本仓）。

## 二、路径清洗说明

原始扫描产物含本机工作路径（`D:\Workbuddy\...`），入仓前已将 `file` 字段归一化为仓内相对路径，避免内部工作痕迹外泄（同 Muse P2-6 整改要求）。清洗仅改动 `file` 字段路径前缀，不改变 findings 内容、severity、行号。

## 三、红队复核记录

- 复核流程：publish-redteam-review（发布前红队评审，G0–G6 + 七问 + 构造击败输入）。
- 结论：**可发布（Gate 通过）**，附 6 条改进建议；复核细节留档于项目评审记录（`07-竞品逆向调研.md` 与 `.skillgate-audit.jsonl`）。
- 说明：本证据仅登记"可发布"结论与上述留档位置，不在此复述评审原文。

## 四、登记

本目录 4 个文件（含本 README）与 `hash-manifest.txt` v4 对应条目逐项一致，可用 `verify_hash_manifest.py` 复核。
