# Segurança, supply chain e pipeline

Módulos **M4** (sempre), **M5** (modo Completo) e a parte de segurança de **M7** (API e backend). Riscos específicos de IA — agente no repositório e produto que usa LLM — estão em `modulos/ia.md`.

---

## Fronteira entre superfícies (bloco C da entrevista)

- **Domínio pai compartilhado com sessão (C4):** cookie de sessão host-only com prefixo `__Host-`. A superfície pública fica proibida de ler ou escrever cookie de domínio pai. É a regra que impede um XSS no site de marketing de virar sessão roubada no painel.
- **API na mesma origem** quando possível — sem CORS a configurar. Cliente não-navegador autentica por token de dispositivo, não por cookie.
- **Embutimento (C5):** `postMessage` valida origem explicitamente; iframe de terceiro com `sandbox` mínimo; nada de `*` como origem alvo.
- **Multi-tenant (C3):** tenant derivado do lado servidor (sessão ou host), nunca de parâmetro que o cliente controla sem checagem.
- **Banco acessível pelo cliente (C7):** BaaS com SDK no navegador ou no app (regras de acesso, *row level security*) só com a regra escrita por tabela e teste que tenta ler e gravar como outro usuário e como anônimo. Sem regra testada, o banco é público.
- **Ambientes separados (C7):** desenvolvimento, teste e produção com bancos e credenciais distintos. Ferramenta de interno (painel, admin, staging) nunca fica pública sem autenticação.

---

## M4 · Segurança base

### Segredos

- Segredo nunca em variável exposta ao cliente (prefixos do tipo `NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_`). Chave de terceiro só no servidor.
- Arquivo de exemplo de ambiente com nomes e descrições; valores só no ambiente e em arquivo ignorado pelo Git.
- **Scan de segredos** determinístico e **bloqueante**, sobre o histórico completo. Exceção só por arquivo de ignore com justificativa no commit — nunca desligando o job.
- **No primeiro setup, escaneie o histórico inteiro uma vez.** Segredo apagado em commit posterior continua lá, e a correção é **rotacionar**, não remover.
- **Segredo também vaza pelo que o build produz.** O scan cobre o artefato, não só o código: bundle do cliente, source map publicado, camadas de imagem de contêiner (`.env` copiado), artefato e cache de CI. Source map de produção não fica público.
- **Credencial com escopo mínimo e prazo.** Token de acesso pessoal, de API e de publicação de pacote tem só o escopo que usa e data de expiração registrada. Credencial sem dono ou sem uso é revogada.
- Nenhum segredo de produção alcançável pelo gate de PR. Permissão mínima no workflow.
- Config que o agente executa (hooks, workflows, scripts de gate, husky, config do agente, lista de MCP) muda só por PR com revisor humano — `CODEOWNERS` sobre esses caminhos.

### Código gerado por IA

Código gerado é tratado como código de terceiro não revisado. Estudos com dezenas de modelos encontram falha do OWASP Top 10 em parte relevante do código que compila, e a segurança piora ao longo de iterações sem revisão (ver [Referências](#referências)).

- **SAST no ciclo.** Análise estática de segurança roda local no modo Médio e bloqueia na CI no modo Completo, com as regras da linguagem do projeto. Achado suprimido usa a válvula de escape do M1, com motivo.
- **Autenticação e autorização no servidor, sempre.** Esconder botão ou rota no cliente não é controle de acesso. Cada endpoint e cada operação de dados confere sessão e permissão do lado servidor (CWE-306, CWE-862).
- **Teste negativo de acesso** por recurso protegido: anônimo é recusado, usuário A não lê nem altera dado de B, papel comum não executa ação de admin.
- **Funções perigosas proibidas com entrada externa:** `eval`, `exec`, `Function`, shell montado por string (`shell=True`, `exec` com concatenação), desserialização de formato que executa código, SQL concatenado. Use a forma parametrizada da linguagem. O gate pega o padrão; a exceção leva motivo na linha (CWE-94, CWE-78, CWE-89, CWE-502).
- **Upload de arquivo** valida tipo pelo conteúdo e tamanho no servidor, grava fora da raiz servida, com nome gerado pelo servidor, e nunca é executado (CWE-434).
- **Banco com o menor privilégio.** A credencial da aplicação não é dona do schema, não roda DDL e só alcança as tabelas que usa. Migração roda com credencial separada.
- **Requisito de setor** (arredondamento financeiro, log de acesso a dado de saúde, retenção fiscal) não é inferido pelo agente: vem da entrevista e da norma citada (M11, M12).

### Checklist de revisão de diff gerado por IA

| Pergunta | "Sim" reprova? |
|---|---|
| A dependência existe no registro oficial, é a que se pretendia (não um nome parecido) e tem histórico de publicação? | — (verificar) |
| A API usada existe nessa versão? | — (verificar) |
| Duplica abstração que já existe no repositório? | sim |
| Engole erro? | sim |
| Introduz literal de cor, segredo ou URL interna? | sim |
| Checa permissão só no cliente, ou cria rota ou operação de dados sem checagem no servidor? | sim |
| Usa função perigosa ou monta SQL ou comando por concatenação com entrada externa? | sim |
| Foi refeito em várias rodadas pelo agente sem revisão de segurança do diff inteiro? | sim |
| Toca o harness (hooks, CI, gates, config do agente) de carona? | sim |
| Resolve o que foi pedido, e só isso? | "não" reprova |

---

## M7 · Segurança de API e backend

- Validação de payload **no servidor**, com schema. Validação de cliente não conta.
- Erro nunca engolido; nenhum dado pessoal em log; mensagem de erro que não vaza estrutura interna.
- Rate limit nos endpoints públicos; honeypot em formulário; preferir controle próprio a script de terceiro que exija consentimento.
- Cabeçalhos (quando há navegador): CSP com nonce, sem `unsafe-inline` em script; HSTS; `nosniff`; política de referrer; política de permissões negando o que não usa; bloqueio de enquadramento. **Verificados por teste**, não por inspeção.

---

## M5 · Supply chain e CI

### Dependências

- Dependências diretas **pinadas na versão exata**; configuração do gerenciador forçando isso.
- Lockfile em sync, verificado com instalação congelada.
- **Pacote novo sugerido por IA é verificado antes de instalar:** existe no registro oficial, nome exato, mantenedor e histórico de versões. Nome inventado por modelo é registrado por atacante (*slopsquatting*).
- Bot de atualização com **modo declarado na primeira linha** do arquivo de config, majors excluídos, tudo agrupado.
- Nunca correção automática forçada de vulnerabilidade. Validar contra baseline; o que ficou de fora é documentado com motivo.
- Servidor MCP e skill de terceiro pinados como qualquer dependência: versão exata ou digest; versionados no repositório, nunca em config pessoal, nunca `latest`. Ver `modulos/ia.md`.

### Pipeline

- Actions ou passos de pipeline pinados por **SHA de 40 caracteres**, com a versão em comentário. Tag é mutável. O SHA é do repositório oficial da action, não de um fork.
- Roda em todo PR e no push da principal.
- **Todos os checks bloqueiam**; nenhum informativo.
- Ordem barato → caro; canários antes dos gates.
- Timeout em todo job; permissão mínima; concorrência cancelando só em PR.
- Nenhum exit code engolido (`pipefail`); nenhum veredito cacheado.
- Mudança de workflow só em PR dedicado, com comentário-sentinela nos passos do gate.

### Segredos na pipeline

- **Federação (OIDC) no lugar de chave de longa duração** para nuvem e para publicação de pacote, quando o provedor oferece. Chave fixa em secret de CI é exceção registrada no ADR, com escopo e expiração.
- **Segredo de produção em ambiente protegido**, liberado só para o job de deploy e com aprovação de revisor.
- **Log não mostra segredo.** Um secret por valor (nunca JSON ou YAML inteiro num secret só); valor derivado de segredo (token gerado, Base64) é mascarado também. Segredo que aparecer em log: apague o log e rotacione.
- Artefato e cache de CI não carregam `.env`, credencial nem dump.

### Servidor, não laptop

- **Branch protection exigindo o check e bloqueando push direto.** Sem isso, o workflow só avisa — hook local não segura agente com permissão desligada; servidor segura.
- Evento de PR que não expõe segredo a código de fork.
- Input de usuário (título de PR, nome de branch, corpo de issue) entra por variável de ambiente, nunca interpolado em comando.
- Auto-aprovação de PR desligada.

---

## Referências

Regras com redação própria. Os relatórios e incidentes mostram o problema; as diretrizes dão o controle.

### Diretrizes

| Fonte | O que sustenta aqui |
|---|---|
| [OpenSSF — Security-Focused Guide for AI Code Assistant Instructions](https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions) (2025) | Código gerado como não confiável, SAST, funções perigosas, dependência verificada, regras de segurança nas instruções do agente |
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) e [CWE Top 25](https://cwe.mitre.org/top25/) | Classes de falha citadas nas regras (CWE-78, 89, 94, 306, 434, 502, 862) |
| [GitHub Docs — Secure use reference (Actions)](https://docs.github.com/en/actions/reference/security/secure-use) | OIDC, ambiente com revisor, segredo por valor e derivado mascarado, SHA do repositório oficial |

### Estudos e incidentes

| Fonte | O que mostra |
|---|---|
| [Kaspersky — Os perigos ocultos da codificação com IA](https://www.kaspersky.com.br/blog/vibe-coding-2025-risks/24465/) (2025) | Panorama de incidentes e estudos que originou esta revisão |
| [Veracode — GenAI Code Security Report](https://www.veracode.com/blog/genai-code-security-report/) (2025) | Código gerado que compila e ainda tem falha do OWASP Top 10 |
| [arXiv 2506.11022](https://arxiv.org/abs/2506.11022) | Segurança piora em iterações sucessivas feitas pelo modelo |
| [arXiv 2502.06039](https://arxiv.org/abs/2502.06039) | Prefixo de prompt focado em segurança reduz vulnerabilidade gerada |
| [arXiv 2412.15004](https://arxiv.org/abs/2412.15004) | Revisão sistemática sobre as vulnerabilidades que LLMs introduzem ao gerar código |
| [arXiv 2406.10279](https://arxiv.org/abs/2406.10279) (USENIX Security 2025) | Pacotes inventados por modelos de código (*slopsquatting*) |
| [Wiz Research — riscos em apps de vibe coding](https://www.wiz.io/blog/common-security-risks-in-vibe-coded-apps) (2025) | Autenticação só no cliente, segredo no bundle, regra de acesso do banco permissiva, app interno público |
