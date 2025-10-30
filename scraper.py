import requests
from bs4 import BeautifulSoup
import re

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def buscar_precos(produto_texto: str):
    termos = produto_texto.split("|")
    termo_busca = termos[0].strip() if termos else produto_texto
    termo_busca = termo_busca.replace(" ", "-")
    url = f"https://lista.mercadolivre.com.br/{termo_busca}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(r.text, "html.parser")
        resultados = []
        items = soup.select(".ui-search-result__content-wrapper")[:6]
        for it in items:
            title_el = it.select_one(".ui-search-item__title")
            price_el = it.select_one(".price-tag-text__price") or it.select_one('.price-tag-fraction')
            if not title_el or not price_el:
                continue
            nome = title_el.get_text(strip=True)
            preco_text = price_el.get_text(strip=True)
            preco_digits = re.sub(r"[^0-9,]", "", preco_text).replace(".", "").replace(",", ".")
            try:
                preco = float(preco_digits)
            except:
                preco = None
            resultados.append({"loja": "Mercado Livre", "nome": nome, "preco": preco})
        resultados.append({"loja": "Amazon (simulado)", "nome": termo_busca.replace('-', ' '), "preco": None})
        return resultados
    except Exception as e:
        return [{"loja": "erro", "nome": str(e), "preco": None}]
