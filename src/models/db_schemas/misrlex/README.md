# Database Migration Guide

## Alembic Setup & Usage

1. **Initialize Alembic** (run from `src/models/db_schemas/misrlex`):
```bash
alembic init alembic
```
   - Creates `alembic` directory with migration scripts
   - Generates `alembic.ini` configuration file

2. **Configure `alembic.ini`**:
```ini
[alembic]
sqlalchemy.url = postgresql://${POSTGRES_USERNAME}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_MAIN_DATABASE}
```

3. **Modify `env.py` to import models**:
```python:src/models/db_schemas/misrlex/alembic/env.py
from schemas import SQLAlchemyBase  # Add this import
target_metadata = SQLAlchemyBase.metadata  # Ensure this line exists
```

4. **Create First Migration**:
```bash
alembic revision --autogenerate -m "Initial tables"
```
   - Generates migration script in `versions/`
   - **Important**: Review generated script before applying

5. **Apply Migrations**:
```bash
alembic upgrade head
```
   - Creates tables in PostgreSQL
   - Updates `alembic_version` table with current revision

## Docker Database Management

1. **Start Services**:
```bash
docker-compose -f docker/docker-compose.dev.yml up -d
```

2. **Access pgAdmin**:
   - URL: `http://localhost:5050`
   - Login with credentials from `.env`
   - **First Connection**:
     1. Right-click "Servers" → Register → Server
     2. Name: `Local PG`
     3. Connection:
        - Host: `pgvector`
        - Port: `5432`
        - Maintenance DB: `${POSTGRES_MAIN_DATABASE}`

## Troubleshooting Tips

- If `autogenerate` doesn't detect changes:
  1. Verify model imports in `env.py`
  2. Check SQLAlchemy model definitions match database state
  3. Run `alembic stamp head` to sync version table

## Database Management Alternatives

### DBeaver
1. Download and install from [dbeaver.io](https://dbeaver.io)
2. Create new connection:
   - Type: PostgreSQL
   - Host: localhost
   - Port: 5432
   - Database: ${POSTGRES_MAIN_DATABASE}
   - Authentication: Username/Password

### TablePlus
1. Download from [tableplus.com](https://tableplus.com)
2. New → PostgreSQL
3. Enter connection details matching DBeaver setup
        