/**
 * Reusable component for displaying a Buddy Finder event.
 */

interface EventCardProps {
  title: string;
  date: string;
  location: string;
}

/**
 * Displays an event and its primary action.
 */
function EventCard({ title, date, location }: EventCardProps) {
  return (
    <article className="event-card">

      <div className="event-details">
        <h3 className="event-title">{title}</h3>
        <p className="event-date">{date}</p>
        <p className="event-location">{location}</p>
      </div>

      <div className="event-actions">
        <button
          type="button"
          className="primary-button"
        >
          Find my group
        </button>
      </div>

    </article>
  );
}

export default EventCard;