import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import App from "./App.tsx";
import List from "./List.tsx";
import Pair from "./Pair.tsx";

function Main() {
  return (
    <Router basename="/secret-santa/">
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/list/:listId" element={<List />} />
        <Route path="/pair/:listId" element={<Pair />} />
      </Routes>
    </Router>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Main />
  </React.StrictMode>,
);
