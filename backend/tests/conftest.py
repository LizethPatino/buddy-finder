"""Test fixtures: a fresh Postgres database set up exactly like Neon.

Needs TEST_ADMIN_DATABASE_URL: a superuser on a throwaway Postgres server
(never Neon production), e.g. postgresql://postgres@localhost:5432/postgres.
Database tests are skipped when it isn't set. Also needs psql on the PATH.
"""
import os
import subprocess
import uuid
from pathlib import Path

import psycopg
import pytest
from flask_migrate import upgrade
from sqlalchemy.engine import make_url

from app import create_app

BACKEND = Path(__file__).resolve().parent.parent
ROLE_PASSWORDS = {"bf_migrator": "test-migrator", "bf_app": "test-app", "bf_analytics": "test-analytics"}


def _url(base, **parts):
    """Return base with some URL parts replaced, as a plain string."""
    return make_url(base).set(**parts).render_as_string(hide_password=False)


@pytest.fixture(scope="session")
def db_urls():
    """Create a database, run roles.sql and the migrations, and yield a URL per role."""
    admin = os.environ.get("TEST_ADMIN_DATABASE_URL")
    if not admin:
        pytest.skip("TEST_ADMIN_DATABASE_URL not set")

    name = f"bf_test_{uuid.uuid4().hex[:8]}"
    with psycopg.connect(admin, autocommit=True) as conn:
        conn.execute(f'CREATE DATABASE "{name}"')
    owner = _url(admin, database=name)
    try:
        subprocess.run(
            ["psql", owner, "-q", "-f", str(BACKEND / "db" / "roles.sql"),
             "-v", f"migrator_password={ROLE_PASSWORDS['bf_migrator']}",
             "-v", f"app_password={ROLE_PASSWORDS['bf_app']}",
             "-v", f"analytics_password={ROLE_PASSWORDS['bf_analytics']}"],
            check=True,
        )
        urls = {
            role: _url(owner, username=role, password=password)
            for role, password in ROLE_PASSWORDS.items()
        }
        app = create_app({"SQLALCHEMY_DATABASE_URI": urls["bf_migrator"]})
        with app.app_context():
            upgrade(directory=str(BACKEND / "migrations"))
        yield urls
    finally:
        with psycopg.connect(admin, autocommit=True) as conn:
            conn.execute(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)')


@pytest.fixture
def connect(db_urls):
    """Open autocommit connections as a given role; all are closed after the test."""
    opened = []

    def _connect(role="bf_app"):
        conn = psycopg.connect(db_urls[role], autocommit=True)
        opened.append(conn)
        return conn

    yield _connect
    for conn in opened:
        conn.close()


@pytest.fixture
def event_with_students(connect):
    """Insert an event and n students holding tickets for it. Returns (event_id, [user_ids])."""
    conn = connect()

    def _make(n):
        event_id = conn.execute(
            "INSERT INTO events (title, venue, starts_at) VALUES ('Quiz', 'The Hub', now()) RETURNING id"
        ).fetchone()[0]
        user_ids = []
        for _ in range(n):
            user_id = conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES ('S', %s, 'x') RETURNING id",
                (f"{uuid.uuid4().hex}@qmul.ac.uk",),
            ).fetchone()[0]
            conn.execute("INSERT INTO tickets (user_id, event_id) VALUES (%s, %s)", (user_id, event_id))
            user_ids.append(user_id)
        return event_id, user_ids

    return _make
