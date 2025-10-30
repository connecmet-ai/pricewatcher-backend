from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
from gpt_utils import analisar_produto
from scraper import buscar_precos
from database import salvar_historico, obter_historico_produto
from alerts import verificar_e_enviar_alertas
import os

app = FastAPI(title="PriceWatcher Backend")

class ProdutoInput(BaseModel):
    nome: str = None
    link: str = None

@app.post("/produto/")
async def cadastrar_produto(produto: ProdutoInput):
    texto = produto.nome or produto.link
    info = analisar_produto(texto)
    precos = buscar_precos(info)
    salvar_historico(info, precos)
    verificar_e_enviar_alertas(info, precos)
    return {"produto": info, "precos": precos}

@app.post("/upload_photo/")
async def upload_photo(file: UploadFile = File(...)):
    contents = await file.read()
    descr = analisar_produto("Imagem enviada: descreva marca e modelo com base na foto (simulação).")
    return {"descricao": descr}

@app.get("/historico/")
def historico_produto(nome: str):
    rows = obter_historico_produto(nome)
    return {"historico": rows}
