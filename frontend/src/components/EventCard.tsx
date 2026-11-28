/**
 * Reusable component for displaying a Buddy Finder event.
 */

import { Link } from 'react-router';

interface EventCardProps {
  eventId: number;
  title: string;
  date: string;
  location: string;
}

/**
 * Displays an event and its primary action.
 */
function EventCard({
  eventId,
  title,
  date,
  location,
}: EventCardProps) {
  return (
    <article className="event-card">

      <div className="event-details">
        <h3 className="event-title">{title}</h3>
        <p className="event-date">{date}</p>
        <p className="event-location">{location}</p>
      </div>

      <div className="event-actions">
        <Link
          to={`/events/${eventId}`}
          className="primary-button event-link"
        >
          Find my group
        </Link>
      </div>

    </article>
  );
}

export default EventCard;