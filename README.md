# 🎮 Game Catalog — Catálogo de Videojogos

## 📌 Sobre o projeto

O **Game Catalog — Catálogo de Videojogos** é uma aplicação web desenvolvida no âmbito da formação, com o objetivo de gerir, organizar e consultar informações sobre videojogos num único local.

O catálogo contém 150 videojogos e permite consultar os seus dados, capas, géneros, plataformas e anos de lançamento.

## 🎯 Objetivos

- Organizar informações sobre videojogos.
- Permitir adicionar, consultar, editar e eliminar videojogos.
- Associar vários géneros e plataformas a cada jogo.
- Pesquisar e filtrar jogos.
- Consultar estatísticas do catálogo.
- Gerir uma lista de videojogos favoritos.
- Utilizar uma base de dados relacional para guardar a informação.
- Aplicar boas práticas de organização e separação do código.

## 🛠️ Tecnologias utilizadas

- **Python** — linguagem de programação principal.
- **FastAPI** — desenvolvimento da aplicação web.
- **SQLite** — armazenamento dos dados.
- **HTML** — estrutura das páginas web.
- **CSS** — apresentação visual das páginas.
- **Jinja2** — integração de dados nas páginas HTML.
- **Pytest** — realização de testes automatizados.
- **Git e GitHub** — controlo de versões e alojamento do código-fonte.

## ⚙️ Funcionalidades implementadas

1. **Página inicial** — apresentação e acesso às principais áreas da aplicação.
2. **Gestão de videojogos** — adicionar, consultar, editar e eliminar jogos.
3. **Capas dos videojogos** — carregamento e apresentação de imagens.
4. **Pesquisa** — pesquisa de videojogos pelo título.
5. **Filtros** — filtragem por ano de lançamento, género e plataforma.
6. **Géneros** — associação de vários géneros a cada videojogo.
7. **Plataformas** — associação de várias plataformas a cada videojogo.
8. **Estatísticas** — consulta do número total de jogos e distribuição por décadas.
9. **Sistema de favoritos** — adicionar e retirar jogos dos favoritos.
10. **Página de favoritos** — consulta dos videojogos favoritos.
11. **Página de detalhes** — apresentação individual da informação de cada videojogo.
12. **Ordenação** — organização por título (A-Z e Z-A) e por ano de lançamento.

## 🗄️ Base de dados

A aplicação utiliza **SQLite** para guardar as informações do catálogo.

O modelo de dados é composto por seis tabelas:

| Tabela | Descrição |
|---|---|
| `JOGO` | Informações dos videojogos |
| `GENERO` | Géneros dos videojogos |
| `PLATAFORMA` | Plataformas disponíveis |
| `JOGO_GENERO` | Associação entre jogos e géneros |
| `JOGO_PLATAFORMA` | Associação entre jogos e plataformas |
| `JOGO_FAVORITO` | Registo dos videojogos favoritos |

As tabelas de associação permitem que um videojogo tenha vários géneros e várias plataformas.

O projeto inclui um script SQL para criar a estrutura da base de dados:

`app/database/criar_base_dados.sql`

## 🏗️ Organização do projeto

A aplicação está organizada por responsabilidades, separando a interface, a lógica de negócio e o acesso aos dados.

Principais elementos:

- `app/main.py` — rotas e funcionamento principal da aplicação.
- `app/repositorio.py` — operações de acesso à base de dados.
- `app/services/jogos.py` — lógica de negócio e validações.
- `app/database/` — configuração, inicialização e script SQL da base de dados.
- `app/templates/` — páginas HTML da aplicação.
- `app/static/` — ficheiros CSS e capas dos videojogos.
- `dados/jogos.csv` — ficheiro com os dados dos videojogos.
- `tests/` — testes automatizados.
- `registo_desenvolvimento.md` — histórico do desenvolvimento do projeto.
- `requirements.txt` — dependências necessárias para executar a aplicação.

 Testes automatizados

O projeto utiliza Pytest para verificar algumas das principais operações do catálogo.

Foram realizados seis testes automatizados, que passaram com sucesso:

- Registo de um videojogo.
- Listagem dos videojogos.
- Pesquisa por título.
- Filtragem por ano.
- Edição de um videojogo.
- Eliminação de um videojogo.

Para executar os testes:


python -m pytest -v


 Instalação e execução

 1. Clonar o repositório


git clone https://github.com/eduardomoreira47/catalogo-videojogos.git


 2. Entrar na pasta do projeto


cd catalogo-videojogos


 3. Criar um ambiente virtual


python -m venv .venv313


 4. Ativar o ambiente virtual

No Windows, utilizando Git Bash:


source .venv313/Scripts/activate


 5. Instalar as dependências


pip install -r requirements.txt


 6. Iniciar a aplicação


python -m uvicorn app.main:app --reload


 7. Abrir no navegador

Aceder ao seguinte endereço:

http://127.0.0.1:8000

 📋 Estado do projeto

O projeto encontra-se numa fase avançada de desenvolvimento, disponibilizando funcionalidades de gestão, pesquisa, filtragem, organização e consulta de videojogos.

Foram também implementados testes automatizados e documentação técnica.

 🎓 Contexto de desenvolvimento

Projeto desenvolvido no âmbito da **UFCD 5425 — Projeto de Tecnologias e Programação de Sistemas de Informação**, com o objetivo de aplicar conhecimentos de programação, bases de dados, desenvolvimento web, testes e controlo de versões.

 👨‍💻 Repositório

O código-fonte está disponível no GitHub:

https://github.com/eduardomoreira47/catalogo-videojogos
