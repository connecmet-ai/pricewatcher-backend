import os
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.getenv("EMAIL_SMTP_HOST")
SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
SMTP_USER = os.getenv("EMAIL_SMTP_USER")
SMTP_PASS = os.getenv("EMAIL_SMTP_PASS")
ALERT_TO = os.getenv("ALERT_EMAIL_TO")

def verificar_e_enviar_alertas(produto_info: str, precos: list):
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASS or not ALERT_TO:
        return False

    validos = [p for p in precos if p.get('preco')]
    if not validos:
        return False

    preco_atual = min([p['preco'] for p in validos if p['preco'] is not None])

    assunto = f"PriceWatcher — Alerta: possível preço baixo para {produto_info}" 
    corpo = f"Foram encontradas as seguintes ofertas para {produto_info}:\n\n"
    for p in validos:
        corpo += f"- {p['loja']}: R$ {p['preco']}\n"
    corpo += "\nAcesse seu painel PriceWatcher para ver o histórico e configurar alertas."

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = SMTP_USER
    msg['To'] = ALERT_TO
    msg.set_content(corpo)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Erro enviando e-mail:", e)
        return False
