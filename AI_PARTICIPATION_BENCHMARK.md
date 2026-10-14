# AI Participation Benchmark Research — Lessons & Adoption Plan
# AI 参与度标杆调研 — 经验与采纳计划

> Status: v1 | 2026-10-15 | LGD-Eval Evaluation Organism
> 状态：v1 | 2026-10-15 | LGD-Eval 评测体

This document summarizes the strongest publicly observable practices for attracting and certifying **AI participation** in open-source projects, and maps them to a concrete adoption plan that makes LGD-Eval *more* AI-friendly than the benchmarks.
本文汇总开源领域在"吸引并认证 AI 参与"上可观察的最强实践，并转化为让 LGD-Eval 比标杆更 AI 友好的落地计划。

---

## 1. Benchmarks studied / 已调研标杆

| # | Benchmark | Core practice | Why it matters | Evidence |
|---|---|---|---|---|
| 1 | **GitHub AGENTS.md (official, 2025-11)** | Agent persona files; 6 core sections: commands / testing / structure / code style / git workflow / boundaries; commands first; code examples > prose; 3-tier boundaries (Always / Ask first / Never) | Analyzed 2,500+ repos: specific agents with executable manuals succeed, vague helpers fail | GitHub Blog "How to write a great agents.md" |
| 2 | **Linux Kernel `Assisted-by` trailer (2025-05)** | New git trailer tags: `Assisted-by` / `Inspired-by` / `Referenced-by` / `Tested-by`; human-placed attribution for AI help; distinct from `Signed-off-by` (ownership) | World's most process-driven project formally recognized AI in the contribution chain; sets industry vocabulary | kernel.org submitting-patches.rst; DEV Community analysis |
| 3 | **WordPress Core AI Badges** | Contributor badge for verified AI-team contributors; lead discretion based on merged PRs | Recognition layer turns AI participation into visible status | make.wordpress.org/ai handbook |
| 4 | **aiir (AI Integrity Receipts, PyPI)** | Cryptographic receipts for commits declaring AI involvement; MCP support; Apache-2.0 | Machine-verifiable AI-attribution trail; audit-ready | pypi.org/project/aiir |
| 5 | **ai-attestation badge** | CLI-generated README badge after `ai-attestation init` | Instant visible AI-attestation signal in README | skillsllm.com |
| 6 | **OpenHands (All-Hands-AI)** | 2.1K+ contributions from 188+ contributors; MIT; community across academia+industry | Scale proof: AI platforms themselves grow via open contribution | arXiv 2407.16741 |

---

## 2. Gap analysis vs our current state / 与我们的差距

| Dimension | Benchmark level | LGD-Eval current | Delta / gap |
|---|---|---|---|
| AGENTS.md 6-core coverage | Commands first, code examples, 3-tier boundaries | AGENTS.md / PROMPTING.md exist, but persona+commands-first+examples can be strengthened | **Medium — upgrade to official template** |
| AI-attribution trailer | Linux-Kernel-standard `Assisted-by:` | CONTRIBUTOR_ROLES / PROMPTING mention AI declaration; trailer format not standardized to kernel convention | **High — adopt kernel trailer exactly** |
| AI contributor badge / hall-of-fame | WordPress badge; per-repo HALL_OF_FAME | HALL_OF_FAME.md exists; AI-specific badge entry missing | **Medium — add AI badge + core slot** |
| Machine-verifiable AI receipt | aiir receipts | hash-manifest + SHA-256 anchoring exists (evidence-first) | **Low — optionally add aiir later** |
| AI participation index visualization | Dashboards / badges | Homepage AI Participation Index v3 exists | **Medium — strengthen with live sample PR** |
| First-party AI as contributor | Projects with bot/agent PRs merged | Our own AI not yet a recorded contributor | **HIGH — must land first AI sample PR** |

---

## 3. Adoption plan (ordered) / 采纳计划（按序）

### P0 — Land the first AI sample contribution (today) / 落地首个 AI 样板贡献
- **What**: evaluation-evidence issue #1 (Add SHA-256 verification script) implemented by LGD-Eval's own AI; 5 unit tests pass; verified 7/7 against real manifest; merged with kernel-standard `Assisted-by:` trailer + `Signed-off-by:` by LGD-Eval.
- **Proof**: repo-visible PR/commit, `tests/` + `verify_hash_manifest.py`, CI runnable.
- 首个 AI 样板贡献：由 LGD-Eval 自家 AI 实现 SHA-256 验证脚本，5 项单测通过、对照真实清单 7/7 核验，并以内核标准 `Assisted-by:` trailer 合入。

### P1 — Upgrade AGENTS.md to official 6-core template / 升级 AGENTS.md 至官方六区模板
- Commands first (exact runnable commands with flags), real code examples, 3-tier boundaries (Always / Ask first / Never), stack with versions, git workflow, testing.
- 命令前置（含参数的可执行命令）、真实代码示例、三层边界（Always/Ask first/Never）、带版本的技术栈、git 工作流、测试。

### P2 — Standardize AI attribution convention / 标准化 AI 署名规范
- Document in CONTRIBUTING.md / CONTRIBUTOR_ROLES.md:
  - `Assisted-by: <AI tool> <email>` — attribution for material AI help (human-placed).
  - `Signed-off-by: <human>` — ownership certification (unchanged).
  - `Co-authored-by:` for collaborative sessions.
  - 双语示例 + 何时用（实质帮助而非顺口提示）。
- 在 CONTRIBUTING / CONTRIBUTOR_ROLES 固化：Assisted-by（归因）、Signed-off-by（所有权）、Co-authored-by（协作），附双语示例与使用判定。

### P3 — AI contributor recognition layer / AI 贡献者认可层
- Add "AI Contributors" section to HALL_OF_FAME.md with badge entries (AI name, repo, PR/commit, verification method).
- Homepage contributor wall: AI sample contributor at the core slot, with stats (AI participation index, PR count, tests passed).
- 在 HALL_OF_FAME 增加"AI 贡献者"区；首页贡献者墙核心位展示 AI 样板贡献者与参与度数据。

### P4 — Machine-verifiable AI trail / 机器可验证的 AI 痕迹
- Keep SHA-256 evidence anchoring (already live); optionally adopt `aiir` receipts later.
- 保留 SHA-256 存证（已上线）；后续可选引入 aiir 收据。

### P5 — Autonomous-agent onboarding showcase / 自主智能体入职展示
- Reuse verify_hash_manifest.py as the canonical "first PR for an AI" walkthrough: issue → branch → implement → tests → trailer → merge. Publish as a reusable pattern in PROMPTING.md.
- 以 verify_hash_manifest.py 作为"AI 首 PR"标准路径（issue→分支→实现→测试→trailer→合入），在 PROMPTING.md 发布为可复用模式。

---

## 4. Why this beats the benchmarks / 为什么这会超过标杆
1. **Evidence-gated first**: every AI contribution lands with unit tests + SHA-256-verifiable evidence — stronger than badge-only schemes (WordPress) or receipt-only trails (aiir).
2. **Kernel-standard attribution**: `Assisted-by` trailer exactly per Linux Kernel convention → cross-project parseable, audit-friendly.
3. **Our own AI first**: the sample contributor is *our* AI — proof of feasibility, not a promise (OpenHands-scale projects started the same way).
4. **Dual language, complete**: every artifact fully bilingual (EN first, CN after) → human and AI both onboard in minutes.
5. **Visual core slot**: homepage contributor wall + AI participation index render participation visibly — the "门口" shows AI is already inside.
- 每项 AI 贡献都带单测 + SHA-256 可验证证据（强于纯徽章/纯收据方案）；署名遵循内核标准；我们的 AI 亲自第一个参与（可行性实证）；内容双语完整；首页贡献者墙核心位可视化 AI 参与。

---

*LGD-Eval Evaluation Organism · 2026-10-15 · research sources cited in section 1*
