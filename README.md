<img width="1774" height="887" alt="Bootstrap modular para agentes de IA" src="https://github.com/user-attachments/assets/e70b11ec-a8f8-4bb4-8e5b-98c1171e37e9" />

# agent-bootstrap

Pacote de instruções para um agente de IA montar o setup de um repositório: ele entrevista o dono, escolhe os módulos que se aplicam e gera contrato (`AGENTS.md`), glossário, ADRs, gates e canários.

Não é framework nem dependência. São arquivos Markdown que o agente lê. Depois do setup, a pasta pode sair do repositório.

## Como usar

1. Copie esta pasta para a raiz do repositório.
2. Diga ao agente: **"Siga `AGENT-BOOTSTRAP.md`."**
3. Responda as rodadas de perguntas. Aprove os módulos. Revise os PRs.

## Estrutura

```
AGENT-BOOTSTRAP.md              índice: regras da sessão, modos, mapa de módulos, saída
skills/
  bootstrap-interview/SKILL.md  entrevista em rodadas sobre árvore de decisão; glossário e ADR na hora
  design-critique/SKILL.md      revisão visual em 5 dimensões com nota e evidência
modulos/
  nucleo.md                     M1 e regras de verificação
  design.md                     M2, M13, bloco D, pacote DESIGN.md
  seguranca.md                  M4, M5, fronteira de sessão, segurança de API
  privacidade.md                M11, bloco E, inventário de dados
  ia.md                         M3 anti-slop, M15 agente no repositório, M14 produto com LLM (OWASP LLM Top 10 2026)
  engenharia.md                 M6, M7, M8, M9, M10, M12
templates/
  ADR-0000.md  CONTEXT.md  DESIGN.md  manifest.json
```

## Modos

| Modo | Para quê | Peso |
|---|---|---|
| Enxuto | script pessoal, experimento | contrato curto e hook de git |
| Médio | ferramenta interna, protótipo com usuário | + gates locais, CHECKLIST, ADR estrutural |
| Completo | produto com cliente externo, vários autores | + CI bloqueante, canários, CODEOWNERS, supply chain travada |

## Origem

Derivado de dois setups reais: um monorepo TypeScript de PDV offline, multi-tenant e com emissão fiscal; e um site institucional multi-marca com conteúdo em MDX e LGPD.

| Referência | O que veio dela |
|---|---|
| [`goul4rt/quick-guardrails-ia`](https://github.com/goul4rt/quick-guardrails-ia) (MIT) | Princípios de guardrail para agente |
| [`mattpocock/skills` — grill-with-docs](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md) | Entrevista por rodadas sobre árvore de decisão, `CONTEXT.md` como glossário, critério de três condições para ADR |
| [`nexu-io/open-design`](https://github.com/nexu-io/open-design) (Apache-2.0) | Pacote de marca `manifest.json` + `DESIGN.md` + `tokens.css`; crítica de design em 5 dimensões |
| [OWASP Top 10 for LLM Applications 2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10) (CC BY-SA 4.0) | Taxonomia de risco para agente no repositório e para produto que usa LLM |

## Contribuindo

Ver [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Licença

[CC BY-SA 4.0](LICENSE). Você pode usar, adaptar e redistribuir, inclusive comercialmente, desde que dê crédito e distribua adaptações sob a mesma licença. Os arquivos que o agente **gera** no seu repositório a partir destas instruções são seus.

O conteúdo de `modulos/ia.md` adapta o [OWASP Top 10 for LLM Applications 2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10), © OWASP Foundation, CC BY-SA 4.0.
