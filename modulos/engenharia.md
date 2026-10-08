# Engenharia por superfície

Módulos ativados por gatilho da entrevista: **M6** frontend web, **M7** API e backend, **M8** monorepo, **M9** mobile e desktop, **M10** conteúdo versionado, **M12** dinheiro, fiscal e cálculo crítico.

Segurança de M7 está em `modulos/seguranca.md`. Identidade visual de M6 e M9 está em `modulos/design.md`.

---

## M6 · Frontend web — gatilho: C1 inclui site ou painel

- **Orçamento de desempenho que bloqueia merge**, com número: LCP, CLS, INP, peso de JS na rota mais visitada, nota de acessibilidade, zero violação séria de a11y.
- Consequência explícita: renderização no servidor é o padrão; ilha interativa só no componente-folha. Um marcador de cliente no lugar errado arrasta a árvore e estoura o orçamento.
- **Acessibilidade:** tudo alcançável por teclado, foco visível, modal e menu prendem foco e fecham com `Esc`, contraste AA nos dois temas, animação respeitando redução de movimento, um `h1` por tela, sem pulo de heading.
- Imagem, link interno e data sempre pelas APIs do framework / `Intl` com locale e fuso do público.
- Padrão de recursos de interface do projeto, se houver: liste como checklist e marque quais a CI verifica sozinha.

---

## M7 · API e backend — gatilho: C1 inclui API ou serviço

- Contrato de API versionado; **dono do contrato definido** quando há mais de um repositório, e ordem contrato → provedor → consumidor.
- Migração de banco: para frente, reversível, testada em cópia; nunca destrutiva no mesmo deploy da mudança de código que depende dela.

---

## M8 · Monorepo — gatilho: B2 = monorepo

- Regra de dependência entre pacotes escrita e verificada: domínio puro não importa infraestrutura; pacote de UI não importa pacote de aplicação.
- `CODEOWNERS` por pacote.
- Gate incremental pelo que o PR afeta, com piso que nunca baixa.
- Pacote compartilhado (tokens, tipos, domínio) versionado como dependência de verdade, com semver — não por caminho relativo entre aplicações.

---

## M9 · Mobile e desktop — gatilho: C1 inclui app nativo, híbrido ou desktop

- Tokens exportados para o formato nativo, gerados do mesmo `tokens.css` que a web.
- Literal de cor proibido também na linguagem nativa — o gate cobre esses arquivos.
- Requisito de hardware ou periférico vira **spike com risco registrado antes** de virar dependência de cronograma. Plano B nomeado.
- Assinatura e distribuição de build: quem tem a chave, onde ela vive, o que acontece se ela for perdida.
- Offline, se for eliminatório (B5): fonte de verdade local, estratégia de resolução de conflito e teste que **desliga a rede** fazem parte do gate, não da intenção.

---

## M10 · Conteúdo versionado — gatilho: E5 indica texto mantido no repositório

### Entrevista (conteúdo)

- **E5.** Quem escreve o conteúdo (textos, páginas, copy)? Essa pessoa usa Git?
- **E6.** Já existe número, preço, depoimento ou caso de cliente que pode ser publicado? **Se não existir, o agente não inventa** — marca pendência.

### Regras

- Conteúdo em arquivos com frontmatter **validado por schema no build**; inválido quebra o build. Não existe página publicada sem metadado.
- Campo novo no frontmatter atualiza o schema na mesma mudança.
- Componentes disponíveis no conteúdo vêm de pasta própria, registrados; sem import no arquivo de conteúdo, sem HTML bruto.
- Selo de "última atualização" lendo campo do frontmatter; editar conteúdo atualiza o campo.
- **Barreira de edição é risco real:** se quem escreve não usa Git (E5), registre como risco com gatilho de revisão — site que ninguém atualiza é pior que site lento.

---

## M12 · Dinheiro, fiscal e cálculo crítico — gatilho: G3

- Nenhum ponto flutuante para dinheiro; unidade mínima inteira, ou decimal exato, declarado no contrato.
- Arredondamento com regra única e escrita, testada nos limites.
- Cobertura medida **no código novo do PR**, não no repositório inteiro; piso que nunca baixa.
- Mutation testing com baseline nos módulos quentes: sabotar uma comparação (`>` → `>=`) tem que deixar teste vermelho.
- Teste de propriedade complementando teste de exemplo em lógica pura, parser e cálculo.
- Integração fiscal ou de pagamento: contrato de terceiro versionado, ambiente de teste obrigatório, e comportamento definido para indisponibilidade do provedor.
