import telebot
import time
import random

# --- CONFIGURAÇÕES OFICIAIS ---
CHAVE_API = "8701938906:AAGiR_5JSl3cO6lutKkpc2cUBFbt9WXkNWc"
ID_CANAL = "-1003945705854" 

# --- AJUSTE DE TEMPO ---
# 900 segundos = 15 minutos | 1200 segundos = 20 minutos
INTERVALO = 900 

bot = telebot.TeleBot(CHAVE_API)

# --- SUA LISTA DE POSTAGENS ---
# Você pode colocar dezenas de frases aqui! 
# O bot vai escolher uma por uma aleatoriamente.
postagens = [
    "Dica da Vision Lens: Use iluminação natural para suas fotos de IA ficarem mais reais! 📸",
    "Temos contas de TikTok aquecidas e prontas para o Shop. Chama no PV! 💸",
    "Já conferiu nosso catálogo de hoje? Não perca as novidades. 🚀",
    "A constância é a chave do sucesso no tráfego orgânico. Vamos pra cima! 🔥",
    "Transforme suas ideias em realidade com nossas ferramentas de IA. 🤖",
    "Provas sociais de hoje: Mais um cliente faturando no TikTok! ✅"
]

def iniciar_autopost():
    print("🚀 Bot da Bia rodando a cada 15 minutos!")
    
    while True:
        try:
            # Escolhe uma postagem aleatória da lista
            post_da_vez = random.choice(postagens)
            
            bot.send_message(ID_CANAL, post_da_vez)
            print(f"✅ Postado agora: {post_da_vez[:30]}...")
            
            # Espera os 15 minutos
            time.sleep(INTERVALO) 
            
        except Exception as e:
            print(f"❌ Erro: {e}. Tentando novamente em 1 minuto...")
            time.sleep(60)

if __name__ == "__main__":
    iniciar_autopost()
