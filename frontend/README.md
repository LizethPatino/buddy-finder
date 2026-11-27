# Buddy Finder — Frontend

Responsive web interface for Buddy Finder, developed as part of the ECS781P Cloud Computing group project at Queen Mary University of London.

## Technology Stack

- React
- TypeScript
- Vite
- CSS (Flexbox, with CSS Grid planned)
- ESLint

## Local Development

### Prerequisites

- Node.js
- npm

### Getting Started

From the repository root:

```bash
cd frontend
npm ci
npm run dev
```

Open http://localhost:5173 in your browser.

## Available Commands

| Command | Description |
|---|---|
| `npm run dev` | Start the development server |
| `npm run build` | Type-check and generate the production build |
| `npm run lint` | Run ESLint checks |
| `npm run preview` | Preview the production build |

## Project Structure

- `src/components/` — Reusable UI components.
- `src/data/` — Temporary mock data for frontend development.
- `src/types/` — TypeScript data models.
- `src/App.tsx` — Root application component.
- `src/App.css` — Component and layout styling.
- `src/index.css` — Global styles and design tokens.
- `src/main.tsx` — React application entry point.

## Current Implementation

- Reusable navigation bar.
- Reusable event cards.
- Dynamic event rendering.
- Event search and filtering.
- Global design tokens.
- Flexbox-based adaptive layouts.

## Planned Features

- Responsive desktop and mobile layouts.
- Authentication screens.
- Student and staff dashboards.
- Interest selection and buddy group management.
- Flask REST API integration.

## Development Notes

The frontend currently uses mock event data. Authentication, navigation and group matching are not yet connected to the backend.

The production build is generated in `dist/`. Generated files, installed dependencies and environment secrets must not be committed to the repository.

Refer to the root README, CONTRIBUTING.md and docs/api.md for project-wide architecture, contribution guidelines and API contracts.