/**
 * Temporary event data for frontend development.
 * Will be replaced by responses from the Flask REST API.
 */

import type { BuddyEvent } from '../types/event';

export const mockEvents: BuddyEvent[] = [
  {
    id: 1,
    title: "Winter Social",
    date: "4 December 2026",
    location: "Students' Union"
  },
  {
    id: 2,
    title: "Charity Football",
    date: "5 December 2026",
    location: "Mile End Campus"
  },
  {
    id: 3,
    title: "Jazz Society Live",
    date: "7 December 2026",
    location: "The Griff Inn"
  },
  {
    id: 4,
    title: "End of Term Quiz",
    date: "9 December 2026",
    location: "Students' Union"
  }
];