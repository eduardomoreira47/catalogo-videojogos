
from app.repositorio import (
    guardar_jogo,
    listar_jogos,
    obter_jogo_por_id,
    atualizar_jogo,
    eliminar_jogo,
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


def criar_jogo(titulo, descricao, ano_lancamento, capa=None):
    """Valida os dados e regista um videojogo."""

    titulo = validar_dados_jogo(titulo, ano_lancamento)

    return guardar_jogo(titulo, descricao, ano_lancamento, capa)


def obter_jogos():
    """Devolve a lista de videojogos registados."""

    return listar_jogos()


def obter_jogo(id_jogo):
    """Procura um videojogo através do seu ID."""

    return obter_jogo_por_id(id_jogo)


def editar_jogo(id_jogo, titulo, descricao, ano_lancamento, capa=None):
    """Valida os dados e atualiza um videojogo existente."""

    titulo = validar_dados_jogo(titulo, ano_lancamento)

    jogo = obter_jogo_por_id(id_jogo)

    if jogo is None:
        raise ValueError("O videojogo que pretendes editar não existe.")

    if capa is None:
        capa = jogo["capa"]

    return atualizar_jogo(
        id_jogo,
        titulo,
        descricao,
        ano_lancamento,
        capa
    )


def remover_jogo(id_jogo):
    """Remove um videojogo existente do catálogo."""

    jogo = obter_jogo_por_id(id_jogo)

    if jogo is None:
        raise ValueError("O videojogo que pretendes eliminar não existe.")

    return eliminar_jogo(id_jogo)
