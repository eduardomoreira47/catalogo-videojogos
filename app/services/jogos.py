
from app.repositorio import (
    guardar_jogo,
    listar_jogos,
    obter_jogo_por_id,
    atualizar_jogo,
    eliminar_jogo,
    obter_generos,
    pesquisar_jogos as pesquisar_jogos_repositorio,
    obter_estatisticas_jogos as obter_estatisticas_repositorio,
    adicionar_favorito as adicionar_favorito_repositorio,
    remover_favorito as remover_favorito_repositorio,
    verificar_favorito as verificar_favorito_repositorio,
    listar_favoritos as listar_favoritos_repositorio,
)


def validar_dados_jogo(titulo, ano_lancamento):
    """Valida os dados principais de um videojogo."""

    titulo = titulo.strip()

    if not titulo:
        raise ValueError("O título do videojogo é obrigatório.")

    if not isinstance(ano_lancamento, int) or isinstance(ano_lancamento, bool):
        raise ValueError("O ano de lançamento tem de ser um número inteiro.")

    if ano_lancamento < 1950 or ano_lancamento > 2100:
        raise ValueError("O ano de lançamento deve estar entre 1950 e 2100.")

    return titulo


def obter_lista_generos():
    """Devolve todos os géneros disponíveis."""

    return obter_generos()


def criar_jogo(
    titulo,
    descricao,
    ano_lancamento,
    capa=None,
    genero_id=None,
):
    """Valida os dados e regista um videojogo."""

    titulo = validar_dados_jogo(titulo, ano_lancamento)

    if genero_id is not None:
        try:
            genero_id = int(genero_id)
        except (ValueError, TypeError):
            raise ValueError("O género selecionado é inválido.")

        generos = obter_generos()

        if not any(genero["id_genero"] == genero_id for genero in generos):
            raise ValueError("O género selecionado não existe.")

    return guardar_jogo(
        titulo,
        descricao,
        ano_lancamento,
        capa,
        genero_id,
    )


def obter_jogos(ordenar_por="titulo_az"):
    """Devolve a lista de videojogos com a ordenação escolhida."""

    return listar_jogos(ordenar_por)


def pesquisar_jogos(titulo="", ano_lancamento=None, genero_id=None):
    """Pesquisa videojogos pelo título, ano e género."""

    return pesquisar_jogos_repositorio(
        titulo,
        ano_lancamento,
        genero_id,
    )


def obter_jogo(id_jogo):
    """Procura um videojogo através do seu ID."""

    return obter_jogo_por_id(id_jogo)


def obter_estatisticas():
    """Devolve as estatísticas gerais do catálogo."""

    return obter_estatisticas_repositorio()


def editar_jogo(
    id_jogo,
    titulo,
    descricao,
    ano_lancamento,
    capa=None,
    genero_id=None,
):
    """Valida os dados e atualiza um videojogo existente."""

    titulo = validar_dados_jogo(titulo, ano_lancamento)

    jogo = obter_jogo_por_id(id_jogo)

    if jogo is None:
        raise ValueError("O videojogo que pretendes editar não existe.")

    if capa is None:
        capa = jogo["capa"]

    if genero_id is not None:
        try:
            genero_id = int(genero_id)
        except (ValueError, TypeError):
            raise ValueError("O género selecionado é inválido.")

        generos = obter_generos()

        if not any(genero["id_genero"] == genero_id for genero in generos):
            raise ValueError("O género selecionado não existe.")

    return atualizar_jogo(
        id_jogo,
        titulo,
        descricao,
        ano_lancamento,
        capa,
        genero_id,
    )


def remover_jogo(id_jogo):
    """Remove um videojogo existente do catálogo."""

    jogo = obter_jogo_por_id(id_jogo)

    if jogo is None:
        raise ValueError("O videojogo que pretendes eliminar não existe.")

    return eliminar_jogo(id_jogo)


def adicionar_favorito(id_jogo):
    """Adiciona um videojogo aos favoritos."""

    jogo = obter_jogo_por_id(id_jogo)

    if jogo is None:
        raise ValueError("O videojogo não existe.")

    adicionar_favorito_repositorio(id_jogo)


def remover_favorito(id_jogo):
    """Remove um videojogo dos favoritos."""

    jogo = obter_jogo_por_id(id_jogo)

    if jogo is None:
        raise ValueError("O videojogo não existe.")

    remover_favorito_repositorio(id_jogo)


def verificar_favorito(id_jogo):
    """Verifica se um videojogo é favorito."""

    return verificar_favorito_repositorio(id_jogo)


def obter_favoritos():
    """Devolve todos os videojogos favoritos."""

    return listar_favoritos_repositorio()
