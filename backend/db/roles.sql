-- Buddy Finder database roles. Run ONCE per database, before the first migration,
-- as the database owner (on Neon: neondb_owner, using the DIRECT connection string):
--
--   psql "$OWNER_DATABASE_URL" \
--     -v migrator_password="$(openssl rand -base64 24)" \
--     -v app_password="$(openssl rand -base64 24)" \
--     -v analytics_password="$(openssl rand -base64 24)" \
--     -f backend/db/roles.sql
--
-- Save the three passwords in the team's private store. Never commit them.
--
-- Roles are created here in SQL on purpose: roles made in the Neon dashboard are
-- added to neon_superuser, which would give all three far more rights than they need.
--
--   bf_migrator   owns the tables; runs migrations (CREATE / ALTER / DROP)
--   bf_app        what the Flask API uses: read and write rows, cannot change tables
--   bf_analytics  read-only on the event_stats view, nothing else
--
-- Table-level grants for bf_app and bf_analytics are set by the first migration,
-- because only the tables' owner (bf_migrator) can grant on them.
-- Safe to run again: existing roles are left alone (use ALTER ROLE to change a password).

\set ON_ERROR_STOP on

SELECT format('CREATE ROLE bf_migrator LOGIN PASSWORD %L', :'migrator_password')
WHERE NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'bf_migrator') \gexec

SELECT format('CREATE ROLE bf_app LOGIN PASSWORD %L', :'app_password')
WHERE NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'bf_app') \gexec

SELECT format('CREATE ROLE bf_analytics LOGIN PASSWORD %L', :'analytics_password')
WHERE NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'bf_analytics') \gexec

-- Nobody but bf_migrator may create objects in the schema (already the default on Postgres 15+).
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT USAGE, CREATE ON SCHEMA public TO bf_migrator;
GRANT USAGE ON SCHEMA public TO bf_app, bf_analytics;
