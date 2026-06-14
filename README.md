# Bank DIO API

API REST de banco digital com cadastro de usuarios, autenticacao JWT Bearer,
contas e movimentacoes. O projeto usa FastAPI, PostgreSQL, SQLAlchemy async,
Alembic e uma separacao inspirada em Clean Architecture.

## Estado atual

O fluxo principal esta funcional e coberto por testes:

- `POST /api/v1/users`;
- `POST /api/v1/auth/login`;
- `GET /api/v1/users/me`;
- `GET /health`;
- Swagger em `/docs`;
- repositorio de usuarios com `AsyncSession`;
- migrations Alembic sem `create_all` no startup;
- 12 testes automatizados.

Contas, deposito e saque existem, mas ainda precisam de testes de integracao em
PostgreSQL, idempotencia e geracao distribuida de numero de conta antes de um
uso real.

## Stack

- Python 3.13
- FastAPI e Uvicorn
- Pydantic e Pydantic Settings
- SQLAlchemy 2 async e AsyncPG
- PostgreSQL
- Alembic e Psycopg
- python-jose
- pwdlib com Argon2
- Pytest, pytest-asyncio, HTTPX e aiosqlite
- Poetry

## Arquitetura

```text
src/app/
|-- domain/          # entidades, regras, excecoes e contratos
|-- application/     # casos de uso e portas
|-- infrastructure/  # SQLAlchemy, repositorios, conexao e UoW
|-- interfaces/api/  # FastAPI, schemas, dependencias e rotas
|-- core/            # configuracao e adaptadores de seguranca
`-- main.py           # composicao da aplicacao
```

Fluxo principal:

```text
HTTP -> route -> service/use case -> repository -> AsyncSession -> PostgreSQL
```

Detalhes: [ARCHITECTURE.md](ARCHITECTURE.md).

## Requisitos

- Python `>=3.13,<4.0`
- Poetry 2.x
- PostgreSQL

## Instalacao

Na raiz do repositorio:

```bash
poetry install
```

Crie a configuracao local:

```powershell
Copy-Item src/.env.example src/.env
```

Em Bash:

```bash
cp src/.env.example src/.env
```

Edite `src/.env` e use uma chave forte exclusiva por ambiente.

## Variaveis de ambiente

| Variavel | Obrigatoria | Descricao |
| --- | --- | --- |
| `DB_USER` | sim | Usuario PostgreSQL |
| `DB_PASSWORD` | sim | Senha PostgreSQL |
| `DB_HOST` | sim | Host PostgreSQL |
| `DB_PORT` | sim | Porta PostgreSQL |
| `DB_NAME` | sim | Banco da aplicacao |
| `SECRET_KEY` | sim | Chave HS256 com pelo menos 32 caracteres |
| `ALGORITHM` | nao | Somente `HS256`; padrao `HS256` |
| `TOKEN_EXPIRE_MINUTES` | sim | Expiracao do access token |

O arquivo esperado e `src/.env`. Nao versione o `.env`.

## Banco e migrations

Crie o banco configurado em `DB_NAME` e aplique:

```bash
poetry run alembic upgrade head
```

Historico:

```bash
poetry run alembic history
```

Nova migration:

```bash
poetry run alembic revision --autogenerate -m "descricao"
```

Revise migrations autogeradas antes de aplicar.

## Executar a API

```bash
poetry run uvicorn app.main:app --reload
```

URLs:

- API: <http://127.0.0.1:8000>
- Health: <http://127.0.0.1:8000/health>
- Swagger: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## Endpoints principais

| Metodo | Rota | Auth | Funcao |
| --- | --- | --- | --- |
| `POST` | `/api/v1/users` | nao | Criar usuario |
| `POST` | `/api/v1/auth/login` | nao | Emitir access token |
| `GET` | `/api/v1/users/me` | Bearer | Usuario atual |
| `GET` | `/health` | nao | Health check |

Login usa formulario OAuth2:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=maria@example.com&password=SenhaForte1!"
```

Veja payloads e status em [API.md](API.md).

## Testes

```bash
poetry run pytest -q
```

Os testes HTTP nao usam o banco de producao. Os testes de repositorio usam
SQLite async isolado para validar o contrato, persistencia e constraint unica.
Veja [TESTING.md](TESTING.md).

## Documentacao

- [Diagnostico tecnico](docs/DIAGNOSTIC.md)
- [Arquitetura](ARCHITECTURE.md)
- [Seguranca](SECURITY.md)
- [Testes](TESTING.md)
- [API](API.md)
- [Guia de estudo](docs/STUDY_GUIDE.md)
- [ADRs](docs/adr/)
- [Changelog](CHANGELOG.md)

## Limites antes de producao

- adicionar RBAC/ABAC e revisar listagem global de usuarios;
- refresh token, revogacao, `iss`, `aud` e rotacao de chaves;
- rate limiting, MFA e trilha de auditoria;
- observabilidade com metricas, logs estruturados e traces;
- PostgreSQL efemero no CI para validar migrations;
- numero de conta alocado pelo banco em ambiente multiworker;
- idempotencia e testes de concorrencia para operacoes financeiras.
