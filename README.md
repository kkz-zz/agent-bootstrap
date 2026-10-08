<img width="1774" height="887" alt="Bootstrap modular para agentes de IA" src="https://github.com/user-attachments/assets/e70b11ec-a8f8-4bb4-8e5b-98c1171e37e9" />

# agent-bootstrap

Pacote de instruções para um agente de IA montar o setup de um repositório: ele entrevista o dono, escolhe os módulos que se aplicam e gera contrato (`AGENTS.md`), glossário, ADRs, gates e canários.

Não é framework nem dependência. São arquivos Markdown que o agente lê. Depois do setup, a pasta pode sair do repositório.

## Como usar

1. Copie esta pasta para a raiz do repositório, **sem** a pasta `.github/`: ela é a CI deste pacote, não do seu projeto.
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
  privacidade.md                M11, bloco E, inventário, gates; LGPD, ECA Digital e guias da ANPD
  ia.md                         M3 anti-slop, M15 agente no repositório, M14 produto com LLM (OWASP LLM Top 10 2026)
  engenharia.md                 M6, M7, M8, M9, M10, M12
templates/
  ADR-0000.md  CONTEXT.md  DESIGN.md  manifest.json
.github/                        CI deste pacote (não copiar): check-docs, scan de segredos, canários, workflows
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
| [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026) (CC BY-SA 4.0) e [MCP — Security Best Practices](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices) | Ambiente do agente no M15: sandbox, alcance de produção, memória persistente, servidor MCP |
| [OpenSSF — Security-Focused Guide for AI Code Assistant Instructions](https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions) | Código gerado por IA no M4 e regras de segurança no `AGENTS.md` |
| [GitHub Docs — Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) | Segredos na pipeline no M5 |
| [Kaspersky — Os perigos ocultos da codificação com IA](https://www.kaspersky.com.br/blog/vibe-coding-2025-risks/24465/) e estudos que ele cita (Veracode, Wiz, arXiv) | Levantamento de incidentes e estudos que originou a revisão de segurança |
| [LGPD — Lei 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm), [ECA Digital — Lei 15.211/2025](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15211.htm) e [resoluções da ANPD](https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd) (atos oficiais) | Bases legais, direitos e prazos do titular, incidentes, encarregado, transferência internacional e requisitos para produto acessado por menores em `modulos/privacidade.md` |
| [Guias orientativos](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes) e [documentos técnicos](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/documentos-tecnicos-orientativos) da ANPD (CC BY-ND 3.0) | Interpretação aplicada a cookies, legítimo interesse, papéis, anonimização e IA generativa — referenciados, não adaptados |

## Contribuindo

Ver [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Licença

[CC BY-SA 4.0](LICENSE). Você pode usar, adaptar e redistribuir, inclusive comercialmente, desde que dê crédito e distribua adaptações sob a mesma licença. Os arquivos que o agente **gera** no seu repositório a partir destas instruções são seus.

O conteúdo de `modulos/ia.md` adapta o [OWASP Top 10 for LLM Applications 2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10), © OWASP Foundation, CC BY-SA 4.0. A seção "Ambiente do agente" do M15 adapta o [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026), © OWASP Foundation, CC BY-SA 4.0.

As regras de `modulos/privacidade.md` são redação própria. Normas brasileiras são citadas pelo artigo; texto oficial de lei não tem proteção de direito autoral (Lei 9.610/1998, art. 8º, IV). Os guias e estudos da ANPD são publicados sob [CC BY-ND 3.0](https://creativecommons.org/licenses/by-nd/3.0/deed.pt_BR) e, por isso, aparecem só como referência, sem trecho adaptado.
