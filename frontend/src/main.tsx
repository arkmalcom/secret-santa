import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import App from './App.tsx';
import List from './List.tsx';

function Main() {
  return (
    <Router> {/* Make sure Router is wrapping your Routes */}
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/list/:listId" element={<List />} />
      </Routes>
    </Router>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Main />
  </React.StrictMode>
);
