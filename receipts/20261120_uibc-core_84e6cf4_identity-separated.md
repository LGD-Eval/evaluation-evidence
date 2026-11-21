# 评测回执（更正版）：uibc-core @ 84e6cf4（身份隔离评测）

- 评测身份：**LGD-Eval** ｜ 被测身份：**zhaoxinghua09-cell** ｜ 时间 2026-11-20
- 机器：公司机 DESKTOP-IGJBTUB，Windows 10.0.19045，Python **3.13.18**
- 对象：`main@84e6cf4`（PR #324 squash 合并后）

> **本文件更正同目录的前一版。** 前一版"发现 2"（"6 向量包不在 main"）**是错的**，已于同日撤回并在此重写。错因与更正见"更正记录"。

## 一句话结论

**机制层面 PASS；发现项由 2 条降为 1 条**（对外表述与 main 状态的差异仅剩一处）。

## 方法（如实写）

**不是 `git clone`。** 本机对 `github.com` 的 HTTPS 返回 `Empty reply from server`、SSH 无权限，故改用 **API 快照** `GET /repos/.../zipball/84e6cf4`（2,580,039 字节）。快照无 `.git`，完整性由 API 端点保证，不由我保证。
**评测与被测是同一个人的两个身份** → 本回执为 **L2 身份隔离评测**，**不是 L4 第三方验证**。

## 实际运行与结果

| # | 命令 | 结果 |
|---|---|---|
| 1 | `python tools/external_node_check.py --out external_node_result.json` | `independent=PASS  reference=PASS(27ms)  probes=3/3 rejected -> CONSISTENT` |
| 2 | `python independent_verifier/cross_check.py` | `checks compared: 70, mismatches: 0`，`AGREEMENT: PASS` |
| 3 | `python tools/build_standalone_verifier.py` | 产出 `build/uibc_verify.py`（23,478 字节，单文件、纯标准库） |
| 4 | `python build/uibc_verify.py tools/out/_mb/base` | `"result": "PASS"` |
| 5 | `python -m uibc_core.cli verify tools/out/_mb/base` | `"result": "PASS"`，`verifier_version 0.4.1`，`spec_id …@ba0e02c98a65` |

基准复跑：open 9.5% / pinned 4.8%，`M20` 两模式 PASS（已声明的调用方层边界）；语料锚点 `base_open`/`base_pinned` 均 PASS。

## 发现（现存 1 条）

**1. `tools/check_scitt_vectors_standalone.py` 不在 main。**
该文件只存在于未合并分支 `feat/scitt-ambiguous-tree-size-vector`（`07c053c`）。main 上等效但**不等价**的是 `tools/build_standalone_verifier.py` 生成的 `build/uibc_verify.py`：后者验整包（V1–V9），前者是从 RFC 9162 文本重写叶哈希与折叠、专门复算 SCITT 向量包。**两个东西不能互相替代叙述。**

**2. （已撤回）原"6 向量包不在 main"** —— 见下。

## 更正记录（这一条必须留在文件里）

- **前一版写的**："`docs/upstream-package/scitt-rfc9162/v1/manifest.json` 不在 main，目录为空"。
- **事实**：main 上该包**存在**，含 `manifest.json`（6,968 B）、`README.md`、`SHA256SUMS`、`.gitattributes` 与 **5 个向量目录**（`valid-tree4-index0`、`valid-tree8-index2`、`fail-tampered-path`、`fail-wrong-leaf-index`、`fail-wrong-tree-size`）。
- **权威依据**：`GET /git/trees/main?recursive=1`（1,639 项，未截断）逐项列出。
- **错因**：我在本地用 `Get-ChildItem -Recurse -Filter manifest.json` 得到空结果，**误把"我没看到"当成"不存在"**；随后 `GET /contents/<path>?ref=main` 又返回失败（该调用被 try/catch 静默吞掉，未打印状态码），两处错误互相加固，于是我写下了那条结论。
- **正确的写法**：main 上是 **5 个向量**；第 **6** 个（`ambiguous-tree-size`）才在分支上。所以"6 向量包"这个说法本身在 main 上不成立，但"包不在 main"是错的。

## 登记口径

- 本回执归 **L2**（身份隔离，同人）；**不改变 `EVIDENCE-INDEX` 的 V8 = 1**（Correctover，L4）；
- 合并本 PR 的批准来自第三个身份（`stevenzhao07`），**同一人**，属机制性批准，**不构成独立评审**，在 PR 评审正文里已明写。
