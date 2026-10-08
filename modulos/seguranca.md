# Segurança, supply chain e pipeline

Módulos **M4** (sempre), **M5** (modo Completo) e a parte de segurança de **M7** (API e backend). Riscos específicos de IA — agente no repositório e produto que usa LLM — estão em `modulos/ia.md`.

---

## Fronteira entre superfícies (bloco C da entrevista)

- **Domínio pai compartilhado com sessão (C4):** cookie de sessão host-only com prefixo `__Host-`. A superfície pública fica proibida de ler ou escrever cookie de domínio pai. É a regra que impede um XSS no site de marketing de virar sessão roubada no painel.
- **API na mesma origem** quando possível — sem CORS a configurar. Cliente não-navegador autentica por token de dispositivo, não por cookie.
- **Embutimento (C5):** `postMessage` valida origem explicitamente; iframe de terceiro com `sandbox` mínimo; nada de `*` como origem alvo.
- **Multi-tenant (C3):** tenant derivado do lado servidor (sessão ou host), nunca de parâmetro que o cliente controla sem checagem.

---

## M4 · Segurança base

- Segredo nunca em variável exposta ao cliente (prefixos do tipo `NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_`). Chave de terceiro só no servidor.
- Arquivo de exemplo de ambiente com nomes e descrições; valores só no ambiente e em arquivo ignorado pelo Git.
- **Scan de segredos** determinístico e **bloqueante**, sobre o histórico completo. Exceção só por arquivo de ignore com justificativa no commit — nunca desligando o job.
- **No primeiro setup, escaneie o histórico inteiro uma vez.** Segredo apagado em commit posterior continua lá, e a correção é **rotacionar**, não remover.
- Nenhum segredo de produção alcançável pelo gate de PR. Permissão mínima no workflow.
- Config que o agente executa (hooks, workflows, scripts de gate, husky, config do agente, lista de MCP) muda só por PR com revisor humano — `CODEOWNERS` sobre esses caminhos.

### Checklist de revisão de diff gerado por IA

| Pergunta | "Sim" reprova? |
|---|---|
| A dependência existe e é a que se pretendia (não um nome parecido)? | — (verificar) |
| A API usada existe nessa versão? | — (verificar) |
| Duplica abstração que já existe no repositório? | sim |
| Engole erro? | sim |
| Introduz literal de cor, segredo ou URL interna? | sim |
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
- Bot de atualização com **modo declarado na primeira linha** do arquivo de config, majors excluídos, tudo agrupado.
- Nunca correção automática forçada de vulnerabilidade. Validar contra baseline; o que ficou de fora é documentado com motivo.
- Servidor MCP e skill de terceiro pinados como qualquer dependência: versão exata ou digest; versionados no repositório, nunca em config pessoal, nunca `latest`. Ver `modulos/ia.md`.

### Pipeline

- Actions ou passos de pipeline pinados por **SHA de 40 caracteres**, com a versão em comentário. Tag é mutável.
- Roda em todo PR e no push da principal.
- **Todos os checks bloqueiam**; nenhum informativo.
- Ordem barato → caro; canários antes dos gates.
- Timeout em todo job; permissão mínima; concorrência cancelando só em PR.
- Nenhum exit code engolido (`pipefail`); nenhum veredito cacheado.
- Mudança de workflow só em PR dedicado, com comentário-sentinela nos passos do gate.

### Servidor, não laptop

- **Branch protection exigindo o check e bloqueando push direto.** Sem isso, o workflow só avisa — hook local não segura agente com permissão desligada; servidor segura.
- Evento de PR que não expõe segredo a código de fork.
- Input de usuário (título de PR, nome de branch, corpo de issue) entra por variável de ambiente, nunca interpolado em comando.
- Auto-aprovação de PR desligada.
