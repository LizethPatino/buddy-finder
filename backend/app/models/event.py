"""The events table: Students' Union events with their map location and cached weather."""
from sqlalchemy.dialects.postgresql import JSONB

from app.extensions import db


class Event(db.Model):
    """An event staff created. Weather is cached here for 1 hour to protect the weather API."""

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float)  # filled once by geocoding when the event is created
    longitude = db.Column(db.Float)
    starts_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    meeting_point = db.Column(db.String(200))
    native_url = db.Column(db.String(500))
    weather = db.Column(JSONB)
    weather_updated_at = db.Column(db.DateTime(timezone=True))
    # Keep the event if the staff member who made it is deleted.
    created_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
