<div align="center">

# ✨ Imagination

**異なるアイデアを生み出し、自分で選び、生き残った案を深める。**

Codex と Claude Code のための、人間参加型クリエイティブプラグイン。

[![Tests](https://github.com/djfksjd/imagination/actions/workflows/tests.yml/badge.svg)](https://github.com/djfksjd/imagination/actions/workflows/tests.yml)
![Version](https://img.shields.io/badge/version-0.1.2-7c3aed)
![License](https://img.shields.io/badge/license-MIT-0f766e)

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

</div>

---

Imagination は、AI が自動化すべきでない **選択** をユーザーに残します。
因果的に異なる案を先に提示し、選択された案だけを検証・具体化します。

```text
ブリーフ → 3〜5案 → あなたが選択 → 検証済みコンセプト
```

## クイックスタート

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination/main/install.sh | bash
```

```text
$imagination を使って、このブリーフに対する異なる方向性を複数提案して。
```

最初の回答で番号を選ぶと、次のターンでその案だけを発展させます。

## 3つのスキル

| スキル | 用途 |
|---|---|
| `$imagination` | 推奨。発散から選択、具体化まで |
| `$imagination-engine` | 有用で意外性のある3〜5案を生成 |
| `$imagination-brainstorming` | 選択済みの案を意思決定可能な形にする |

> [!IMPORTANT]
> 同じターンでAIが勝手に選び、発展させることはありません。ユーザーの
> 選択が発散と具体化の境界です。

## 評価結果

| ランタイム | 強い通常プロンプトとの比較 | 主な改善 |
|---|---:|---|
| Engine v0.5.3 | **50–0 (100.0%)** | 有用な意外性 `+0.97`、多様性 `+0.66`、適合性 `+0.60` |
| Workshop v0.4.1 | **25–5 (83.3%)** | 実行可能性 `+1.37`、適合性 `+0.59`、因果的明瞭さ `+0.59` |

これは事前登録したテスト分布でのモデル審査結果であり、普遍的な創造性を
保証するものではありません。

## 手動インストール

```bash
claude plugin marketplace add djfksjd/imagination
claude plugin install imagination@djfksjd
codex plugin marketplace add djfksjd/imagination
codex plugin add imagination@djfksjd
```

MIT License.
