/**
 * Entry point of the Buddy Finder frontend.
 * Initialises React and mounts the root application component
 * into the browser's DOM.
 */

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)