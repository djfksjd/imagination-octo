<div align="center">

# ✨ Imagination

**生成不同创意，由你选择，再深入打磨经得住检验的方向。**

面向 Codex 与 Claude Code 的人机协作创意插件。

[![Tests](https://github.com/djfksjd/imagination/actions/workflows/tests.yml/badge.svg)](https://github.com/djfksjd/imagination/actions/workflows/tests.yml)
![Version](https://img.shields.io/badge/version-0.1.1-7c3aed)
![License](https://img.shields.io/badge/license-MIT-0f766e)

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

</div>

---

Imagination 把 AI 不应替你完成的环节——**选择**——留给用户。它先产生
因果机制不同的方向，等待你选择，然后只对选中的创意进行检验和深化。

```text
需求简报 → 3–5 个不同方向 → 你来选择 → 经检验的概念
```

## 快速开始

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination/main/install.sh | bash
```

```text
使用 $imagination 为这个需求提出几个真正不同的方向。
```

首次回答会停在选择环节；回复编号后，下一轮才会深化该方向。

## 三个技能

| 技能 | 用途 |
|---|---|
| `$imagination` | 推荐入口：发散、选择、深化 |
| `$imagination-engine` | 生成 3–5 个有用且非显而易见的方向 |
| `$imagination-brainstorming` | 把已选方向变成可决策的概念备忘录 |

> [!IMPORTANT]
> 路由器不会在同一轮中替用户选择并继续深化。用户选择是两个阶段之间的
> 必要边界。

## 测试结果

| 运行时 | 对强普通提示词的偏好 | 主要提升 |
|---|---:|---|
| Engine v0.5.2 | **25–5（83.3%）** | 有用的意外性 `+0.98`、多样性 `+0.93`、契合度 `+0.31` |
| Workshop v0.4.1 | **25–5（83.3%）** | 可执行性 `+1.37`、契合度 `+0.59`、因果清晰度 `+0.59` |

结果来自预注册测试分布中的模型评审，并不代表对所有创意任务都普遍占优。

## 手动安装

```bash
claude plugin marketplace add djfksjd/imagination
claude plugin install imagination@djfksjd
codex plugin marketplace add djfksjd/imagination
codex plugin add imagination@djfksjd
```

MIT License.
