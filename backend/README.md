# Tattuu Backend API

API FastAPI para a plataforma Tattuu de descoberta de tatuadores.

## Arquitetura

O backend segue uma arquitetura em camadas com separação clara de responsabilidades:

- **Routes**: Endpoints da API com lógica de manipulação de requisições/respostas
- **Schemas**: Validação de dados com Pydantic
- **Models**: Modelos ORM com SQLAlchemy
- **Database**: Configuração e gerenciamento de conexões
- **Core**: Segurança, autenticação e configurações

## Setup

### Pré-requisitos

- Python 3.10+
- PostgreSQL 12+ (provável escolha) ou banco relacional compatível

### Instalação

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais
```

### Execução

```bash
# Desenvolvimento com reload
uvicorn app.main:app --reload

# Produção
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

A API estará disponível em `http://localhost:8000`  
Documentação interativa em `http://localhost:8000/docs`

## Endpoints

### Autenticação

- `POST /api/v1/users/register` - Registrar novo usuário
- `POST /api/v1/users/login` - Fazer login e obter token JWT
- `GET /api/v1/users/me/profile` - Obter perfil do usuário autenticado (requer token)

### Usuários

- `GET /api/v1/users/{user_id}` - Obter dados de um usuário

### Tatuadores

- `POST /api/v1/artists/` - Criar perfil de tatuador
- `GET /api/v1/artists/` - Listar tatuadores com filtros opcionais
- `GET /api/v1/artists/{artist_id}` - Obter detalhes completos de um tatuador
- `PUT /api/v1/artists/{artist_id}` - Atualizar perfil de tatuador

### Portfólio

- `POST /api/v1/portfolios/` - Criar novo item de portfólio
- `GET /api/v1/portfolios/{portfolio_id}` - Obter detalhes de item de portfólio
- `GET /api/v1/portfolios/artista/{artist_id}` - Listar portfólio de um tatuador
- `PUT /api/v1/portfolios/{portfolio_id}` - Atualizar item de portfólio
- `DELETE /api/v1/portfolios/{portfolio_id}` - Deletar item de portfólio

### Avaliações e Comentários

- `POST /api/v1/ratings/` - Criar avaliação de tatuador
- `GET /api/v1/ratings/{rating_id}` - Obter detalhes de uma avaliação
- `GET /api/v1/ratings/artista/{artist_id}` - Listar avaliações de um tatuador
- `GET /api/v1/ratings/usuario/{user_id}` - Listar avaliações feitas por um usuário
- `PUT /api/v1/ratings/{rating_id}` - Atualizar avaliação
- `DELETE /api/v1/ratings/{rating_id}` - Deletar avaliação

### Favoritos

- `POST /api/v1/favorites/{artist_id}` - Adicionar tatuador aos favoritos
- `GET /api/v1/favorites/usuario/{user_id}` - Listar favoritos de um usuário
- `DELETE /api/v1/favorites/{artist_id}` - Remover tatuador dos favoritos
- `GET /api/v1/favorites/usuario/{user_id}/verificar/{artist_id}` - Verificar se é favorito

### Busca Avançada

- `GET /api/v1/search/artistas` - Buscar tatuadores com filtros (estilo, localização, avaliação)
- `GET /api/v1/search/recomendados` - Tatuadores mais bem avaliados
- `GET /api/v1/search/novos` - Tatuadores registrados mais recentemente
- `GET /api/v1/search/experiencia` - Buscar por anos de experiência
- `GET /api/v1/search/estilos` - Listar todos os estilos disponíveis
- `GET /api/v1/search/artistas/estilo/{style_id}/top` - Melhores tatuadores por estilo

### Utilitários

- `GET /` - Health check básico
- `GET /health` - Health check detalhado

## Modelos de Dados

### User
```
id: int (PK)
email: str (unique)
username: str (unique)
full_name: str (opcional)
hashed_password: str
is_active: bool
created_at: datetime
updated_at: datetime
```

### Artist
```
id: int (PK)
user_id: int (FK → users)
bio: str (opcional)
location: str (opcional)
latitude: float (opcional)
longitude: float (opcional)
years_experience: int (opcional)
rating: float (média de avaliações)
total_ratings: int
created_at: datetime
updated_at: datetime
```

### Style
```
id: int (PK)
name: str (unique)
description: str (opcional)
created_at: datetime
```

### Portfolio
```
id: int (PK)
artist_id: int (FK → artists)
title: str
description: str (opcional)
image_url: str
style_id: int (FK → styles, opcional)
created_at: datetime
```

### Rating
```
id: int (PK)
user_id: int (FK → users)
artist_id: int (FK → artists)
score: float (1-5)
comment: str (opcional)
created_at: datetime
```

### Favorite
```
user_id: int (FK → users, PK)
artist_id: int (FK → artists, PK)
created_at: datetime
```

## Autenticação

A autenticação é baseada em **JWT (JSON Web Tokens)**:

1. Usuário faz login com `/users/login` enviando `username/email` e `password`
2. API retorna um `access_token`
3. Cliente envia o token no header: `Authorization: Bearer {token}`
4. Token expira após 30 minutos (configurável via `ACCESS_TOKEN_EXPIRE_MINUTES`)

### Exemplo de Uso

```bash
# 1. Registrar usuário
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "artista@example.com",
    "username": "artista123",
    "full_name": "João Tatuador",
    "password": "senha_segura"
  }'

# 2. Fazer login
curl -X POST http://localhost:8000/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "artista123",
    "password": "senha_segura"
  }'

# 3. Usar token em requisição protegida
curl -X GET http://localhost:8000/api/v1/users/me/profile \
  -H "Authorization: Bearer {token_retornado}"
```

## Testes

Execute testes unitários:

```bash
pytest
```

Com cobertura:

```bash
pytest --cov=app
```

## Estrutura de Diretórios

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py       # Configurações e variáveis de ambiente
│   │   └── security.py     # Funções de segurança e JWT
│   ├── models/
│   │   └── models.py       # Modelos ORM SQLAlchemy
│   ├── schemas/
│   │   └── schemas.py      # Schemas Pydantic para validação
│   ├── routes/
│   │   ├── users.py        # Endpoints de usuários
│   │   ├── artists.py      # Endpoints de tatuadores
│   │   ├── portfolios.py   # Endpoints de portfólio
│   │   ├── ratings.py      # Endpoints de avaliações
│   │   ├── favorites.py    # Endpoints de favoritos
│   │   └── search.py       # Endpoints de busca
│   ├── database.py         # Configuração de banco de dados
│   └── main.py             # Aplicação FastAPI
├── tests/
│   ├── conftest.py         # Fixtures de testes
│   └── test_api.py         # Testes dos endpoints
├── requirements.txt        # Dependências Python
├── .env.example           # Variáveis de ambiente (exemplo)
├── Dockerfile             # Docker image
└── README.md             # Este arquivo
```

## Variáveis de Ambiente

Ver `.env.example` para lista completa. Variáveis principais:

- `DEBUG`: Modo debug (True/False)
- `SECRET_KEY`: Chave secreta para JWT (mínimo 32 caracteres)
- `DATABASE_URL`: Connection string do banco (provável PostgreSQL)
- `REDIS_URL`: URL do Redis (para cache e eventos)
- `KAFKA_BOOTSTRAP_SERVERS`: Servidores Kafka (para streaming)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Expiração do token (padrão: 30)

## Próximos Passos

- [ ] Implementar autenticação OAuth 2.0
- [ ] Adicionar rate limiting
- [ ] Implementar cache com Redis
- [ ] Integração com Kafka para eventos
- [ ] Testes de carga e performance
- [ ] Documentação OpenAPI customizada
- [ ] Implementar soft delete para dados sensíveis

## Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JWT.io](https://jwt.io/)

---

**Versão**: 1.0.0  
**Última atualização**: Maio 2026
