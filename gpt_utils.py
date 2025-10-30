import os
import openai

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("Defina a variável de ambiente OPENAI_API_KEY")
openai.api_key = OPENAI_KEY

MODEL = "gpt-5-mini"

def analisar_produto(texto: str) -> str:
    prompt = (
        "Você é um assistente que extrai nome, marca e modelo de um produto. "
        "Retorne uma string curta com: Marca | Modelo | Categoria.\n"
        f"Texto de entrada: {texto}"
    )
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=150
    )
    content = resp.choices[0].message.get("content", "").strip()
    return content
