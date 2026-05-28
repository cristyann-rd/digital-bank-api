# Bank DIO API

API REST desenvolvida com FastAPI para cadastro de usuarios, autenticacao JWT e base para operacoes bancarias. O projeto usa uma arquitetura em camadas, separando dominio, casos de uso, infraestrutura e interface HTTP.

## Sumario

- [Visao geral](#visao-geral)
- [Tecnologias](#tecnologias)
- [Requisitos](#requisitos)
- [Instalacao](#instalacao)
- [Configuracao](#configuracao)
- [Execucao local](#execucao-local)
- [Endpoints](#endpoints)
- [Exemplos de uso](#exemplos-de-uso)
- [Estrutura de pastas](#estrutura-de-pastas)
- [Scripts e comandos uteis](#scripts-e-comandos-uteis)
- [Testes](#testes)
- [Deploy](#deploy)
- [Contribuicao](#contribuicao)

## Visao geral

O Bank DIO e uma API backend para um contexto bancario. Atualmente, a aplicacao possui endpoints para:

- cadastro de usuarios;
- login com email e senha;
- emissao de token JWT Bearer;
- consulta, listagem e atualizacao de usuarios autenticados;
- persistencia em PostgreSQL usando SQLAlchemy assincrono;
- migrations com Alembic.

O codigo tambem contem entidades, modelos e servicos iniciais para contas e transacoes bancarias, incluindo geracao de digito de conta, mas essas funcionalidades ainda nao estao expostas em rotas HTTP registradas no `app/main.py`.

## Tecnologias

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic e Pydantic Settings
- SQLAlchemy 2.x com suporte assincrono
- PostgreSQL
- AsyncPG
- Psycopg
- Alembic
- python-jose para JWT
- pwdlib com Argon2 para hash de senhas
- Poetry para gerenciamento de dependencias

Dependencias adicionais presentes no projeto incluem `python-multipart`, `email-validator`, `python-dotenv`, `redis`, `structlog`, `slowapi`, `tenacity`, `pendulum` e `uuid6`.

## Requisitos

Antes de executar o projeto, instale:

- Python `>=3.13,<4.0.0`
- Poetry `>=2.0`
- PostgreSQL em execucao
- Git, opcional para versionamento

## Instalacao

Clone o repositorio e acesse a pasta onde esta o `pyproject.toml`:

```bash
git clone <url-do-repositorio>
cd Desafio_dio/src
```

Instale as dependencias com Poetry:

```bash
poetry install
```

Ative o ambiente virtual, se desejar:

```bash
poetry shell
```

Tambem e possivel executar os comandos diretamente com `poetry run`.

## Configuracao

A aplicacao carrega variaveis de ambiente a partir de um arquivo `.env` localizado na pasta `src`.

Crie o arquivo:

```bash
cp .env.example .env
```

Caso nao exista um `.env.example`, crie manualmente um arquivo `.env` com o conteudo abaixo:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bank_dio

SECRET_KEY=altere-esta-chave-em-producao
ALGORITHM=HS256
TOKEN_EXPIRE_MINUTES=60
```

As variaveis usadas pelo projeto sao:

| Variavel | Obrigatoria | Descricao |
| --- | --- | --- |
| `DB_USER` | Sim | Usuario do PostgreSQL. |
| `DB_PASSWORD` | Sim | Senha do PostgreSQL. |
| `DB_HOST` | Sim | Host do banco de dados. |
| `DB_PORT` | Sim | Porta do banco de dados. |
| `DB_NAME` | Sim | Nome do banco de dados. |
| `SECRET_KEY` | Sim | Chave usada para assinar tokens JWT. |
| `ALGORITHM` | Nao | Algoritmo JWT. Padrao: `HS256`. |
| `TOKEN_EXPIRE_MINUTES` | Sim | Tempo de expiracao do token de acesso, em minutos. |

> Observacao: o `Settings` do projeto monta automaticamente as URLs `postgresql+asyncpg://...` e `postgresql+psycopg://...` a partir dessas variaveis.

## Banco de dados e migrations

Crie o banco no PostgreSQL antes de aplicar as migrations:

```sql
CREATE DATABASE bank_dio;
```

Execute as migrations:

```bash
poetry run alembic upgrade head
```

Para criar uma nova migration a partir dos modelos:

```bash
poetry run alembic revision --autogenerate -m "descricao da alteracao"
```

Para desfazer a ultima migration:

```bash
poetry run alembic downgrade -1
```

## Execucao local

Execute a API com Uvicorn:

```bash
poetry run uvicorn app.main:create_app --factory --reload
```

Por padrao, a aplicacao ficara disponivel em:

- API: <http://127.0.0.1:8000>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## Endpoints

### Autenticacao

| Metodo | Rota | Autenticacao | Descricao |
| --- | --- | --- | --- |
| `POST` | `/api/v1/auth/login` | Nao | Autentica o usuario e retorna um token JWT Bearer. |

O login usa `OAuth2PasswordRequestForm`, portanto deve ser enviado como `application/x-www-form-urlencoded`.

### Usuarios

| Metodo | Rota | Autenticacao | Descricao |
| --- | --- | --- | --- |
| `POST` | `/api/v1/users/register` | Nao | Cadastra um novo usuario. |
| `GET` | `/api/v1/users/` | Sim | Lista usuarios cadastrados. |
| `GET` | `/api/v1/users/{user_id}` | Sim | Busca um usuario por ID. |
| `PATCH` | `/api/v1/users/{user_id}` | Sim | Atualiza dados de um usuario. |

Rotas privadas exigem o header:

```http
Authorization: Bearer <access_token>
```

## Exemplos de uso

### Health check manual

A aplicacao nao possui uma rota especifica de health check. Para validar se o servidor subiu corretamente, acesse a documentacao interativa:

```bash
curl http://127.0.0.1:8000/docs
```

### Cadastrar usuario

```bash
curl -X POST http://127.0.0.1:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria Silva",
    "email": "maria@example.com",
    "password": "Senha123"
  }'
```

Resposta esperada:

```json
{
  "id": 1,
  "email": "maria@example.com"
}
```

### Fazer login

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=maria@example.com&password=Senha123"
```

Resposta esperada:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

### Listar usuarios autenticados

```bash
curl http://127.0.0.1:8000/api/v1/users/ \
  -H "Authorization: Bearer <jwt>"
```

### Buscar usuario por ID

```bash
curl http://127.0.0.1:8000/api/v1/users/1 \
  -H "Authorization: Bearer <jwt>"
```

### Atualizar usuario

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/users/1 \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria Souza",
    "email": "maria.souza@example.com",
    "password": "NovaSenha123"
  }'
```

## Estrutura de pastas

```text
src/
|-- alembic.ini
|-- pyproject.toml
|-- poetry.lock
|-- migrations/
|   |-- env.py
|   `-- versions/
|-- tests/
|   `-- __init__.py
`-- app/
    |-- main.py
    |-- core/
    |   |-- config.py
    |   `-- security.py
    |-- domain/
    |   |-- entities/
    |   |-- policy/
    |   |-- repositories/
    |   `-- validators/
    |-- application/
    |   |-- services/
    |   `-- use_cases/
    |-- infrastructure/
    |   |-- database/
    |   |-- events/
    |   |-- models/
    |   `-- repositories/
    `-- interfaces/
        `-- api/
            |-- dependencies.py
            |-- schemas/
            `-- v1/routes/
```

### Camadas principais

- `app/main.py`: cria a aplicacao FastAPI e registra as rotas.
- `app/core`: configuracoes da aplicacao e utilitarios de seguranca.
- `app/domain`: entidades, contratos de repositorios, politicas e validadores.
- `app/application`: casos de uso e servicos de aplicacao.
- `app/infrastructure`: banco de dados, modelos SQLAlchemy, repositorios concretos e eventos.
- `app/interfaces/api`: schemas Pydantic, dependencias FastAPI e rotas HTTP.
- `migrations`: configuracao e historico de migrations Alembic.
- `tests`: pacote reservado para testes automatizados.

## Principais funcionalidades

- Cadastro de usuario com email unico.
- Hash de senha usando `pwdlib` com algoritmo recomendado.
- Autenticacao por email e senha.
- Geracao de token JWT com expiracao configuravel.
- Protecao de rotas privadas com `OAuth2PasswordBearer`.
- Repositorio assincrono de usuarios com SQLAlchemy.
- Migration inicial da tabela `users`.
- Base de dominio para contas e transacoes.
- Geracao de digito de conta por soma dos digitos e modulo 10.

## Scripts e comandos uteis

O projeto ainda nao define scripts customizados no `pyproject.toml`. Use os comandos abaixo durante o desenvolvimento:

| Comando | Descricao |
| --- | --- |
| `poetry install` | Instala as dependencias. |
| `poetry run uvicorn app.main:create_app --factory --reload` | Executa a API localmente com reload. |
| `poetry run alembic upgrade head` | Aplica migrations pendentes. |
| `poetry run alembic downgrade -1` | Reverte a ultima migration. |
| `poetry run alembic revision --autogenerate -m "mensagem"` | Gera uma nova migration. |

## Testes

A pasta `tests` existe, mas ainda nao ha testes automatizados implementados.

Recomendacao para evolucao:

```bash
poetry add --group dev pytest pytest-asyncio httpx
```

Depois de adicionar testes, execute:

```bash
poetry run pytest
```

Sugestoes de cobertura inicial:

- validacao de cadastro de usuarios;
- bloqueio de email duplicado;
- login com credenciais validas e invalidas;
- acesso a rotas privadas com e sem token;
- testes de repositorio usando banco de teste;
- validacao da politica de senha.

## Deploy

Para publicar a API em producao:

1. Configure um banco PostgreSQL gerenciado ou dedicado.
2. Defina variaveis de ambiente seguras no provedor de hospedagem.
3. Use uma `SECRET_KEY` forte e exclusiva por ambiente.
4. Instale as dependencias com `poetry install --only main`.
5. Execute as migrations com `poetry run alembic upgrade head`.
6. Inicie a aplicacao com Uvicorn.

Exemplo de comando para producao:

```bash
poetry run uvicorn app.main:create_app --factory --host 0.0.0.0 --port 8000
```

Em ambientes produtivos, recomenda-se executar a aplicacao atras de um proxy reverso, como Nginx, ou usar um servidor/process manager adequado ao provedor escolhido.

## Pontos de atencao

- As rotas de conta e transacao ainda nao estao expostas na API.
- A migration atual cria apenas a tabela `users`.
- O arquivo `.env` nao deve ser versionado.
- A politica de senha exige simbolo em `PASSWORD_POLICY`, mas o validador atual ainda nao verifica simbolos.
- O projeto mistura imports `app...` e `src.app...`; padronizar os imports pode evitar problemas em alguns ambientes.

## Contribuicao

1. Crie uma branch para sua alteracao:
bash
git checkout -b feature/minha-alteracao

2. Instale as dependencias e configure o `.env`.

3. Implemente a alteracao mantendo a separacao entre dominio, aplicacao, infraestrutura e interface.

4. Adicione ou atualize testes quando aplicavel.

5. Execute migrations e testes localmente.

6. Abra um pull request descrevendo o problema, a solucao e os impactos.

## Licenca

Este projeto ainda nao possui uma licenca definida. Adicione um arquivo `LICENSE` antes de distribuir ou publicar o codigo.
