# Imagination

Imagination은 창의적 작업을 한 흐름으로 제공하는 통합 플러그인입니다.

```text
$imagination → 서로 다른 아이디어 3~5개 → 사용자 선택 → 하나의 검증된 컨셉
```

세 개의 스킬이 들어 있습니다.

- `$imagination`: 대부분의 사용자를 위한 통합 진입점
- `$imagination-engine`: 아이디어 발산을 직접 호출
- `$imagination-brainstorming`: 선택한 아이디어 구체화를 직접 호출

통합 스킬은 같은 답변에서 아이디어를 선택하고 구체화하지 않습니다.
자동 연쇄 테스트에서 제약 적합성이 떨어졌기 때문에, 사용자의 선택을 발산과
발전 사이의 필수 경계로 유지합니다.

## 설치

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination/main/install.sh | bash
```

수동 설치:

```bash
claude plugin marketplace add djfksjd/imagination
claude plugin install imagination@djfksjd

codex plugin marketplace add djfksjd/imagination
codex plugin add imagination@djfksjd
```

## 사용

처음에는 `$imagination`만 호출하면 됩니다.

```text
$imagination을 사용해서 대화 트리, 숨은 주사위, 설득 능력치 없이 작동하는
게임 협상 메커니즘을 여러 개 만들어 줘.
```

첫 답변은 아이디어 포트폴리오를 보여주고 선택을 묻습니다. 번호나 방향으로
답하면 됩니다.

```text
2번을 발전시켜 줘.
```

다음 답변에서 선택한 방향만 작동 원리, 실제 사용 장면, 운영 부담, 실패
방식과 반증 조건까지 구체화합니다. 구현은 사용자가 컨셉을 승인한 뒤 별도
단계로 진행합니다.

## 검증 근거

포함된 전문 런타임은 새 홀드아웃으로 검증한 버전입니다.

- Imagination Engine v0.5.1: 강한 일반 프롬프트 대비 26 대 4로 선호
- Imagination Brainstorming v0.4.1: 강한 일반 프롬프트 대비 25 대 5로 선호

전체 결과는
[`imagination-engine-skill`](https://github.com/djfksjd/imagination-engine-skill)과
[`imagination-brainstorming-skill`](https://github.com/djfksjd/imagination-brainstorming-skill)에
기록되어 있습니다. 심사자는 서로 독립된 호출이지만 같은 모델 계열이므로,
모든 창의적 작업에서 항상 우월하다는 의미는 아닙니다.

## 개발

두 전문 스킬은 각 저장소에서 독립적으로 유지·평가합니다. 릴리스 전에는
각 런타임 `SKILL.md`를 동기화하고, 세 스킬 검증과 저장소 테스트, 두 턴의
사용자 선택 경계 전방 테스트를 모두 실행합니다.
