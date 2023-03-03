import constantes as llaves
import respuestas as r
from telegram import *
from telegram.ext import *

print("Iniciado")
type="img"
usuarios=[]
busquedas=[]
inthread=[]
stopped=[]
def start_command(update, context):
    if update.message.chat.id not in usuarios:
        usuarios.append(update.message.chat.id)
        busquedas.append(5)
        inthread.append(False)
        stopped.append(False)
    texto=""
    texto=texto+"Write the H code that you want or write something to browse. "
    texto=texto+"You can also search by \"Tag:\", \"Artist:\", \"Character:\" or \"Parody:\".\n"
    texto=texto+"Examples: \n\"Tag: Albino\"\n"
    texto=texto+"\"Character:Deku\"\n"
    texto=texto+"or search by title \"Monogatari\"\n\n"
    texto=texto+"If you want to search more set \"Page:\" and a number at the end of your request.\n"
    texto=texto+"Examples: \"Tag: Albino page: 2\""
    texto=texto+"\n, \"big page:6\""
    texto=texto+"\n/help : Show commands and function"
    texto=texto+"\n/stop : Stop the current sent"
    texto=texto+"\n/search5 : Search set to 5"
    texto=texto+"\n/search10 : Search set to 10"
    texto=texto+"\n/search15 : Search set to 15"
    texto=texto+"\n/search20 : Search set to 20"
    texto=texto+"\n/search25 : Search set to 25"
    texto=texto+"\n/donate : Gives you the PayPal donation link"
    texto=texto+"\nThis bot uses https://nhentai.xxx"
    update.message.reply_text(texto)

def help_command(update, context):
    texto=""
    texto=texto+"Write the H code that you want or write something to browse. "
    texto=texto+"You can also search by \"Tag:\", \"Artist:\", \"Character:\" or \"Parody:\".\n"
    texto=texto+"Examples: \n\"Tag: Albino\"\n"
    texto=texto+"\"Character:Deku\"\n"
    texto=texto+"or search by title \"Monogatari\"\n\n"
    texto=texto+"If you want to search more set \"Page:\" and a number at the end of your request.\n"
    texto=texto+"Examples: \"Tag: Albino page: 2\""
    texto=texto+"\n, \"big page:6\""
    texto=texto+"\n/help : Show commands and function"
    texto=texto+"\n/stop : Stop the current sent"
    texto=texto+"\n/search5 : Search set to 5"
    texto=texto+"\n/search10 : Search set to 10"
    texto=texto+"\n/search15 : Search set to 15"
    texto=texto+"\n/search20 : Search set to 20"
    texto=texto+"\n/search25 : Search set to 25"
    texto=texto+"\n/donate : Gives you the PayPal donation link"
    texto=texto+"\nThis bot uses https://nhentai.xxx"
    update.message.reply_text(texto)

def changetypetopdf(update, context):
    update.message.reply_text("pdf")
    global type
    type="pdf"

def stop(update, context):
    i=0
    for usuario in usuarios:
        if usuario==update.message.chat.id:
            stopped[i]=True
            update.message.reply_text("Stopped")
        i=i+1


def search5(update, context):
    i=0
    for usuario in usuarios:
        if usuario==update.message.chat.id:
            busquedas[i]=5
            update.message.reply_text("Search qty set to "+str(busquedas[i]))
        i=i+1

def donate(update, context):
    update.message.reply_text("https://www.paypal.com/donate/?hosted_button_id=JQXBRC88DKTSA")

def search10(update, context):
    i=0
    for usuario in usuarios:
        if usuario==update.message.chat.id:
            busquedas[i]=10
            update.message.reply_text("Search qty set to "+str(busquedas[i]))
        i=i+1

def search15(update, context):
    i=0
    for usuario in usuarios:
        if usuario==update.message.chat.id:
            busquedas[i]=15
            update.message.reply_text("Search qty set to "+str(busquedas[i]))
        i=i+1

def search20(update, context):
    i=0
    for usuario in usuarios:
        if usuario==update.message.chat.id:
            busquedas[i]=20
            update.message.reply_text("Search qty set to "+str(busquedas[i]))
        i=i+1

def search25(update, context):
    i=0
    for usuario in usuarios:
        if usuario==update.message.chat.id:
            busquedas[i]=25
            update.message.reply_text("Search qty set to "+str(busquedas[i]))
        i=i+1

def changetypetoimg(update, context):
    update.message.reply_text("img")
    global type
    type="img"

def handle_message(update, context):
    i=0
    checador=True
    if update.message.chat.id in usuarios:
        for usuario in usuarios:
            if usuario==update.message.chat.id:
                if inthread[i]==False:
                    usuarionumero=i
                    checador=False
            i=i+1
        if checador==False:
            inthread[usuarionumero]=True
            text = str(update.message.text).lower()
            response,two = r.respuesta_hola(text,type,int(busquedas[usuarionumero]))
            if response.__class__ == list:
                i=0
                for image in response:
                    if not stopped[usuarionumero]:
                        if two is None:
                            try:
                                update.message.reply_photo(image)
                            except:
                                update.message.reply_text("Image can't be procesed, process stopped")
                                stopped[usuarionumero]=True
                        else:
                            try:
                                update.message.reply_photo(image,two[i])
                            except:
                                update.message.reply_text("Image can't be processed\n"+two[i])
                    i=i+1
            else:
                if response.__class__!=str:
                    update.message.reply_document(response)
                else:
                    update.message.reply_text(response)
            inthread[usuarionumero]=False
            stopped[usuarionumero]=False
        else: update.message.reply_text("Wait until we finish the last request")    
    else: update.message.reply_text("Use command /start")


def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(llaves.API_KEY, use_context=True,workers=100)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start",start_command,run_async=True))
    dp.add_handler(CommandHandler("help",help_command,run_async=True))
    dp.add_handler(CommandHandler("stop",stop,run_async=True))
    dp.add_handler(CommandHandler("donate",donate,run_async=True))
    dp.add_handler(CommandHandler("donate",donate,run_async=True))
    dp.add_handler(CommandHandler("search5",search5,run_async=True))
    dp.add_handler(CommandHandler("search10",search10,run_async=True))
    dp.add_handler(CommandHandler("search15",search15,run_async=True))
    dp.add_handler(CommandHandler("search20",search20,run_async=True))
    dp.add_handler(CommandHandler("search25",search25,run_async=True))
    dp.add_handler(CommandHandler("changetoimg",changetypetoimg,run_async=True))
    dp.add_handler(MessageHandler(Filters.text,handle_message,run_async=True))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()