Registo de Desenvolvimento — Catálogo de Videojogos

Este ficheiro serve para registar o trabalho realizado em cada sessão de desenvolvimento do projeto.

Sessão 1 — Preparação do projeto
Trabalho realizado:

- Definição da ideia do projeto: desenvolver uma aplicação web para organizar e consultar videojogos.
- Definição das funcionalidades pretendidas: adicionar, consultar, editar e eliminar videojogos, pesquisar por título e filtrar por género, plataforma e ano de lançamento.
- Escolha das tecnologias: Python, FastAPI, SQLite, HTML, CSS, Jinja2, Pytest, Git e GitHub.
- Preparação da estrutura inicial do projeto e do ambiente virtual Python.
- Criação e configuração da aplicação FastAPI.
- Criação das pastas para templates, ficheiros estáticos, base de dados, serviços e testes.
- Criação da base de dados SQLite (catalogo.db).
- Criação das tabelas JOGO, GENERO, PLATAFORMA, JOGO_GENERO e JOGO_PLATAFORMA.
- Criação da função obter_conexao() para estabelecer ligação à base de dados.
- Criação da função criar_jogo() para guardar um videojogo na base de dados.
- Preparação da página inicial HTML com um formulário para registar videojogos.
- Configuração do FastAPI para apresentar a página HTML e receber os dados do formulário.
- Instalação das dependências necessárias, incluindo FastAPI, Uvicorn, Jinja2 e python-multipart.
Testes realizados
- Execução do script de criação das tabelas da base de dados.
- Arranque da aplicação web e abertura da página inicial no navegador.
- Submissão de um videojogo de teste através do formulário.
- Confirmação de que o videojogo foi guardado na base de dados SQLite.


Resultado confirmado:

Foi registado com sucesso o seguinte videojogo de teste:
- Título: Minecraft
- Descrição: Jogo de construção e exploração.
- Ano de lançamento: 2011
Estado no final da sessão
- A página inicial e o formulário de registo estão preparados.
- A gravação de videojogos na base de dados foi testada com sucesso.
- Ainda falta apresentar na página a lista de videojogos guardados.
- Ainda falta implementar e testar as restantes operações CRUD (consultar, editar e eliminar).
- Ainda falta implementar as associações entre videojogos, géneros e plataformas.
- Ainda falta implementar a pesquisa, os filtros e os testes automatizados.

 Registo de Desenvolvimento — Aula 2

 Trabalho realizado:

Nesta aula, foi criado o módulo `app/repositorio.py`, responsável pelo acesso à base de dados, separando essa tarefa da lógica de negócio da aplicação.

Foram implementadas validações para garantir que o título dos videojogos não está vazio e que o ano de lançamento se encontra entre 1950 e 2100. A aplicação foi também melhorada para apresentar os jogos guardados, ordenados pelo título, e mostrar mensagens de erro quando os dados introduzidos são inválidos.

Testes realizados:

Foram testados o catálogo vazio, o registo de videojogos e a rejeição de títulos inválidos. Foi também verificada a validação do ano de lançamento.

 Próximos passos:

Melhorar a interface da aplicação, desenvolver funcionalidades para organizar e filtrar os videojogos e continuar a implementar e testar as funcionalidades previstas para o projeto.