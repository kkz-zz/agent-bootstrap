# Design system, marca e documentos gerados

Módulos **M2** (gatilho: existe interface) e **M13** (gatilho: o produto emite .docx, .pdf, .xlsx, .svg, .dxf), mais o **bloco D** da entrevista.

O formato do pacote de marca segue o de [`nexu-io/open-design`](https://github.com/nexu-io/open-design/blob/main/design-systems/README.md): cada marca é uma pasta com `manifest.json`, `DESIGN.md` e `tokens.css`. O `DESIGN.md` é o contrato de marca que o agente lê antes de qualquer peça visual.

---

## Bloco D — Entrevista

**Não escolha nenhuma cor, fonte ou escala antes de receber o material.** Se o dono não tem identidade pronta, registre como pendência e gere o resto do setup sem M2.

- **D1.** Você vai me enviar a identidade visual? Em que forma — arquivo do Figma (peça o *file key* e os *node IDs* dos swatches), guia de marca em PDF, imagens, ou pacote de tokens já publicado?
- **D2.** Uma marca só, ou mais de uma convivendo no mesmo produto? Quais superfícies pertencem a qual marca?
- **D3.** Se mais de uma: **qual manda em cada superfície**, e como a outra aparece? (assinatura em rodapé, chrome, crédito)
- **D4.** Alguma cor tem restrição especial? Pergunte explicitamente por estes três casos, que aparecem sempre:
  - cor que **mantém o valor em toda aplicação** e nunca recolore (um ícone, um símbolo);
  - cor de **apoio de interface** que não é cor de marca e não entra em logo;
  - cor que **reprova em contraste** sobre o fundo padrão e por isso não pode ir em texto pequeno.
- **D5.** Tema claro, escuro, ou os dois? Alta densidade / modo quiosque / impressão?
- **D6.** Quais plataformas consomem os tokens? (CSS custom properties, preset de Tailwind, `ThemeData` do Flutter, `tokens.json` W3C, XML de Android, Swift)
- **D7.** Tipografia: quais famílias, de onde vêm, e há licença a respeitar?
- **D8.** Existe pacote de tokens publicado, ou preciso propor um? Quem versiona?
- **D9.** Qual a **direção** visual, em uma frase? (a tese que toda microdecisão precisa sustentar — vira a primeira seção do `DESIGN.md` e é o critério da dimensão "Filosofia" na crítica)

**Extraia os valores da fonte**, nunca de aproximação visual. Com Figma, use a API/MCP e os node IDs. Se a extração falhar, diga que falhou e peça os valores — cor aproximada à mão é defeito de marca.

---

## Pacote de marca

```
design-system/<marca>/
├── manifest.json   metadados, procedência, caminhos declarados
├── DESIGN.md       contrato de marca em prosa, lido pelo agente
└── tokens.css      tokens semânticos compilados — única fonte de valor
```

Opcionais, quando a marca precisar: `USAGE.md` (ordem de leitura para o agente), `components.html` (fixture de componentes), `design-tokens.json` e preset de Tailwind (**derivados** de `tokens.css`, nunca editados à mão), `fonts/`, `assets/`, `source/` (evidência da extração: export do Figma, PDF do guia).

Regras do pacote:

- Pasta e `manifest.id` com o mesmo slug, ASCII normalizado.
- Todo caminho declarado no manifesto existe e é relativo.
- Arquivo derivado é cache, não fonte. Gate confere paridade com `tokens.css`.
- `manifest.source` registra **de onde** cada valor veio. Valor sem procedência é valor inventado.
- `DESIGN.md` com no mínimo **sete seções H2 substantivas**, nomeadas pelo que a marca precisa. Ponto de partida em `templates/DESIGN.md`. Valor numérico não se repete no `DESIGN.md` — ele cita o token.

---

## M2 · Regras de design system

- Camadas: `marca` (rampas) → `semântica` (o que componente usa) → `componente` (exceção).
- **Componente não conhece cor.** Literal de cor existe só em `tokens.css`. Em qualquer outro arquivo é erro de build.
- Proibido: literal de cor, classe de cor crua do framework de CSS, valor arbitrário fora da escala, estilo visual inline, rampa de marca usada direto em componente.
- Faltou um token semântico? É lacuna do design system, não caso especial. Proponha o token.
- Troca de marca e de tema por atributo no elemento raiz do segmento, **sem fallback silencioso** — superfície sem marca declarada quebra o build.
- Script de tema inline e bloqueante antes da primeira pintura, senão pisca o tema errado.
- Contraste verificado em **todas** as combinações marca × tema.
- Com mais de uma marca: a regra é por **superfície**, não por produto. Escreva a tabela (qual marca manda, como a outra aparece). Proibido degradê interpolando paletas de marcas diferentes — a costura é faixa de cor neutra.
- Fluxo de mudança de cor: fonte de verdade → extração → `tokens.css` → derivados → versão semântica → PR nos consumidores. Mudança de valor é `minor`; remoção ou renomeação de token semântico é `major`.
- **Gate:** script que procura literal, classe crua, valor arbitrário e rampa em componente, e confere paridade dos derivados. Com canário.

---

## Controle de qualidade visual

O gate pega o que é padrão; ele não sabe se a tela é boa. Para isso existe `skills/design-critique`: revisão em cinco dimensões com nota 0–10 e evidência por nota.

- Toda peça visual nova (tela, landing, deck, documento gerado) passa pela crítica **antes** de ser dada como pronta.
- Dimensão com nota abaixo de 5 é `FALHOU` na entrega.
- O relatório da crítica vai anexado ao PR como evidência.
- A crítica **não** roda no mesmo turno em que a peça foi gerada; o dono vê a peça primeiro, ou a crítica roda numa sessão separada.

---

## M13 · Documentos gerados

- Identidade visual do documento sai do **mesmo** `tokens.css` da interface; literal de cor proibido no gerador.
- Gabarito versionado; conteúdo separado de layout.
- Saída verificada por teste que abre o arquivo gerado e confere estrutura — não só "não deu erro".
- Fonte embutida só com licença compatível; registre qual.
- Documento gerado também passa pela `design-critique` na primeira versão do gabarito.
