import constantes as llaves
import funciones as f
import respuestas as r
from telegram import *
from telegram.ext import *

print("Iniciado")
usuarios=[]
busquedas=[]
inthread=[]
stopped=[]

with open('help.txt') as a: #Guarda el contenido de help.txt en una variable
    help=a.read()
a.close()

with open('examples.txt') as a: #Guarda el contenido de examples.txt en una variable
    examples=a.read()
a.close()

def start_command(update, context):
    if update.message.chat.id not in usuarios: #Verifica si el usuario ya se había inicializado
        usuarios.append(update.message.chat.id) #Agrega al usuario
        busquedas.append(5) #Le da valores predeterminados al usuario
        inthread.append(False)
        stopped.append(False)
    update.message.reply_text(help) #Manda mensaje de help y ejemplos
    update.message.reply_text(examples)

def help_command(update, context):
    update.message.reply_text(help) #Manda mensaje de help y ejemplos
    update.message.reply_text(examples)

def stop(update, context):
    i=0
    for usuario in usuarios: 
        if usuario==update.message.chat.id: #Identifica al usuarios que solicitó detener la operación
            stopped[i]=True #Marca al usuario para detener la operación
            update.message.reply_text("Stopped")
        i=i+1

def search5(update, context):
    i=0
    for usuario in usuarios:
        if usuario==update.message.chat.id: #Identifica al usuarios que solicitó la operación
            busquedas[i]=5 #Actualiza la cantidad de búsquedas
            update.message.reply_text("Search qty set to "+str(busquedas[i]))
        i=i+1

def donate(update, context):
    update.message.reply_text(llaves.LINK_DONACION)

def search10(update, context):
    i=0
    for usuario in usuarios:
        if usuario==update.message.chat.id: #Identifica al usuarios que solicitó la operación
            busquedas[i]=10 #Actualiza la cantidad de búsquedas
            update.message.reply_text("Search qty set to "+str(busquedas[i]))
        i=i+1

def search15(update, context):
    i=0
    for usuario in usuarios:
        if usuario==update.message.chat.id: #Identifica al usuarios que solicitó la operación
            busquedas[i]=15 #Actualiza la cantidad de búsquedas
            update.message.reply_text("Search qty set to "+str(busquedas[i]))
        i=i+1

def search20(update, context):
    i=0
    for usuario in usuarios:
        if usuario==update.message.chat.id: #Identifica al usuarios que solicitó la operación
            busquedas[i]=20 #Actualiza la cantidad de búsquedas
            update.message.reply_text("Search qty set to "+str(busquedas[i]))
        i=i+1

def search25(update, context):
    i=0
    for usuario in usuarios:
        if usuario==update.message.chat.id: #Identifica al usuarios que solicitó la operación
            busquedas[i]=25 #Actualiza la cantidad de búsquedas
            update.message.reply_text("Search qty set to "+str(busquedas[i]))
        i=i+1



def handle_message(update, context):
    if update.message.chat.id in usuarios: #Identifica si el usuario está inicializado
        usuarionumero,enhilo = f.enHilo(usuarios,inthread,update.message.chat.id) #Identifica si el usuario está en un hilo
        if not enhilo:
            inthread[usuarionumero]=True #Marca al usuario para evitar que use otro hilo
            text = str(update.message.text).lower()
            response,two = r.respuesta_hola(text,type,int(busquedas[usuarionumero])) #Solicita y recibe respuesta
            responder(response,two,update,usuarionumero) #Se envía la respuesta al usuario
            inthread[usuarionumero]=False #Se desmarca al usuario para permitir más solicitudes
            stopped[usuarionumero]=False #Seguridad de que el usuario pueda seguir realizando solicitudes
        else: update.message.reply_text("Wait until we finish the last request")    
    else: update.message.reply_text("Use command /start")


def error(update, context):
    print(f"Update {update} caused error {context.error}") #Marca errores en la terminal

def responder(response,two,update,usuarionumero):
    if response.__class__ == list:
        i=0
        for image in response:
            if not stopped[usuarionumero]: #Identifica si el usuario solicitó detener la operación
                if two is None: #Identifica cual tipo de respuesta se recibió
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

def main():
    updater = Updater(llaves.API_KEY, use_context=True,workers=100)
    dp = updater.dispatcher
    
    #Identifica el tipo de operación que se desea realizar
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
    dp.add_handler(MessageHandler(Filters.text,handle_message,run_async=True))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()