/**
 * Root component of the Buddy Finder application.
 */

import { useState } from 'react';
import Navbar from './components/Navbar';
import EventCard from './components/EventCard';
import GroupSummary from './components/GroupSummary';
import { mockEvents } from './data/mockEvents';
import './App.css';

/**
 * Displays the student dashboard with upcoming events,
 * dynamic search functionality and a buddy group summary.
 */
function App() {
  const [searchQuery, setSearchQuery] = useState<string>("");

  const filteredEvents = mockEvents.filter((event) =>
    event.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <>
      <Navbar />

      <main className="main-container">

        {/* Welcome section */}
        <section className="welcome-section">
          <h2>Find your people before the event starts.</h2>
          <p>Discover events and meet your new buddies.</p>
        </section>

        {/* Student dashboard layout */}
        <div className="dashboard-layout">

          {/* Left section: Upcoming events */}
          <section className="events-section">
            <h2>Upcoming events</h2>

            <div className="search-toolbar">
              <input
                type="search"
                className="search-input"
                aria-label="Search events"
                placeholder="Search events..."
                value={searchQuery}
                onChange={(event) =>
                  setSearchQuery(event.target.value)
                }
              />

              <button
                type="button"
                className="secondary-button"
                onClick={() => setSearchQuery("")}
              >
                Clear
              </button>
            </div>

            <p className="event-count">
              Showing {filteredEvents.length} of {mockEvents.length} events
            </p>

            {filteredEvents.length === 0 && (
              <p>No events found.</p>
            )}

            <div className="event-list">
              {filteredEvents.map((event) => (
                <EventCard
                  key={event.id}
                  title={event.title}
                  date={event.date}
                  location={event.location}
                />
              ))}
            </div>
          </section>

          {/* Right section: Buddy group summary */}
          <div className="dashboard-sidebar">
            <GroupSummary
              eventTitle="Winter Social"
              members={['Sara', 'Tom', 'Aisha']}
            />
          </div>

        </div>
      </main>
    </>
  );
}

export default App;
