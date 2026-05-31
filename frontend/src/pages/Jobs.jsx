import { useEffect, useState } from "react";

import api from "../api.js";

export default function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [sources, setSources] = useState([]);
  const [sourceId, setSourceId] = useState("");

  async function loadSources() {
    const response = await api.get("/sources");
    setSources(response.data);
  }

  async function loadJobs(selectedSourceId = sourceId) {
    const response = await api.get("/jobs", {
      params: selectedSourceId ? { source_id: selectedSourceId } : {},
    });
    setJobs(response.data);
  }

  useEffect(() => {
    loadSources();
    loadJobs("");
  }, []);

  async function updateFilter(value) {
    setSourceId(value);
    await loadJobs(value);
  }

  async function removeJob(id) {
    await api.delete(`/jobs/${id}`);
    loadJobs();
  }

  return (
    <section className="page">
      <div className="page-header">
        <div>
          <h2>Jobs</h2>
          <span>{jobs.length} vagas encontradas</span>
        </div>
        <select value={sourceId} onChange={(event) => updateFilter(event.target.value)}>
          <option value="">Todas as sources</option>
          {sources.map((source) => (
            <option key={source.id} value={source.id}>
              {source.name}
            </option>
          ))}
        </select>
      </div>

      <div className="panel table-panel">
        <table>
          <thead>
            <tr>
              <th>Titulo</th>
              <th>Empresa</th>
              <th>Link</th>
              <th>Data</th>
              <th>Notificacao</th>
              <th>Acoes</th>
            </tr>
          </thead>
          <tbody>
            {jobs.map((job) => (
              <tr key={job.id}>
                <td>{job.title}</td>
                <td>{job.company || "Nao informada"}</td>
                <td>
                  <a href={job.url} target="_blank" rel="noreferrer">
                    Abrir vaga
                  </a>
                </td>
                <td>{new Date(job.found_at).toLocaleString("pt-BR")}</td>
                <td>
                  <span className={job.notified ? "badge success" : "badge muted"}>
                    {job.notified ? "Notificado" : "Pendente"}
                  </span>
                </td>
                <td className="actions">
                  <button className="danger" onClick={() => removeJob(job.id)}>
                    Excluir
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
