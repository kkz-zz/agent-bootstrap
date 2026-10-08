# Dados pessoais e conformidade

Módulo **M11** — gatilho: E1 ou E2 afirmativo. Escrito com a LGPD como referência; para outra jurisdição, troque a base legal e mantenha a mecânica.

Dado pessoal que passa por LLM tem controles próprios em `modulos/ia.md` (LLM02).

---

## Bloco E — Entrevista (dados)

- **E1.** O produto coleta dado de pessoa? Quais campos, e para quê?
- **E2.** Envolve pagamento, documento fiscal, dado de saúde, ou usuário menor de idade?
- **E3.** Vai ter analytics? Pixel de campanha? Cookie além do necessário?
- **E4.** Qual a retenção, e quem responde pedido de exclusão?
- **E4a.** Algum desses dados vai para um provedor de LLM, embedding ou ferramenta de terceiro? (se sim, ativa M14 e entra no inventário abaixo)

---

## Inventário

Antes de qualquer regra, a tabela. Vai em `docs/rules/privacidade.md` e é atualizada no mesmo PR que muda a coleta.

| Dado | Finalidade | Base legal | Onde fica | Quem acessa | Terceiros | Retenção |
|---|---|---|---|---|---|---|
| ⟨campo⟩ | ⟨para quê⟩ | ⟨base⟩ | ⟨sistema⟩ | ⟨papel⟩ | ⟨fornecedor ou "nenhum"⟩ | ⟨prazo⟩ |

Campo sem finalidade não é coletado.

---

## M11 · Regras

- **Base legal declarada por finalidade.** Medição agregada e sem identificador pode rodar por legítimo interesse; qualquer coisa que identifique ou rastreie entre sites espera consentimento explícito por categoria.
- **Banner sem padrão escuro:** recusar é um clique, no mesmo nível visual de aceitar. Registro do consentimento com versão da política e data. Link permanente para revogar.
- Atribuição de origem em cookie próprio, não compartilhada com terceiro.
- **Mudança no que é coletado atualiza as páginas legais no mesmo PR.** PR que adiciona terceiro sem tocar nelas é reprovado.
- Script de terceiro entra junto da entrada correspondente na política de cookies, no mesmo PR.
- Retenção e canal de pedido do titular escritos, com responsável nomeado.
- Nenhum dado pessoal em log, em mensagem de erro, em ambiente de teste ou em fixture versionada.
- Menor de idade (E2): fluxo de consentimento do responsável decidido antes de qualquer tela de cadastro.
- **Revisão jurídica antes do lançamento** quando houver dado pessoal, pagamento ou dado sensível. Registre como risco bloqueante até acontecer.
