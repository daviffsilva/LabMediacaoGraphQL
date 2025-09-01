# LAB01 — Relatório: Características de repositórios populares

## Introdução

Objetivo: caracterizar 1.000 repositórios open‑source mais estrelados do GitHub e responder às RQs por estatísticas de tendência central (mediana). Hipóteses informais: (H1) repositórios populares tendem a ser maduros; (H2) recebem muitas contribuições externas; (H3) lançam releases com frequência; (H4) são atualizados continuamente; (H5) concentram‑se em linguagens populares; (H6) mantêm alta taxa de issues fechadas. Para bônus, (H7) linguagens mais populares favorecem mais PRs, mais releases e atualizações mais recentes.

## Metodologia

- Fonte: CSV com 1.000 repositórios mais estrelados; campos utilizados: createdDate, updatedDate, primaryLanguage, mergedPRs, releases, issuesTotal, issuesClosed, stargazers.

- Derivados: idade (anos) = hoje − createdDate; recência de atualização (dias) = hoje − updatedDate; razão de issues fechadas = issuesClosed/issuesTotal.

- Estatística: mediana por RQ; contagem por categoria para linguagem. Data da análise: 2025‑08‑31.

- Diretrizes do enunciado seguidas conforme documento do laboratório.

## Resultados e Discussão

**RQ01. Sistemas populares são maduros/antigos?**

Mediana da idade: **8.32 anos**. Interpretação: confirma (H1). Repositórios populares tendem a ser de longa duração.

**RQ02. Sistemas populares recebem muita contribuição externa?**

Mediana de PRs aceitas: **708**. Interpretação: confirma (H2). Volume elevado de PRs aceitas.

**RQ03. Sistemas populares lançam releases com frequência?**

Mediana de releases: **36**. Interpretação: apoia (H3). Cadência de versões substantiva.

**RQ04. Sistemas populares são atualizados com frequência?**

Mediana de dias desde a última atualização: **1 dia(s)**. Interpretação: confirma (H4). Atualização praticamente contínua.

**RQ05. Sistemas populares são escritos nas linguagens mais populares?**

Top‑10 linguagens por contagem:

| primaryLanguage   |   count |
|:------------------|--------:|
| Python            |     191 |
| TypeScript        |     156 |
| JavaScript        |     129 |
| Unknown           |     103 |
| Go                |      73 |
| Java              |      50 |
| C++               |      47 |
| Rust              |      45 |
| C                 |      25 |
| Jupyter Notebook  |      22 |


Interpretação: confirma (H5). Python, TypeScript e JavaScript dominam; Go, Java, C++ e Rust seguem fortes. ‘Unknown’ agrega repositórios sem linguagem principal definida (monorepos/poliglotas).

**RQ06. Sistemas populares possuem alto percentual de issues fechadas?**

Mediana da razão issues fechadas/total: **86.8%**. Interpretação: confirma (H6). Gestão de issues madura.

**RQ07 (Bônus). Por linguagem: PRs, releases e recência de atualização**

Medianas por linguagem (apenas linguagens com ≥ 30 repositórios):

| primaryLanguage   |   repos |   mergedPRs_median |   releases_median |   days_since_update_median |
|:------------------|--------:|-------------------:|------------------:|---------------------------:|
| Python            |     191 |              576   |              24   |                          0 |
| TypeScript        |     156 |             2134.5 |             148.5 |                          0 |
| JavaScript        |     129 |              553   |              33   |                          1 |
| Unknown           |     103 |              129   |               0   |                          1 |
| Go                |      73 |             1692   |             124   |                          1 |
| Java              |      50 |              650.5 |              42.5 |                          1 |
| C++               |      47 |              934   |              56   |                          1 |
| Rust              |      45 |             2176   |              79   |                          0 |


Síntese: TypeScript, Go e Rust exibem medianas elevadas de PRs e releases e medianas de recência próximas de 0–1 dia, sugerindo forte intensidade de contribuição e entrega contínua. Python e JavaScript mantêm alta atividade absoluta, porém com medianas de PRs/releases inferiores às de TypeScript/Go/Rust, possivelmente por ecossistemas fragmentados e múltiplos subprojetos. ‘Unknown’ e Jupyter Notebook apresentam baixas medianas de PRs e releases, condizentes com naturezas de código exemplo/ciência de dados e monorepos.

## Limitações

- Idades e recência calculadas em relação à data da análise; não refletem exatamente a data de coleta original.

- Métricas agregadas por mediana; não capturam caudas longas típicas de repos extremamente populares.

- ‘Unknown’ pode distorcer distribuição por linguagem devido a setups monorepo.
