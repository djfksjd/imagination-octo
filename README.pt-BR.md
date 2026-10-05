<div align="center">

<img src="assets/brand/imagination-octo-logo.png" alt="IMAGINATION OCTO — Alcance longe, escolha uma" width="380" />

# IMAGINATION OCTO

**REACH WIDE · CHOOSE ONE**

### Um plugin criativo com a pessoa no circuito para Claude Code e Codex —<br/>primeiro ideias distintas, depois a sua escolha, por fim um conceito testado sob pressão

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

[![Tests](https://img.shields.io/github/actions/workflow/status/djfksjd/imagination-octo/tests.yml?style=flat-square&label=tests)](https://github.com/djfksjd/imagination-octo/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-MIT-1f2937?style=flat-square)](LICENSE)
![Stage](https://img.shields.io/badge/stage-v0.2%20beta-d69526?style=flat-square)
![Skills](https://img.shields.io/badge/skills-3-6d5ef5?style=flat-square)
![Hosts](https://img.shields.io/badge/hosts-Claude%20Code%20%C2%B7%20Codex-0ea5b7?style=flat-square)

</div>

O Imagination Octo se estende em várias direções ao mesmo tempo e então para. Ele devolve um pequeno portfólio de ideias que diferem no mecanismo, não na redação, e encerra o turno. Só depois que você escolhe uma é que ele testa e desenvolve essa direção. A decisão é a única parte que ele se recusa a automatizar.

**Esta é a `v0.2 beta`.** As medições abaixo vêm de um único modelo (`gpt-5.4`), julgado por chamadas de IA da mesma família, em um conjunto pequeno de briefs. Nada foi medido no Claude, e isto não é uma afirmação de criatividade universal.

## O que ele faz

| | |
|---|---|
| **Portfólio divergente** | 3–5 direções construídas em três passagens: direta, transferência de mecanismo e mudança de premissa. Variantes que só mudam de nome ou tema são descartadas. |
| **Adequação é veto** | Uma ideia que enfraquece um requisito inegociável é descartada, por mais surpreendente que seja. Uma violação renomeada continua sendo violação. |
| **Você escolhe** | O roteador nunca escolhe e desenvolve no mesmo turno. O encadeamento automático reduziu a aderência às restrições nos testes, então a pausa é obrigatória. |
| **Teste de pressão** | A ideia escolhida enfrenta sua premissa de sustentação, seu concorrente convencional mais simples e a falha causada pelo próprio mecanismo. |
| **Falha honesta** | Se a resposta convencional for melhor, ou a direção não se sustentar, ele diz isso e devolve você à divergência. |
| **Runtime pequeno** | Três arquivos de skill. Sem baralhos, listas de proibição, portões ou scripts em execução; cerca de 1,1× os tokens de um prompt comum nos testes. |

## Como funciona

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

- A pausa entre as duas metades faz parte do método, não é um detalhe de interface.
- Busca e prova ficam privadas. Você recebe as ideias, não o relatório de um pipeline.
- Nada é implementado. O resultado é um conceito para levar ao planejamento.

## Início rápido

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination-octo/main/install.sh | bash
```

Depois peça:

```text
Use $imagination-octo para inventar várias mecânicas de negociação para um jogo
narrativo sem árvores de diálogo, dados ocultos ou atributo de persuasão.
```

A primeira resposta termina com uma escolha. Responda com um número ou uma direção:

```text
Desenvolva a opção 2.
```

## Um plugin, três skills

| Skill | Ideal para | Retorna |
|---|---|---|
| `$imagination-octo` | A maioria dos pedidos | Portfólio → sua escolha → conceito desenvolvido |
| `$imagination-engine` | Apenas divergência | 3–5 direções úteis e não óbvias |
| `$imagination-brainstorming` | Uma ideia já escolhida | Um memorando de conceito pronto para decisão |

## Medições (2026-07-30)

Comparações cegas pré-registradas contra um prompt comum forte. 10 briefs novos em inglês e coreano, 5 execuções por condição, 5 juízes.

| Runtime | Preferido para continuar | Maiores ganhos (escala 1–7) | Tokens |
|---|---|---|---|
| Engine v0.5.3 | **50–0 (100,0%)** | surpresa útil `+0.97` · diversidade `+0.66` · adequação `+0.60` | 1,12× |
| Concept Workshop v0.4.2 | **45–5 (90,0%)** | acionabilidade `+1.37` · adequação `+0.95` · robustez `+0.82` | 1,14× |

Leia com honestidade:

- **Somente o `gpt-5.4` gerou e julgou.** Ainda não há execuções com Claude nem juízes humanos. Juízes da mesma família podem compartilhar o mesmo gosto.
- **Dez briefs são uma distribuição pequena.** Intervalos de Wilson de 95%: Engine 92,9–100,0%, Workshop 78,6–95,7%.
- **Ele pode perder.** Um brief do Workshop foi por unanimidade para o prompt comum, e uma versão anterior do Engine perdeu um brief de drama do mesmo jeito.
- **Um projeto anterior falhou por completo.** O pipeline de baralhos e portões (Engine v0.4.0) perdeu de 0–30 para um prompt comum com 48× o custo e foi substituído. Esse registro permanece no repositório do Engine.
- **Não medido:** se execuções separadas convergem para as mesmas ideias, e o fluxo completo de dois turnos como um único produto.

Protocolos, regras de decisão e arquivos de resultado: [Imagination Engine](https://github.com/djfksjd/imagination-engine-skill) · [Imagination Brainstorming](https://github.com/djfksjd/imagination-brainstorming-skill).

## Quando usar e quando não usar

**Use** quando quiser opções que realmente diferem: conceitos, premissas, mecânicas, produtos, serviços, mundos, rituais, ou quando as ideias anteriores pareceram genéricas.

**Use um prompt comum** para perguntas factuais, implementação rotineira, apenas nomes, ou qualquer caso em que a resposta convencional seja a correta.

## Renomeado de `imagination`

Este plugin e sua skill roteadora se chamavam `imagination` até a v0.1.3. O GitHub redireciona a URL antiga do repositório, mas o nome do plugin e o comando do roteador mudaram: remova o plugin `imagination` antigo, instale `imagination-octo` e chame `$imagination-octo`. As duas skills especializadas mantêm seus nomes.

## Instalação manual

```bash
# Claude Code
claude plugin marketplace add djfksjd/imagination-octo
claude plugin install imagination-octo@djfksjd

# Codex
codex plugin marketplace add djfksjd/imagination-octo
codex plugin add imagination-octo@djfksjd
```

## Desenvolvimento

Os runtimes especializados são mantidos e avaliados em seus próprios repositórios. Antes de um release, sincronize os `SKILL.md`, valide as três skills, rode os testes do repositório e faça o teste direto da fronteira de dois turnos.

```bash
python3 -m pytest tests/ -q
bash -n install.sh
```

## Licença

[MIT](LICENSE).
