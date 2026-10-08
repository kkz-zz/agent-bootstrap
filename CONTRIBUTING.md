# Contribuindo

Contribuição boa aqui é regra que veio de um setup real e evitou um problema real.

## O que aceitamos

- **Regra nova em um módulo**, com o motivo: o que deu errado sem ela.
- **Módulo novo**, com gatilho de entrevista que o ativa e os arquivos que ele gera.
- **Correção** de regra que não se verifica em diff, ou de referência desatualizada (ex.: nova edição do OWASP, norma ou guia novo da ANPD). Fonte de privacidade é a norma oficial ou a página da ANPD, citada pelo artigo ou pelo título; blog de escritório serve para achar, não para citar.
- **Tradução** dos arquivos para outro idioma, em pasta própria.

## O que não aceitamos

- Regra sem motivo, ou que não dá para verificar.
- Regra que depende de uma stack específica dentro de módulo genérico — vai no módulo da superfície (`engenharia.md`) com gatilho.
- Texto de preenchimento. Os mesmos critérios de `modulos/ia.md` (anti-slop) valem para este repositório.

## Como

1. Abra uma issue descrevendo o problema que a regra resolve.
2. PR com uma mudança temática por vez. Se mexer em ID de módulo (M1–M15) ou de pergunta (A1, D9…), atualize todas as referências.
3. Teste de fumaça: rode o bootstrap com um agente num repositório de exemplo e anexe ao PR o trecho da sessão em que a regra nova atuou.

Ao contribuir, você concorda em licenciar sua contribuição sob [CC BY-SA 4.0](LICENSE).
