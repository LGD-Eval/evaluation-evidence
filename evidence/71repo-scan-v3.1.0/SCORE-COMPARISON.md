# Trust Score 双引擎口径声明（P1-5 整改）

> 背景：Muse 外审指出自评口径不可复现（BLOG 99/100 A+ vs 派单 68→94/A+ vs 复算 89/A、0/F；lgd-gate 与 skillgate 对同一样本给 61/C 与 80/A 无分工/换算说明）。本文件统一口径。

## 一、引擎分工（两套是不同的产品线，非同一引擎的两个版本）

| 引擎 | 位置 | 定位 | 扫描面 |
|---|---|---|---|
| lgd-gate 引擎 | `LGD-Eval/lgd-gate/skillgate.py` | LGD 评测线方法论引擎（有籍/有证/有门禁） | SKILL.md 门禁 + 代码注入/外泄/伪装声明（40 规则 / 101 模式） |
| skillgate 扫描器 | `zhaoxinghua09-cell/skillgate/scripts/skillgate.py` | 独立 AI 技能安全扫描器（Snyk for skills） | 更宽规则集：含 FIXED_DOWNGRADE 降级表、依赖漏洞、跨行 shell 等 |

## 二、计分公式（两引擎相同）

- 100 起扣：CRITICAL -15 / HIGH -8 / MEDIUM -4 / LOW -1；缺 frontmatter 必需字段 -10（无 frontmatter -20）；clamp 0–100。
- 等级：A+ (≥90) / A (≥80) / B (≥70) / C (≥60) / D (≥40) / F (<40)。

## 三、同一样本得分不同（61/C vs 80/A）的原因

两引擎计分权重相同，但**规则集与扫描面不同** → 同一技能命中的 findings 集合不同 → 扣分不同。差异是设计使然（分工不同），不是同一算法的不一致。

## 四、引用规范（对外强制）

1. 引用任何 Trust Score / 等级，必须同时标注：**引擎名 + rule_version + 扫描对象 + 日期**。例：`skillgate v3.1.0 @ 71仓全量 = 753 findings（CRIT1/HIGH8，误报0）`。
2. 禁止裸引自评数字（如「68→94/A+」）不附证据；全部数字须能在 evaluation-evidence 仓找到原始产物（P1-4 目录）。
3. 两引擎分数**不得互比**（口径不同）；同引擎跨版本对比须注明版本。
4. 自评分（如 89/A）仅作内部基线；对外以第三方实测（Muse 外审）为准。

## 五、复算记录（2026-11-04）

- lgd-gate 引擎扫描 lgd-gate 自身：89/A（v3.1.1）。
- skillgate 扫描器扫描 skillgate 整仓：0/F（规则自扫自证陷阱，与引擎计分无换算关系）。
- 结论：两分数属不同引擎口径，均不得单独对外引用，须按第四条规范附带完整标注。
