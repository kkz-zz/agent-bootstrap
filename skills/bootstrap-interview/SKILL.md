---
name: bootstrap-interview
description: Entrevista o dono do projeto em rodadas sobre uma árvore de decisões até não restar nada presumido, registrando glossário e ADRs no momento em que se fecham. Use na Fase 1 do AGENT-BOOTSTRAP ou quando pedirem para "entrevistar", "sabatinar" ou "fechar o escopo" de um projeto.
---

# Entrevista de bootstrap

Entreviste o dono até chegar a um entendimento compartilhado. Trate a entrevista como uma **árvore de decisões**: cada decisão abre as decisões que dependem dela.

Adaptado de [`mattpocock/skills` — grilling e domain-modeling](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md).

## Antes da primeira pergunta

Descobrir **fato** é trabalho seu, nunca do dono. Se o repositório existe, levante sozinho: linguagens e versões, gerenciador de pacotes, scripts, lint, tipos, CI e se está verde, estrutura de pastas, quantidade de erros de lint e de tipo, segredos no histórico. O que você levantou entra na rodada 1 como confirmação, não como pergunta aberta.

Fato que demora a levantar não bloqueia a rodada: só as perguntas que dependem dele esperam.

## Rodadas

A **fronteira** é o conjunto de decisões cujos pré-requisitos já estão resolvidos — o que dá para perguntar *agora* sem adivinhar resposta que você ainda não ouviu. Pergunte a fronteira inteira em uma rodada, numerada, cada pergunta com sua recomendação e o motivo. Depois espere.

```
❓ **Q1** — **<título>**: <pergunta, com opções quando houver>

➡️ <sua recomendação> — <por quê>

---

❓ **Q2** — **<título>**: …

➡️ …
```

Cada resposta muda a árvore: decisões fechadas empurram a fronteira e liberam as que dependiam delas. Recalcule e faça a próxima rodada. Pergunta que depende de outra ainda aberta **nesta** rodada pertence à rodada seguinte.

Limite prático: se a fronteira passar de seis perguntas, quebre por bloco, na ordem da árvore abaixo.

A entrevista termina quando a fronteira está vazia: todo ramo visitado, nada presumido em silêncio. Não gere o contrato antes de o dono confirmar que vocês chegaram a um entendimento comum.

## Durante a entrevista

**Confronte com o glossário.** Se o dono usa um termo em conflito com o `CONTEXT.md`, aponte na hora: "o glossário define 'pedido' como X, mas você parece falar de Y. Qual vale?"

**Afie termo vago.** Termo sobrecarregado ganha nome canônico. "Quando você diz 'conta', é o Cliente ou o Usuário? São coisas diferentes."

**Teste com cenário.** Quando a relação entre conceitos for discutida, invente o caso de borda que força o dono a ser preciso sobre a fronteira.

**Cruze com o código.** Se o dono descreve um comportamento, confira se o código concorda. Contradição vai para a rodada seguinte.

**Escreva o `CONTEXT.md` na hora.** Termo resolvido entra imediatamente, no formato de `templates/CONTEXT.md`. O arquivo é glossário e nada mais — sem implementação, sem decisão, sem rascunho. Crie-o só quando o primeiro termo se resolver.

**ADR com parcimônia.** Além dos ADRs mínimos exigidos pelo bootstrap, proponha ADR só quando as três condições valem:

1. **Difícil de reverter** — mudar de ideia depois custa caro.
2. **Surpreendente sem contexto** — quem ler depois vai perguntar "por que assim?".
3. **Resultado de trade-off real** — havia alternativas de verdade, e uma foi escolhida por motivo específico.

Faltou uma: sem ADR. Formato em `templates/ADR-0000.md`.

## A árvore

Setas indicam dependência: o bloco da direita só entra na fronteira depois que o da esquerda fecha.

```
A (projeto) ──► B (stack) ──► C (superfícies) ──┬─► D (identidade visual)
     │                                           ├─► E (dados pessoais e conteúdo)
     │                                           └─► H (uso de IA)
     └──────► F (processo) ──► G (gates)
```

Bloco que não se aplica, pule e diga por quê.

### A — Projeto

- **A1.** O que é o projeto, em uma frase? Quem usa, e para resolver o quê?
- **A2.** Nome do repositório. É do zero, ou já existe código?
- **A3.** Quem trabalha nele? Quem decide código, quem decide marca, quem decide produto?
- **A4.** É **produto com cliente externo**, **ferramenta interna**, ou **script/experimento pessoal**? → define o modo.
- **A5.** Quem mais vai escrever neste repositório — outras pessoas, outros agentes? Quantos em paralelo?

### B — Stack (confirme o que detectou)

- **B1.** Confirmando: ⟨linguagens, frameworks, versões⟩. Está certo? Falta algo?
- **B2.** Repositório único ou monorepo? Se monorepo, quais pacotes e qual a regra de dependência entre eles?
- **B3.** Gerenciador de pacotes, e versão de runtime fixada em algum lugar?
- **B4.** Onde roda em produção? Quem tem acesso de admin ao deploy?
- **B5.** Há requisito técnico **eliminatório**? (funcionar sem internet, falar com periférico, latência máxima, hardware específico)

### C — Superfícies e fronteiras

- **C1.** Quais superfícies existem ou vão existir? (site público, painel logado, app mobile, API, terminal de venda, bot, CLI, job)
- **C2.** Qual domínio ou subdomínio de cada uma?
- **C3.** Alguma tem sessão? É multi-tenant? O tenant vem do login ou do endereço?
- **C4.** Duas superfícies compartilham domínio pai, e uma delas tem sessão? → regra em `modulos/seguranca.md`.
- **C5.** Alguma superfície embute outra (iframe, webview, postMessage)?
- **C6.** Login único entre as superfícies, ou cada uma autentica sozinha?

### D — Identidade visual

Perguntas e regras em `modulos/design.md`. Não escolha cor, fonte ou escala antes de receber o material.

### E — Dados pessoais e conteúdo

Perguntas e regras em `modulos/privacidade.md` (E1–E4) e `modulos/engenharia.md` (E5, E6).

### F — Processo

- **F1.** Repositório público ou privado? (branch protection com check obrigatório é paga em repositório privado — se for privado e sem verba, a ausência vira decisão registrada)
- **F2.** Já existe CI? Está verde? Quantos erros de lint e de tipo existem hoje? (confirmação do que você levantou)
- **F3.** Quem revisa PR? Há mais de uma pessoa, ou revisão é só do agente?
- **F4.** Tracker de tarefa? Convenção de branch e de commit?
- **F5.** O agente pode commitar e abrir PR, ou só propor diff?

### G — Gates

- **G1.** Posso ligar os gates como **bloqueantes** já, ou precisa de período em modo relatório? (gate ligado com dívida aberta trava todo PR e o time desliga o gate. O correto é zerar a dívida **no mesmo PR** que liga o bloqueio)
- **G2.** Há orçamento de desempenho com número? Se não, proponha a partir do tipo de produto e confirme.
- **G3.** Existe módulo onde um bug passaria silencioso — dinheiro, imposto, autenticação, hash, ordenação, parsing, unidade de medida?
- **G4.** Há operação em que o "fix" sugerido pela ferramenta é catastrófico? Vira regra de STOP.

### H — Uso de IA

Perguntas e regras em `modulos/ia.md`.

## Encerramento

Antes de passar para a Fase 2, mostre:

1. A árvore com cada nó fechado e a resposta em uma linha.
2. Os termos que entraram no `CONTEXT.md`.
3. Os ADRs abertos durante a entrevista.
4. Os `⟨pendente⟩` e quem decide cada um.

E pergunte uma vez: "chegamos a um entendimento comum?" Só avance com o sim.
