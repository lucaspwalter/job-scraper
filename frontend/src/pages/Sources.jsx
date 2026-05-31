import React from "react";
import { useEffect, useState } from "react";

import api from "../api.js";

const emptyForm = {
  name: "",
  search_term: "",
  url: "",
  interval_minutes: 30,
  is_active: true,
};

export default function Sources() {
  const [sources, setSources] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);

  async function loadSources() {
    const response = await api.get("/sources");
    setSources(response.data);
  }

  useEffect(() => {
    loadSources();
  }, []);

  function updateForm(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function editSource(source) {
    setEditingId(source.id);
    setForm({
      name: source.name,
      search_term: source.search_term,
      url: source.url,
      interval_minutes: source.interval_minutes,
      is_active: source.is_active,
    });
  }

  async function saveSource(event) {
    event.preventDefault();
    const payload = {
      ...form,
      interval_minutes: Number(form.interval_minutes),
      url: form.url || null,
    };

    if (editingId) {
      await api.put(`/sources/${editingId}`, payload);
    } else {
      await api.post("/sources", payload);
    }

    setForm(emptyForm);
    setEditingId(null);
    loadSources();
  }

  async function removeSource(id) {
    await api.delete(`/sources/${id}`);
    loadSources();
  }

  async function toggleSource(source) {
    await api.put(`/sources/${source.id}`, { is_active: !source.is_active });
    loadSources();
  }

  async function runNow() {
    setLoading(true);
    try {
      await api.post("/scheduler/run");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="page">
      <div className="page-header">
        <div>
          <h2>Sources</h2>
          <span>{sources.length} fontes configuradas</span>
        </div>
        <button onClick={runNow} disabled={loading}>
          {loading ? "Rodando..." : "Rodar agora"}
        </button>
      </div>

      <form className="panel source-form" onSubmit={saveSource}>
        <input
          placeholder="Nome"
          value={form.name}
          onChange={(event) => updateForm("name", event.target.value)}
          required
        />
        <input
          placeholder="Termo de busca"
          value={form.search_term}
          onChange={(event) => updateForm("search_term", event.target.value)}
          required
        />
        <input
          placeholder="URL customizada opcional"
          value={form.url}
          onChange={(event) => updateForm("url", event.target.value)}
        />
        <input
          type="number"
          min="1"
          value={form.interval_minutes}
          onChange={(event) => updateForm("interval_minutes", event.target.value)}
        />
        <label className="checkbox">
          <input
            type="checkbox"
            checked={form.is_active}
            onChange={(event) => updateForm("is_active", event.target.checked)}
          />
          Ativa
        </label>
        <button type="submit">{editingId ? "Salvar" : "Adicionar"}</button>
      </form>

      <div className="panel table-panel">
        <table>
          <thead>
            <tr>
              <th>Nome</th>
              <th>Termo</th>
              <th>Intervalo</th>
              <th>Status</th>
              <th>Acoes</th>
            </tr>
          </thead>
          <tbody>
            {sources.map((source) => (
              <tr key={source.id}>
                <td>{source.name}</td>
                <td>{source.search_term}</td>
                <td>{source.interval_minutes} min</td>
                <td>
                  <span className={source.is_active ? "badge success" : "badge muted"}>
                    {source.is_active ? "Ativa" : "Inativa"}
                  </span>
                </td>
                <td className="actions">
                  <button onClick={() => editSource(source)}>Editar</button>
                  <button onClick={() => toggleSource(source)}>
                    {source.is_active ? "Desativar" : "Ativar"}
                  </button>
                  <button className="danger" onClick={() => removeSource(source.id)}>
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
