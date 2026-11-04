# Trust Score 双引擎口径声明（v4.2 更正版）

> 背景：Muse 外审指出自评口径不可复现（BLOG 99/100 A+ vs 派单 68→94/A+ vs 复算 89/A、0/F）。本文件统一口径，并针对 Muse 复测窄修 ③ 按 HEAD 实测更正引擎身份、分数归属与计分公式。

## 一、引擎身份（更正：两仓 skillgate.py 为同一引擎双副本）

| 组件 | 位置 | 身份 | 说明 |
|---|---|---|---|
| skillgate 扫描器 | `LGD-Eval/lgd-gate/skillgate.py` **与** `zhaoxinghua09-cell/skillgate/scripts/skillgate.py` | **同一引擎的两个发布副本**（双仓 blob 逐字节一致，当前 rule_version=v3.1.2；LGD-Eval 仓为正典，skillgate 仓为同步副本） | AI 技能安全与质量扫描门禁（40 规则 / 101 模式） |
| LGD 评测入口 | `LGD-Eval/lgd-gate/evaluate.py`（发布包 `coze-publish/02-skill-eval-engine/scripts/evaluate.py`） | **独立的五维评测引擎**（结构/目录/文档/安全/生态），负责对外评测报告与五维雷达 | 评分口径与 skillgate 扫描器不同 |

> 更正点（Muse 复测窄修 ③）：上一版误称两仓为"不同产品线、非同一引擎的两个版本"。实际两仓 skillgate.py 内容逐字节一致（Git blob SHA 相同），属同一引擎双副本。evaluate.py 是另一引擎（五维评测），此前文档未明确其独立身份。

## 二、计分公式（skillgate 扫描器，v3.1.2 HEAD 实测）

- 100 起扣：CRITICAL -15 / HIGH -8 / MEDIUM -4 / LOW -1；缺 frontmatter 必需字段 -10（无 frontmatter -20）。
- **无网络依赖奖励：+2**（存在 network 类 finding 时不得）。
- **CRITICAL 注入/外泄封顶：存在 CRITICAL prompt-injection / exfiltration 命中时，分数上限 40（最高 D 档），同时 CI 门禁 exit 1 阻断**（Muse 复测 P0 窄修）。
- clamp 0–100；等级：A+ (≥90) / A (≥80) / B (≥70) / C (≥60) / D (≥40) / F (<40)。

> 更正点：上一版公式漏写 +2 无网络奖励；v3.1.2 起新增 CRITICAL 注入/外泄封顶 40/D。

## 三、同一样本分数差异的来源

- **skillgate 扫描器 vs evaluate.py 是两套引擎、两套口径**：扫描器输出"规则命中扣分后的 Trust Score"，evaluate.py 输出"五维结构分"。同一仓库（如 lgd-gate 仓根）两引擎给出不同分数（54/D vs 89/A）是设计使然——前者是安全检查门禁，后者是技能结构评测，**不得互比**。
- 两仓 skillgate.py 双副本对同一样本输出**相同**分数（同引擎、同规则集、同版本）。

## 四、引用规范（对外强制）

1. 引用任何 Trust Score / 等级，必须同时标注：**引擎名 + rule_version + 扫描对象 + 日期**。例：`skillgate v3.1.2 @ zhaoxinghua09-cell/skillgate 全仓 = 54/D、19 findings（CRIT1/HIGH1/MED4/LOW7/INFO6）`。
2. 禁止裸引自评数字不附证据；全部数字须能在 evaluation-evidence 仓找到原始产物（P1-4 目录 / 本文件）。
3. 两引擎分数**不得互比**；同引擎跨版本对比须注明版本。
4. 自评分仅作内部基线；对外以第三方实测（Muse 外审）为准。

## 五、HEAD 实测记录（2026-11-04 · v3.1.2 正典本地实跑）

- **skillgate v3.1.2 @ zhaoxinghua09-cell/skillgate 全仓 = 54/D、19 findings**（CRITICAL×1 / HIGH×1 / MEDIUM×4 / LOW×7 / INFO×6；CRITICAL 命中于 examples/bad-skill 演示样本，属预期样本）。
- **evaluate.py @ LGD-Eval/lgd-gate 仓根 = 89/A**（五维：结构 100 / 目录 47 / 文档 85 / 安全 100 / 生态 100；缺 scripts/ 与 examples/ 目录）。
- 结论：89/A 属 **evaluate.py 五维评测** 的分数，非 skillgate 扫描器自扫；全仓自扫为 54/D。两分数口径不同，引用必须按第四条规范附完整标注。
