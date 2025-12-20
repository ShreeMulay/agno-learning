# Lesson 03: Database Configuration

Configure database storage for sessions, memories, and knowledge.

## Key Concepts

### Supported Databases

Agno supports multiple database backends:

| Database | Class | Use Case |
|----------|-------|----------|
| SQLite | `SqliteDb`, `AsyncSqliteDb` | Development, single-server |
| PostgreSQL | `PostgresDb`, `AsyncPostgresDb` | Production, multi-server |
| MySQL | `MySqlDb` | Production alternative |
| MongoDB | `MongoDb` | Document-based storage |
| Redis | `RedisDb` | Caching, fast sessions |

### SQLite Configuration

```python
from agno.db.sqlite import SqliteDb, AsyncSqliteDb

# Synchronous
db = SqliteDb(
    id="my_db",
    db_file="data/app.db",
    session_table="agent_sessions",
)

# Asynchronous (recommended for production)
db = AsyncSqliteDb(
    id="my_async_db",
    db_file="data/app.db",
)
```

### PostgreSQL Configuration

```python
from agno.db.postgres import PostgresDb, AsyncPostgresDb

# From URL
db = PostgresDb(
    db_url="postgresql://user:pass@localhost:5432/mydb"
)

# Async for production
db = AsyncPostgresDb(
    db_url="postgresql+asyncpg://user:pass@localhost:5432/mydb"
)
```

### What Gets Stored?

- **Sessions**: Conversation history per session_id
- **User Memories**: Long-term facts about users
- **Knowledge Content**: Embedded documents (with vector DB)
- **Evals**: Agent evaluation results

## Run the Example

```bash
python main.py

# Check the generated database
ls -la tmp/
```

## Key Points

1. **Use Async**: `AsyncSqliteDb` and `AsyncPostgresDb` for production
2. **Session Tables**: Customize with `session_table` parameter
3. **Auto-Migration**: Tables created automatically on first use
4. **History**: Use `add_history_to_context=True` with `num_history_runs`

## Exercises

1. Create an agent with SQLite persistence
2. Run multiple conversations with the same session_id
3. Inspect the database file to see stored sessions
4. Switch to PostgreSQL (requires local Postgres)
