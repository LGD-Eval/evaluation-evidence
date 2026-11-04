# Trust Score 双引擎口径声明（v4.3 更正版）

> 背景：Muse 外审指出自评口径不可复现（BLOG 99/100 A+ vs 派单 68→94/A+ vs 复算 89/A、0/F）。本文件统一口径；v4.2 按 HEAD 实测更正引擎身份、分数归属与计分公式；v4.3 按 Muse 2026-11-05 复核要求，以干净克隆实测值更正全仓自扫数字，并记录 v3.1.2→v3.1.3 的 AST 双计修复。

## 一、引擎身份（更正：两仓 skillgate.py 为同一引擎双副本）

| 组件 | 位置 | 身份 | 说明 |
|---|---|---|---|
| skillgate 扫描器 | `LGD-Eval/lgd-gate/skillgate.py` **与** `zhaoxinghua09-cell/skillgate/scripts/skillgate.py` | **同一引擎的两个发布副本**（双仓 blob 逐字节一致，当前 rule_version=v3.1.3；两仓均含 ast_analyzer.py，AST 分析能力一致；LGD-Eval 仓为正典，skillgate 仓为同步副本） | AI 技能安全与质量扫描门禁（40 规则 / 101 模式） |
| LGD 评测入口 | `LGD-Eval/lgd-gate/evaluate.py`（发布包 `coze-publish/02-skill-eval-engine/scripts/evaluate.py`） | **独立的五维评测引擎**（结构/目录/文档/安全/生态），负责对外评测报告与五维雷达 | 评分口径与 skillgate 扫描器不同 |

> 更正点（Muse 复测窄修 ③）：上一版误称两仓为"不同产品线、非同一引擎的两个版本"。实际两仓 skillgate.py 内容逐字节一致（Git blob SHA 相同），属同一引擎双副本。evaluate.py 是另一引擎（五维评测），此前文档未明确其独立身份。

## 二、计分公式（skillgate 扫描器，v3.1.3 HEAD 实测）

- 100 起扣：CRITICAL -15 / HIGH -8 / MEDIUM -4 / LOW -1；缺 frontmatter 必需字段 -10（无 frontmatter -20）。
- **无网络依赖奖励：+2**（存在 network 类 finding 时不得）。
- **CRITICAL 注入/外泄封顶：存在 CRITICAL prompt-injection / exfiltration 命中时，分数上限 40（最高 D 档），同时 CI 门禁 exit 1 阻断**（Muse 复测 P0 窄修）。
- clamp 0–100；等级：A+ (≥90) / A (≥80) / B (≥70) / C (≥60) / D (≥40) / F (<40)。

> 更正点：上一版公式漏写 +2 无网络奖励；v3.1.2 起新增 CRITICAL 注入/外泄封顶 40/D；v3.1.3 修复 scan_python_file 中 AST 分析重复执行（同一命中曾被报两条），现每行至多一条。

## 三、同一样本分数差异的来源

- **skillgate 扫描器 vs evaluate.py 是两套引擎、两套口径**：扫描器输出"规则命中扣分后的 Trust Score"，evaluate.py 输出"五维结构分"。同一仓库（如 lgd-gate 仓根）两引擎给出不同分数（54/D vs 89/A）是设计使然——前者是安全检查门禁，后者是技能结构评测，**不得互比**。
- 两仓 skillgate.py 双副本对同一样本输出**相同**分数（同引擎、同规则集、同版本）。

## 四、引用规范（对外强制）

1. 引用任何 Trust Score / 等级，必须同时标注：**引擎名 + rule_version + 扫描对象 + 日期**。例：`skillgate v3.1.3 @ zhaoxinghua09-cell/skillgate 全仓（干净克隆 948b0ff）= 0/F、23 findings（CRIT4/HIGH4/MED4/LOW6/INFO5）`。
2. 禁止裸引自评数字不附证据；全部数字须能在 evaluation-evidence 仓找到原始产物（P1-4 目录 / 本文件）。
3. 两引擎分数**不得互比**；同引擎跨版本对比须注明版本。
4. 自评分仅作内部基线；对外以第三方实测（Muse 外审）为准。

## 五、HEAD 实测记录（2026-11-04 · v3.1.2 正典本地实跑）

- **skillgate v3.1.3 @ zhaoxinghua09-cell/skillgate 全仓（干净克隆 tarball @948b0ff，含 ast_analyzer.py）= 0/F、23 findings**（CRITICAL×4 / HIGH×4 / MEDIUM×4 / LOW×6 / INFO×5）。CRIT/HIGH 全部命中于引擎仓库自身的开发脚本与演示样本——`run.py`、`run-all-tests.py`、`ci-simulator.py` 的 subprocess(shell=True)，`ecosystem.py`、`pressure_test.py` 的 shutil.rmtree，以及 `examples/bad-skill` 演示样本——属"扫描器扫自身源码"的自证特性，**不代表被扫技能包的交付质量**；本工具的正确扫描对象是技能包（SKILL.md + scripts/），对引擎仓库全仓自扫仅供内部基线。
- **evaluate.py @ LGD-Eval/lgd-gate 仓根 = 89/A**（五维：结构 100 / 目录 47 / 文档 85 / 安全 100 / 生态 100；缺 scripts/ 与 examples/ 目录）。
- 结论：89/A 属 **evaluate.py 五维评测** 的分数，非 skillgate 扫描器自扫；全仓自扫（v3.1.3）= **0/F、23 findings**。两分数口径不同，引用必须按第四条规范附完整标注。

## 六、口径变更记录（v4.3 · 2026-11-05）

- **触发**：Muse 复核（receipts/20261105_01）指出 v4.2 所载"54/D、19 findings（LOW7/INFO6）"在干净克隆上不可复现，实测为 55/D、17 findings。
- **复盘**：执行席 v4.2 数字取自本地工作树（含未跟踪/旧文件，多 1 LOW + 1 INFO），非发布字节；同时 v3.1.2 的 `scan_python_file` 存在 AST 分析重复执行缺陷——AST 与正则两条通道各报一次同一命中（发现 12 条中 6 组双计）。
- **修复（v3.1.3）**：`scan_python_file` 移除重复 AST 调用，保留函数开头带行级去重的 AST 步骤；`ast_analyzer.py` 同步进 LGD-Eval/lgd-gate 仓，使两仓扫描能力（含 AST）一致。两仓 blob 逐字节一致（skillgate.py `7126100ab55d`，ast_analyzer.py `58a2b79e6099`）。
- **双口径对照（同一棵树 zhaoxinghua09-cell/skillgate @948b0ff）**：
  - 纯正则口径（ast_analyzer 未加载，Muse 2026-11-05 复跑环境）：**17 findings / 55/D**（CRIT1/HIGH1/MED4/LOW6/INFO5）。
  - AST + 正则口径（v3.1.3 起两仓均可用，本文采用）：**23 findings / 0/F**（CRIT4/HIGH4/MED4/LOW6/INFO5）。
  - 差额 6 条 = AST 通道额外检出的 subprocess(shell=True) 与 shutil.rmtree（均已去重，每行一条）。
- **v3.1.3 回归实测（P0 不回归）**：frontmatter 恶意样本 → CRITICAL prompt-injection 检出 + 40/D + exit 1；正文注入样本 → 同上；干净样本 → 0 findings / 100/A+ / exit 0。
