# 02 - Definição e Classificação dos Dados

## Fontes de Dados

| Fonte | Tipo | Formato | Volume Estimado | Frequência | Latência Esperada |
|---|---|---|---|---|---|
| Banco transacional (agendamentos, clientes, orçamentos) | Operacional | SQL (PostgreSQL) | ~5 GB/semestre | Contínuo | Baixa (segundos) |
| Eventos de navegação (cliques, funil, abandono) | Streaming | JSON | ~50 mil eventos/dia | Contínuo | Quase tempo real (1-5 s) |
| Logs de API e aplicação | Streaming | JSON/Texto | ~1-2 GB/dia | Contínuo | Quase tempo real |
| Exportações administrativas | Operacional histórico | CSV | ~200 MB/mês | Diário/Semanal | Média (minutos-horas) |

## Classificação Explícita

### Dados Operacionais

- **Transacionais:** clientes, sessões, pagamentos, agenda.
- **Batch/históricos:** snapshots diários de indicadores e exportações CSV.
- **Armazenamento primário:** PostgreSQL.

### Dados de Streaming

- **Eventos em tempo real:** cliques na web, criação/cancelamento de sessão, logs de API.
- **Canal de ingestão:** broker de eventos compatível com Kafka.
- **Destino inicial:** zona Bronze do data lake (objetos em Parquet/JSON).

## Detalhes das Fontes

- Origem: Frontend web, backend transacional, integrações administrativas.
- Formatos: JSON (eventos), CSV (lotes), tabelas relacionais (PostgreSQL), Parquet (camadas analíticas).
- Periodicidade: contínua (streaming) e janelas programadas (batch).
- Latência: baixa para observabilidade e média para consolidações analíticas.
