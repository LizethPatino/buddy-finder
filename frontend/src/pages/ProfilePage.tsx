
/**
 * Student profile screen.
 */

import { Link } from 'react-router';

/**
 * Displays student profile information.
 */
function ProfilePage() {
  return (
    <main className="main-container">

      <section className="welcome-section">
        <h2>My profile</h2>
        <p>Manage your Buddy Finder account.</p>
      </section>

      <section className="page-panel">
        <h3>Account information</h3>
        <p>
          Your profile information will appear here
          after authentication is implemented.
        </p>

        <Link to="/events" className="back-link">
             ← Back to events
        </Link>
      </section>

    </main>
  );
}

export default ProfilePage;
