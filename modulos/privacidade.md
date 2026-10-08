# Dados pessoais e conformidade

Módulo **M11** — gatilho: E1, E2 ou E11 afirmativo. Escrito com a LGPD (Lei 13.709/2018) como referência; para outra jurisdição, troque a base legal e mantenha a mecânica.

Dado pessoal que passa por LLM tem controles próprios em `modulos/ia.md` (LLM02). Segurança da fronteira, segredos e logs estão em `modulos/seguranca.md`.

O órgão regulador é a **Agência Nacional de Proteção de Dados (ANPD)**, nome e natureza dados pela Lei 15.352/2026. Documento gerado não usa mais "Autoridade Nacional".

As regras abaixo são redação própria. Cada uma aponta para a norma ou o guia que a sustenta (ver [Referências](#referências)), mas não substitui a leitura do original nem a revisão jurídica.

---

## Bloco E — Entrevista (dados)

- **E1.** O produto coleta dado de pessoa? Quais campos, de quem (cliente, funcionário, visitante, terceiro citado), e para quê?
- **E2.** Envolve pagamento, documento fiscal, dado de saúde, biometria, ou usuário menor de idade?
- **E3.** Vai ter analytics? Pixel de campanha? Cookie além do necessário?
- **E4.** Qual a retenção, e quem responde pedido de exclusão?
- **E4a.** Algum desses dados vai para um provedor de LLM, embedding ou ferramenta de terceiro? (se sim, ativa M14 e entra no inventário abaixo)
- **E7.** Quem é o **controlador** de cada dado: você, ou o seu cliente (SaaS B2B, em que você é **operador**)? A resposta muda quem atende o titular e quem comunica incidente.
- **E8.** O controlador é microempresa, EPP, startup ou pessoa física (pequeno porte)? Há tratamento de alto risco (muitos titulares **e** dado sensível, de vulnerável, decisão automatizada ou tecnologia emergente)?
- **E9.** Algum dado sai do Brasil? (nuvem, e-mail transacional, analytics, suporte, provedor de LLM hospedados fora)
- **E10.** Alguma decisão que afeta o titular é tomada só por processo automatizado? (aprovação, bloqueio, score, preço, ranking, moderação)
- **E11.** O produto é **direcionado** a criança ou adolescente, ou é de **acesso provável** por eles? (jogo, rede social, app educacional, qualquer coisa com chat ou compartilhamento)
- **E12.** Dado já coletado vai ser reutilizado para outra finalidade? (treinar ou avaliar modelo, marketing, venda, enriquecimento)
- **E13.** Quem é o encarregado (DPO)? Se pequeno porte sem encarregado: qual o canal do titular?

E5 e E6 estão em `modulos/engenharia.md` (M10).

---

## Inventário

Antes de qualquer regra, a tabela. Vai em `docs/rules/privacidade.md` e é atualizada **no mesmo PR** que muda a coleta. É o registro de operações exigido pelo art. 37 da LGPD; pequeno porte pode usar a versão simplificada (Res. CD/ANPD 2/2022).

| Dado | Titular | Categoria | Finalidade | Base legal | Onde fica | Quem acessa | Operadores | País / mecanismo | Retenção | Eliminação |
|---|---|---|---|---|---|---|---|---|---|---|
| ⟨campo⟩ | ⟨cliente, funcionário…⟩ | ⟨comum, sensível, criança⟩ | ⟨para quê⟩ | ⟨art. 7º, inciso; ou art. 11⟩ | ⟨sistema, tabela⟩ | ⟨papel⟩ | ⟨fornecedor ou "nenhum"⟩ | ⟨BR, ou país + mecanismo do art. 33⟩ | ⟨prazo + gatilho⟩ | ⟨job, script ou manual + quem⟩ |

- Campo sem finalidade não é coletado.
- Base legal escrita com **artigo e inciso**. "LGPD" sozinho não é base legal.
- Uma linha por finalidade. O mesmo e-mail usado para login e para newsletter são duas linhas, com bases diferentes.
- Coluna sem resposta é `⟨pendente: o quê (quem decide)⟩`, nunca chute.

---

## M11 · Regras

### Papéis

- **Papel decidido por operação, não por empresa.** Quem decide finalidade e meio é controlador; quem trata em nome dele é operador (Guia de agentes de tratamento, ANPD). Registre no ADR de privacidade.
- **Operador segue instrução do controlador** (art. 39). Em SaaS B2B, pedido de titular que chega ao operador é encaminhado ao cliente controlador. O fluxo de encaminhamento fica escrito.

### Base legal e finalidade

- **Base legal declarada por finalidade** (arts. 7º e 11). Sem base, não coleta.
- **Dado sensível** (saúde, biometria, genético, origem racial ou étnica, religião, opinião política, filiação sindical, vida sexual) só pelas hipóteses do art. 11. Legítimo interesse não cobre dado sensível (Guia de Legítimo Interesse, ANPD, 2024).
- **Consentimento é por finalidade determinada.** Autorização genérica é nula (art. 8º, §4º). Revogar é gratuito e facilitado (art. 8º, §5º). O registro guarda versão do texto, data e o que foi aceito.
- **Legítimo interesse exige teste de balanceamento escrito antes do uso**, guardado junto do inventário (art. 37; Guia de Legítimo Interesse). Sem o teste, a base não vale para o projeto.
- **Medição** agregada e sem identificador pode rodar por legítimo interesse, com o teste registrado. Qualquer coisa que identifique ou rastreie entre sites espera consentimento por categoria.
- **Mudança de finalidade** (E12) é finalidade nova: precisa de base própria e aviso ao titular antes de começar (art. 9º).
- **Minimização.** Formulário pede só o que a finalidade usa. CPF, data de nascimento, telefone e endereço completo exigem motivo na linha do inventário.

### Transparência, cookies e rastreamento

- **Política de privacidade** diz, por finalidade: o quê, para quê, base, com quem compartilha, por quanto tempo, como exercer direitos e quem é o controlador e o encarregado (art. 9º).
- **Banner sem padrão escuro:** recusar é um clique, no mesmo nível visual de aceitar. Categorias descritas por finalidade. Link permanente para revogar (Guia de Cookies, ANPD).
- **Nada não necessário carrega antes do consentimento.** Tag, pixel, SDK e cookie de categoria não necessária só são injetados depois do aceite daquela categoria. Verificado por teste que abre a página limpa e falha se houver requisição a domínio de terceiro não listado como necessário.
- Atribuição de origem em cookie próprio, não compartilhada com terceiro.
- **Mudança no que é coletado atualiza as páginas legais no mesmo PR.** PR que adiciona terceiro sem tocar nelas é reprovado.
- Script de terceiro entra junto da entrada correspondente na política de cookies, no mesmo PR.

### Direitos do titular

- **Um canal**, publicado, com responsável nomeado. Ele recebe confirmação, acesso, correção, anonimização, bloqueio ou eliminação, portabilidade, informação sobre compartilhamento e revogação (art. 18).
- **Prazo de acesso:** formato simplificado imediato; declaração completa em até 15 dias (art. 19). Pequeno porte tem prazos em dobro (Res. CD/ANPD 2/2022). O prazo vira campo no sistema de atendimento, não lembrança.
- **Identidade confirmada antes de entregar ou apagar.** Pedido de titular é vetor de vazamento se qualquer um consegue pedir o dado de outro.
- **Exclusão alcança tudo:** banco principal, réplicas, busca, cache, filas, arquivos enviados, operadores, índices vetoriais e logs de prompt. Backup sai por expiração documentada. Existe script de exclusão por titular, com teste que cria um titular, roda o script e falha se sobrar registro.
- **Decisão automatizada** (E10): o titular pode pedir revisão (art. 20). Existe fluxo para isso, e os critérios principais da decisão ficam registrados.

### Retenção e eliminação

- **Prazo por linha do inventário, com gatilho** (fim do contrato, N meses de inatividade, fim da campanha). "Indeterminado" não é prazo.
- Ao fim do tratamento, o dado é eliminado, salvo as exceções do art. 16 (obrigação legal, por exemplo). **Prazo legal mínimo cita a norma** na linha. Exemplo: aplicação de internet operada por empresa guarda registro de acesso por 6 meses, em sigilo e ambiente controlado (Marco Civil da Internet, art. 15).
- **Expurgo é job, não intenção.** Job agendado, com teste e alerta de falha. Modo Enxuto: script manual com data na agenda do dono.
- **Pseudonimizado continua pessoal.** Hash de e-mail, ID trocado e dado criptografado com chave guardada são pseudonimização, não anonimização (estudos técnicos de anonimização, ANPD, 2023). Só chame de anonimizado o conjunto que passou por avaliação de risco de reidentificação registrada.

### Segurança e incidentes

- **Proteção desde a concepção** (art. 46, §2º). Regras técnicas em `modulos/seguranca.md`. Este módulo acrescenta:
  - Acesso a dado pessoal por papel, mínimo necessário, revisado quando alguém sai.
  - Dado sensível e documento de identidade criptografados em repouso.
  - Acesso de operador interno a dado pessoal fica em log de auditoria (quem, quando, qual titular), sem o conteúdo.
- **Nenhum dado pessoal** em log, mensagem de erro, ferramenta de monitoramento, ambiente de teste, fixture versionada ou seed. Dado de teste é sintético.
- **Dump de produção não sai de produção** sem anonimização avaliada. Depurar com dado real é decisão do dono, registrada, com prazo de descarte.
- **Runbook de incidente** em `docs/runbooks/incidente-dados.md`, dizendo quem decide se comunica. Comunicação à ANPD e aos titulares em **3 dias úteis** do conhecimento de que dado pessoal foi afetado; complementação em até 20 dias úteis (Res. CD/ANPD 15/2024; pequeno porte, prazo em dobro). Se o projeto for operador, o runbook avisa o controlador primeiro.
- **Todo incidente é registrado**, e o registro fica guardado por no mínimo 5 anos, mesmo quando não há comunicação (Res. CD/ANPD 15/2024).

### Terceiros e transferência internacional

- **Todo operador tem contrato** que limita o uso à instrução do controlador (art. 39). O nome dele está no inventário e na política.
- **Fornecedor novo que recebe dado pessoal** entra por PR que atualiza inventário e política juntos.
- **Dado que sai do Brasil** (E9) é transferência internacional. A linha do inventário diz o país e o mecanismo do art. 33. Isso inclui nuvem, e-mail, analytics e provedor de LLM.
- **País com adequação reconhecida** pela ANPD dispensa outro mecanismo. A União Europeia foi reconhecida pela Res. CD/ANPD 32/2026; para outros destinos, confira a lista vigente.
- **Usando cláusulas-padrão contratuais** (Res. CD/ANPD 19/2024): o contrato incorpora o texto aprovado pela ANPD, e o site publica em português a página de transparência sobre a transferência (finalidade, país, controlador, direitos).

### Encarregado e governança

- **Encarregado nomeado**, com identidade e contato públicos, de preferência no site (art. 41, §1º; Res. CD/ANPD 18/2024). Pequeno porte pode dispensar o encarregado, mas mantém o canal do titular (Res. CD/ANPD 2/2022).
- **Pequeno porte com tratamento de alto risco perde as flexibilizações** (Res. CD/ANPD 2/2022). A avaliação de E8 fica escrita no ADR.
- **Relatório de impacto (RIPD)** antes do lançamento quando houver alto risco, dado sensível em escala, decisão automatizada relevante ou IA treinada com dado pessoal (art. 38). Feito antes de o tratamento começar e revisto quando o risco muda (perguntas e respostas sobre RIPD, ANPD).

### Crianças e adolescentes (E2, E11)

- **Melhor interesse** da criança e do adolescente orienta qualquer tratamento (art. 14).
- **Criança:** consentimento específico e em destaque de um dos pais ou responsável, com esforço razoável de verificar que veio dele (art. 14, §§1º e 5º). Jogo ou aplicação não condiciona participação a dado além do necessário (§4º). Texto adequado ao entendimento da criança (§6º).
- **ECA Digital** (Lei 15.211/2025) vale para produto direcionado a menores **ou de acesso provável** por eles (art. 1º). O que vira requisito de produto:
  - Configuração padrão na opção mais protetiva de privacidade; reduzir proteção é escolha informada (art. 7º).
  - Aferição de idade confiável onde o acesso é restrito por idade; autodeclaração não basta. Dado coletado para aferir idade só serve para isso (arts. 9º a 14).
  - Proibido perfilar menor para publicidade comercial dirigida (art. 22).
  - Ferramentas de supervisão para pais e responsáveis, já no padrão mais protetivo (arts. 16 a 18). Conta de usuário de até 16 anos vinculada à de um responsável (art. 24).
  - Proibida loot box em jogo direcionado ou de acesso provável por menores (art. 20).
- O fluxo de consentimento do responsável e de aferição de idade é decidido **antes** de qualquer tela de cadastro. A fiscalização é da ANPD. Regulamentação complementar (Decreto 12.880/2026) é conferida na revisão jurídica. ⟨pendente: ler o Decreto 12.880/2026 e incorporar as obrigações de produto que ele detalha (mantenedor)⟩

### Dado pessoal e IA (E4a, E12)

Complementa M14 (LLM02) e M15.

- **Só entra no prompt o dado que a tarefa usa.** Campos pessoais que a tarefa não precisa são removidos ou mascarados antes da chamada.
- **Provedor de LLM recebe dado pessoal só se constar no inventário** com: país e mecanismo de transferência, retenção do provedor e se o provedor usa o dado para treinar. O que diz o contrato ou os termos do provedor é registrado com a data da leitura.
- **Treinar, ajustar ou avaliar modelo com dado de usuário é finalidade nova** (E12): base própria, aviso prévio e caminho de oposição. A ANPD já atuou em casos assim (Notas Técnicas 27/2024 e 39/2024).
- **Eliminação alcança embeddings, índices vetoriais, histórico de conversa e logs de prompt.** Dado que não dá para remover do artefato (modelo ajustado) não entra no ajuste.
- Decisão que afeta o titular, tomada pela saída do modelo, cai no art. 20 (revisão) e em LLM07 (não decidir só pelo modelo).

### Agente no repositório e dados pessoais (M15)

- **O agente não lê** dump, backup, export de produção nem planilha de clientes. Esses caminhos ficam na lista de leitura negada da config do agente.
- **O agente não cola dado pessoal** em issue, PR, commit, mensagem, prompt de ferramenta externa ou servidor MCP de terceiro.
- **Fixture e seed são sintéticos.** CPF, CNPJ, telefone e e-mail de teste são gerados ou de domínio reservado (`example.com`), nunca de pessoa real.
- **Migração que cria campo pessoal atualiza o inventário no mesmo PR.** O agente não abre esse PR sem a linha nova da tabela.
- **O agente não declara conformidade.** Texto de produto, README ou política nunca diz "em conformidade com a LGPD". Política e termos gerados são rascunho marcado `⟨revisão jurídica⟩`.

### Revisão jurídica

- **Revisão jurídica antes do lançamento** quando houver dado pessoal de cliente, pagamento, dado sensível, menor de idade, transferência internacional ou IA com dado pessoal. Registre como **risco bloqueante** até acontecer.
- O agente lista, para o revisor, as linhas do inventário, as bases escolhidas e os pontos `⟨pendente⟩`. Ele não escolhe sozinho base legal discutível: apresenta as opções com consequência (regra 5 da sessão de bootstrap).

---

## Gates

Cada gate segue `modulos/nucleo.md`: canário must-block e must-pass, sabotagem uma vez, válvula de escape com motivo na linha.

| Gate | Reprova quando | Modo |
|---|---|---|
| **inventário-acompanha-schema** | Diff de migração, schema ou modelo adiciona campo cujo nome casa com a lista de dado pessoal do projeto (`cpf`, `email`, `telefone`, `nascimento`, `endereco`, `rg`…) e o PR não toca `docs/rules/privacidade.md` | Médio, Completo |
| **sem-pessoal-em-log** | Chamada de log ou de erro interpola campo da mesma lista | Médio, Completo |
| **terceiro-acompanha-política** | Diff adiciona domínio de script, pixel ou SDK externo e não toca a política de cookies | Médio, Completo |
| **sem-dado-real-em-fixture** | Fixture ou seed contém CPF com dígito verificador válido fora da lista de CPFs de teste do projeto, ou e-mail fora de domínio reservado | Médio, Completo |
| **nada-antes-do-consentimento** | Teste de navegador em página limpa registra requisição a domínio de terceiro não necessário antes do aceite | Completo |
| **exclusão-por-titular** | Teste cria titular, roda o script de exclusão e encontra registro remanescente | Completo |

A lista de nomes de campo pessoal é do projeto, versionada junto do gate, e cresce quando um caso escapa (regra de promoção do M1).

---

## Por modo

| Modo | O que o M11 exige |
|---|---|
| **Enxuto** | Inventário; base legal por linha; nada pessoal em log, fixture ou commit; retenção com data. Sem gate |
| **Médio** | Enxuto + política e canal do titular + os quatro gates de diff + expurgo por script + runbook de incidente |
| **Completo** | Médio + testes de consentimento e de exclusão no CI + RIPD quando couber + contratos de operador e de transferência registrados + revisão jurídica como bloqueio de lançamento |

---

## Entregáveis do M11

- `docs/rules/privacidade.md`: inventário, testes de balanceamento de legítimo interesse, matriz de retenção, fluxo do titular, lista de operadores e transferências.
- ADR de privacidade: papel (controlador ou operador), porte e risco (E8), encarregado ou canal, decisões de base legal e o que ficou pendente para o jurídico.
- `docs/runbooks/incidente-dados.md`: quem decide, prazos, modelo de comunicação, onde fica o registro.
- Gates e canários do modo escolhido.
- Rascunho de política de privacidade e de cookies marcado `⟨revisão jurídica⟩`.
- RIPD, quando couber.

---

## Referências

Norma é citada pelo artigo. Texto oficial de lei e ato normativo não tem proteção de direito autoral (Lei 9.610/1998, art. 8º, IV). O conteúdo do site da ANPD é publicado sob [CC BY-ND 3.0](https://creativecommons.org/licenses/by-nd/3.0/deed.pt_BR) (sem derivações): os guias são **referenciados**, não adaptados nem traduzidos para este pacote.

### Normas

| Fonte | O que sustenta aqui |
|---|---|
| [Lei 13.709/2018 — LGPD (texto compilado)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm) | Bases legais, direitos, prazos, papéis, encarregado, segurança, incidentes, transferência |
| [Lei 15.352/2026](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/lei/L15352.htm) | ANPD como Agência Nacional de Proteção de Dados |
| [Lei 15.211/2025 — ECA Digital](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15211.htm) | Requisitos para produto direcionado ou de acesso provável por menores |
| [Lei 12.965/2014 — Marco Civil da Internet](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm) | Guarda de registros de acesso (art. 15) |
| Decreto 12.880/2026 ⟨pendente: link oficial (mantenedor)⟩ | Regulamentação do ECA Digital |
| Resolução CD/ANPD 2/2022 | Agente de tratamento de pequeno porte ⟨pendente: citar os artigos (dispensa de encarregado, registro simplificado, prazos em dobro, alto risco) conferidos no texto oficial, e o que a Res. 15/2024 alterou nela (mantenedor)⟩ |
| Resolução CD/ANPD 15/2024 | Comunicação de incidente de segurança |
| Resolução CD/ANPD 18/2024 | Encarregado |
| Resolução CD/ANPD 19/2024 | Transferência internacional e cláusulas-padrão |
| Resolução CD/ANPD 32/2026 | Adequação da União Europeia para transferência internacional |

⟨pendente: link de cada resolução para o texto oficial no DOU ou na ANPD (mantenedor)⟩

As resoluções estão na página de [regulamentações da ANPD](https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd).

### Guias e estudos da ANPD

| Fonte | O que sustenta aqui |
|---|---|
| [Guias orientativos (lista oficial)](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes) | Ponto de partida para conferir a versão vigente |
| Guia — Cookies e proteção de dados pessoais (2022) | Banner, categorias, consentimento |
| Guia — Hipóteses legais: Legítimo Interesse (2024) | Teste de balanceamento; não cobre dado sensível |
| Guia — Definições dos agentes de tratamento e do encarregado (v2.0, 2022) | Controlador × operador |
| Guia — Atuação do encarregado (2024) | Encarregado |
| Guia — Segurança da informação para agentes de tratamento de pequeno porte | Medidas mínimas nos modos Enxuto e Médio |
| [Documentos técnicos e orientativos](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/documentos-tecnicos-orientativos) | Estudos de anonimização (2023), Radar Tecnológico nº 3 (IA generativa) e nº 5 (aferição de idade), Notas Técnicas 27/2024 e 39/2024 (IA generativa com dado pessoal) |

O guia de anonimização e pseudonimização teve minuta em consulta pública em 2024 e não consta da lista oficial de guias; até ser publicado, cite os estudos técnicos.

### Modelos

| Fonte | Uso |
|---|---|
| [Governo Digital — Guia de Elaboração de Inventário de Dados Pessoais (v2.0, 2023)](https://www.gov.br/governodigital/pt-br/privacidade-e-seguranca/ppsi/guia_inventario_dados_pessoais.pdf) | Referência de colunas do inventário. Feito para o setor público; não é obrigatório |
| [ANPD — Perguntas e respostas sobre RIPD](https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/relatorio-de-impacto-a-protecao-de-dados-pessoais-ripd) | Quando elaborar o RIPD (alto risco, antes de começar o tratamento) e revisão contínua |

Fontes revisadas em 2026-10-08. Ao contribuir, confira a versão vigente na página oficial antes de citar.
