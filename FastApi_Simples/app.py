from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

PRODUTOS = [
    {
        "id":1,
        "nome":"Smartphone",
        "descricao":"Celular 5G",
        "preco":2500.99,
        "disponivel":"True",
    },
    {
        "id":2,
        "nome":"Televisao",
        "descricao":"55 polegadas",
        "preco":3299.99,
        "disponivel":"False",
    }
]

class Produto(BaseModel):
    """Clase de produto"""
    
    id: int
    nome: str
    descricao: str = None
    preco: float
    disponivel: bool = True

@app.get("/produtos", tags=["produtos"])
def listar_produtos() -> list:
    """"Listar produtos."""
    return PRODUTOS

@app.get("/produtos/{produto_id}", tags=["produtos"])
def obter_produto(produto_id: int) -> dict:
    """obter produto."""
    for produto in PRODUTOS:
        if produto["id"] == produto_id:
            return produto
    return {}


@app.post("/produtos", tags=["produtos"])
def criar_produto(produto: Produto) -> Produto:
    PRODUTOS.append(produto)
    return produto

@app.put("/produtos/{produto_id}")
def atualizar_produto(produto_id: int, produto: Produto) -> dict:
    """Atualizar produto."""
    for index, prod in enumerate(PRODUTOS):
        if prod["id"] == produto_id:
            PRODUTOS[index] = produto
            return produto
    return {}