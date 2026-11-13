# 🎮 Game Catalog — Catálogo de Videojogos

## 📌 Sobre o projeto

O **Game Catalog — Catálogo de Videojogos** é uma aplicação web desenvolvida no âmbito de um projeto de formação, com o objetivo de gerir, organizar e consultar informações sobre videojogos num único local.

A aplicação permite criar e gerir uma coleção de videojogos, consultar os seus detalhes, organizar os jogos por género e acompanhar os títulos favoritos.

## 🎯 Objetivos

- Organizar informações sobre videojogos.
- Permitir adicionar, consultar, editar e eliminar videojogos.
- Associar vários géneros a um videojogo.
- Pesquisar e filtrar jogos.
- Consultar estatísticas do catálogo.
- Gerir uma lista de videojogos favoritos.
- Utilizar uma base de dados relacional para guardar a informação.

## 🛠️ Tecnologias utilizadas

- **Python** — linguagem de programação principal.
- **FastAPI** — desenvolvimento da aplicação web.
- **SQLite** — armazenamento dos dados.
- **HTML** — estrutura das páginas web.
- **CSS** — apresentação visual das páginas.
- **Jinja2** — integração de dados nas páginas HTML.
- **Pytest** — realização de testes.
- **Git e GitHub** — controlo de versões e alojamento do código-fonte.

## ⚙️ Funcionalidades implementadas

1. **Página inicial** — apresentação e acesso às principais áreas da aplicação.
2. **Gestão de videojogos** — adicionar, consultar, editar e eliminar jogos.
3. **Capas dos videojogos** — carregamento e apresentação de imagens.
4. **Pesquisa e filtros** — pesquisa por título e filtragem por ano e género.
5. **Gestão de géneros** — associação de géneros aos videojogos.
6. **Estatísticas** — consulta do número total de jogos e distribuição por décadas.
7. **Sistema de favoritos** — adicionar e retirar jogos dos favoritos.
8. **Página de favoritos** — consulta dos videojogos favoritos.
9. **Página de detalhes** — apresentação individual da informação de cada videojogo.
10. **Ordenação** — organização por título (A-Z e Z-A) e por ano de lançamento.

## 🗄️ Base de dados

É utilizada a base de dados **SQLite** para guardar as informações do catálogo.

O modelo de dados inclui as seguintes entidades e tabelas:

- **JOGO** — informações dos videojogos.
- **GENERO** — géneros dos videojogos.
- **PLATAFORMA** — plataformas associadas aos videojogos.
- **JOGO_GENERO** — associação entre videojogos e géneros.
- **JOGO_PLATAFORMA** — associação entre videojogos e plataformas.
- **JOGO_FAVORITO** — registo dos videojogos favoritos.

Um videojogo pode estar associado a vários géneros e plataformas.

## 🏗️ Organização do projeto

A aplicação está organizada por responsabilidades, separando a interface, a lógica de negócio e o acesso aos dados.

Principais elementos:

- `app/main.py` — rotas e funcionamento principal da aplicação.
- `app/repositorio.py` — operações de acesso à base de dados.
- `app/services/jogos.py` — lógica de negócio e validações.
- `app/database/` — configuração e inicialização da base de dados.
- `app/templates/` — páginas HTML da aplicação.
- `app/static/` — ficheiros CSS e capas dos videojogos.
- `registo_desenvolvimento.md` — histórico do desenvolvimento do projeto.

## 🚀 Instalação e execução

### 1. Clonar o repositório

```bash
git clone https://github.com/eduardomoreira47/catalogo-videojogos.git
```

### 2. Entrar na pasta do projeto

```bash
cd catalogo-videojogos
```

### 3. Criar um ambiente virtual

```bash
python -m venv .venv
```

### 4. Ativar o ambiente virtual

No Windows, utilizando Git Bash:

```bash
source .venv/Scripts/activate
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Iniciar a aplicação

```bash
python -m uvicorn app.main:app --reload
```

### 7. Abrir no navegador

Aceder ao endereço:

http://127.0.0.1:8000

## 🚧 Estado do projeto

**Em desenvolvimento.**

A aplicação já disponibiliza várias funcionalidades de gestão e consulta de videojogos. Continuam previstas melhorias e novas funcionalidades.

## 🎓 Contexto de desenvolvimento

Projeto desenvolvido no âmbito das **UFCD 5425 e 10790**, com o objetivo de aplicar conhecimentos de programação, bases de dados, desenvolvimento web, testes e controlo de versões.

## 👨‍💻 Repositório

O código-fonte está disponível no GitHub:

[Catálogo de Videojogos — Repositório GitHub](https://github.com/eduardomoreira47/catalogo-videojogos)