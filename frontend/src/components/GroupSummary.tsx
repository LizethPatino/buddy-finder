/**
 * Displays a summary of the student's matched buddy group
 * on the desktop dashboard.
 */

import './GroupSummary.css'
import { Link } from 'react-router';

interface GroupSummaryProps {
  eventTitle: string;
  members: string[];
  showViewLink?: boolean;
}

/**
 * Renders group members and a preview of the matched group.
 */
function GroupSummary({
  eventTitle,
  members,
  showViewLink = true,
}: GroupSummaryProps) {
  return (
    <aside
      className="group-summary"
      aria-labelledby="group-summary-title"
    >
      <h2
        id="group-summary-title"
        className="group-summary-heading"
      >
        Your group
      </h2>

      <div className="group-summary-content">
        {members.length > 0 ? (
          <>
            <span className="group-status">
              Group ready
            </span>

            <div
              className="group-avatars"
              aria-hidden="true"
            >
              {members.map((member, index) => (
                <div
                  key={`${member}-${index}`}
                  className={`group-avatar avatar-${index % 3}`}
                >
                  {member.charAt(0).toUpperCase()}
                </div>
              ))}
            </div>

            <h3 className="group-member-names">
              {members.join(', ')}
            </h3>

            <p className="group-event-title">
              {eventTitle}
            </p>

            {/* <button
              className="group-view-button"
              type="button"
              disabled
            >
              See my group
            </button> */}
            
            {showViewLink && (
                <Link
                    to="/groups"
                    className="group-view-button"
                >
                    See my group
                </Link>
            )}

          </>
        ) : (
          <p className="group-empty-message">
            You haven't joined a buddy group yet.
            Find an upcoming event to get started.
          </p>
        )}
      </div>
    </aside>
  )
}

export default GroupSummary