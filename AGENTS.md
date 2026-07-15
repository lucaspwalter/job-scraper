# Job Scraper para Codex

## Objetivo

Este repositório combina monitor de vagas com workflows do Codex para pesquisar vagas, avaliar compatibilidade, adaptar documentos e preparar entrevistas.

## Configuração

Perfil, localização, experiência e preferências são dados locais. Execute `$setup` no Codex para preencher os arquivos de perfil. Nunca versione CVs, cartas geradas, documentos, credenciais, banco SQLite ou histórico de candidaturas.

## Fluxo

1. `$setup`: cria perfil local.
2. `$scrape`: busca e organiza vagas.
3. `$rank`: classifica vagas.
4. `$apply <URL>`: avalia vaga e gera documentos.
5. `$interview`: prepara entrevista.

## Segurança

- Não inventar experiência, formação ou habilidades.
- Manter dados pessoais somente nos caminhos ignorados pelo Git.
- Confirmar antes de enviar candidatura ou mensagem externa.
