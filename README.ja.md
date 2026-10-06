<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/brand/imagination-octo-logo-dark.png" />
  <img src="assets/brand/imagination-octo-logo.png" alt="IMAGINATION OCTO — 広く伸ばし、ひとつを選ぶ" width="380" />
</picture>

# IMAGINATION OCTO

**REACH WIDE · CHOOSE ONE**

### Claude Code と Codex のための人間参加型クリエイティブプラグイン —<br/>まず異なるアイデア、次にあなたの選択、最後に検証済みのコンセプト

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

[![Tests](https://img.shields.io/github/actions/workflow/status/djfksjd/imagination-octo/tests.yml?style=flat-square&label=tests)](https://github.com/djfksjd/imagination-octo/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-MIT-1f2937?style=flat-square)](LICENSE)
![Stage](https://img.shields.io/badge/stage-v0.4%20beta-d69526?style=flat-square)
![Skills](https://img.shields.io/badge/skills-3-6d5ef5?style=flat-square)
![Hosts](https://img.shields.io/badge/hosts-Claude%20Code%20%C2%B7%20Codex-0ea5b7?style=flat-square)

</div>

Imagination Octo は複数の方向へ同時に腕を伸ばし、そこで止まります。言い回しではなく仕組みが異なるアイデアを少数返してターンを終えます。あなたがひとつ選んだ後にだけ、その方向を検証し発展させます。決定だけは自動化しません。

**現在は `v0.4 beta` です。** 下の表は、ひとつのモデル（`gpt-5.4`）が生成し、同じ系列の AI 呼び出しが審査した、少数のブリーフでの結果です。その後 GPT と Claude でモデル横断の実験を行いましたが、その選好結果は再審査まで無効です。「正直な読み方」を参照してください。いずれも普遍的な創造性を主張するものではありません。

## できること

| | |
|---|---|
| **発散ポートフォリオ** | 直接探索・メカニズム転用・前提の転換という 3 つのパスから 3〜5 の方向を作ります。名前やテーマだけが違う変種は除外します。 |
| **適合性は拒否権** | どれほど意外でも、必須条件を弱めるアイデアは捨てます。名前を変えただけの違反も違反です。 |
| **選ぶのはあなた** | ルーターは同じターンで選択と発展を行いません。自動連鎖はテストで制約への適合を下げたため、停止を強制します。 |
| **圧力テスト** | 選ばれたアイデアを、支えとなる前提、より単純な従来案、その仕組み自体が生む失敗にぶつけます。 |
| **正直な失敗** | 従来の答えの方が良い場合や方向が耐えられない場合は、そう伝えて発散に戻します。 |
| **小さなランタイム** | スキルファイル 3 つだけです。実行時にデッキ・禁止リスト・ゲート・スクリプトはなく、テストではトークンは通常プロンプトの約 1.1 倍でした。 |

## 仕組み

```text
 your brief ──► ┌──────── diverge · imagination-octo-engine ─────────┐
                │  direct pass · mechanism transfer · premise shift  │
                │    cull by failure · private proof per survivor    │
                └──────────────────────────┬─────────────────────────┘
                                           ▼
                               3–5 distinct directions
                                           ▼
                                    ◆ YOU CHOOSE ◆        the turn always ends here
                                           ▼
                ┌───── develop · imagination-octo-brainstorming ─────┐
                │ load-bearing assumption · conventional competitor  │
                │   native failure mode · boring half · falsifier    │
                └──────────────────────────┬─────────────────────────┘
                                           ▼
                             decision-ready concept memo
```

- 2 つの段階の間の停止は UI 上の都合ではなく、手法の一部です。
- 探索と検証は内部に留めます。受け取るのはパイプラインの報告ではなくアイデアです。
- 実装は行いません。成果物は計画段階へ渡せるコンセプトです。

## クイックスタート

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination-octo/main/install.sh | bash
```

更新するときも同じコマンドを再実行します。以前に個別インストールしたスキルのコピーが報告された場合は、コマンドの末尾を `| bash -s -- --clean-legacy` に変えて実行してください。削除はせず、別の場所へ移します。

次のように依頼します。

```text
$imagination-octo を使って、会話ツリー・隠しダイス・説得ステータスを使わない
物語ゲームの交渉メカニクスを複数作ってください。
```

`codex exec` やスクリプトでは、Codex は完全な名前だけを認識します: `$imagination-octo:imagination-octo`。

最初の応答は選択の問いで終わります。番号か方向で答えます。

```text
2 番を発展させてください。
```

## 1 つのプラグイン、3 つのスキル

| スキル | 適した場面 | 返すもの |
|---|---|---|
| `$imagination-octo` | ほとんどの依頼 | ポートフォリオ → あなたの選択 → 発展したコンセプト |
| `$imagination-octo-engine` | 発散だけが必要なとき | 有用で自明でない 3〜5 の方向 |
| `$imagination-octo-brainstorming` | すでに選んだアイデアがあるとき | 意思決定できるコンセプトメモ |

## 測定結果（2026-07-30）

強い通常プロンプトとの事前登録ブラインド比較です。新しい英語・韓国語ブリーフ 10 件、条件ごとに 5 回実行、審査員 5 名。

| ランタイム | 続けて発展させたい側 | 主な向上（1〜7 段階） | トークン |
|---|---|---|---|
| Engine v0.5.3 | **50 対 0（100.0%）** | 有用な意外性 `+0.97` · 多様性 `+0.66` · 適合性 `+0.60` | 1.12 倍 |
| Concept Workshop v0.4.2 | **45 対 5（90.0%）** | 実行可能性 `+1.37` · 適合性 `+0.95` · 堅牢性 `+0.82` | 1.14 倍 |

正直に読むために:

- **生成も審査も `gpt-5.4` のみです。** Claude での実行も人間の審査員もまだありません。同じ系列の審査員は好みを共有している可能性があります。
- **10 件のブリーフは小さな分布です。** 95% Wilson 区間は Engine 92.9〜100.0%、Workshop 78.6〜95.7% です。
- **負けることもあります。** Workshop のブリーフ 1 件は全審査員が通常プロンプトを選び、以前の Engine ビルドもドラマのブリーフ 1 件で同じ結果でした。
- **以前の設計は完敗しました。** デッキとゲートのパイプライン（Engine v0.4.0）は 48 倍のコストで通常プロンプトに 0 対 30 で敗れ、置き換えました。その記録は Engine リポジトリに残しています。
- **Experiment A（2026-10-06）：選好結果は現時点で無効です。** 事前登録したモデル横断の実験です ([規則](evals/PREREGISTRATION.md), [結果](evals/results/2026-10-06-experiment-a.md))。新しいブリーフ 12 件を `gpt-5.5` と `claude-opus-5-5` で生成し、互いに別系列が審査しました。エンジンは GPT で 12 件中 11 件、Claude で 12 件中 10 件のブリーフで通常プロンプトより好まれ、労力をそろえた通常プロンプトでも差は埋まりませんでした。しかし、どちらがスキルを使ったかを審査側が両モデルとも 24 回中 22 回言い当てました。事前に定めた規則により、出力の形式を正規化して再審査するまで、この選好の数値は根拠として扱いません。作者によるブラインド確認も未実施です。これに影響されない結果：エンジンを使うと、別々の実行で同じメカニズムが繰り返される度合いが下がりました（重複度 GPT 0.40 対 0.54、Claude 0.50 対 0.63）。トークンは GPT で 1.08 倍、Claude で 1.99 倍でした。
- **候補 v0.6.0 は不合格でした（2026-10-06）。** ポートフォリオを広げ、繰り返しを減らすことを狙った版です。新しいブリーフ 12 件で v0.5.3 を上回れず（GPT 5 勝 5 敗 2 分、Claude 4 勝 6 敗 2 分）、両モデルで事前登録の基準を満たさなかったため、v0.5.3 を維持します（[結果](evals/results/2026-10-06-experiment-b.md)）。
- **2 ターンの流れ：** 動作のみ確認しました。回帰テストは 14 件中 13 件が合格し、失敗した 1 件（返答が 2 つの方向に当てはまるときに推測で選んだ）はルーターを修正しました。流れ全体の選好評価はありません。

プロトコル、判定規則、結果ファイル: [Imagination Octo Engine](https://github.com/djfksjd/imagination-octo-engine) · [Imagination Octo Brainstorming](https://github.com/djfksjd/imagination-octo-brainstorming)。

## 使うとき、使わないとき

**使う場面:** 本当に異なる選択肢が欲しいとき。コンセプト、前提、メカニクス、製品、サービス、世界観、儀式、あるいはこれまでのアイデアが平凡に感じられたとき。

**通常プロンプトを使う場面:** 事実の質問、定型的な実装、命名だけの依頼、従来の答えが正解であるすべての場合。

## 選択ログ（オプトイン）

既定ではオフです。オンにすると、方向を選ぶかポートフォリオを却下するたびに、手元の `~/.imagination-octo/choices.jsonl` に 1 行が追記されます。提示された方向、選んだ番号、あなたが述べた理由が記録されます。ブリーフは本文の保存を指定しない限りハッシュだけが残ります。どこにもアップロードされず、スキルがこのログを読むこともありません。自分の選択をあとで振り返るための記録です。`enable --hosts` はスキルがオプトインを確認できるよう、グローバルの `CLAUDE.md` / `AGENTS.md` に印付きの 1 行を追加し、`disable` はそれを取り除きます。

```bash
LOG=https://raw.githubusercontent.com/djfksjd/imagination-octo/main/skills/imagination-octo/scripts/choice_log.py
curl -fsSL $LOG | python3 - enable --hosts claude,codex   # --with-brief keeps the brief text
curl -fsSL $LOG | python3 - stats
curl -fsSL $LOG | python3 - disable
```

## `imagination` から改名しました

このプラグインとルータースキルは v0.1.3 まで `imagination` という名前でした。旧リポジトリ URL は GitHub がリダイレクトしますが、プラグイン名とルーターのコマンドは変わりました。古い `imagination` プラグインを削除し、`imagination-octo` をインストールして `$imagination-octo` で呼び出してください。v0.4 からは 2 つの専門スキルとそのリポジトリも同じ系列名になりました。`$imagination-engine` と `$imagination-brainstorming` の代わりに `$imagination-octo-engine` と `$imagination-octo-brainstorming` を使ってください。 v0.3 からはマーケットプレイス ID も `djfksjd` から `imagination-octo` に変わりました。同じ作者の別のプラグインと ID が衝突していたためです。インストール対象は `imagination-octo@imagination-octo` です。

## 手動インストール

```bash
# Claude Code
claude plugin marketplace add djfksjd/imagination-octo
claude plugin install imagination-octo@imagination-octo

# Codex
codex plugin marketplace add djfksjd/imagination-octo
codex plugin add imagination-octo@imagination-octo
```

## 開発

専門ランタイムはそれぞれのリポジトリで管理・評価しています。リリース前に両方の `SKILL.md` を同期し、3 つのスキルを検証し、リポジトリのテストと 2 ターン境界のフォワードテストを実行します。

```bash
python3 -m pytest tests/ -q
bash -n install.sh
```

## ライセンス

[MIT](LICENSE)。
