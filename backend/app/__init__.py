"""Buddy Finder Flask app factory.

Only the database wiring lives here for now. Routes, auth and schemas get
registered here as those pieces are merged.
"""
import os

from flask import Flask

from app.extensions import db, migrate


def create_app(config=None):
    """Build the Flask app.

    DATABASE_URL is the main connection (the app connects as bf_app).
    ANALYTICS_DATABASE_URL is optional: when set, admin stats can read the
    event_stats view through the read-only bf_analytics role, via
    db.engines["analytics"].
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    # Neon closes idle connections when it scales to zero; pre_ping reconnects instead of failing.
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True, "pool_recycle": 300}
    if os.environ.get("ANALYTICS_DATABASE_URL"):
        app.config["SQLALCHEMY_BINDS"] = {"analytics": os.environ["ANALYTICS_DATABASE_URL"]}
    app.config.update(config or {})

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  # noqa: F401  registers the tables for migrations

    return app
