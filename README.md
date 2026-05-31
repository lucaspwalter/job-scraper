# Job Scraper

## O que o projeto faz

Job Scraper monitora vagas remotas pela API publica da Remotive a partir de fontes configuradas, salva vagas novas em PostgreSQL, evita duplicatas por URL e envia notificacoes por email. O WhatsApp via Evolution API e opcional.

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- APScheduler
- smtplib
- React
- Axios

## Como configurar o email

- Crie uma senha de app do Gmail em https://myaccount.google.com/apppasswords
- Copie `backend/.env.example` para `backend/.env`
- Preencha:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu@gmail.com
SMTP_PASSWORD=sua-senha-de-app
NOTIFY_EMAIL=destino@gmail.com
```

## WhatsApp opcional

O envio por WhatsApp usa Evolution API. Ele so roda quando todas as variaveis abaixo estiverem preenchidas:

```env
EVOLUTION_API_URL=
EVOLUTION_API_KEY=
EVOLUTION_INSTANCE=
NOTIFY_PHONE=
```

Se alguma variavel estiver vazia, o sistema ignora o WhatsApp silenciosamente e continua tentando email.

## Como rodar localmente

Suba o banco com Docker:

```bash
docker run --name jobscraper-db \
  -e POSTGRES_USER=jobscraper \
  -e POSTGRES_PASSWORD=jobscraper \
  -e POSTGRES_DB=jobscraper \
  -p 5432:5432 \
  -d postgres:16
```

Configure o backend:

```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
python seed.py
python main.py
```

Rode o frontend:

```bash
cd frontend
npm install
npm start
```

Abra:

- Frontend: http://localhost:5173
- API: http://localhost:8000

## Endpoints

- `POST /sources`
- `GET /sources`
- `PUT /sources/{id}`
- `DELETE /sources/{id}`
- `GET /jobs`
- `GET /jobs?source_id={id}`
- `DELETE /jobs/{id}`
- `POST /scheduler/run`
- `GET /scheduler/status`
