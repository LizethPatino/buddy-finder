"""The tickets table: filled by the simulated Native "ticket claimed" webhook."""
from sqlalchemy import UniqueConstraint, func

from app.extensions import db


class Ticket(db.Model):
    """A student's ticket for one event. One ticket per user per event (a repeat is a 409)."""

    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = db.Column(
        db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    claimed_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (UniqueConstraint("user_id", "event_id", name="uq_tickets_user_event"),)
