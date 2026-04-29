# Tattuu — Plataforma de Descoberta de Tatuadores

Projeto acadêmico de Engenharia de Dados desenvolvido com arquitetura Lakehouse (Modelo Medalhão) para centralizar tatuadores profissionais e facilitar a descoberta baseada em estilo, localização, portfólio e avaliações.

## Descrição do Projeto

O Tattuu é uma plataforma digital que conecta usuários finais com tatuadores profissionais, permitindo:
- Busca e filtragem por estilo de tatuagem e localização geográfica
- Visualização de portfólios de tatuadores
- Sistema de avaliações e comentários
- Análise de dados de interação para recomendações personalizadas

### Escopo e Dados

O projeto trabalha com dois grupos principais de dados:

- **Dados operacionais**: cadastro de usuários, tatuadores, estilos, portfólios, favoritos e avaliações, persistidos em PostgreSQL (provável escolha).
- **Dados de streaming**: eventos de busca, clique, visualização e atualização de perfil, produzidos em tempo real para análise comportamental.

Essa separação permite combinar consistência transacional no núcleo da aplicação com análise analítica sobre eventos de uso.

### Domínios e Serviços

- **Usuários**: cadastro, autenticação, perfil, histórico e favoritos.
- **Tatuadores**: cadastro profissional, portfólio, estilos e localização.
- **Busca**: filtros por estilo, localização e ordenação de resultados.
- **Analytics**: coleta de eventos, métricas, relatórios e recomendações.

Serviços compartilhados:

- Autenticação e autorização
- Armazenamento de mídia
- Logging e monitoramento
- Publicação/consumo de eventos

## Arquitetura

O projeto implementa uma arquitetura **Lakehouse** baseada no **modelo Medalhão**, combinando características de Data Lakes (flexibilidade, escalabilidade) com Data Warehouses (qualidade, governança).

### Camadas de Dados

1. **Bronze Layer**: Ingestão de dados brutos (operacionais e eventos)
2. **Silver Layer**: Dados limpos, validados e padronizados
3. **Gold Layer**: Dados agregados e otimizados para análise

### Fluxo de Dados

```
Aplicação → API FastAPI → PostgreSQL (camada operacional, provável escolha) + Kafka (eventos)
     ↓
  Bronze Layer (S3/armazenamento local)
     ↓
  Silver Layer (Transformações com Pandas/Spark)
     ↓
  Gold Layer (Agregações e métricas)
     ↓
  Power BI (Dashboards) + API (Recomendações)
```

### Caminhos de Processamento

- **Batch**: Exportação diária de PostgreSQL (provável base operacional) para Bronze, processamento noturno (Silver → Gold)
- **Streaming**: Ingestão contínua de eventos via Kafka, processamento em janelas de 5 minutos

### Justificativa da Arquitetura

- **Bronze** preserva o dado bruto para rastreabilidade e reprocessamento.
- **Silver** aplica limpeza, padronização e validação para reduzir ruído.
- **Gold** concentra dados prontos para leitura analítica e consumo por dashboards ou recomendações.
- A combinação de batch e streaming reduz latência sem perder confiabilidade na persistência operacional.

Para detalhes completos, consulte [Documento de Arquitetura](docs/doc.txt).

## Estrutura do Repositório

```
tatt-oo/
├── frontend/                # Aplicação React + TypeScript (Vite)
│   ├── src/
│   │   ├── screens/        # Telas/páginas principais
│   │   ├── pages/          # Rotas e páginas
│   │   ├── components/     # Componentes reutilizáveis
│   │   ├── navigation/     # Navegação e rotas
│   │   ├── services/       # Integração com API
│   │   ├── styles/         # Estilos globais e temas
│   │   ├── types/          # Tipos TypeScript
│   │   ├── data/           # Dados estáticos ou fixtures
│   │   ├── App.tsx         # Componente raiz
│   │   ├── main.tsx        # Entry point
│   │   └── index.css       # Estilos globais
│   ├── public/             # Arquivos estáticos
│   ├── docker/             # Configuração Docker
│   ├── package.json
│   └── Dockerfile
├── backend/                # API FastAPI (Python)
│   ├── app/
│   │   ├── core/           # Configuração e segurança
│   │   ├── models/         # Modelos SQLAlchemy (ORM)
│   │   ├── schemas/        # Schemas Pydantic (validação)
│   │   ├── routes/         # Endpoints da API
│   │   ├── database.py     # Conexão e sessões
│   │   └── main.py         # Aplicação FastAPI
│   ├── tests/              # Testes unitários
│   ├── requirements.txt    # Dependências Python
│   └── Dockerfile
├── docs/                   # Documentação
│   └── doc.txt            # Especificação completa (Parte 1)
├── infra/                 # Configuração de infraestrutura
├── scripts/               # Scripts de utilidade
├── docker-compose.yml     # Orquestração de containers
└── README.md             # Este arquivo
```

## Tecnologias

### Ingestão

- **FastAPI**: expõe a API e recebe os dados transacionais e eventos da aplicação.
- **Kafka**: desacopla a geração de eventos do processamento analítico em tempo real.

### Armazenamento

- **PostgreSQL**: provável banco relacional para garantir consistência transacional das entidades operacionais.
- **Armazenamento de Bronze**: mantém dados brutos para auditoria e reprocessamento.

### Processamento

- **Pandas**: adequado para as transformações iniciais do pipeline Silver/Gold em ambiente acadêmico.
- **SQLAlchemy**: organiza o acesso aos dados e mantém o código desacoplado do banco.

### Validação e Contratos

- **Pydantic**: valida entradas e saídas da API com schemas explícitos.
- **pytest**: apoia validações básicas do comportamento da aplicação.

### Consumo

- **React**: interface para navegação, busca e consumo dos dados operacionais.
- **Vite**: entrega um ambiente rápido de desenvolvimento e build para o frontend.

### Infraestrutura e Governança

- **Docker** e **Docker Compose**: padronizam execução local e ambiente reprodutível.
- **Prometheus** e **Grafana**: suportam observabilidade.
- **Adminer**: facilita inspeção do banco relacional, provavelmente PostgreSQL, durante desenvolvimento.

### Frontend

- **React**: Biblioteca de UI
- **TypeScript**: Tipagem estática em JavaScript
- **Vite**: Build tool moderno

## Pré-requisitos

- Docker >= 20.10
- Docker Compose >= 2.0

## Setup e Execução

### Com Docker Compose

1. Clone o repositório:
```bash
git clone <url-repositorio>
cd tatt-oo
```

2. Inicie os serviços (PASSO MUITO IMPORTANTE):
```bash
docker compose up --build
```

Os serviços estarão disponíveis em:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Documentação API: http://localhost:8000/docs
- PostgreSQL: localhost:5432 (provável porta do banco relacional, via Adminer em http://localhost:8081)
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

### Desenvolvimento Local (Backend)

1. Entre no diretório backend:
```bash
cd backend
```

2. Crie ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Instale dependências:
```bash
pip install -r requirements.txt
```

4. Configure ambiente:
```bash
cp .env.example .env
# Edite .env com suas configurações
```

5. Inicie servidor:
```bash
uvicorn app.main:app --reload
```

## Endpoints da API

### Usuários
- `POST /api/v1/users/register` - Registrar novo usuário
- `GET /api/v1/users/{user_id}` - Recuperar dados do usuário

### Tatuadores
- `POST /api/v1/artists/` - Criar perfil de tatuador
- `GET /api/v1/artists/` - Listar tatuadores (filtros: style_id, location)
- `GET /api/v1/artists/{artist_id}` - Detalhes completos do tatuador
- `PUT /api/v1/artists/{artist_id}` - Atualizar perfil

Documentação interativa disponível em `/docs` após iniciar o servidor.

## Modelos de Dados

### Entidades Principais

- **User**: Usuários clientes da plataforma
- **Artist**: Tatuadores profissionais
- **Style**: Estilos de tatuagem
- **Portfolio**: Itens de portfólio dos tatuadores
- **Rating**: Avaliações e comentários de usuários
- **Favorite**: Relação de tatuadores favoritos

Ver `backend/app/models/models.py` para esquema completo.

## Documentação

- [Especificação Completa de Arquitetura](docs/doc.txt) - Contém:
  - Descrição detalhada do projeto e contexto de negócio
  - Classificação e análise de dados
  - Definição de domínios e serviços
  - Arquitetura e fluxo de dados com diagramas
  - Justificativa e trade-offs de tecnologias
  - Análise de riscos e limitações
  - Referências bibliográficas


## Referências

- Databricks Lakehouse: https://databricks.com/blog/2020/01/30/what-is-a-data-lakehouse.html
- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- Apache Kafka: https://kafka.apache.org/


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
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
