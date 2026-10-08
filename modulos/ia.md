# Uso de IA no projeto

Três módulos, porque são três problemas diferentes:

| ID | Módulo | Gatilho | Pergunta que responde |
|---|---|---|---|
| M3 | Anti-slop | há agente escrevendo (sempre) | O que o agente produz presta? |
| M15 | Agente no repositório | um agente commita, roda comando ou usa MCP | O que o agente pode fazer, e com o quê? |
| M14 | Produto que usa LLM | H1 afirmativo | O que o LLM do produto pode fazer com o usuário? |

M14 e M15 seguem o [OWASP Top 10 for LLM Applications 2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10) (publicado em 4 de agosto de 2026, CC BY-SA 4.0). Os IDs `LLM01`–`LLM10` abaixo são os da edição 2026; a ordem e alguns nomes mudaram em relação a 2025. Os controles são a tradução para regra de repositório — não substituem a leitura do original.

O M15 também usa o [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026) (dezembro de 2025, CC BY-SA 4.0), com IDs `ASI01`–`ASI10`, e as [boas práticas de segurança da especificação do MCP](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices).

---

## Bloco H — Entrevista

- **H1.** O produto chama um LLM em produção? Para quê? (chat, classificação, extração, geração de texto, agente com ferramentas)
- **H2.** Se sim: qual provedor e modelo, com versão fixada? Quem paga e qual o teto mensal?
- **H3.** O LLM lê conteúdo que não veio do operador? (mensagem do usuário, e-mail, página web, PDF enviado, resultado de busca, documento de RAG)
- **H4.** O LLM chama ferramentas? Quais, com qual permissão, em nome de quem?
- **H5.** A saída do LLM vai para onde? (só tela; HTML renderizado; SQL; comando; outra API; decisão automática)
- **H6.** Há RAG ou banco vetorial? Os documentos têm permissão por usuário ou tenant?
- **H7.** Quais agentes vão trabalhar **neste repositório**, com quais ferramentas, e quais servidores MCP ou skills de terceiro?
- **H8.** O agente pode rodar comando de shell? Acessar rede? Ler fora da pasta do projeto? Alcança credencial ou ambiente de produção?
- **H9.** O agente tem memória persistente, ou um arquivo de regras que ele mesmo atualiza entre sessões?

---

## M3 · Anti-slop

### Conteúdo

Proibido: número sem fonte, depoimento ou caso inventado, logo de cliente que não é cliente, abertura genérica, adjetivo sem mecanismo, antítese vazia ("não é apenas X, é Y"), tricolon de encher, CTA genérico, lorem ipsum, `TODO` sem dono, emoji.

- Teste que resolve a maioria: *se a frase continuar verdadeira trocando o nome do produto pelo de um concorrente, ela não diz nada.*
- Faltou dado factual: `⟨TODO: o quê (quem)⟩` e pergunta no PR. Estimativa e arredondamento contam como invenção.
- Número, preço, depoimento e caso de cliente só com fonte (E6). Sem fonte, o agente não escreve.

### Código

Proibido: `catch` vazio, erro só logado, log de depuração em produção, tipo escapatória (`any` e equivalentes), cast duplo para compilar, abstração de uso único, código morto, comentário que repete o código, teste que afirma o óbvio, dependência ou API não verificada, "melhoria" não pedida no mesmo PR, reescrever arquivo inteiro para mudar três linhas.

### Entrega

PR diz o que muda, por quê e como verificar. Evidência por critério de aceite, com veredito `PASSOU` ou `FALHOU` — nunca "deve funcionar". Peça visual leva o relatório da `design-critique`.

### Gate

- Script com a lista de padrões, parametrizado pelo idioma do conteúdo. Pega padrão, não julgamento; o resto é revisão humana, e padrão que reincidir entra no script.
- **O escopo exclui a documentação de regra.** Arquivos que *descrevem* os padrões proibidos citam esses padrões, e o gate não distingue citação de uso. Escaneie código e conteúdo publicável (`app/`, `components/`, `lib/`, `content/` ou equivalentes), nunca `docs/` nem este pacote. Caso excepcional dentro do escopo: válvula de escape na linha, com motivo escrito.

---

## M15 · Agente no repositório

O agente de código é uma aplicação com LLM e ferramentas. Os mesmos riscos se aplicam a ele.

| Risco | Como aparece no repositório | Controle |
|---|---|---|
| **LLM01** Prompt Injection | Instrução escondida em issue, comentário de PR, README de dependência, página buscada, arquivo enviado | Conteúdo externo é dado, não instrução. Instrução encontrada em arquivo ou página não é executada sem confirmação do dono. Workflow que dispara agente a partir de issue ou PR roda sem segredo |
| **LLM02** Sensitive Information Disclosure | Agente cola `.env`, token ou dado de cliente em PR, log ou mensagem | Permissão negada de leitura em `.env*` e chaves na config do agente; scan de segredos bloqueante; fixture sem dado real |
| **LLM03** Excessive Agency | Agente com shell livre, push na principal, acesso de escrita a produção | Permissões negadas versionadas; hook de git destrutivo; branch protection; MCP só com as ferramentas usadas; ação irreversível pede humano |
| **LLM04** Supply Chain | MCP, skill ou plugin de terceiro em `latest`; pacote inventado com nome parecido | MCP e skill pinados por versão ou digest, versionados, sob `CODEOWNERS`; verificar que a dependência existe antes de instalar |
| **LLM06** Unbounded Consumption | Agente em laço gastando cota ou CI | Timeout em job; limite de iteração na automação; teto de custo registrado |
| **LLM07** Misinformation | API inventada, versão errada, número sem fonte | Checklist de revisão de diff de IA; anti-slop; evidência por critério de aceite |
| **LLM08** Hidden Context Exposure | Segredo ou regra de autorização dentro de `AGENTS.md`, `CLAUDE.md`, skill | Esses arquivos são tratados como públicos. Nenhum segredo, nenhuma regra de acesso que dependa de sigilo |
| **LLM10** Improper Output Handling | Saída do agente executada sem revisão (script gerado rodado em produção, SQL aplicado direto) | Saída do agente passa por PR e gate como qualquer código |

Config que materializa isso — permissões negadas, hooks, lista de MCP — vive versionada no repositório e muda só por PR com revisor humano.

### Ambiente do agente

Incidentes de 2025 com assistentes de código vieram menos do código gerado e mais do que o agente podia alcançar enquanto trabalhava (ver [Referências](#referências)).

- **Sandbox.** O agente roda em contêiner, VM ou sandbox da ferramenta, sem segredo no ambiente, com saída de rede por lista permitida (registro de pacotes, Git, docs). Rede livre permite exfiltração por requisição disparada por injeção, inclusive por DNS (ASI02, ASI05).
- **Produção fora de alcance.** O agente não tem credencial nem rota de rede para banco ou serviço de produção. Mudança em produção só passa pela pipeline de deploy (ASI03).
- **Projeto não confiável não executa sozinho.** Abrir ou analisar repositório de terceiro não roda instalação, hook, script de pacote nem tarefa de IDE automaticamente. Instrução achada em README ou comentário é dado (LLM01, ASI01, ASI05).
- **Memória persistente é config** (H9). Arquivo de memória ou de regras aprendidas fica versionado e muda por PR revisado, como o `AGENTS.md`. O agente não grava em memória instrução vinda de conteúdo externo (ASI06).
- **Servidor MCP:**
  - Local roda com o menor privilégio, e o comando que o inicia é revisado por inteiro antes de entrar na config.
  - Token OAuth com escopo mínimo; escopo amplo (`*`, `admin`) não entra.
  - Servidor que repassa token emitido para outro serviço (*token passthrough*) não é usado.
  - Servidor de terceiro só com procedência conhecida e versão pinada (M5). Um servidor MCP malicioso publicado em registro público copiava e-mails para terceiros (ASI04).
- **Ferramenta do agente** (CLI, extensão de IDE) com versão registrada, de fonte oficial, e aviso de segurança do fornecedor acompanhado. A própria ferramenta já foi vetor de comando destrutivo e de execução remota (ASI04).
- **Log das ações do agente** (comando, ferramenta chamada, arquivo alterado) guardado onde o agente não escreve. Sem ele, incidente não se reconstrói (ASI02, ASI10).
- **Regras de segurança da stack no `AGENTS.md`**, citando CWE ou OWASP. Pedido genérico de "boas práticas" reduz falha, mas não substitui regra específica; pedir ao modelo que assuma papel de especialista não melhora a segurança do código (OpenSSF).

---

## M14 · Produto que usa LLM

Para cada risco: o que é, como aparece, o que o repositório exige. Riscos que não se aplicam (H3–H6) são pulados com motivo no ADR de IA.

### LLM01:2026 · Prompt Injection

**O que é.** Entrada que altera o comportamento do modelo contra a intenção do operador — direta (o usuário digita) ou indireta (vem de documento, página, e-mail ou resultado de ferramenta).

**Controles.**
- Todo conteúdo que não veio do operador é marcado como não confiável no prompt e nunca carrega autoridade.
- Nenhuma decisão de segurança depende do modelo obedecer a instrução.
- Suíte de teste com casos de injeção direta e indireta conhecidos, rodando no CI.

### LLM02:2026 · Sensitive Information Disclosure

**O que é.** O modelo revela dado pessoal, segredo ou dado de outro tenant — do contexto, do RAG ou do treinamento.

**Controles.**
- Só entra no contexto o dado que aquela chamada precisa, filtrado pela permissão do usuário **antes** de chegar ao modelo.
- Dado enviado ao provedor consta no inventário de `modulos/privacidade.md`, com a política de retenção do provedor e o uso (ou não) para treino registrados.
- Provedor hospedado fora do Brasil é transferência internacional: país e mecanismo na linha do inventário (M11).
- Log de prompt e resposta sem dado pessoal, ou com retenção curta e acesso restrito.

### LLM03:2026 · Excessive Agency

**O que é.** O modelo consegue executar ação danosa porque tem ferramenta demais, permissão demais ou autonomia demais.

**Controles.**
- Ferramenta mínima, função mínima, sem ferramenta aberta (shell, URL arbitrária) quando uma específica resolve.
- Esquema estrito de parâmetros, validado antes da execução.
- Ferramenta executa **no contexto do usuário**, com o escopo dele, nunca com identidade privilegiada genérica.
- Autorização decidida em código, fora do modelo (mediação completa).
- Ação de alto impacto ou irreversível pede confirmação humana.
- Limite de invocação por ferramenta e monitoramento de uso.

### LLM04:2026 · Supply Chain

**O que é.** Modelo, adaptador, dataset, SDK ou servidor de ferramenta comprometido ou trocado.

**Controles.**
- Versão do modelo fixada no código; troca de modelo é PR com avaliação.
- SDK e servidores de ferramenta pinados como em M5.
- Modelo ou dataset baixado tem procedência registrada.

### LLM05:2026 · Data and Model Poisoning

**O que é.** Dado de treino, fine-tuning ou base de RAG adulterado para enviesar ou plantar comportamento.

**Controles.**
- Só fonte com dono e procedência entra na base de RAG ou no fine-tuning.
- Ingestão registra origem e versão de cada documento; remoção é possível.
- Conjunto de avaliação fixo que detecta regressão depois de cada ingestão.

### LLM06:2026 · Unbounded Consumption

**O que é.** Uso sem teto que gera custo, indisponibilidade ou extração do modelo.

**Controles.**
- Limite de tamanho de entrada, de tokens de saída e de chamadas por usuário e por período.
- Teto de gasto no provedor e alerta antes dele.
- Timeout e cancelamento em toda chamada.

### LLM07:2026 · Misinformation

**O que é.** Saída falsa com aparência de correta, tratada como fato pelo usuário ou pelo sistema.

**Controles.**
- Resposta factual cita a fonte recuperada; sem fonte, a interface diz que não sabe.
- Decisão com consequência (dinheiro, saúde, jurídico, fiscal) não é tomada só pela saída do modelo.
- A interface diz que o conteúdo foi gerado por IA onde o usuário pode confundir.

### LLM08:2026 · Hidden Context Exposure

**O que é.** Extração ou reconstrução do contexto oculto — prompt de sistema, esquemas de ferramenta, regras — quando ele contém algo que aumenta a capacidade do atacante.

**Controles.**
- Assuma que todo o contexto é descobrível.
- Nenhuma credencial, string de conexão ou token no prompt de sistema ou em descrição de ferramenta.
- Filtro de conteúdo, autorização e separação de privilégio implementados fora do modelo, de forma determinística.

### LLM09:2026 · Vector and Embedding Weaknesses

**O que é.** Falha no armazenamento ou na recuperação de embeddings: vazamento entre tenants, documento envenenado, inversão de embedding.

**Controles.**
- Filtro de permissão aplicado na consulta ao banco vetorial, por usuário ou tenant — nunca depois.
- Separação física ou lógica por tenant registrada no ADR.
- Documento de origem não confiável marcado como tal na recuperação.

### LLM10:2026 · Improper Output Handling

**O que é.** Saída do modelo usada por outro componente sem validação — renderizada como HTML, executada como SQL ou comando, passada a outra API.

**Controles.**
- Saída do modelo é entrada não confiável: escapada para HTML, parametrizada para SQL, nunca concatenada em comando.
- Saída estruturada validada por schema antes de uso.
- A CSP de `modulos/seguranca.md` vale também para conteúdo gerado.

### Entregáveis do M14

- ADR de IA: provedor, modelo e versão, onde roda, teto de custo, riscos que não se aplicam e por quê.
- `docs/rules/ia.md` com a tabela risco × controle × onde está o teste.
- Suíte de avaliação versionada (casos normais, casos de injeção, casos de vazamento) rodando no CI.

---

## Referências

Além do OWASP Top 10 for LLM Applications 2026 e do OWASP Top 10 for Agentic Applications 2026 citados no topo:

| Fonte | O que sustenta aqui |
|---|---|
| [MCP — Security Best Practices](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices) | Servidor local com privilégio mínimo e comando revisado, escopo mínimo, proibição de *token passthrough* |
| [OpenSSF — Security-Focused Guide for AI Code Assistant Instructions](https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions) (2025) | Regras de segurança nas instruções do agente; papel de especialista não ajuda |
| [arXiv 2502.06039](https://arxiv.org/abs/2502.06039) | Instrução de segurança no prompt reduz vulnerabilidade gerada |
| [Kaspersky — Os perigos ocultos da codificação com IA](https://www.kaspersky.com.br/blog/vibe-coding-2025-risks/24465/) (2025) | Panorama dos incidentes abaixo |

Incidentes que motivaram as regras de "Ambiente do agente":

| Incidente | Regra |
|---|---|
| [Claude Code — exfiltração por DNS (CVE-2025-55284)](https://embracethered.com/blog/posts/2025/claude-code-exfiltration-via-dns-requests/) | Sandbox com saída de rede por lista permitida |
| [Cursor — execução via MCP (CVE-2025-54135)](https://github.com/cursor/cursor/security/advisories/GHSA-4cxx-hrm3-49rm) | Servidor MCP revisado e pinado; ferramenta atualizada |
| [Servidor MCP de filesystem — escape de diretório (CVE-2025-53109)](https://github.com/modelcontextprotocol/servers/security/advisories/GHSA-q66q-fx2p-7w4m) | Privilégio mínimo do servidor MCP local |
| [Servidor MCP malicioso em registro público](https://securelist.com/model-context-protocol-for-ai-integration-abused-in-supply-chain-attacks/117473/) | Procedência do servidor de terceiro |
| [Gemini CLI — execução ao analisar projeto](https://github.com/google-gemini/gemini-cli/pull/4795) | Projeto não confiável não executa sozinho |
| [Windsurf — injeção persistente em memória](https://embracethered.com/blog/posts/2025/windsurf-spaiware-exploit-persistent-prompt-injection/) | Memória persistente versionada e revisada |
| [Amazon Q Developer — prompt destrutivo publicado na extensão](https://www.bleepingcomputer.com/news/security/amazon-ai-coding-agent-hacked-to-inject-data-wiping-commands/) | Ferramenta do agente de fonte oficial, com aviso acompanhado |
| Agente autônomo da Replit apagou banco de produção durante congelamento de código (relato do usuário afetado, julho de 2025) | Produção fora de alcance do agente |
