<p align="center">
  <img src="assets/mascot/pip_flight_loop.gif" alt="Job Scraper mascot" width="200">
</p>

# Raspador de Trabalho

Plataforma de monitoramento de trabalho local com backend FastAPI, frontend React e fluxos de trabalho OpenAI Codex.

## Visão geral

O Job Scraper centraliza fontes, coleta listas de empregos, evita duplicatas e oferece suporte à avaliação, inscrições e preparação para entrevistas.

Adaptação independente do Codex; não é afiliado nem mantido pela OpenAI. Os fluxos de trabalho de aplicativos são baseados no projeto `ai-job-search` de Mads Lorentzen, licenciado pelo MIT.

## Características

- O backend consulta fontes configuradas, normaliza listagens e armazena dados em PostgreSQL com Docker ou SQLite em modo manual.
- O frontend permite aos usuários gerenciar fontes e visualizar resultados.
- O agendador executa pesquisas periódicas.
- E-mail e WhatsApp são opcionais e permanecem desativados sem credenciais.
- `.agents/skills/` contém fluxos de trabalho do Codex, incluindo `$setup`, `$scrape`, `$rank`, `$apply` e `$interview`.

## Pilha de tecnologia

- Python e FastAPI
- Reagir
- PostgreSQL com Docker
- SQLite para configuração local manual
- Docker Compor
- Fluxos de trabalho do OpenAI Codex

## Começando

### Docker — recomendado

Requisitos: Git e Docker Desktop/Engine com Compose.

```bash
git clone https://github.com/lucaspwalter/job-scraper.git
cd job-scraper
docker compose up --build
```

Abrir:

- Interface: http://localhost:5173
- API: http://localhost:8000
- API documentation: http://localhost:8000/docs

Para parar:

```bash
docker compose down
```

### Configuração manual — Linux/macOS

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

### Configuração manual — Windows PowerShell

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

Se o PowerShell bloquear a ativação do ambiente, execute isto uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Usando com Codex

Da raiz do projeto:

```bash
codex
```

Então execute `$setup`. Os dados pessoais gerados são ignorados pelo Git. Comandos principais:

- `$scrape`: busca por empregos.
- `$rank`: classifica os resultados.
- `$apply <URL>`: avalia um trabalho e prepara uma aplicação.
- `$entrevista`: prepara-se para uma entrevista.

## Configuração opcional

Edite `backend/.env` para ativar notificações. As variáveis ​​`SMTP_*`, `EVOLUTION_*` e `NOTIFY_*` podem permanecer vazias.

## Dados privados

Não publique `.env`, bancos de dados SQLite, currículos pessoais, cartas de apresentação geradas, documentos, rastreadores ou resultados de pesquisa. `.gitignore` já protege esses caminhos.

## Testes

```bash
python3 -m unittest discover -s tests
```

## Licença

MIT. Veja `LICENÇA`.
