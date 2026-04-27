import telebot
import time
import sqlite3
from threading import Thread
from telebot import types

# --- CONFIGURAÇÕES ---
TOKEN = "8701938906:AAGiR_5JSl3cO6lutKkpc2cUBFbt9WXkNWc"
ID_CANAL = "-1003945705854"
INTERVALO = 900 # 15 minutos

bot = telebot.TeleBot(TOKEN)

# --- BANCO DE DADOS (Agora salva tipo de mídia e botões) ---
def iniciar_db():
    conn = sqlite3.connect('esteira_vendas.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       tipo TEXT, file_id TEXT, legenda TEXT, link_url TEXT)''')
    conn.commit()
    return conn

db = iniciar_db()

# --- COMANDOS DE GERENCIAMENTO ---
@bot.message_handler(commands=['start'])
def boas_vindas(message):
    msg = ("Bia, para adicionar à esteira, envie a FOTO ou VÍDEO com uma legenda.\n\n"
           "Para colocar BOTÃO, escreva o link na última linha da legenda assim:\n"
           "LINK: https://seusite.com")
    bot.reply_to(message, msg)

@bot.message_handler(content_types=['photo', 'video'])
def salvar_na_esteira(message):
    link = ""
    legenda = message.caption if message.caption else ""
    
    # Extrai o link se houver
    if "LINK:" in legenda:
        partes = legenda.split("LINK:")
        legenda = partes[0].strip()
        link = partes[1].strip()

    file_id = ""
    tipo = ""

    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        tipo = "foto"
    else:
        file_id = message.video.file_id
        tipo = "video"

    cursor = db.cursor()
    cursor.execute('INSERT INTO posts (tipo, file_id, legenda, link_url) VALUES (?, ?, ?, ?)', 
                   (tipo, file_id, legenda, link))
    db.commit()
    bot.reply_to(message, f"✅ {tipo.capitalize()} adicionado à esteira de 15 minutos!")

@bot.message_handler(commands=['limpar'])
def limpar_esteira(message):
    cursor = db.cursor()
    cursor.execute('DELETE FROM posts')
    db.commit()
    bot.reply_to(message, "🗑 Esteira limpa!")

# --- MOTOR DA ESTEIRA (SEQUENCIAL) ---
def loop_esteira():
    index_atual = 0
    while True:
        try:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM posts ORDER BY id ASC')
            posts = cursor.fetchall()

            if posts:
                # Se o índice passou do tamanho da lista, volta pro zero (loop infinito)
                if index_atual >= len(posts):
                    index_atual = 0
                
                post = posts[index_atual]
                tipo, file_id, legenda, url = post[1], post[2], post[3], post[4]

                # Criar botão se houver link
                markup = None
                if url:
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("SAIBA MAIS / COMPRAR 🚀", url=url))

                # Enviar de acordo com o tipo
                if tipo == "foto":
                    bot.send_photo(ID_CANAL, file_id, caption=legenda, reply_markup=markup)
                else:
                    bot.send_video(ID_CANAL, file_id, caption=legenda, reply_markup=markup)

                index_atual += 1
                time.sleep(INTERVALO)
            else:
                time.sleep(30) # Espera 30s se não tiver nada na lista
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(60)

Thread(target=loop_esteira).start()
bot.polling(none_stop=True)
