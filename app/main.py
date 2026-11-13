
from pathlib import Path
from uuid import uuid4
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database.init_db import criar_tabelas

from app.services.jogos import (
    criar_jogo,
    obter_jogos,
    pesquisar_jogos,
    obter_jogo,
    editar_jogo,
    remover_jogo,
    obter_estatisticas,
    obter_lista_generos,
    adicionar_favorito,
    remover_favorito,
    obter_favoritos,
)


@asynccontextmanager
async def ciclo_vida(app: FastAPI):
    """Prepara a base de dados quando a aplicação inicia."""
    criar_tabelas()
    yield


app = FastAPI(
    title="Catálogo de Videojogos",
    lifespan=ciclo_vida,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

PASTA_CAPAS = Path("app/static/capas")
PASTA_CAPAS.mkdir(parents=True, exist_ok=True)

EXTENSOES_PERMITIDAS = {".png", ".jpg", ".jpeg"}
TAMANHO_MAXIMO = 5 * 1024 * 1024  # 5 MB


async def guardar_capa(ficheiro: UploadFile | None):
    """Valida e guarda a capa de um videojogo."""

    if not ficheiro or not ficheiro.filename:
        return None

    extensao = Path(ficheiro.filename).suffix.lower()

    if extensao not in EXTENSOES_PERMITIDAS:
        raise ValueError("A capa tem de estar no formato PNG, JPG ou JPEG.")

    conteudo = await ficheiro.read(TAMANHO_MAXIMO + 1)

    if not conteudo:
        raise ValueError("O ficheiro de imagem está vazio.")

    if len(conteudo) > TAMANHO_MAXIMO:
        raise ValueError("A imagem não pode ultrapassar 5 MB.")

    if extensao == ".png" and not conteudo.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("O conteúdo do ficheiro não é uma imagem PNG.")

    if extensao in {".jpg", ".jpeg"} and not conteudo.startswith(b"\xff\xd8\xff"):
        raise ValueError("O conteúdo do ficheiro não é uma imagem JPG.")

    nome_ficheiro = f"{uuid4().hex}{extensao}"
    destino = PASTA_CAPAS / nome_ficheiro

    destino.write_bytes(conteudo)

    return f"capas/{nome_ficheiro}"


def apagar_capa(caminho_capa):
    """Apaga uma capa guardada na pasta de capas da aplicação."""

    if not caminho_capa:
        return

    caminho = Path(caminho_capa)

    if caminho.name != caminho_capa or caminho_capa != str(caminho):
        return

    ficheiro = (PASTA_CAPAS / caminho.name).resolve()

    if ficheiro.parent == PASTA_CAPAS.resolve():
        ficheiro.unlink(missing_ok=True)


# ==========================================
# PÁGINA INICIAL
# ==========================================

@app.get("/", response_class=HTMLResponse)
def pagina_inicial(request: Request):
    """Apresenta a página inicial e o resumo das estatísticas."""

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "estatisticas": obter_estatisticas(),
        },
    )


# ==========================================
# PÁGINA DE ESTATÍSTICAS
# ==========================================

@app.get("/estatisticas", response_class=HTMLResponse)
def pagina_estatisticas(request: Request):
    """Apresenta as estatísticas do catálogo."""

    return templates.TemplateResponse(
        request=request,
        name="estatisticas.html",
        context={
            "estatisticas": obter_estatisticas(),
        },
    )


# ==========================================
# PÁGINA COM TODOS OS JOGOS
# ==========================================

@app.get("/jogos", response_class=HTMLResponse)
def pagina_jogos(
    request: Request,
    ordenar: str = "titulo_az",
):
    """Apresenta todos os videojogos com a ordenação escolhida."""

    opcoes_ordenacao = {
        "titulo_az",
        "titulo_za",
        "ano_antigo",
        "ano_recente",
    }

    if ordenar not in opcoes_ordenacao:
        ordenar = "titulo_az"

    return templates.TemplateResponse(
        request=request,
        name="jogos.html",
        context={
            "jogos": obter_jogos(ordenar),
            "ordenar": ordenar,
        },
    )


# ==========================================
# PÁGINA DE DETALHES DE UM JOGO
# ==========================================

@app.get("/jogos/{id_jogo}", response_class=HTMLResponse)
def pagina_detalhes_jogo(request: Request, id_jogo: int):
    """Apresenta os detalhes de um videojogo."""

    jogo = obter_jogo(id_jogo)

    if jogo is None:
        return HTMLResponse(
            "Videojogo não encontrado.",
            status_code=404,
        )

    return templates.TemplateResponse(
        request=request,
        name="detalhes_jogo.html",
        context={
            "jogo": jogo,
        },
    )


# ==========================================
# PÁGINA DE FAVORITOS
# ==========================================

@app.get("/favoritos", response_class=HTMLResponse)
def pagina_favoritos(request: Request):
    """Apresenta todos os videojogos favoritos."""

    return templates.TemplateResponse(
        request=request,
        name="favoritos.html",
        context={
            "jogos": obter_favoritos(),
        },
    )


# ==========================================
# ADICIONAR AOS FAVORITOS
# ==========================================

@app.post("/jogos/{id_jogo}/favorito")
def rota_adicionar_favorito(
    id_jogo: int,
    origem: str = Form("jogos"),
):
    """Adiciona um videojogo à lista de favoritos."""

    try:
        adicionar_favorito(id_jogo)
    except ValueError:
        return HTMLResponse(
            "Videojogo não encontrado.",
            status_code=404,
        )

    destino = "/favoritos" if origem == "favoritos" else "/jogos"

    return RedirectResponse(url=destino, status_code=303)


# ==========================================
# RETIRAR DOS FAVORITOS
# ==========================================

@app.post("/jogos/{id_jogo}/retirar-favorito")
def rota_remover_favorito(
    id_jogo: int,
    origem: str = Form("favoritos"),
):
    """Retira um videojogo da lista de favoritos."""

    try:
        remover_favorito(id_jogo)
    except ValueError:
        return HTMLResponse(
            "Videojogo não encontrado.",
            status_code=404,
        )

    destino = "/favoritos" if origem == "favoritos" else "/jogos"

    return RedirectResponse(url=destino, status_code=303)


# ==========================================
# PÁGINA DE PESQUISA E FILTROS
# ==========================================

@app.get("/filtrar", response_class=HTMLResponse)
def pagina_filtrar(
    request: Request,
    q: str = "",
    ano: str = "",
    genero_id: str = "",
):
    """Pesquisa videojogos por título, ano e género."""

    ano_filtro = None
    genero_filtro = None

    if ano.strip():
        try:
            ano_filtro = int(ano)
        except ValueError:
            ano_filtro = None

    if ano_filtro is not None and not 1950 <= ano_filtro <= 2100:
        ano_filtro = None

    if genero_id.strip():
        try:
            genero_filtro = int(genero_id)
        except ValueError:
            genero_filtro = None

    jogos = pesquisar_jogos(
        q,
        ano_filtro,
        genero_filtro,
    )

    return templates.TemplateResponse(
        request=request,
        name="filtrar.html",
        context={
            "jogos": jogos,
            "pesquisa": q,
            "ano_filtro": ano,
            "generos": obter_lista_generos(),
            "genero_filtro": genero_id,
        },
    )


# ==========================================
# PÁGINA PARA ADICIONAR JOGOS
# ==========================================

@app.get("/adicionar", response_class=HTMLResponse)
def pagina_adicionar(request: Request):
    """Apresenta o formulário para registar um videojogo."""

    return templates.TemplateResponse(
        request=request,
        name="adicionar.html",
        context={
            "erro": None,
            "titulo": "",
            "descricao": "",
            "ano_lancamento": "",
            "generos": obter_lista_generos(),
            "genero_id": "",
        },
    )


@app.post("/jogos", response_class=HTMLResponse)
async def registar_jogo(
    request: Request,
    titulo: str = Form(""),
    descricao: str = Form(""),
    ano_lancamento: str = Form(""),
    genero_id: str = Form(""),
    ficheiro_capa: UploadFile | None = File(None),
):
    """Valida e regista um novo videojogo."""

    caminho_capa = None

    try:
        titulo = titulo.strip()

        if not titulo:
            raise ValueError("O título do videojogo é obrigatório.")

        if not ano_lancamento.strip():
            raise ValueError("O ano de lançamento é obrigatório.")

        try:
            ano = int(ano_lancamento)
        except ValueError:
            raise ValueError(
                "O ano de lançamento tem de ser um número inteiro."
            )

        genero_selecionado = int(genero_id) if genero_id.strip() else None

        caminho_capa = await guardar_capa(ficheiro_capa)

        criar_jogo(
            titulo,
            descricao,
            ano,
            caminho_capa,
            genero_selecionado,
        )

    except ValueError as erro:
        apagar_capa(caminho_capa)

        return templates.TemplateResponse(
            request=request,
            name="adicionar.html",
            status_code=400,
            context={
                "erro": str(erro),
                "titulo": titulo,
                "descricao": descricao,
                "ano_lancamento": ano_lancamento,
                "generos": obter_lista_generos(),
                "genero_id": genero_id,
            },
        )

    finally:
        if ficheiro_capa:
            await ficheiro_capa.close()

    return RedirectResponse(url="/jogos", status_code=303)


# ==========================================
# EDITAR JOGOS
# ==========================================

@app.get("/jogos/{id_jogo}/editar", response_class=HTMLResponse)
def pagina_editar_jogo(request: Request, id_jogo: int):
    """Apresenta o formulário para editar um videojogo."""

    jogo = obter_jogo(id_jogo)

    if jogo is None:
        return HTMLResponse(
            "Videojogo não encontrado.",
            status_code=404,
        )

    return templates.TemplateResponse(
        request=request,
        name="editar_jogo.html",
        context={
            "jogo": jogo,
            "erro": None,
            "titulo": None,
            "descricao": None,
            "ano_lancamento": None,
            "generos": obter_lista_generos(),
        },
    )


@app.post("/jogos/{id_jogo}/editar", response_class=HTMLResponse)
async def guardar_edicao_jogo(
    request: Request,
    id_jogo: int,
    titulo: str = Form(""),
    descricao: str = Form(""),
    ano_lancamento: str = Form(""),
    genero_id: str = Form(""),
    ficheiro_capa: UploadFile | None = File(None),
):
    """Valida e guarda as alterações de um videojogo."""

    jogo = obter_jogo(id_jogo)

    if jogo is None:
        if ficheiro_capa:
            await ficheiro_capa.close()

        return HTMLResponse(
            "Videojogo não encontrado.",
            status_code=404,
        )

    nova_capa = None

    try:
        titulo = titulo.strip()

        if not titulo:
            raise ValueError("O título do videojogo é obrigatório.")

        if not ano_lancamento.strip():
            raise ValueError("O ano de lançamento é obrigatório.")

        try:
            ano = int(ano_lancamento)
        except ValueError:
            raise ValueError(
                "O ano de lançamento tem de ser um número inteiro."
            )

        genero_selecionado = int(genero_id) if genero_id.strip() else None

        if ficheiro_capa and ficheiro_capa.filename:
            nova_capa = await guardar_capa(ficheiro_capa)

        editar_jogo(
            id_jogo,
            titulo,
            descricao,
            ano,
            nova_capa,
            genero_selecionado,
        )

    except ValueError as erro:
        apagar_capa(nova_capa)

        return templates.TemplateResponse(
            request=request,
            name="editar_jogo.html",
            status_code=400,
            context={
                "jogo": jogo,
                "erro": str(erro),
                "titulo": titulo,
                "descricao": descricao,
                "ano_lancamento": ano_lancamento,
                "generos": obter_lista_generos(),
                "genero_id": genero_id,
            },
        )

    finally:
        if ficheiro_capa:
            await ficheiro_capa.close()

    if nova_capa and jogo["capa"]:
        apagar_capa(jogo["capa"])

    return RedirectResponse(url="/jogos", status_code=303)


# ==========================================
# ELIMINAR JOGOS
# ==========================================

@app.post("/jogos/{id_jogo}/eliminar")
def rota_eliminar_jogo(id_jogo: int):
    """Elimina um videojogo e a respetiva capa, se existir."""

    jogo = obter_jogo(id_jogo)

    if jogo is None:
        return HTMLResponse(
            "Videojogo não encontrado.",
            status_code=404,
        )

    remover_jogo(id_jogo)

    if jogo["capa"]:
        apagar_capa(jogo["capa"])

    return RedirectResponse(url="/jogos", status_code=303)
