import sqlite3
from datetime import datetime

DB_PATH = "pricewatcher.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS historico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto TEXT,
    loja TEXT,
    preco REAL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def salvar_historico(produto_info: str, precos: list):
    for p in precos:
        try:
            c.execute(
                "INSERT INTO historico (produto, loja, preco) VALUES (?, ?, ?)",
                (produto_info, p.get("loja"), p.get("preco"))
            )
        except:
            pass
    conn.commit()

def obter_historico_produto(produto_nome: str):
    q = "%" + produto_nome + "%"
    c.execute("SELECT produto, loja, preco, data FROM historico WHERE produto LIKE ? ORDER BY data DESC LIMIT 200", (q,))
    rows = c.fetchall()
    return [{"produto": r[0], "loja": r[1], "preco": r[2], "data": r[3]} for r in rows]
