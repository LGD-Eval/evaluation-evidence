# 评测回执：uibc-core @ 84e6cf4（身份隔离评测）

- 评测身份：**LGD-Eval**（评测号）
- 被测身份：**zhaoxinghua09-cell**（理论号）
- 时间：2026-11-20（北京时间 16:0x）
- 机器：公司机 DESKTOP-IGJBTUB，Windows 10.0.19045，Python **3.13.18**
- 对象：`main@84e6cf4`（PR #324 squash 合并后的提交）

## 一句话结论

**机制层面 PASS；文档层面的两处"已交付"说法需降级。** 见"发现"第 1、2 条——这不是代码缺陷，是**对外文字与 main 实际状态不一致**，属于我方最忌的那类错。

## 方法（必须如实写清，因为它影响可信度）

**不是 `git clone`。** 本机对 `github.com` 的 HTTPS 返回 `Empty reply from server`，SSH 报无权限；因此改用 **API 快照**：`GET /repos/zhaoxinghua09-cell/uibc-core/zipball/84e6cf4`（2,580,039 字节），解压后运行。快照**没有 `.git`**，无法自证"确为 84e6cf4 的完整树"——这一条由 API 端点自身保证，不由我保证。

**评测身份与被测身份是同一个人。** 因此本回执是 **L2 身份隔离评测**，**不是 L4 第三方外部节点**。任何把它写成"第三方验证"的引用都是错的，包括我方自己引用。

## 实际运行与结果

| # | 命令 | 结果 |
|---|---|---|
| 1 | `python tools/external_node_check.py --out external_node_result.json` | `independent=PASS  reference=PASS(27ms)  probes=3/3 rejected -> CONSISTENT` |
| 2 | `python independent_verifier/cross_check.py` | `checks compared: 70, mismatches: 0`，`AGREEMENT: PASS` |
| 3 | `python tools/build_standalone_verifier.py` | 产出 `build/uibc_verify.py`（23,478 字节，单文件、纯标准库） |
| 4 | `python build/uibc_verify.py tools/out/_mb/base` | `"result": "PASS"`（V 系列检查项） |
| 5 | `python -m uibc_core.cli verify tools/out/_mb/base` | `"result": "PASS"`，`verifier_version 0.4.1`，`spec_id uibc-core/0.3.3-proposal@ba0e02c98a65` |

基准复跑（`external_node_check` 内含）：open 假接受率 9.5%、pinned 4.8%，`M20` 在两模式 PASS（属已声明的调用方层边界）；语料锚点 `base_open/base_pinned` 均需 PASS，本次均 PASS。

## 发现（按严重度）

**1. `check_scitt_vectors_standalone.py` 不在 main。** 该文件只存在于未合并分支 `feat/scitt-ambiguous-tree-size-vector`（`07c053c`）。任何"零依赖复算器已交付/clone 即跑"的表述，若指这个文件名，**在 main 上不成立**。main 上等效的东西是 `tools/build_standalone_verifier.py` 生成的 `build/uibc_verify.py`（第 3、4 行已验证可用），**名字不同、用途也不同**（前者复算 RFC 9162 向量，后者验整包），不能互相替代叙述。

**2. `docs/upstream-package/scitt-rfc9162/v1/manifest.json` 也不在 main。** `docs/upstream-package/scitt-rfc9162` 目录存在但为空表（无 manifest、无向量）。所以"6 向量包（含 `ambiguous-tree-size`）"同样是**分支状态**，不能写成仓库现状。**这一点比第 1 条更要紧**：issue #684 里我引用了该路径并写明"branch `feat/...`"，措辞没超界；但任何省略分支限定的转述都会变成不实陈述。

**3. 无新缺陷。** 以上两条均为**表述—现状不一致**，代码本身在第 1–5 行命令下全部通过。

## 登记口径

- 本回执归 **L2 异体对抗审查**（身份隔离，同人）；
- **EVIDENCE-INDEX 的 V8 仍为 1**（Correctover，L4），本回执**不改变该数字**；
- 若要把这里的第 1–5 行升级为 L4，唯一路径是：**由仓外的人**在仓外环境跑同一组命令并回传结果文件。
