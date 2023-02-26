import requests
from urllib3.exceptions import InsecureRequestWarning
from PIL import Image
import constantes as llaves

def collect_search(texto,cantidad):
    lista_imagenes=[]
    lista_codigos=[]
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) #Desactiva advertencias en terminal
    session = requests.Session()
    session.verify = False
    url,texto=correcturl(texto) #Identifica el tipo de BG
    page = requests.get(url,verify=False) #Se almacena el contenido de la pagina en una variable
    if page.status_code==200: #Verifica si la página de la BG existe
        verificarContenido(cantidad,page.text,lista_imagenes,lista_codigos) #Verifica si existe contenido en la página
        return lista_imagenes,lista_codigos
    return "No H in search",None

def guardarImagen(lista_imagenes,page): #Guarda el contenido recibido en la lista recibida
    lista_imagenes.append(page.content)

def download_image(code,tipo): #Obtiene las imagenes de la BPC
    lista_imagenes=[]
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) #Desactiva advertencias en terminal
    session = requests.Session()
    session.verify = False 
    url = llaves.URL_IMG+code+"/" #Obtiene la url de la BPC
    page = requests.get(url,verify=False) #Se almacena el contenido de la pagina en una variable
    if page.status_code==200: #Verifica la existencia de la página
        urlpagina=geturlpagina(page.text) #Obtiene la url base de las imágenes
        more=True
        i=1
        while(more is True):
            page,more=getimages(urlpagina,True,i) #Verifica si existe otra imagen y la obtiene
            if more:
                guardarImagen(lista_imagenes,page) #Guarda el contenido en la lista de imágenes
            i=i+1
    if len(lista_imagenes)==0: #Identifica si se obtuvo contenido
        return "H not founded"
    return lista_imagenes

def checanum(a): #Verifica si se tiene solicitó una BPC o BG
    papalist=[]
    papa=False
    for x in a:
        for y in llaves.NUM:
            if y==x:
                papa=True
        papalist.append(papa)
        papa=False
    if False in papalist:
        return False
    return True

def find_nth_overlapping(haystack, needle, n): #Identifica la localización de un subtring repetido en un string
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+1)
        n -= 1
    return start
    
def correcturl(text): #Identifica el tipo de BG
    url=llaves.URL_SEARCH
    urlfinal=setpage(text) #Identifica si se solicitó más contenido
    if "tag:" in text:
        if "tag: " in text: text=text.replace("tag: ","")
        else: text=text.replace("tag:","")
        url=llaves.URL_TAG
    if "artist:" in text:
        if "artist: " in text: text=text.replace("artist: ","")
        else: text=text.replace("artist:","")
        url=llaves.URL_ARTIST
    if "character:" in text:
        if "character: " in text: text=text.replace("character: ","")
        else: text=text.replace("character:","")
        url=llaves.URL_CHARACTER
    if "parody:" in text:
        if "parody: " in text: text=text.replace("parody: ","")
        else: text=text.replace("parody:","")
        url=llaves.URL_PARODY
    if len(urlfinal)!=0:
        text=text[0:text.find(" page:")]
    if url==llaves.URL_SEARCH:
        url=url+str(text).replace(" ","+")+urlfinal
    else:url=url+str(text).replace(" ","-")+"/"+urlfinal
    return url,text

def setpage(text): #Identifica si se solicitó más contenido
    if "page:" in text:
        if " page: " in text:
            texto=text[text.find("page: ")+6:]
        else: texto=text[text.find("page:")+5:]
        if ":" in text[:text.find("page:")]:
            return llaves.TAGPAGE+texto
        return llaves.SEARCHPAGE+texto
    return ""

def getimages(urlpagina,more,i): #Verifica si existe una imagen y la obtiene
    url = urlpagina+'/'+str(i)+'.jpg' 
    page = requests.get(url) 
    if page.status_code!=200: #Se identifica si la imagen es jpg
        url = urlpagina+'/'+str(i)+'.png' #Se identifica si la imagen es png
        page = requests.get(url)
        if page.status_code!=200:
            url = urlpagina+'/'+str(i)+'.gif' #Se identifica si la imagen es gif
            page = requests.get(url)
            if page.status_code!=200: #Se identifica su hubo o no más imágenes
                more=False
    return page,more

def geturlpagina(urlpagina): #Obtiene la url base de las imágenes
    if "cover.jpg" in urlpagina:
        urlpagina=urlpagina[urlpagina.find("cover.jpg",2)-34:urlpagina.find("cover.jpg",2)]
    else:
        if "cover.png" in urlpagina:
            urlpagina=urlpagina[urlpagina.find("cover.png",2)-34:urlpagina.find("cover.png",2)]
        else: urlpagina=urlpagina[urlpagina.find("cover.gif",2)-34:urlpagina.find("cover.gif",2)]
    return urlpagina[urlpagina.find("https",0):len(urlpagina)-1]

def enHilo(usuarios,inthread,id): #Identifica si el usuario está en un hilo o no
    i=0
    numUsuario=95
    for usuario in usuarios:
        if usuario==id:
            if inthread[i]==False:
                numUsuario=i
                return numUsuario,False
        i=i+1
    return numUsuario,True

def verificarContenido(cantidad,urlpagina,lista_imagenes,lista_codigos): #Verifica si existe contenido en la página
    j=0
    while j<cantidad:
        buffer=""
        index=int(find_nth_overlapping(urlpagina,"thumb",j*2+1))
        buffer=urlpagina[index-34:index-1]+"/cover"
        url = buffer+'.jpg'
        if "png" in urlpagina[index:index+20]: #Se verifica el tipo de imagen que representa el H
            url = buffer+'.png'
        if "gif" in urlpagina[index:index+20]:
            url = buffer+'.gif'
        if "\n" in url: #Se asegura que se haya obtenido una url
            if len(lista_imagenes)!=0: #En el caso de haber obtenido contenido lo manda y en caso contrario manda mensaje
                return lista_imagenes, lista_codigos 
            return "No H in search",None
        index=int(find_nth_overlapping(urlpagina,"class=\"cover\"",j+1)) #Se identifica la ubicación del H dentro de la página
        codigo=urlpagina[index-9:index-3]
        papa=True
        while papa: #Se obtienen los códigos H de las imágenes obtenidas anteriormente
            if "/" in codigo:
                codigo=codigo[codigo.find("/")+1:]
            else: papa=False
        lista_codigos.append(codigo)
        url=url[url.find("https"):]
        page = requests.get(url)
        if page.status_code!=200: #Se identifica si la imagen es gif
            url = buffer+'/.gif'
            page = requests.get(url)
        guardarImagen(lista_imagenes,page) #Guarda el contenido en la lista de imágenes
        j=j+1