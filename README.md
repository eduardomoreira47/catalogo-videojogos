# catalogo-videojogos
# 🎮 Catálogo de Videojogos

## 📌 Sobre o projeto

O **Catálogo de Videojogos** é uma aplicação web desenvolvida no âmbito de um projeto de formação, com o objetivo de gerir, organizar e consultar informações sobre videojogos num único local.

A aplicação permitirá organizar os jogos por género, plataforma e ano de lançamento, facilitando a pesquisa e a consulta das informações de cada videojogo.

## 🎯 Objetivos

- Organizar informações sobre videojogos.
- Permitir adicionar, consultar, editar e eliminar videojogos.
- Associar vários géneros a um videojogo.
- Associar várias plataformas a um videojogo.
- Pesquisar jogos pelo título.
- Filtrar os resultados por género, plataforma e ano de lançamento.
- Utilizar uma base de dados relacional para guardar a informação.

## 🛠️ Tecnologias utilizadas

O projeto será desenvolvido com as seguintes tecnologias:

- **Python** — linguagem de programação principal.
- **FastAPI** — desenvolvimento da aplicação web.
- **SQLite** — armazenamento dos dados.
- **HTML** — estrutura das páginas web.
- **CSS** — apresentação visual das páginas.
- **Jinja2** — integração de dados nas páginas HTML.
- **Pytest** — realização de testes.
- **Git e GitHub** — controlo de versões e alojamento do código-fonte.

## ⚙️ Funcionalidades previstas

A aplicação deverá permitir:

1. Registar novos videojogos.
2. Consultar os videojogos existentes.
3. Editar as informações dos videojogos.
4. Eliminar videojogos do catálogo.
5. Pesquisar videojogos pelo título.
6. Filtrar videojogos por género, plataforma e ano de lançamento.
7. Gerir os géneros e as plataformas associados aos videojogos.

## 🗄️ Base de dados

Será utilizada a base de dados **SQLite** para guardar as informações do catálogo.

O modelo de dados será organizado em três entidades principais:

- **Jogo** — contém as informações de cada videojogo, como título, descrição e ano de lançamento.
- **Género** — identifica os géneros dos videojogos.
- **Plataforma** — identifica as plataformas em que os videojogos estão disponíveis.

Um videojogo poderá estar associado a vários géneros e plataformas.

## 🏗️ Organização do projeto

A aplicação será desenvolvida com uma estrutura organizada por responsabilidades, separando a interface, a lógica de negócio e o acesso aos dados.

A estrutura será definida e desenvolvida progressivamente ao longo do projeto.

## 🚧 Estado do projeto

**Em desenvolvimento.**

Nesta fase inicial, o ambiente de desenvolvimento está configurado e a aplicação FastAPI já consegue ser executada localmente. As restantes funcionalidades serão implementadas progressivamente.

## 🎓 Contexto de desenvolvimento

Projeto desenvolvido no âmbito das UFCD 5425 e 10790, com o objetivo de aplicar conhecimentos de programação, bases de dados, desenvolvimento web, testes e controlo de versões.

## 👨‍💻 Repositório

O código-fonte do projeto está disponível no GitHub:

[Catálogo de Videojogos — Repositório GitHub](https://github.com/eduardomoreira47/catalogo-videojogos)