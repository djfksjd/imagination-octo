<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/brand/imagination-octo-logo-dark.png" />
  <img src="assets/brand/imagination-octo-logo.png" alt="IMAGINATION OCTO — 넓게 뻗고, 하나를 고른다" width="380" />
</picture>

# IMAGINATION OCTO

**REACH WIDE · CHOOSE ONE**

### Claude Code와 Codex를 위한 사람 중심 창의성 플러그인 —<br/>서로 다른 아이디어를 먼저, 선택은 사용자가, 검증된 컨셉은 그다음에

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

[![Tests](https://img.shields.io/github/actions/workflow/status/djfksjd/imagination-octo/tests.yml?style=flat-square&label=tests)](https://github.com/djfksjd/imagination-octo/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-MIT-1f2937?style=flat-square)](LICENSE)
![Stage](https://img.shields.io/badge/stage-v0.3%20beta-d69526?style=flat-square)
![Skills](https://img.shields.io/badge/skills-3-6d5ef5?style=flat-square)
![Hosts](https://img.shields.io/badge/hosts-Claude%20Code%20%C2%B7%20Codex-0ea5b7?style=flat-square)

</div>

Imagination Octo는 여러 방향으로 동시에 뻗은 다음 멈춥니다. 표현이 아니라 작동 원리가 다른 아이디어 몇 개를 내놓고 턴을 끝냅니다. 사용자가 하나를 고른 뒤에만 그 방향을 검증하고 발전시킵니다. 결정만큼은 자동화하지 않습니다.

**현재 `v0.3 beta`입니다.** 아래 측정값은 모델 하나(`gpt-5.4`)로 생성하고 같은 모델 계열의 AI 호출이 심사한 결과이며, 브리프 수도 적습니다. Claude에서는 측정하지 않았고, 보편적 창의성을 주장하지 않습니다.

## 하는 일

| | |
|---|---|
| **발산 포트폴리오** | 직접 탐색, 메커니즘 전이, 전제 전환의 세 패스로 3–5개 방향을 만듭니다. 이름이나 테마만 다른 변형은 걸러냅니다. |
| **적합성은 거부권** | 아무리 의외여도 필수 제약을 약화시키는 아이디어는 버립니다. 이름만 바꾼 위반도 위반입니다. |
| **선택은 사용자** | 라우터는 같은 턴에 고르고 발전시키지 않습니다. 자동 연쇄는 테스트에서 제약 적합성을 낮췄기 때문에 멈춤을 강제합니다. |
| **압력 테스트** | 고른 아이디어를 핵심 가정, 더 단순한 기존 대안, 그 메커니즘이 스스로 만드는 실패에 부딪혀 봅니다. |
| **정직한 실패** | 평범한 답이 더 낫거나 방향이 버티지 못하면 그렇게 말하고 발산 단계로 돌려보냅니다. |
| **작은 런타임** | 스킬 파일 세 개가 전부입니다. 실행 시 덱·금지 목록·게이트·스크립트가 없고, 테스트에서 일반 프롬프트 대비 토큰은 약 1.1배였습니다. |

## 작동 방식

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

- 두 단계 사이의 멈춤은 UI 장치가 아니라 방법의 일부입니다.
- 탐색과 검증 과정은 드러내지 않습니다. 파이프라인 보고서가 아니라 아이디어를 받습니다.
- 구현은 하지 않습니다. 결과물은 기획 단계로 넘길 수 있는 컨셉입니다.

## 빠른 시작

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination-octo/main/install.sh | bash
```

업데이트할 때도 같은 명령을 다시 실행하면 됩니다. 예전에 따로 설치한 스킬 복사본이 있다고 나오면 명령 끝을 `| bash -s -- --clean-legacy`로 바꿔 실행하세요. 삭제하지 않고 옮겨 둡니다.

그다음 이렇게 요청합니다.

```text
$imagination-octo를 사용해서 대화 트리, 숨은 주사위, 설득 능력치 없이 작동하는
게임 협상 메커니즘을 여러 개 만들어 줘.
```

첫 응답은 선택 질문으로 끝납니다. 번호나 방향으로 답하면 됩니다.

```text
2번을 발전시켜 줘.
```

## 하나의 플러그인, 세 개의 스킬

| 스킬 | 권장 상황 | 결과 |
|---|---|---|
| `$imagination-octo` | 대부분의 요청 | 포트폴리오 → 사용자 선택 → 발전된 컨셉 |
| `$imagination-engine` | 발산만 필요할 때 | 쓸모 있고 비자명한 방향 3–5개 |
| `$imagination-brainstorming` | 이미 고른 아이디어가 있을 때 | 의사결정 가능한 컨셉 메모 |

## 측정 결과 (2026-07-30)

강한 일반 프롬프트와의 사전 등록 블라인드 비교입니다. 새 영어·한국어 브리프 10개, 조건당 5회 실행, 심사자 5명.

| 런타임 | 계속 발전시키고 싶은 쪽 | 주요 향상 (1–7 척도) | 토큰 |
|---|---|---|---|
| Engine v0.5.3 | **50 대 0 (100.0%)** | 유용한 의외성 `+0.97` · 다양성 `+0.66` · 적합성 `+0.60` | 1.12배 |
| Concept Workshop v0.4.2 | **45 대 5 (90.0%)** | 실행 가능성 `+1.37` · 적합성 `+0.95` · 견고성 `+0.82` | 1.14배 |

정직하게 읽는 법:

- **생성도 심사도 `gpt-5.4`뿐입니다.** Claude 실행과 사람 심사는 아직 없습니다. 같은 모델 계열 심사자는 취향을 공유할 수 있습니다.
- **브리프 10개는 작은 분포입니다.** 95% Wilson 구간은 Engine 92.9–100.0%, Workshop 78.6–95.7%입니다.
- **질 때도 있습니다.** Workshop 브리프 하나는 심사자 전원이 일반 프롬프트를 택했고, 이전 Engine 빌드도 드라마 브리프 하나에서 같은 결과였습니다.
- **이전 설계는 완패했습니다.** 덱과 게이트 파이프라인(Engine v0.4.0)은 48배 비용으로 일반 프롬프트에 0 대 30으로 져서 교체했습니다. 그 기록은 Engine 저장소에 남아 있습니다.
- **측정하지 않은 것:** 여러 번 실행했을 때 같은 아이디어로 수렴하는지, 그리고 두 턴 전체 흐름을 하나의 제품으로 본 평가.
- **측정 중:** Experiment A를 [`evals/`](evals/PREREGISTRATION.md)에 사전 등록했습니다. 노력을 맞춘 대조군을 포함한 네 조건, GPT와 Claude 생성, 교차 계열 심사, 실행 간 수렴도, 블라인드 검증을 포함합니다. 결과가 어느 쪽이든 이 목록을 대체합니다. 두 턴 흐름의 동작 회귀 테스트도 같은 폴더에 있습니다.

프로토콜, 판정 규칙, 결과 파일: [Imagination Engine](https://github.com/djfksjd/imagination-engine-skill) · [Imagination Brainstorming](https://github.com/djfksjd/imagination-brainstorming-skill).

## 쓸 때와 쓰지 않을 때

**쓰세요:** 실제로 서로 다른 선택지가 필요할 때. 컨셉, 전제, 메커니즘, 제품, 서비스, 세계관, 의식, 또는 이전 아이디어가 뻔하게 느껴질 때.

**일반 프롬프트를 쓰세요:** 사실 질문, 일상적인 구현, 이름 짓기만 필요한 경우, 평범한 답이 정답인 모든 경우.

## 선택 로그 (옵트인)

기본은 꺼져 있습니다. 켜면 방향을 고르거나 포트폴리오를 거절할 때마다 내 컴퓨터의 `~/.imagination-octo/choices.jsonl`에 한 줄이 추가됩니다. 제시된 방향, 고른 번호, 직접 말한 이유가 기록됩니다. 브리프는 원문 저장을 요청하지 않는 한 해시로만 남습니다. 어디에도 업로드하지 않고, 스킬은 이 로그를 읽지 않습니다. 자신의 선택을 나중에 살펴보기 위한 기록입니다. `enable --hosts`는 스킬이 옵트인 여부를 볼 수 있도록 전역 `CLAUDE.md` / `AGENTS.md`에 표시된 한 줄을 추가하고, `disable`은 그 줄을 지웁니다.

```bash
LOG=https://raw.githubusercontent.com/djfksjd/imagination-octo/main/skills/imagination-octo/scripts/choice_log.py
curl -fsSL $LOG | python3 - enable --hosts claude,codex   # --with-brief keeps the brief text
curl -fsSL $LOG | python3 - stats
curl -fsSL $LOG | python3 - disable
```

## `imagination`에서 이름이 바뀌었습니다

이 플러그인과 라우터 스킬은 v0.1.3까지 `imagination`이었습니다. 예전 저장소 URL은 GitHub가 리다이렉트하지만 플러그인 이름과 라우터 명령은 바뀌었습니다. 기존 `imagination` 플러그인을 제거하고 `imagination-octo`를 설치한 뒤 `$imagination-octo`로 호출하세요. 전문 스킬 두 개의 이름은 그대로입니다. v0.3부터는 마켓플레이스 ID도 `djfksjd`에서 `imagination-octo`로 바뀌었습니다. 같은 제작자의 다른 플러그인과 ID가 겹쳤기 때문입니다. 설치 대상은 이제 `imagination-octo@imagination-octo`입니다.

## 수동 설치

```bash
# Claude Code
claude plugin marketplace add djfksjd/imagination-octo
claude plugin install imagination-octo@imagination-octo

# Codex
codex plugin marketplace add djfksjd/imagination-octo
codex plugin add imagination-octo@imagination-octo
```

## 개발

전문 런타임은 각자의 저장소에서 관리하고 평가합니다. 릴리스 전에 두 `SKILL.md`를 동기화하고, 세 스킬을 검증하고, 저장소 테스트와 두 턴 선택 경계 전방 테스트를 실행합니다.

```bash
python3 -m pytest tests/ -q
bash -n install.sh
```

## 라이선스

[MIT](LICENSE).
