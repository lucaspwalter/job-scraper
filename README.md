# Job Scraper

## O que é

Acompanhar vagas manualmente em vários sites é trabalhoso, repetitivo e aumenta a chance de perder oportunidades novas. Quando a busca depende de abrir páginas todos os dias, comparar resultados e lembrar o que já foi visto, o processo fica pouco confiável.

Job Scraper automatiza esse acompanhamento. O projeto monitora fontes configuráveis, identifica vagas novas por URL única, salva o histórico em banco de dados e envia notificações quando encontra uma oportunidade ainda não registrada.

## Portfólio

Este projeto faz parte do meu portfólio:

https://lucaspwalter.github.io/portfolio/

## Como funciona

- Monitoramento de fontes de vagas configuráveis com intervalo por fonte
- Detecção automática de vagas novas por URL única
- Notificação por email via SMTP ao encontrar vaga nova
- Notificação opcional via WhatsApp com Evolution API
- Interface web para gerenciar fontes e visualizar histórico de vagas

## Notificações por email

- Usa smtplib nativo do Python, sem dependência externa
- Requer conta Gmail com senha de app
- Link para criar senha de app: https://myaccount.google.com/apppasswords

## Notificações WhatsApp

- Opcional — só funciona se Evolution API estiver configurada
- Documentação: https://doc.evolution-api.com

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- APScheduler
- React

## Como rodar localmente

As instruções completas de instalação e execução estão disponíveis na página do projeto no portfólio:

https://lucaspwalter.github.io/portfolio/

## Estrutura do projeto

```text
job-scraper/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── jobs.py
│   │   │   ├── scheduler.py
│   │   │   └── sources.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── job.py
│   │   │   └── source.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── detector.py
│   │   │   ├── notifier.py
│   │   │   └── scraper.py
│   │   └── scheduler.py
│   ├── .env.example
│   ├── clean_jobs.py
│   ├── main.py
│   ├── requirements.txt
│   ├── reset_sources.py
│   └── seed.py
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Jobs.jsx
│   │   │   └── Sources.jsx
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── index.html
│   ├── package-lock.json
│   └── package.json
├── .gitignore
└── README.md
```
