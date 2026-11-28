
/**
 * Navigation bar for the Buddy Finder application.
 */

import { NavLink } from 'react-router';
import './Navbar.css';

/**
 * Displays the application brand and responsive navigation menu.
 * Highlights the navigation item corresponding to the active route.
 */
function Navbar() {
  return (
    <header className="app-header">
      <div className="header-content">

        {/* Application branding */}
        <div className="brand">
          <div className="brand-logo" aria-hidden="true">
            <span className="logo-circle teal"></span>
            <span className="logo-circle purple"></span>
            <span className="logo-circle pink"></span>
          </div>

          <h1>Buddy Finder</h1>
        </div>

        {/* Responsive navigation */}
        <nav className="responsive-nav" aria-label="Main navigation">

          {/* Events */}
          <NavLink
            to="/events"
            className={({ isActive }) =>
              isActive ? 'nav-item nav-item-active' : 'nav-item'
            }
          >
            <svg
              width="22"
              height="22"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              aria-hidden="true"
            >
              <rect x="3" y="5" width="18" height="16" rx="2" />
              <path d="M16 3v4M8 3v4M3 10h18" />
            </svg>
            <span>Events</span>
          </NavLink>

          {/* My Groups */}
          <NavLink
            to="/groups"
            className={({ isActive }) =>
              isActive ? 'nav-item nav-item-active' : 'nav-item'
            }
          >
            <svg
              width="22"
              height="22"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              aria-hidden="true"
            >
              <circle cx="9" cy="8" r="3" />
              <path d="M3 20v-2a6 6 0 0 1 12 0v2" />
              <path d="M16 5a3 3 0 0 1 0 6M17 14a5 5 0 0 1 4 5v1" />
            </svg>
            <span>My Groups</span>
          </NavLink>

          {/* Profile */}
          <NavLink
            to="/profile"
            className={({ isActive }) =>
              isActive ? 'nav-item nav-item-active' : 'nav-item'
            }
          >
            <svg
              width="22"
              height="22"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              aria-hidden="true"
            >
              <circle cx="12" cy="8" r="4" />
              <path d="M4 21v-2a8 8 0 0 1 16 0v2" />
            </svg>
            <span>Profile</span>
          </NavLink>

        </nav>

      </div>
    </header>
  );
}

export default Navbar;
