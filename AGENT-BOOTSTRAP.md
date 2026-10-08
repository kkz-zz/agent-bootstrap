# AGENT-BOOTSTRAP.md

**Arquivo de instrução para o agente.** Dê isto a um agente de IA no início de um projeto novo (ou ao assumir um existente) e ele conduz o setup: entrevista o dono, escolhe os módulos que se aplicam e gera os arquivos de contrato, guardrail e decisão.

Este arquivo **não** é o contrato do projeto — ele é o gerador. O contrato é o `AGENTS.md` que sai daqui. Este arquivo é o **índice**: o detalhe de cada tema vive em `modulos/`, e os procedimentos que o agente executa vivem em `skills/`.

---

## 0. Como usar

1. Copie a pasta para a raiz do repositório, sem `.github/`, que é a CI do próprio pacote (ou cole este arquivo e os que ele aponta no início da sessão).
2. Diga ao agente: **"Siga `AGENT-BOOTSTRAP.md`."**
3. O agente entrevista (`skills/bootstrap-interview`), propõe módulos, você aprova, ele gera.

Ao terminar, a pasta pode sair do repositório — ela já cumpriu a função. O que fica é o que ela gerou.

### Mapa dos arquivos

| Arquivo | O que tem | Quando o agente lê |
|---|---|---|
| `AGENT-BOOTSTRAP.md` | Regras da sessão, modos, mapa de módulos, saída | Sempre, primeiro |
| `skills/bootstrap-interview/SKILL.md` | Como entrevistar: árvore de decisão, rodadas, registro de glossário e ADR | Fase 1 |
| `modulos/nucleo.md` | M1 e regras de verificação | Sempre |
| `modulos/design.md` | M2, M13, bloco D da entrevista, pacote `DESIGN.md` | Se existe interface ou documento gerado |
| `skills/design-critique/SKILL.md` | Revisão de qualidade visual em 5 dimensões | Antes de entregar qualquer peça visual |
| `modulos/seguranca.md` | M4, M5, fronteira de sessão (C4), banco no cliente e ambientes (C7), código gerado por IA, segredos na pipeline, M7 no que toca segurança | Sempre |
| `modulos/privacidade.md` | M11, bloco E da entrevista, inventário, gates de privacidade, referências de LGPD e ECA Digital | Se coleta dado de pessoa ou o produto é de acesso provável por menores |
| `modulos/ia.md` | M3 (anti-slop), uso de agente no repositório, M14 (produto com LLM) — mapeados ao OWASP Top 10 para LLM 2026 | Sempre |
| `modulos/engenharia.md` | M6, M7, M8, M9, M10, M12 | Por gatilho |
| `templates/` | ADR, `CONTEXT.md`, `DESIGN.md`, `manifest.json` | Fase 3 |

---

## 1. Regras da sessão de bootstrap

Valem para o agente, do começo ao fim. Violar qualquer uma invalida o setup.

1. **Não gere nenhum arquivo de contrato antes de concluir a entrevista.** A tentação é começar pelo `AGENTS.md`; é o erro mais comum e produz contrato inventado para um projeto que o agente não conhece. Exceção: glossário (`CONTEXT.md`) e ADR são escritos **durante** a entrevista, no momento em que o termo ou a decisão se fecha — ver `skills/bootstrap-interview`.
2. **Não pergunte o que você pode verificar.** Se o repositório existe, detecte stack, gerenciador de pacotes, scripts, lint, CI, estrutura de pastas e dívida antes de abrir a boca. Pergunte só o que não está no código: intenção, público, restrição de negócio, preferência, acesso.
3. **Entrevista por rodadas, não formulário.** Cada rodada pergunta só o que já pode ser respondido sem depender de resposta pendente, numerado, com sua recomendação e o motivo. Procedimento em `skills/bootstrap-interview`.
4. **Não invente.** Sem paleta enviada, não escolha cor. Sem número, não estime. Sem acesso, não suponha o que tem dentro. Faltou algo: pergunte, ou registre `⟨pendente: o quê (quem decide)⟩`.
5. **Custo, dependência nova e trade-off são decisão do dono.** Apresente opções com consequência, não escolha sozinho.
6. **Se o dono parar de responder, pare também.** Entregue o que já foi decidido e a lista do que falta. Não complete por inferência.
7. **Modo enxuto é uma resposta legítima.** Script pessoal não leva CI bloqueante. Ver §2.
8. **Nada de prosa de preenchimento nos arquivos gerados.** O contrato é lido sob pressão; cada linha precisa ser verificável em diff.

---

## 2. Modos

A resposta de **A4** (ver entrevista) define o peso do setup. Não aplique peso de produto a um script pessoal: guardrail desproporcional é desinstalado na primeira sexta-feira.

| Modo | Quando | Gera |
|---|---|---|
| **Enxuto** | Script pessoal, experimento, automação de uso próprio | `AGENTS.md` curto (postura + regras + STOP), `.gitignore`, hook de git destrutivo. Sem CI, sem ADR, sem CHECKLIST |
| **Médio** | Ferramenta interna, protótipo com usuário real, repositório de uma pessoa | Enxuto + gates locais em `pre-commit` + CHECKLIST + ADR só para decisão estrutural |
| **Completo** | Produto com cliente externo, ou mais de um autor (humano ou agente) escrevendo em paralelo | Todos os arquivos de §4, CI bloqueante, canários, CODEOWNERS, supply chain travada |

---

## 3. Fase 2 — Catálogo de módulos

Ative por gatilho, não por gosto. Para cada módulo ativado, diga ao dono o que ele adiciona e o que custa.

| ID | Módulo | Gatilho | Arquivo |
|---|---|---|---|
| M1 | Núcleo | sempre | `modulos/nucleo.md` |
| M2 | Design system e marca | existe interface | `modulos/design.md` |
| M3 | Anti-slop | há agente escrevendo (sempre) | `modulos/ia.md` |
| M4 | Segurança base | sempre | `modulos/seguranca.md` |
| M5 | Supply chain e CI | modo Completo | `modulos/seguranca.md` |
| M6 | Frontend web | C1 inclui site ou painel | `modulos/engenharia.md` |
| M7 | API e backend | C1 inclui API ou serviço | `modulos/engenharia.md` (segurança da fronteira em `seguranca.md`) |
| M8 | Monorepo | B2 = monorepo | `modulos/engenharia.md` |
| M9 | Mobile e desktop | C1 inclui app nativo, híbrido ou desktop | `modulos/engenharia.md` |
| M10 | Conteúdo versionado | E5 indica texto no repositório | `modulos/engenharia.md` |
| M11 | Dados pessoais e conformidade | E1, E2 ou E11 afirmativo | `modulos/privacidade.md` |
| M12 | Dinheiro, fiscal e cálculo crítico | G3 indica bug silencioso | `modulos/engenharia.md` |
| M13 | Documentos gerados | emite .docx, .pdf, .xlsx, .svg, .dxf | `modulos/design.md` |
| M14 | Produto que usa LLM | H1 afirmativo | `modulos/ia.md` |
| M15 | Agente no repositório | sempre que um agente commita, roda comando ou usa MCP | `modulos/ia.md` |

---

## 4. Fase 3 — Arquivos a gerar

Gere só depois da aprovação, e só os do modo escolhido. Uma branch e um PR por bloco temático.

| Arquivo | Modo | Conteúdo obrigatório |
|---|---|---|
| `AGENTS.md` | todos | O contrato. Estrutura em §5. Teto declarado |
| `CLAUDE.md` | todos | Ponteiro de uma linha para `AGENTS.md` mais a explicação de por que é ponteiro. Nenhuma regra duplicada |
| `CONTEXT.md` | médio, completo | Glossário do domínio, sem detalhe de implementação. Formato em `templates/CONTEXT.md` |
| `README.md` | médio, completo | O que é, o que **não** é, pré-requisitos, como rodar, scripts, estrutura, tabela de guardrails, tabela de ADRs, como contribuir, quem decide o quê |
| `design-system/<marca>/` | se M2 | `manifest.json` + `DESIGN.md` + `tokens.css` por marca. Ver `modulos/design.md` |
| `docs/rules/design-system.md` | se M2 | A regra em uma frase, camadas, mecânica de marca e tema, fluxo de mudança de cor, o que o gate verifica. Aponta para o pacote; não repete valores |
| `docs/rules/anti-slop.md` | se M3 | Tabelas de proibido em conteúdo, em código e em entrega, com o motivo; o que o gate pega e o que fica para revisão humana |
| `docs/rules/ia.md` | sempre | Permissões do agente, sandbox e alcance de rede, memória persistente, fontes não confiáveis, MCP, e — se M14 — controles por risco do OWASP LLM Top 10 |
| `docs/rules/seguranca.md` | todos | Fronteira entre superfícies, segredos (inclusive em artefato e na pipeline), autorização no servidor, funções proibidas, validação, cabeçalhos, supply chain, pipeline, checklist de revisão de diff de IA |
| `docs/rules/privacidade.md` | se M11 | Inventário com base legal por finalidade (artigo e inciso), testes de legítimo interesse, matriz de retenção, consentimento, canal e prazos do titular, operadores e transferências internacionais |
| `docs/runbooks/incidente-dados.md` | se M11, médio e completo | Quem decide, prazos de comunicação à ANPD e aos titulares, modelo de comunicação, onde fica o registro do incidente |
| `docs/adr/0000-template.md` | médio, completo | Cópia de `templates/ADR-0000.md` |
| `docs/adr/0001…` | médio, completo | Um ADR por decisão já tomada na entrevista. No mínimo: stack; arquitetura e fronteiras; design system e marca; guardrails; segurança e supply chain. Risco que bloqueia alguma frente entra numerado |
| `CHECKLIST.md` | médio, completo | Auditoria verificável, item por item, cada um com **comando de verificação** e, quando o sucesso é "nada encontrado", o **caso-controle** |
| `HANDOFF.md` | completo | Ordem de aplicação, placeholders a substituir, o que mais reprova, prompt pronto para o agente de quem assume, o que não delegar, bloqueadores conhecidos |
| hook de git destrutivo | todos | Lê o payload da ferramenta, reprova com código de saída de bloqueio, mensagem dizendo o caminho correto |
| config do agente versionada | todos | Hooks, permissões negadas, MCP pinados. É guardrail de time, não config pessoal |
| `pre-commit` | todos | Bloqueia commit na branch principal; roda os gates; passa sem erro durante rebase ou merge |
| gates (`scripts/`) | se M2, M3, M12 | Um script por gate, com saída dizendo arquivo, linha, regra e **o que fazer**. Válvula de escape exigindo justificativa na mesma linha |
| canários (`scripts/`) | sempre que houver gate | Casos must-block e must-pass por gate, mais checagem de **cobertura de padrões** |
| `scripts/setup.sh` | se houver hook | Restaura bit de execução. Zip e Windows perdem, e sem ele o hook não roda |
| workflow de CI | completo | Ver M5. Todos os checks bloqueantes, canários antes dos gates, SAST da linguagem do projeto |
| workflow de scan de segredos | completo | Histórico completo, bloqueante |
| config do bot de dependência | completo | Modo na primeira linha, majors fora, agrupado |
| `CODEOWNERS` | completo | Caminhos do harness mais contrato, ADRs, pacote de design system e, se M11, `docs/rules/privacidade.md` e `docs/runbooks/incidente-dados.md` |
| config de pins do gerenciador | completo | Versão exata por padrão |

Placeholder que o dono precisa preencher: use `⟨...⟩` e liste todos no final, com o comando que resolve cada um quando houver.

---

## 5. Estrutura obrigatória do `AGENTS.md` gerado

Na ordem. Detalhe longo não entra aqui — vai para `docs/rules/` e aparece como ponteiro.

```
0. Postura                  não presuma; trade-off exposto; evidência; discorde citando a regra; idioma
1. O que é este repositório  uma frase + o que NÃO é + o que fazer se pedirem o que não é
2. Comandos                  os que existem de verdade, com o que roda antes de "terminei"
3. Regras invioláveis        numeradas, checáveis em diff, com exemplo ✅/❌ onde ajudar; inclui as de segurança da stack, citando CWE ou OWASP
4. Regras de STOP            tabela sintoma | PARE, não faça | caminho correto
5. Superfícies e fronteiras  tabela de superfície × marca × sessão × repositório
6. Conteúdo / domínio        ponteiro para CONTEXT.md + invariantes e unidades
7. Desempenho e a11y         números que bloqueiam merge, e a consequência arquitetural deles
8. Anti-patterns             tabela não faça | motivo
9. Antes de dizer que terminou  lista verificável, terminando em evidência anexada
10. Ponteiros                docs/rules, docs/adr, design-system/, CHECKLIST, origem dos guardrails
```

Teto declarado no topo. Se estourar, consolide — não anexe.

**O `AGENTS.md` é contexto oculto do agente e deve ser tratado como público** (OWASP LLM08:2026). Nenhum segredo, URL interna sensível ou regra de autorização entra nele.

---

## 6. Erros que invalidam o bootstrap

Observados em setups reais. Se você cometeu um, refaça o passo.

- Escrever o `AGENTS.md` antes da entrevista, inventando um projeto que não conhece.
- Perguntar o que estava no código.
- Despejar todas as perguntas de uma vez, incluindo as que dependem de resposta ainda aberta.
- Escolher cor, fonte ou escala sem o material de identidade.
- Decidir item de custo ou trade-off sozinho — documentar não substitui perguntar.
- Ligar gate bloqueante com dívida aberta.
- Marcar ✅ em grep vazio sem caso-controle.
- Gerar gate sem canário.
- Aplicar modo Completo a script pessoal.
- Mexer no harness de carona num PR de outra coisa.
- Pôr segredo ou regra de autorização em `AGENTS.md`, `CLAUDE.md` ou prompt de sistema.
- Usar dado pessoal real em fixture, seed, log, issue ou prompt de ferramenta externa.
- Dar ao agente credencial de produção, rede livre ou memória persistente fora do controle de versão.
- Aceitar autenticação ou autorização checada só no cliente.
- Escrever "em conformidade com a LGPD" em qualquer arquivo gerado, ou entregar política de privacidade sem a marca `⟨revisão jurídica⟩`.
- Escolher base legal sem artigo e inciso, ou legítimo interesse sem teste de balanceamento registrado.
- Entregar peça visual sem passar pela `design-critique`.
- Fechar o setup sem listar os `⟨placeholders⟩` e os riscos que ficaram abertos.

---

## 7. Saída do bootstrap

Entregue, ao final, nesta forma:

1. **Resumo das decisões**, uma linha cada, e qual ADR registra cada uma.
2. **Módulos ativados** e, para cada um que ficou de fora, o motivo.
3. **Arquivos gerados**, por PR.
4. **Placeholders `⟨...⟩`** com o comando ou a pessoa que resolve cada um.
5. **Riscos abertos numerados**, com os bloqueantes marcados como bloqueantes.
6. **Evidência**: saída dos canários e dos gates, e o que não pôde ser verificado neste ambiente, com o motivo.
7. **Próximo passo único** — o que fazer primeiro, não uma lista de seis.

Pendência registrada não é falha do setup. Pendência escondida é.
