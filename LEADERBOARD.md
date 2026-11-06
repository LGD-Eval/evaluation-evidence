# LGD 认证榜（LGD Certified）

> 一个技能值不值得装，不该看下载量，该看它有没有过门禁。
> 本榜只收**经 LGD 评测引擎实跑、分数 ≥ 90（A+）**的技能，每条都附可复现命令与证据。

## 为什么会有这个榜

技能市场现在的问题是：**下载量高 ≠ 安全，描述好看 ≠ 能用**。
LGD 三律给了三条硬判据：有籍（有档案）、有证（有证据）、有门禁（有检查）。
本榜就是把这三条变成一张公开可查的表。

## 榜单（按分数排序）

| 排名 | 技能 | 分数 | 等级 | 三律 | 认证日期 | 证据 |
|---|---|---|---|---|---|---|
| 1 | lgd-gate-methodology | 100/100 | A+ | L1✅ L2✅ L3✅ | 2026-11-06 | `python evaluate.py 01-skill-methodology` |
| 2 | lgd-eval-engine | 100/100 | A+ | L1✅ L2✅ L3✅ | 2026-11-06 | `python evaluate.py 02-skill-eval-engine` |
| 3 | skill-scout | 100/100 | A+ | L1✅ L2✅ L3✅ | 2026-11-06 | `python evaluate.py 12-skill-scout` |

## 怎么上榜

```bash
# 1. 自测，看够不够 90
python evaluate.py <你的技能目录> --fix-json fix-plan.json

# 2. 按 fix-plan.json 逐项整改（每项都有 acceptance，改完能自检）

# 3. 达标后登记
python certify.py <你的技能目录> --name <技能名> --repo <仓库地址>
```

上榜要求（三条都满足才收）：

1. **分数 ≥ 90（A+）**，且安全维度无 HIGH / CRITICAL
2. **三律不缺项**：有籍（LICENSE + CHANGELOG）、有证（examples + 可复现命令）、有门禁（SECURITY + 评测记录）
3. **可复现**：任何人 clone 下来跑同一条命令，能得到同一个分数

## 挂徽章

达标后把徽章贴进 README，别人点进来就能看到榜单：

```markdown
[![LGD Certified A+](https://raw.githubusercontent.com/LGD-Eval/evaluation-evidence/main/badge-a-plus.svg)](https://github.com/LGD-Eval/evaluation-evidence)
```

## 反刷分声明

本榜不接受"只为自己刷高分"的提交。评测器是同一份代码、同一套权重，任何条目都能被第三方重跑验证。
分数不达标就如实上榜为"未通过"，不做隐藏。

---

理论依据：LGD 三律（有籍 / 有证 / 有门禁），AI 治理标准参与研究（W3C / ITU-T FG-TIDA）。

> 评测对象说明：上表评的是**技能包目录**（`coze-publish/01-skill-methodology` 等），不是仓库整体。各仓库自身（含 CI、依赖、文档）的自评分见该仓 README 顶部，两者对象不同、不可互相替代，也不存在第二套评分口径。
