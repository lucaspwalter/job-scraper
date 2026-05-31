import { useState } from "react";

import Jobs from "./pages/Jobs.jsx";
import Sources from "./pages/Sources.jsx";

export default function App() {
  const [page, setPage] = useState("sources");

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <h1>Job Scraper</h1>
          <p>Monitoramento de vagas por source.</p>
        </div>
        <nav>
          <button className={page === "sources" ? "active" : ""} onClick={() => setPage("sources")}>
            Sources
          </button>
          <button className={page === "jobs" ? "active" : ""} onClick={() => setPage("jobs")}>
            Jobs
          </button>
        </nav>
      </aside>
      <main>{page === "sources" ? <Sources /> : <Jobs />}</main>
    </div>
  );
}
