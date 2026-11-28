
/**
 * Displays information about the selected university event.
 */

import { Link, useParams } from 'react-router';
import { mockEvents } from '../data/mockEvents';

/**
 * Retrieves the event ID from the URL and renders
 * the corresponding event details.
 */
function EventDetailsPage() {
  const { eventId } = useParams();

  const event = mockEvents.find(
    (item) => String(item.id) === eventId
  );

  if (!event) {
    return (
      <main className="main-container">
        <h2>Event not found</h2>
        <Link to="/events">Back to events</Link>
      </main>
    );
  }

  return (
    <main className="main-container">

      <Link to="/events" className="back-link">
        ← My events
      </Link>

      <section className="welcome-section">
        <h2>{event.title}</h2>
        <p>{event.date}</p>
        <p>{event.location}</p>
      </section>

      <section className="page-panel">
        <h2>Going alone?</h2>
        <p>
          Find other students with similar interests
          and attend the event together.
        </p>

        <p>Interest selection will be available here.</p>
      </section>

    </main>
  );
}

export default EventDetailsPage;
