# Atividades de Coleta e Persistência de Dados

Este repositório contém os trabalhos e projetos acadêmicos desenvolvidos para a disciplina de Coleta e Persistência de Dados. O projeto é dividido em duas áreas principais:

1.  **Coleta:** Scripts para extração de dados da web, tanto por meio de Web Scraping (raspagem de sites) quanto pelo consumo de APIs.
2.  **Persistência:** Uma série de programas em C e Python que comparam diferentes métodos de armazenamento de dados, desde arquivos de texto simples até bancos de dados SQL e NoSQL.

---

## 1. Coleta de Dados

Scripts localizados na pasta `coleta/`. Esta seção abrange desde scripts básicos de requisição até raspadores de dados específicos.

### Scripts Fundamentais

* `coleta_downloader_html.py`: Script básico que recebe uma URL, baixa o conteúdo HTML bruto e o imprime no terminal. É a base para todo web scraper.
* `coleta_cliente_api_json.py`: Script básico que recebe uma URL de API, baixa a resposta e a formata como um JSON legível.

### Web Scrapers (Raspagem de Dados)

* `coleta_g1_feed.py`: Script de Web Scraping que utiliza `requests` e `BeautifulSoup` para extrair os títulos e resumos das notícias do feed principal do G1.
* `coleta_g1_manchetes.py`: Script de Web Scraping focado em extrair apenas as manchetes principais do G1.
* `coleta_climatempo_rj.py`: Script de Web Scraping que busca as temperaturas mínimas e máximas para o Rio de Janeiro no site Climatempo.

### Consumo de API

* `coleta_api_taxa_cambio.py`: Script que consome a `ExchangeRate-API` para buscar e exibir taxas de câmbio em tempo real.

---

## 2. Persistência de Dados

Scripts localizados na pasta `persistencia/`. Esta seção compara diversas abordagens de armazenamento.

### Persistência em Python

* `persistencia_python_json.py`: Implementa um CRUD (Create, Read, Update, Delete) básico de alunos, persistindo os dados em um arquivo local `db.json`.
* `persistencia_python_sqlite.py`: Implementa um CRUD de alunos utilizando um banco de dados SQL embarcado (SQLite) através da biblioteca `sqlite3`.
* `persistencia_python_mongodb.py`: Implementa um CRUD de alunos utilizando um banco de dados NoSQL (MongoDB) através da biblioteca `pymongo`.

### Persistência em C (Comparativo de Métodos)

Quatro implementações de um CRUD de alunos em C, cada uma usando um método de persistência diferente:

* `persistencia_c_binario.c`: Salva os `structs` de alunos diretamente em um arquivo binário.
* `persistencia_c_texto.c`: Salva os dados em um arquivo de texto simples, usando `fprintf` e `fscanf`.
* `persistencia_c_csv.c`: Salva os dados em formato `.csv` (separado por vírgulas), permitindo nomes com espaços.
* `persistencia_c_sqlite.c`: Utiliza a biblioteca `sqlite3` para persistir os dados em um banco de dados SQL.

### Persistência em C (Comparativo de Organização de Arquivos)

Projeto localizado na subpasta `persistencia/comparacao_organizacao_arquivos_c/`.

Este projeto (`main.c`) compara a performance de escrita de três estratégias diferentes de organização de arquivos:

* `normal.h`: Append-only, simplesmente adiciona o novo registro ao final do arquivo (`alunos_normal.bin`).
* `sorted.h`: Mantém o arquivo (`alunos_sorted.bin`) sempre ordenado, recarregando, reordenando e reescrevendo o arquivo a cada nova inserção.
* `heap.h`: Mantém os dados no arquivo (`alunos_heap.bin`) organizados como uma Max-Heap.
