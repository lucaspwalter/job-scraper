<p align="center">
  <img src="assets/mascot/pip_flight_loop.gif" alt="Mascote do Job Scraper" width="200">
</p>

# Job Scraper

Monitor local de vagas com backend FastAPI, frontend React e workflows para OpenAI Codex. Projeto feito para centralizar fontes, coletar vagas, evitar duplicatas e apoiar avaliação, candidatura e preparação para entrevistas.

Adaptação independente para Codex; não afiliada nem mantida pela OpenAI. Workflows de candidatura baseados no projeto `ai-job-search`, de Mads Lorentzen, sob licença MIT.

## Como funciona

- Backend consulta fontes configuradas, normaliza vagas e salva dados em PostgreSQL no Docker ou SQLite no modo manual.
- Frontend permite gerenciar fontes e visualizar resultados.
- Agendador executa buscas periódicas.
- Email e WhatsApp são opcionais e ficam desativados sem credenciais.
- `.agents/skills/` contém workflows usados pelo Codex, incluindo `$setup`, `$scrape`, `$rank`, `$apply` e `$interview`.

## Rodar com Docker — recomendado

Pré-requisitos: Git e Docker Desktop/Engine com Compose.

```bash
git clone https://github.com/lucaspwalter/job-scraper.git
cd job-scraper
docker compose up --build
```

Acesse:

- Interface: http://localhost:5173
- API: http://localhost:8000
- Documentação da API: http://localhost:8000/docs

Parar:

```bash
docker compose down
```

## Rodar manualmente — Linux/macOS

Requer Python 3.10+ e Node.js 20+.

Terminal 1:

```bash
cd backend
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 seed.py
python3 main.py
```

Terminal 2:

```bash
cd frontend
npm install
npm start
```

## Rodar manualmente — Windows PowerShell

Terminal 1:

```powershell
Set-Location backend
Copy-Item .env.example .env
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py seed.py
py main.py
```

Terminal 2:

```powershell
Set-Location frontend
npm install
npm start
```

Se PowerShell bloquear ativação do ambiente, execute uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Usar com Codex

Na raiz do projeto:

```bash
codex
```

Depois execute `$setup`. Dados pessoais gerados ficam ignorados pelo Git. Principais comandos:

- `$scrape`: busca vagas.
- `$rank`: classifica resultados.
- `$apply <URL>`: avalia vaga e prepara candidatura.
- `$interview`: prepara entrevista.

## Configuração opcional

Edite `backend/.env` para notificações. Variáveis `SMTP_*`, `EVOLUTION_*` e `NOTIFY_*` podem permanecer vazias.

## Dados privados

Não publique `.env`, banco SQLite, CVs pessoais, cartas geradas, documentos, rastreadores ou resultados de busca. `.gitignore` já protege esses caminhos.

## Testes

```bash
python3 -m unittest discover -s tests
```

## Licença

MIT. Veja `LICENSE`.
