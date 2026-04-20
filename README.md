# Tatt-oo Data Platform

Projeto acadêmico da disciplina de Engenharia de Dados.

## Estrutura do Repositório

- `frontend/`: aplicação web React + TypeScript
- `backend/`: API Node.js + Express + TypeScript
- `docs/`: documentação da avaliação (Parte 1)

## Entrega da Parte 1 (Planejamento)

- [Descrição do Projeto](docs/01-descricao-projeto.md)
- [Definição e Classificação dos Dados](docs/02-definicao-classificacao-dados.md)
- [Domínios e Serviços](docs/03-dominios-servicos.md)
- [Arquitetura e Fluxo de Dados](docs/04-arquitetura-fluxo-dados.md)
- [Tecnologias e Justificativas](docs/05-tecnologias-como-sera-feito.md)
- [Considerações Finais](docs/06-consideracoes-finais.md)

## Subindo com Docker

### Pré-requisitos

- Docker
- Docker Compose

### Build e execução

```bash
docker compose up --build
```

Serviços expostos:

- Frontend: http://localhost:8080
- Backend: http://localhost:3333/api/health
- Métricas da API: http://localhost:3333/api/metrics
- PostgreSQL: localhost:5432
- Adminer: http://localhost:8081
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)
- cAdvisor: http://localhost:8082

### Comandos úteis

```bash
npm run docker:up
npm run docker:logs
npm run docker:down
```

### Demonstração rápida

```powershell
.\scripts\demo.ps1
.\scripts\smoke-test.ps1
```

O dashboard do Grafana é provisionado automaticamente com métricas da API e dos containers.

### Derrubar ambiente

```bash
docker compose down
```

## Execução local sem Docker

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
npm install
npm run dev
```
