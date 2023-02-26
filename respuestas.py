import constantes as llaves
import funciones
import app



def respuesta_hola(input_text,tipo,cantidad):
    papa=False
    user_message = str(input_text).lower()

    if user_message in ("hello", "hola", "quiero h"):
        return "Hi, I'm your H browser",None
    papa=funciones.checanum(user_message)
    if papa:
        images=funciones.download_image(input_text,tipo)
        return images,None
    return funciones.collect_search(user_message,cantidad)
    #return "No se papu"

