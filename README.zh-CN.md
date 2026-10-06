<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/brand/imagination-octo-logo-dark.png" />
  <img src="assets/brand/imagination-octo-logo.png" alt="IMAGINATION OCTO — 广泛伸展，只选其一" width="380" />
</picture>

# IMAGINATION OCTO

**REACH WIDE · CHOOSE ONE**

### 面向 Claude Code 与 Codex 的人机协作创意插件 —<br/>先给出不同的想法，再由你选择，最后得到经过检验的概念

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

[![Tests](https://img.shields.io/github/actions/workflow/status/djfksjd/imagination-octo/tests.yml?style=flat-square&label=tests)](https://github.com/djfksjd/imagination-octo/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-MIT-1f2937?style=flat-square)](LICENSE)
![Stage](https://img.shields.io/badge/stage-v0.3%20beta-d69526?style=flat-square)
![Skills](https://img.shields.io/badge/skills-3-6d5ef5?style=flat-square)
![Hosts](https://img.shields.io/badge/hosts-Claude%20Code%20%C2%B7%20Codex-0ea5b7?style=flat-square)

</div>

Imagination Octo 同时向多个方向伸展，然后停下。它返回少量在机制上而非措辞上不同的想法，并结束这一轮。只有在你选定一个之后，它才会检验并发展该方向。唯独“决定”这一步，它不做自动化。

**当前为 `v0.3 beta`。** 下列测量结果来自单一模型（`gpt-5.4`）生成、同一模型系列的 AI 调用评审、且简报数量较少的实验。尚未在 Claude 上测量，也不代表普遍意义上的创造力。

## 功能

| | |
|---|---|
| **发散组合** | 通过直接搜索、机制迁移、前提转换三轮产生 3–5 个方向。仅名称或主题不同的变体会被剔除。 |
| **契合度拥有否决权** | 无论多么出人意料，削弱硬性约束的想法都会被舍弃。换个名字的违规仍是违规。 |
| **由你选择** | 路由器不会在同一轮中既选择又发展。自动串联在测试中降低了约束契合度，因此强制停顿。 |
| **压力测试** | 被选中的想法要面对其承重假设、更简单的常规方案，以及自身机制导致的失败。 |
| **诚实的失败** | 如果常规答案更好，或该方向经不起检验，它会直说并让你回到发散阶段。 |
| **小型运行时** | 只有三个技能文件。运行时没有牌组、禁用清单、关卡或脚本；测试中的 token 约为普通提示词的 1.1 倍。 |

## 工作原理

```text
 your brief ──► ┌─────────── diverge · imagination-engine ───────────┐
                │  direct pass · mechanism transfer · premise shift  │
                │    cull by failure · private proof per survivor    │
                └──────────────────────────┬─────────────────────────┘
                                           ▼
                               3–5 distinct directions
                                           ▼
                                    ◆ YOU CHOOSE ◆        the turn always ends here
                                           ▼
                ┌─────── develop · imagination-brainstorming ────────┐
                │ load-bearing assumption · conventional competitor  │
                │   native failure mode · boring half · falsifier    │
                └──────────────────────────┬─────────────────────────┘
                                           ▼
                             decision-ready concept memo
```

- 两个阶段之间的停顿是方法的一部分，而不是界面细节。
- 搜索与验证过程保持内部。你得到的是想法，而不是流水线运行报告。
- 不做实现。产出是可以交给规划阶段的概念。

## 快速开始

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination-octo/main/install.sh | bash
```

更新时再次运行同一条命令即可。如果提示存在以前单独安装的技能副本，请把命令结尾改为 `| bash -s -- --clean-legacy` 再运行；它只会把这些副本移走，不会删除。

然后这样提问：

```text
使用 $imagination-octo，为一款叙事游戏设计几种谈判机制，
不使用对话树、隐藏骰子或说服属性。
```

第一次回复以一个选择题结束。用编号或方向回答即可：

```text
请发展第 2 个方案。
```

## 一个插件，三个技能

| 技能 | 适用场景 | 返回内容 |
|---|---|---|
| `$imagination-octo` | 大多数请求 | 组合 → 你的选择 → 发展后的概念 |
| `$imagination-engine` | 只需要发散时 | 3–5 个有用且不显而易见的方向 |
| `$imagination-brainstorming` | 已经选定想法时 | 可用于决策的概念备忘录 |

## 测量结果（2026-07-30）

与强普通提示词的预注册盲测对比。10 个全新的英文和韩文简报，每个条件运行 5 次，5 名评审。

| 运行时 | 更愿意继续发展的一方 | 主要提升（1–7 分制） | Token |
|---|---|---|---|
| Engine v0.5.3 | **50 比 0（100.0%）** | 有用的意外性 `+0.97` · 多样性 `+0.66` · 契合度 `+0.60` | 1.12 倍 |
| Concept Workshop v0.4.2 | **45 比 5（90.0%）** | 可执行性 `+1.37` · 契合度 `+0.95` · 稳健性 `+0.82` | 1.14 倍 |

请如实解读：

- **生成与评审都只用了 `gpt-5.4`。** 目前没有 Claude 运行，也没有人类评审。同一模型系列的评审可能有相同的偏好。
- **10 个简报是很小的分布。** 95% Wilson 区间：Engine 92.9–100.0%，Workshop 78.6–95.7%。
- **它也会输。** Workshop 有一个简报被全体评审判给普通提示词，更早的 Engine 版本在一个戏剧简报上也是如此。
- **早期设计彻底失败。** 牌组加关卡的流水线（Engine v0.4.0）以 48 倍成本对普通提示词 0 比 30 落败，已被替换。该记录保留在 Engine 仓库中。
- **尚未测量：** 多次独立运行是否收敛到相同的想法，以及把两轮完整流程作为一个产品的评估。
- **正在测量：** Experiment A 已在 [`evals/`](evals/PREREGISTRATION.md) 预注册：包含投入对等的对照组在内的四个条件、GPT 与 Claude 两种生成模型、跨系列评审、多次运行间的收敛度，以及盲测验证。无论结果如何，都会替换这份清单。两轮流程的行为回归测试也在同一目录。

协议、判定规则与结果文件：[Imagination Engine](https://github.com/djfksjd/imagination-engine-skill) · [Imagination Brainstorming](https://github.com/djfksjd/imagination-brainstorming-skill)。

## 何时使用，何时不用

**适合使用：** 你需要真正不同的选项时——概念、前提、机制、产品、服务、世界观、仪式，或之前的想法显得平庸时。

**请用普通提示词：** 事实性问题、常规实现、仅需命名，以及任何常规答案就是正确答案的情况。

## 选择日志（需主动开启）

默认关闭。开启后，每当你选定一个方向或否决一组方案，本机的 `~/.imagination-octo/choices.jsonl` 就会追加一行：展示过的方向、你的选择，以及你给出的理由。除非你要求保存原文，简报只以哈希形式保存。不会上传任何内容，技能也从不读取这份日志；它只用于你日后回看自己的选择。`enable --hosts` 会在全局 `CLAUDE.md` / `AGENTS.md` 中加入带标记的一行，让技能知道你已开启，`disable` 则会将其移除。

```bash
LOG=https://raw.githubusercontent.com/djfksjd/imagination-octo/main/skills/imagination-octo/scripts/choice_log.py
curl -fsSL $LOG | python3 - enable --hosts claude,codex   # --with-brief keeps the brief text
curl -fsSL $LOG | python3 - stats
curl -fsSL $LOG | python3 - disable
```

## 由 `imagination` 更名而来

本插件及其路由技能在 v0.1.3 之前名为 `imagination`。GitHub 会重定向旧仓库地址，但插件名和路由命令已更改：请移除旧的 `imagination` 插件，安装 `imagination-octo`，并使用 `$imagination-octo` 调用。两个专用技能的名称不变。 从 v0.3 起，市场 ID 也由 `djfksjd` 改为 `imagination-octo`，因为旧 ID 与同一作者的其他插件冲突。现在的安装目标是 `imagination-octo@imagination-octo`。

## 手动安装

```bash
# Claude Code
claude plugin marketplace add djfksjd/imagination-octo
claude plugin install imagination-octo@imagination-octo

# Codex
codex plugin marketplace add djfksjd/imagination-octo
codex plugin add imagination-octo@imagination-octo
```

## 开发

专用运行时在各自的仓库中维护和评估。发布前请同步两个 `SKILL.md`，验证全部三个技能，运行仓库测试，并对两轮选择边界做前向测试。

```bash
python3 -m pytest tests/ -q
bash -n install.sh
```

## 许可证

[MIT](LICENSE)。
