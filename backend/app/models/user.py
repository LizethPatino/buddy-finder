"""The users table: students and Students' Union staff."""
from sqlalchemy import CheckConstraint, Index, func

from app.extensions import db


class User(db.Model):
    """A person who can log in. Deleting a user also deletes their tickets and opt-ins."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # bcrypt hash, never the password
    role = db.Column(db.String(10), nullable=False, server_default="student")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint("role IN ('student', 'staff')", name="ck_users_role"),
        # Case-insensitive, so Sara@qmul.ac.uk and sara@qmul.ac.uk can't both register.
        Index("uq_users_email_lower", func.lower(email), unique=True),
    )
