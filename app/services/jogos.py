from app.repositorio import guardar_jogo, listar_jogos


def criar_jogo(titulo, descricao, ano_lancamento):
    """Valida os dados e regista um videojogo."""

    titulo = titulo.strip()

    if not titulo:
        raise ValueError("O título do videojogo é obrigatório.")

    if not isinstance(ano_lancamento, int) or isinstance(ano_lancamento, bool):
        raise ValueError("O ano de lançamento tem de ser um número inteiro.")

    if ano_lancamento < 1950 or ano_lancamento > 2100:
        raise ValueError("O ano de lançamento deve estar entre 1950 e 2100.")

    return guardar_jogo(titulo, descricao, ano_lancamento)


def obter_jogos():
    """Devolve a lista de videojogos registados."""

    return listar_jogos()