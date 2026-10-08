---
name: design-critique
description: Revisa uma peça visual (tela, landing, deck, documento gerado) em cinco dimensões — Filosofia, Hierarquia, Detalhe, Funcionalidade, Inovação — com nota 0–10 e evidência citada por nota, e devolve listas Manter / Corrigir / Ganhos rápidos. Use antes de dar qualquer peça visual como pronta, ou quando pedirem "revisão de design", "crítica", "auditoria visual".
---

# Crítica de design em 5 dimensões

Adaptado do template `critique` de [`nexu-io/open-design`](https://github.com/nexu-io/open-design), que por sua vez deriva de [`alchaincyf/huashu-design`](https://github.com/alchaincyf/huashu-design).

## Quando usar

- Antes de marcar uma peça visual como pronta (exigido por `modulos/design.md`).
- Para comparar duas variantes da mesma peça.
- **Nunca** no mesmo turno em que a peça foi gerada, salvo pedido explícito ("critique o que você acabou de fazer").

## Entrada

1. Identifique a peça. Se houver mais de uma candidata, pergunte qual — não revise todas.
2. Leia o `DESIGN.md` da marca ativa. A direção declarada nele é a régua da dimensão 1.
3. Leia o estilo inteiro e de seis a oito blocos de conteúdo representativos. **Não dê nota pela intenção declarada**; a nota é sobre o que foi executado.
4. Se puder renderizar, renderize e olhe. Nota de layout sem ver o layout é chute.

## As 5 dimensões

Cada dimensão é independente. Uma peça pode ter 9 em Inovação e 4 em Hierarquia, e o relatório diz isso sem amaciar.

Faixas: **0–4** quebrado · **5–6** funcional · **7–8** forte · **9–10** excepcional.

### 1. Filosofia — a peça sustenta uma direção?

- Existe uma direção, ou são três estilos disputando a mesma tela?
- O vocabulário de rótulos, cabeçalhos e chrome fica num registro só?
- Destaque, serifa e mono seguem a mesma regra do início ao fim?
- A direção é a do `DESIGN.md`, ou o agente inventou outra?

**0–4** estilos brigando · **5–6** uma direção, metade dos elementos escapando · **7–8** coerente, deriva nas bordas · **9–10** cada elemento defende a mesma tese.

### 2. Hierarquia — um estranho sabe o que ler primeiro?

- O maior texto é o mais importante em cada tela?
- O papel tipográfico (meta, corpo, destaque) bate com o papel da informação?
- Há um primário, um secundário e um terciário claros, ou tudo grita?

**0–4** tudo grita · **5–6** funciona no topo, quebra no corpo · **7–8** níveis claros, colisão ocasional · **9–10** o olho anda sem atrito.

### 3. Detalhe — o acabamento

- Alinhamento de colunas, linha de base de números grandes, entrelinha.
- Proporção de imagem e legenda consistente entre telas.
- Rótulos com o mesmo espaçamento e a mesma regra de caixa.
- Quebra de linha que deixa palavra órfã.
- Uso só de tokens: valor fora da escala aparece aqui.

**0–4** fita adesiva à mostra · **5–6** quase tudo limpo, uma ou duas telas tortas · **7–8** polido, olho treinado acha dois ou três deslizes · **9–10** acabamento de impressão.

### 4. Funcionalidade — a peça cumpre o que precisa cumprir?

- Alvos de toque, navegação por teclado, foco visível, `Esc` fecha modal.
- Contraste AA nos temas exigidos.
- Landing: ação principal acima da dobra; telefone clicável no celular.
- Documento: imprime certo, copia certo, abre no programa de destino.
- Deck: legível a quatro metros.

**0–4** bonito e inútil · **5–6** fluxo principal funciona, bordas quebradas · **7–8** robusto no uso normal · **9–10** aguenta impressão, tela cheia, colagem e celular sem tropeçar.

### 5. Inovação — algo passa da mediana?

- Há um movimento inesperado (layout, tipografia, movimento) que serve à tese?
- Ou é 100% seguro, poderia ser de qualquer agência?
- A novidade é coerente com a direção, ou foi enxertada?

**0–4** mediana genérica de IA · **5–6** competente e esquecível · **7–8** um momento memorável, o resto sólido · **9–10** vários movimentos que valeria copiar, todos a serviço da tese.

Nota baixa em Inovação é aceitável em peça de produção. Não puna conservadorismo adequado.

## Disciplina de nota

- **Toda nota cita evidência**: elemento, classe, arquivo, linha, tela. "Parece inconsistente" não é evidência.
- **Não arredonde para cima.** A nota é a **pior faixa sustentada**: se a tela 3 quebra a hierarquia, as telas 1 e 2 boas não levantam a nota.
- **Não infle.** 7 significa *forte*, não *aceitável*. Média acima de 8 é suspeita — revise.
- **Cinco notas, sempre.** Relatório parcial não vale.

Exemplo de evidência:

```
Dimensão: Detalhe
Nota: 6/10
Evidência: os cards de indicador da tela 3 alinham na grade, mas na tela 8 a
coluna direita sobe porque .callout tem margem superior e a figura não.
Legendas em mono na tela 5 e em sans na tela 7 — escolher uma.
```

## Saída

Um relatório, no formato que o repositório usa para evidência (Markdown no PR por padrão; HTML autocontido se o dono preferir):

1. **Cabeçalho** — peça revisada, data, veredito em uma linha.
2. **Gráfico de radar** com as cinco notas (no HTML; no Markdown, tabela).
3. **Cinco blocos**, um por dimensão: nota, faixa, parágrafo de evidência de 30 a 80 palavras, e um item de Manter, Corrigir ou Ganho rápido.
4. **Listas finais:**
   - **Manter** (3–5) — o que funciona e não pode quebrar na próxima iteração.
   - **Corrigir** (3–6) — obrigatório, ordenado por custo visual evitado por minuto gasto. Uma frase cada.
   - **Ganhos rápidos** (3–5) — ajustes de 5 a 15 minutos com efeito desproporcional.
5. **Veredito de entrega** — `PASSOU` se nenhuma dimensão está abaixo de 5; senão `FALHOU`, com a dimensão que reprovou.

O relatório usa os tokens do `DESIGN.md` ativo. Sem marca, tema neutro claro.
