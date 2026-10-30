from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.jogos import criar_jogo, obter_jogos

app = FastAPI(title="Catálogo de Videojogos")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def pagina_inicial(request: Request):
    jogos = obter_jogos()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "jogos": jogos,
            "erro": None,
            "titulo": "",
            "descricao": "",
            "ano_lancamento": ""
        }
    )


@app.post("/jogos", response_class=HTMLResponse)
def registar_jogo(
    request: Request,
    titulo: str = Form(""),
    descricao: str = Form(""),
    ano_lancamento: str = Form("")
):
    try:
        titulo = titulo.strip()

        if not titulo:
            raise ValueError("O título do videojogo é obrigatório.")

        if not ano_lancamento.strip():
            raise ValueError("O ano de lançamento é obrigatório.")

        ano = int(ano_lancamento)

        print(f"DEBUG: título recebido = {titulo!r}")

        criar_jogo(titulo, descricao, ano)

    except ValueError as erro:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            status_code=400,
            context={
                "jogos": obter_jogos(),
                "erro": str(erro),
                "titulo": titulo,
                "descricao": descricao,
                "ano_lancamento": ano_lancamento
            }
        )

    return RedirectResponse(url="/", status_code=303)

