from fastapi import FastAPI

app = FastAPI(title="Catálogo de Videojogos")


@app.get("/")
def pagina_inicial():
    return {
        "mensagem": "Bem-vindo ao Catálogo de Videojogos!"
    }