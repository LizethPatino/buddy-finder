/**
 * Displays a summary of the student's matched buddy group
 * on the desktop dashboard.
 */

import './GroupSummary.css'

interface GroupSummaryProps {
  eventTitle: string
  members: string[]
}

/**
 * Renders group members and a preview of the matched group.
 */
function GroupSummary({
  eventTitle,
  members,
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

            <button
              className="group-view-button"
              type="button"
              disabled
            >
              See my group
            </button>
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