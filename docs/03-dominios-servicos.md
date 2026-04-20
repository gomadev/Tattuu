# 03 - Domínios e Serviços

## Domínios de Negócio

- Atendimento e Agenda
- Financeiro
- Marketing e Aquisição
- Operações do Estúdio

## Serviços por Domínio

### Atendimento e Agenda

- Serviço de agendamento
- Serviço de confirmação e lembretes
- Serviço de histórico de sessões

### Financeiro

- Serviço de pagamentos
- Serviço de conciliação
- Serviço de fechamento diário

### Marketing e Aquisição

- Serviço de eventos de navegação
- Serviço de funil de conversão
- Serviço de campanhas

### Operações do Estúdio

- Serviço de capacidade por tatuador
- Serviço de produtividade
- Serviço de qualidade (no-show, retrabalho, avaliação)

### Serviços Compartilhados

- Catálogo de dados e metadados
- Observabilidade e monitoramento
- Governança e qualidade de dados

## Diagrama de Domínios e Serviços

```mermaid
flowchart LR
  A[Atendimento e Agenda] --> A1[Agendamento]
  A --> A2[Confirmacao e Lembretes]
  A --> A3[Historico de Sessoes]

  F[Financeiro] --> F1[Pagamentos]
  F --> F2[Conciliacao]
  F --> F3[Fechamento Diario]

  M[Marketing e Aquisicao] --> M1[Eventos de Navegacao]
  M --> M2[Funil de Conversao]
  M --> M3[Campanhas]

  O[Operacoes do Estudio] --> O1[Capacidade]
  O --> O2[Produtividade]
  O --> O3[Qualidade]

  S[Servicos Compartilhados]
  S --> S1[Catalogo]
  S --> S2[Observabilidade]
  S --> S3[Governanca]

  A --> S
  F --> S
  M --> S
  O --> S
```
