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



 Sessão 3:

Durante esta sessão, continuei o desenvolvimento da aplicação web Catálogo de Videojogos, acrescentando novas funcionalidades e melhorando as que já existiam.

- Adicionei vários videojogos ao catálogo, preenchendo informações como o título, a descrição e o ano de lançamento.
- Implementei a funcionalidade de carregar capas a partir do computador, permitindo associar uma imagem a cada videojogo.
- Desenvolvi a funcionalidade de editar videojogos, permitindo alterar as informações dos jogos já registados.
- Implementei a funcionalidade de eliminar videojogos do catálogo.
- Acrescentei uma mensagem de confirmação antes de eliminar um jogo, para evitar eliminações acidentais.
- Atualizei os ficheiros `repositorio.py`, `jogos.py`, `main.py` e `index.html` para integrar as novas funcionalidades.
- Organizei o código de forma a separar o acesso à base de dados, a lógica de negócio e o funcionamento das páginas da aplicação.
- Realizei testes manuais para verificar o funcionamento das funcionalidades desenvolvidas.

No final da sessão, a aplicação passou a permitir registar, consultar, editar e eliminar videojogos, bem como adicionar capas aos jogos. Estas alterações contribuíram para tornar o catálogo mais completo e prático de utilizar.

 06/11/2026 — Importação de videojogos e preparação das capas

 Trabalho realizado

- Importação de 500 videojogos através do ficheiro `dados/jogos.csv`.
- Verificação da importação: 500 jogos importados, 0 duplicados e 0 registos inválidos.
- Atualização do programa `importar_jogos.py` para importar jogos e associar capas.
- Utilização do FetchArt para procurar capas dos videojogos.
- Criação do programa `criar_lista_fetchart.py` para gerar automaticamente uma lista de títulos a partir do CSV.
- Teste do FetchArt com os primeiros 5 jogos.
- Identificação de 11 ficheiros de imagem na pasta `capas_importadas`.
- Criação de uma lista de jogos sem capa encontrada, através do ficheiro `dados/jogos_fetchart_pendentes.txt`.
- Preparação da pesquisa automática das restantes capas.

 Resultados

- 500 videojogos adicionados à base de dados através do CSV.
- 3 jogos adicionais criados através da importação de capas.
- 3 capas associadas a jogos existentes.
- 11 ficheiros de imagem identificados na pasta de importação.

 Trabalho por concluir

- Confirmar quantas capas foram efetivamente encontradas na pesquisa em massa do FetchArt.
- Associar as novas capas aos respetivos jogos.
- Verificar visualmente as capas no catálogo.
- Continuar a implementação dos géneros e plataformas.

 Observações

A importação dos jogos foi concluída com sucesso. A associação das restantes capas continuará na próxima aula.

 Registo de Desenvolvimento — 06/11/2026

 Gestão e organização do catálogo
- Foi realizada uma limpeza da base de dados, reduzindo o catálogo para 100 videojogos.
- Foi criada uma cópia de segurança da base de dados antes das alterações.
- Foi confirmada a existência de 100 registos na tabela de jogos.

 Pesquisa e associação de capas
- Foi utilizada a ferramenta FetchArt para procurar capas dos jogos sem imagem.
- Foram analisadas diferentes versões e edições das capas encontradas.
- Foram associadas 21 novas imagens aos jogos que ainda não tinham capa.
- As imagens foram copiadas para a pasta `app/static/capas/`.
- Foi criado o ficheiro `associar_21_capas.py` para automatizar a associação das imagens.
- As imagens originais foram preservadas.

 Verificação final
Foi executado o script `verificar_capas.py`, tendo sido obtido o seguinte resultado:

| Verificação | Resultado |
|---|---:|
| Total de jogos | 100 |
| Jogos com capa existente | 100 |
| Jogos sem capa | 0 |
| Capas associadas mas não encontradas | 0 |

##Estado atual
- Catálogo com 100 videojogos.
- Todos os jogos têm uma capa associada.
- Não foram detetadas referências a capas inexistentes.
- Foi mantida uma cópia de segurança da base de dados.

**Nota:** Algumas capas correspondem a versões ou edições diferentes dos títulos registados, conforme decisão tomada durante o desenvolvimento.


 09/11/2026 – Melhorias e novas funcionalidades do catálogo

- Reorganização da aplicação em páginas independentes: Início, Todos os Jogos, Filtrar Jogos e Adicionar Jogo.
- Implementação de uma página de estatísticas com o número total de jogos, anos de lançamento e distribuição por décadas.
- Implementação do sistema de géneros, permitindo associar géneros aos jogos e filtrar o catálogo por género.
- Atualização dos formulários de adicionar e editar jogos.
- Melhorias no menu de navegação e no design visual da aplicação, com um tema escuro e elementos modernos.
- Atualização dos ficheiros de código e dos templates para suportar as novas funcionalidades.
- Preparação das alterações para atualização do repositório no GitHub.