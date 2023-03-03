import telebot
import constantes as llaves
import respuestas as r
bot = telebot.TeleBot(llaves.API_KEY)

tipo="img"
cantidad=5

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Escribe algo")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "/start : Inicia el bot \n/help : estás viendo \n/changetoimg : aun no jala \n/changetopdf : aun no jala \n Basicamente esrcibes tu codigo H que quieras y el bot te lo manda, por ahora en imagenes pero esperamos pronto lograr mandarlo también en pdfs")

@bot.message_handler(commands=['changetopdf'])
def send_welcome(message):
    global tipo
    tipo = "pdf"
    bot.reply_to(message,tipo)

@bot.message_handler(commands=['changetoimg'])
def send_welcome(message):
    global tipo
    tipo = "img"
    bot.reply_to(message,tipo)

@bot.message_handler(commands=['search5'])
def send_welcome(message):
    global cantidad
    cantidad = 5
    bot.reply_to(message,str(cantidad))

@bot.message_handler(commands=['search10'])
def send_welcome(message):
    global cantidad
    cantidad = 10
    bot.reply_to(message,str(cantidad))

@bot.message_handler(commands=['search15'])
def send_welcome(message):
    global cantidad
    cantidad = 15
    bot.reply_to(message,str(cantidad))

@bot.message_handler(commands=['search20'])
def send_welcome(message):
    global cantidad
    cantidad = 20
    bot.reply_to(message,str(cantidad))

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = str(message.text).lower()
    response,two = r.respuesta_hola(text,tipo,cantidad)
    if response.__class__ == list:
        i=0
        for image in response:
            if two is None:
                bot.send_photo(message.chat.id,image)
            else:
                bot.send_photo(message.chat.id,image,caption=two[i])
            i=i+1
    else:
        bot.send_message(message.chat.id,response)

bot.infinity_polling()