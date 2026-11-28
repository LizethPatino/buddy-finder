
/**
 * Root component of Buddy Finder.
 * Defines application routes and shared page layouts.
 */

import { Routes, Route, Navigate, Outlet } from 'react-router';

import Navbar from './components/Navbar';
import EventsPage from './pages/EventsPage';
import EventDetailsPage from './pages/EventDetailsPage';
import MyGroupsPage from './pages/MyGroupsPage';
import ProfilePage from './pages/ProfilePage';

import './App.css';

/**
 * Shared layout for student-facing pages.
 * Keeps the navigation bar visible across screens.
 */
function StudentLayout() {
  return (
    <>
      <Navbar />
      <Outlet />
    </>
  );
}

/**
 * Defines the navigation destinations of the application.
 */
function App() {
  return (
    <Routes>

      <Route element={<StudentLayout />}>

        <Route
          index
          element={<Navigate to="/events" replace />}
        />

        <Route
          path="events"
          element={<EventsPage />}
        />

        <Route
          path="events/:eventId"
          element={<EventDetailsPage />}
        />

        <Route
          path="groups"
          element={<MyGroupsPage />}
        />

        <Route
          path="profile"
          element={<ProfilePage />}
        />

        <Route
          path="*"
          element={<Navigate to="/events" replace />}
        />

      </Route>

    </Routes>
  );
}

export default App;
