
/**
 * Student buddy groups screen.
 */

import GroupSummary from '../components/GroupSummary';

/**
 * Displays the student's current buddy group.
 */
function MyGroupsPage() {
  return (
    <main className="main-container">

      <section className="welcome-section">
        <h2>My groups</h2>
        <p>Meet your new buddies before the event starts.</p>
      </section>

      <GroupSummary
        eventTitle="Winter Social"
        members={['Sara', 'Tom', 'Aisha']}
        showViewLink={false}
      />

    </main>
  );
}

export default MyGroupsPage;
