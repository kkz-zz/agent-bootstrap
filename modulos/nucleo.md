# Núcleo e verificação

Módulo **M1** — sempre ativo. Regras que não dependem de stack, e as regras de verificação que valem na auditoria e no `CHECKLIST.md`.

---

## M1 · Núcleo

- **Postura:** não presuma, exponha trade-off, evidência em vez de afirmação, gap consciente se registra.
- **Teto do contrato** declarado no próprio arquivo (sugerido: 200 linhas). Seção nova diz no PR o que consolidou.
- **Válvula de escape** nomeada e com justificativa obrigatória (`eslint-disable`, `@ts-expect-error`, `# noqa`, e as marcas de exceção dos gates do projeto). Supressão não é correção.
- **Regras de STOP:** sintoma preciso → PARE → caminho correto → proibição do atalho.
- **Anti-patterns em tabela**, com o **motivo** de cada linha.
- Nenhum commit direto na branch principal.
- Nenhum ADR aceito editado no mérito; decisão nova supersede.
- **Regra de promoção:** guardrail que falhou duas vezes sobe de nível — regra escrita → gate executável → hook. Nunca desce sem ADR.
- **Hook** bloqueando operação irreversível de git: push forçado, reset hard, reescrita de histórico, `--no-verify`.
- **Canário por gate:** caso que *deve* reprovar e caso que *deve* passar, versionados. Gate sem canário quebra em silêncio e continua verde.

---

## Regras de verificação

1. **Verificação negativa exige caso-controle.** Item cujo sucesso é "nada encontrado" passa igual em repositório limpo e com comando errado. Antes de marcar ✅, rode o mesmo comando contra uma linha fabricada que *deveria* casar, e mostre as duas saídas.
2. **Item que depende de execução se verifica pelo run, não pelo arquivo.** Workflow correto que nunca executou (cota, billing, evento errado) é pior que inexistente: o repositório parece protegido.
3. **Sabote cada gate uma vez.** Remova uma regra e confirme que o canário fica vermelho; restaure e confirme que volta ao verde. Gate que não reprova nada passa o ano inteiro verde.
4. **Permissão de execução se confere depois de transferir.** Zip, Windows e alguns sistemas de arquivos perdem o bit; o hook então existe e não roda.
5. **Pontuação honesta.** Não há nota mínima. Há gap consciente e gap invisível. Item aberto **com decisão registrada** vale mais que item marcado sem verificação.
