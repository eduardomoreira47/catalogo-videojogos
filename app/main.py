from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.jogos import criar_jogo

app = FastAPI(title="Catálogo de Videojogos")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def pagina_inicial(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/jogos")
def registar_jogo(
    titulo: str = Form(...),
    descricao: str = Form(""),
    ano_lancamento: int = Form(...)
):
    criar_jogo(titulo, descricao, ano_lancamento)

    return RedirectResponse(url="/", status_code=303)
