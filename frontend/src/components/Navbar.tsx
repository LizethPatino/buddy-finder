/**
 * Navigation bar for the Buddy Finder application.
 */

import './Navbar.css';

/**
 * Displays the application brand and navigation menu.
 */
function Navbar() {
  return (
    <header className="app-header">
      <div className="header-content">

        <div className="brand">
          <div className="brand-logo" aria-hidden="true">
            <span className="logo-circle teal"></span>
            <span className="logo-circle purple"></span>
            <span className="logo-circle pink"></span>
          </div>

          <h1>Buddy Finder</h1>
        </div>

        <nav className="navigation" aria-label="Main navigation">
          <button type="button">Events</button>
          <button type="button">My Groups</button>
          <button type="button">Profile</button>
        </nav>

      </div>
    </header>
  );
}

export default Navbar;