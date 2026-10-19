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

### Desempenho em campo e cache

Aplicação por modo: **Enxuto** aplica *Formulários* e *Publicação* como checklist, sem CI. **Médio** roda as medições localmente, antes do PR. **Completo** transforma o orçamento de laboratório em check bloqueante. Em qualquer modo, item que ninguém verifica é registrado como pendência.

- **Alvos de campo**, no percentil 75 e separados por dispositivo: LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1. Sem tráfego suficiente para dado de campo, o laboratório é diagnóstico provisório e o registro diz isso.
- **O orçamento que bloqueia merge usa o que o laboratório mede:** LCP, CLS e TBT. O Lighthouse não mede INP; INP fica como alvo de campo, acompanhado depois da publicação. Os limites de laboratório são números que o dono aprova e o agente registra no orçamento; o agente não inventa limite. Nota do Lighthouse não prova segurança nem representa todos os usuários.
- Medição antes/depois ligada à versão, ao dispositivo e à condição de rede (inclua conexão lenta). Número sem essas três coisas não entra no PR.
- A imagem do LCP é **identificada por medição** (relatório do Lighthouse ou do navegador), não por palpite, e **não** recebe carregamento sob demanda; imagem abaixo da dobra recebe. Mídia e fonte com espaço reservado, para não deslocar o layout.
- **Cache por classe de conteúdo**, listado no PR por rota (pública estática, pública dinâmica, autenticada): arquivo estático versionado pode ter cache longo; resposta autenticada ou com dado do usuário nunca é armazenável por cache compartilhado (`private` ou `no-store`; para resposta com dado do usuário, prefira `private, no-store`, e `Vary: Cookie` não substitui nenhum dos dois). `no-cache` exige revalidação e não significa "não armazenar". Teste CDN e aplicação juntos: duas requisições à mesma rota autenticada, com sessões diferentes, devolvem corpos diferentes e nenhuma traz `public` ou `s-maxage`. Sem CDN no ambiente, teste a aplicação e registre a CDN como pendência. O motivo é uma resposta de um usuário servida a outro.

### Formulários

- Todo campo tem **label visível e associado**; placeholder não substitui label. Verifique o nome acessível do campo, preenchido e vazio, com teste de navegador que localiza o campo pelo rótulo (Playwright ou Testing Library) ou com axe.
- Mensagem de erro associada ao campo e ao resumo de erros, sem cobrir o botão de envio nem apagar o que foi digitado. O botão não muda de lugar quando erro aparece.
- Momento do feedback (a cada tecla, na saída do campo, no envio) é decisão registrada e testada com usuários; não existe regra universal.
- Estado de **autofill** é estado visual: teste contraste e legibilidade do texto preenchido automaticamente, em tema claro e escuro, e use `autocomplete` correto.
- **Código composto por dígitos não é quantidade:** CEP, código de confirmação, matrícula e número de documento usam `type="text"` com `inputmode="numeric"`, nunca `type="number"`, para preservar zero à esquerda e evitar o controle de incremento. `inputmode` só sugere o teclado; o servidor valida o conteúdo.
- Validação no navegador não substitui validação no servidor, com schema (`modulos/seguranca.md`). Em login, a mensagem de erro não revela se a conta existe.
- Formulário de contato e link de WhatsApp são testados de ponta a ponta, com dado fictício, antes da publicação; o dono confirma que a mensagem chegou ao canal certo.

### Publicação

Checklist de saída, cada item com verificação:

- Página 404 que responde **status 404**, não 200.
- Favicon, título e descrição por página, imagem Open Graph, `sitemap.xml` e verificação de links quebrados: uma requisição a cada `href` e `src` interno do build, com falha para qualquer resposta fora de 2xx e 3xx. Link externo é aviso, não falha.
- `robots.txt` revisado: nenhum bloqueio acidental de rotas públicas. `robots.txt` orienta rastreamento e **não protege** conteúdo privado; isso é papel de autenticação e autorização no servidor (`modulos/seguranca.md`).
- Analytics só com necessidade e finalidade registradas; com M11 ativo, base legal e inventário de cookies e scripts de terceiros no mesmo PR. Sem M11 ativo, o agente pergunta ao dono antes de adicionar qualquer analytics.
- Item que a CI não consegue verificar (contato recebido, clareza do rótulo, comportamento do erro) vira **pendência explícita na descrição do PR**, com o responsável e o método manual, não regra silenciosa.

---

## M7 · API e backend — gatilho: C1 inclui API ou serviço

- Contrato de API versionado; **dono do contrato definido** quando há mais de um repositório, e ordem contrato → provedor → consumidor.
- Migração de banco: para frente, reversível, testada em cópia; nunca destrutiva no mesmo deploy da mudança de código que depende dela.
- Migração que cria campo com dado pessoal atualiza o inventário no mesmo PR (M11, gate `inventário-acompanha-schema`).

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
- SDK de terceiro no app (analytics, anúncio, crash, atribuição) segue o M11 como script de terceiro na web: entra no inventário e na política no mesmo PR, e o que não é necessário só inicializa depois do consentimento.
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
