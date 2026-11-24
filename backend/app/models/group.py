"""Buddy groups and the opt-ins that place students in them."""
from sqlalchemy import CheckConstraint, ForeignKeyConstraint, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import ARRAY

from app.extensions import db


class BuddyGroup(db.Model):
    """A group of up to 4 students for one event.

    The 4-member limit is enforced by a database trigger (see the first
    migration), so it holds even when several API pods match at once.
    """

    __tablename__ = "buddy_groups"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(
        db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())


class OptIn(db.Model):
    """A student saying "find me a group" for an event, with their interests.

    group_id is empty while they are still looking. Declined members don't
    count towards the 4-member limit.
    """

    __tablename__ = "optins"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = db.Column(
        db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    interests = db.Column(ARRAY(db.Text), nullable=False)
    group_id = db.Column(
        db.Integer, db.ForeignKey("buddy_groups.id", ondelete="SET NULL"), index=True
    )
    membership = db.Column(db.String(10), nullable=False, server_default="pending")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "event_id", name="uq_optins_user_event"),
        CheckConstraint(
            "membership IN ('pending', 'accepted', 'declined')", name="ck_optins_membership"
        ),
        CheckConstraint("cardinality(interests) > 0", name="ck_optins_interests_not_empty"),
        # No ticket, no opt-in; and losing the ticket removes the opt-in.
        ForeignKeyConstraint(
            ["user_id", "event_id"],
            ["tickets.user_id", "tickets.event_id"],
            name="fk_optins_ticket",
            ondelete="CASCADE",
        ),
    )
