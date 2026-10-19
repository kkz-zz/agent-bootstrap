# Operação

Módulo **M16** (gatilho: C1 inclui superfície publicada — site público, painel logado, API, bot ou job — **e** B4 indica que o time administra o deploy). Biblioteca, CLI distribuída e app só de loja sem servidor próprio não ativam. Cobre o que acontece depois do deploy: o que está exposto, como volta quando cai, como alguém fica sabendo e como se publica sem improviso.

Dado pessoal em incidente é M11 (`modulos/privacidade.md`). Segredo e conta administrativa são M4 (`modulos/seguranca.md`). O agente não alcança produção (M15, "Ambiente do agente"): neste módulo ele **prepara** inventário, regra, teste e diff com reversão; a mudança é aplicada pela pipeline ou por quem tem a credencial.

**Por modo:** Enxuto não ativa o M16. Médio aplica *Exposição*, *Backup* e *Publicação*, com verificação manual registrada. Completo aplica tudo, com os testes de exposição e de alerta automatizados em job agendado da CI que roda **de fora** da rede de produção, contra os endereços públicos, sem credencial de produção.

Os valores de perda e de tempo aceitáveis, retenção, periodicidade e os limiares do critério de rollback dependem do sistema e são definidos pelo dono. O agente pergunta e registra; não propõe número padrão.

---

## Exposição e ambientes

- **Inventário do que está publicado:** domínios e subdomínios, serviços, portas abertas, bancos, filas e painéis administrativos, cada item com dono e motivo. Fica no `CHECKLIST.md`, sem credencial. Item sem dono é candidato a desligar.
- Produção separada de homologação e desenvolvimento: credenciais, banco e domínio diferentes. Dado real não é copiado para ambiente de teste sem o tratamento definido no M11.
- **Banco e painel administrativo não respondem da internet.** Verificação: de uma máquina fora da rede do provedor (runner da CI, por exemplo), a conexão ao endereço público na porta do banco e ao painel falha. Teste no mesmo host não prova nada. Rodar também contra a configuração antiga, como caso-controle, quando ela existia.
- Firewall ou grupo de segurança com o mínimo: só as portas que o inventário justifica. Toda regra nova chega como diff, com a reversão escrita e o teste que prova que o serviço continua acessível.
- Em hospedagem gerenciada, a divisão de responsabilidade com o provedor é escrita: o que ele configura, o que o time confere.

## Backup e restauração

- **A evidência de backup é uma restauração medida**, não o log "backup concluído". Restaurar em ambiente isolado, conferir os dados e registrar data, tempo gasto e versão. Sem restauração testada, o backup conta como inexistente.
- Pelo menos uma cópia fora do alcance da credencial de produção: offline, em outra conta ou em armazenamento imutável. Ransomware e erro humano apagam primeiro o backup que a aplicação alcança (CISA). Verificação: com a credencial da aplicação, em homologação, a tentativa de apagar ou sobrescrever a cópia é negada.
- Perda aceitável de dados e tempo aceitável de recuperação definidos pelo dono e registrados em ADR. A periodicidade do backup e do teste de restauração sai desses dois números.
- Backup contém o mesmo dado pessoal da produção: retenção e acesso seguem o M11.

## Alertas e logs

- **Alerta de indisponibilidade que chega a quem pode agir.** Verificação: disparar um alerta de teste; a pessoa de plantão confirma o recebimento, e a data fica registrada. Entrega técnica a um destino de teste não substitui essa confirmação. Alerta que vai para canal que ninguém lê é igual a não ter alerta.
- Monitorar também o que vence: certificado, domínio, cota e credencial com prazo (M4).
- Log com contexto suficiente para reconstruir o que aconteceu (quem, o quê, quando, resultado) e **sem senha, token ou segredo**. Verificação: teste que faz requisição com token conhecido e confere que ele não aparece no log gerado. Retenção e acesso definidos pelo dono; dado pessoal em log segue o M11.

## Publicação

- Publica só pela pipeline, a partir de versão identificada (tag ou SHA). Deploy feito à mão a partir de máquina local é exceção registrada.
- **Critério de rollback escrito antes do deploy:** o que é medido, e qual resultado manda reverter. Se o critério falhar, reverte; não se corrige produção às pressas.
- Smoke test das jornadas essenciais logo após o deploy, automatizado no modo Completo.
- Mudança de DNS, de firewall, de permissão ou restauração de dados é decisão de quem tem a credencial; o agente entrega evidência, diff e reversão.

## Incidente de operação

- `docs/runbooks/incidente-operacao.md`: quem decide, quem é avisado e como, primeiros passos de contenção, onde ficam evidência e linha do tempo, como se declara encerrado. Cópia fora do sistema que pode cair.
- O runbook é exercitado (simulação com o time) e a data do último exercício fica registrada.
- Incidente que envolve dado pessoal segue também o `docs/runbooks/incidente-dados.md` do M11.
- Ordem de prioridade na correção: exposição de dado, credencial vazada, falha de autorização e acesso administrativo inseguro primeiro; depois o que impede uso, recuperação e observação; desempenho e acabamento por último.

---

## Referências

Regras com redação própria.

| Fonte | O que sustenta aqui |
|---|---|
| [NIST — Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) (2024) | Organização em Governar, Identificar, Proteger, Detectar, Responder e Recuperar, que se sobrepõem ao longo da operação |
| [CISA — #StopRansomware Guide](https://www.cisa.gov/stopransomware/ransomware-guide) | Backup offline ou imutável, restauração testada, plano de incidente exercitado, separação de contas administrativas e segmentação |
