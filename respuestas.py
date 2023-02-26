import constantes as llaves
import funciones
import app



def respuesta_hola(input_text,tipo,cantidad):
    papa=False
    user_message = str(input_text).lower()

    if user_message in ("hello", "hola", "quiero h"): #Mensajes con respuesta predeterminada
        return "Hi, I'm your H browser",None
    papa=funciones.checanum(user_message) #Identifica el tipo de solicitud que es
    if papa:
        images=funciones.download_image(input_text,tipo) #Realiza BPC
        return images,None
    return funciones.collect_search(user_message,cantidad) #Realiza BG
