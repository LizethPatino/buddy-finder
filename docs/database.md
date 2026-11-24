# Database

PostgreSQL on [Neon](https://neon.tech). The tables are in [`architecture.md`](architecture.md#data-model); this page covers setup, roles and the rules the database enforces on its own.

## Code map

| Path | What it is |
| --- | --- |
| `backend/app/models/` | SQLAlchemy tables |
| `backend/migrations/` | Alembic migrations (Flask-Migrate). `0001_initial_schema.py` also creates the group-size trigger, the `event_stats` view and the role grants |
| `backend/db/roles.sql` | Creates the three database roles. Run once per database |
| `backend/tests/test_database.py` | Checks roles, constraints and group size against a real Postgres |

## Roles

| Role | Used by | Can |
| --- | --- | --- |
| `bf_migrator` | `flask db upgrade` | Own and change the tables |
| `bf_app` | The Flask API (`DATABASE_URL`) | Read and write rows. Cannot create, alter or drop tables |
| `bf_analytics` | Admin stats (`ANALYTICS_DATABASE_URL`) | Read the `event_stats` view only |

The roles are created with SQL, not in the Neon dashboard: dashboard roles join `neon_superuser` and would get far more rights than they need.

## Set up Neon (once)

1. Create a Neon project in the London region (AWS `eu-west-2`), close to our GKE cluster.
2. Copy the owner's **direct** connection string (Connect → turn **Connection pooling** off). Then create the roles:

   ```bash
   psql "<owner direct connection string>" \
     -v migrator_password="$(openssl rand -base64 24)" \
     -v app_password="$(openssl rand -base64 24)" \
     -v analytics_password="$(openssl rand -base64 24)" \
     -f backend/db/roles.sql
   ```

   Save the three passwords in the team's private store before closing the terminal. No `psql`? `brew install libpq`.
3. Build three connection strings from the owner's ones by swapping in each role's name and password:

   | Variable | Role | Host |
   | --- | --- | --- |
   | `MIGRATOR_DATABASE_URL` | `bf_migrator` | direct (no `-pooler`) |
   | `DATABASE_URL` | `bf_app` | **pooled** (`-pooler` in the host) |
   | `ANALYTICS_DATABASE_URL` | `bf_analytics` | pooled |

   The API uses the pooled host because 2–6 pods, each with its own connection pool, would run past the free plan's connection limit. Migrations need the direct host.
4. Run the migrations:

   ```bash
   cd backend
   DATABASE_URL="$MIGRATOR_DATABASE_URL" FLASK_APP=app:create_app flask db upgrade
   ```

In Kubernetes these URLs go in a Secret, never in the repo.

## Rules the database enforces

These hold even if the API has a bug, and even with several pods running at once. The API should turn each error into the response in brackets.

- Email is unique, ignoring case (409 email taken).
- One ticket per user per event (409 already claimed).
- An opt-in needs a ticket for the same event (403 no ticket), and at least one interest.
- One opt-in per user per event (409 already in).
- **A group has at most 4 members**, not counting anyone who declined. A trigger locks the group row while it counts, so two pods matching at the same moment can't make a group of 5. The loser gets a `check_violation` error ("group N is full"): matching should retry with another group or start a new one.
- A student can only join a group for the event they opted in to.
- Deleting a user deletes their tickets and opt-ins. Deleting an event deletes its tickets, groups and opt-ins. Deleting a staff member keeps their events.

## Changing the schema

1. Edit the models in `backend/app/models/`.
2. Generate a migration against a local database, then read it before committing:

   ```bash
   DATABASE_URL=postgresql://postgres@localhost:5432/buddy FLASK_APP=app:create_app flask db migrate -m "add x"
   ```

3. New tables are granted to `bf_app` automatically. Only views for `bf_analytics` need their own `GRANT`.

## Tests

The database tests need a throwaway Postgres (never Neon) where you are a superuser, plus `psql`. Each run creates and drops its own database.

```bash
cd backend
TEST_ADMIN_DATABASE_URL=postgresql://postgres@localhost:5432/postgres pytest
```

Without `TEST_ADMIN_DATABASE_URL` they are skipped.
