# Arquitetura

## Visao geral

O projeto aplica Clean Architecture de forma pragmatica. Dependencias de codigo
apontam para dentro: HTTP e banco conhecem aplicacao e dominio; dominio nao
conhece FastAPI, Pydantic, SQLAlchemy ou JWT.

```text
HTTP request
  -> FastAPI route
  -> application use case/service
  -> repository port
  -> SQLAlchemy async repository
  -> PostgreSQL
```

## Camadas

### `app/domain`

Contem entidades, regras de negocio, excecoes e contratos:

- `entities`: `User`, `Account` e `Transaction`;
- `validators` e `policy`: politica de senha;
- `repositories`: interfaces assincronas de persistencia;
- `unit_of_work.py`: contrato transacional para contas e transacoes;
- `exceptions`: erros independentes de HTTP.

Esta camada nao importa frameworks.

### `app/application`

Orquestra casos de uso. `UserService`, `AuthService`, `AccountUseCase`,
`DepositMoneyUseCase` e `WithdrawMoneyUseCase` dependem de contratos.
`application/ports/security.py` abstrai hash de senha e token, evitando acoplar
os casos de uso a `pwdlib` e JWT.

### `app/infrastructure`

Implementa detalhes externos:

- modelos SQLAlchemy;
- repositorios com `AsyncSession`;
- conexao PostgreSQL por `asyncpg`;
- Unit of Work;
- implementacao do gerador de numero de conta.

Repositorios convertem modelos ORM em entidades de dominio. Nenhum modelo ORM
e retornado diretamente pelas rotas.

### `app/interfaces/api`

Adapta HTTP para os casos de uso:

- schemas Pydantic validam entrada e filtram saida;
- dependencias FastAPI compoem repositorios, servicos e seguranca;
- rotas convertem excecoes da aplicacao em status HTTP.

As rotas nao implementam hash, JWT nem consultas SQL.

### `alembic`

Mantem a evolucao do schema. A aplicacao nao executa
`Base.metadata.create_all()` no startup.

## SQLAlchemy async

O runtime usa `create_async_engine`, `async_sessionmaker` e `AsyncSession`.
Consultas usam `select()` e `await session.execute(...)`; nao ha
`session.query()` nem `Session` sincrona. Alembic usa uma URL sincrona com
`psycopg`, pois o runner de migrations e separado do runtime async.

Para contas e transacoes, o Unit of Work delimita `commit` e `rollback`. O
repositorio de usuarios ainda controla sua propria transacao; unificar essa
politica em um unico Unit of Work e uma evolucao recomendada.

## JWT

`core/security.py` implementa os contratos de seguranca. O token contem `sub`,
`iat`, `exp` e `type=access`. A camada de aplicacao conhece apenas
`TokenManager`, nao a biblioteca JOSE.

## Decisoes e limites

- PostgreSQL e o banco de producao; SQLite em memoria e usado apenas nos testes
  de repositorio.
- `password_hash` existe na entidade interna, mas schemas de resposta nunca o
  incluem.
- O gerador sequencial atual e reutilizado no processo para evitar reinicio a
  cada request. Em multiplos workers, deve ser substituido por sequencia ou
  alocacao transacional no PostgreSQL.
- A listagem global de usuarios exige autenticacao, mas ainda precisa de RBAC
  antes de uso real.

## Anti-patterns evitados

- regra de negocio em rota;
- `HTTPException` em repositorio;
- ORM ou Pydantic no dominio;
- sessao sincrona em fluxo async;
- criacao automatica de tabelas no startup;
- retorno de hash de senha;
- caso de uso importando implementacao concreta de JWT ou hash.

## Referencias

- [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [SQLAlchemy asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Martin Fowler: Repository](https://martinfowler.com/eaaCatalog/repository.html)
- [Martin Fowler: Service Layer](https://martinfowler.com/eaaCatalog/serviceLayer.html)
- [Martin Fowler: Unit of Work](https://martinfowler.com/eaaCatalog/unitOfWork.html)
