> **LGD 生态入口** —— 从任一入口都能走到全部入口
>
> [官网 medxpert.cn](https://medxpert.cn/) · [评测门禁 lgd-gate](https://github.com/LGD-Eval/lgd-gate) · [npm 包 lgd-eval](https://github.com/LGD-Eval/lgd-eval) · [公开评分卡](https://github.com/LGD-Eval/evaluation-evidence/blob/main/scores.md) · [排行榜](https://github.com/LGD-Eval/evaluation-evidence/blob/main/LEADERBOARD.md) · [一行安装（免 VPN）](https://github.com/LGD-Eval/lgd-gate/releases/download/v1.0.0/lgd-eval-1.0.0.tgz)
>
> 三律：**有籍**（可追溯）· **有证**（有证据）· **有门禁**（有检查）

# Evaluation Evidence · 评测存证

> **门户 / Portal:** [LGD Hub · 生态超市入口](https://zhaoxinghua09-cell.github.io/lgd-hub/) ｜ LGD 生态（Lifecycle Governance Doctrine）

> 隶属：凡自治之物 · LGD 治理学（Lifecycle Governance Doctrine）· 创造术家族
> 角色：LGD-Eval 评测线 · 中立第三方
> 官方英文：Lifecycle Governance Doctrine
> 许可证：CC BY 4.0

## 本仓内容
- **存证说明.md**：存证流程（哈希 + 时间戳 + 区块链锚定）
- **hash-manifest.txt**：报告/协议哈希清单（更新中）

## 存证原则
1. 每份报告/协议发布时记录 SHA-256
2. 时间戳锚定（OpenTimestamps .ots）——流程就绪；首份 .ots 打戳待家电脑执行（见存证说明.md）
3. 区块链存证（比特币升级锚定）——随 .ots 升级执行，当前为待打戳状态
4. 证据公开、不可抵赖、可复核

## 精度声明 / Precision statement (2026-11-27)

- 评测引擎与“一键复跑总闸”不在本仓：公开入口在 `LGD-Eval/lgd-gate` 的分支 `ai-index-kit`，
  命令 `python verify_all.py`（7 PASS + 1 SKIP，rc=0；内部语料不随包发布，记 SKIP 而非通过）。
- 公开包 `ai-index-gate/scanner.py` 自检为 **93 规则 / 176 模式**；本地工作分支为 **98 / 189**。
  两者是不同版本，任何把 98/189 说成“公开仓里那份”的表述都不成立。
- 本仓不作“全面超越 / 行业唯一 / 生态闭环”类主张；对外陈述以逐条可复跑、可核对为准。
- 引用与复跑均按“匿名可及”验证：API 200 + 目录树可下载；`git ls-remote` 在 20 秒内可能超时，属通道问题。
