import requests
from urllib3.exceptions import InsecureRequestWarning
from PIL import Image
import constantes as llaves

def collect_search(texto,cantidad):
    lista_imagenes=[]
    lista_codigos=[]
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    session = requests.Session()
    session.verify = False
    url,texto=correcturl(texto)
    page = requests.get(url,verify=False) #Se almacena el contenido de la pagina en una variable
    if page.status_code==200:
        verificarContenido(cantidad,page.text,lista_imagenes,lista_codigos)
        return lista_imagenes,lista_codigos
    return "No H in search",None
def guardarImagen(lista_imagenes,page):
    lista_imagenes.append(page.content)

def download_image(code,tipo):
    lista_imagenes=[]
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    session = requests.Session()
    session.verify = False 
    url = llaves.URL_IMG+code+"/"
    page = requests.get(url,verify=False) #Se almacena el contenido de la pagina en una variable
    if page.status_code==200:
        urlpagina=geturlpagina(page.text)
        more=True
        i=1
        while(more is True):
            page,more=getimages(urlpagina,True,i)
            if more:
                guardarImagen(lista_imagenes,page)
            i=i+1
    if len(lista_imagenes)==0:
        return "H not founded"
    return lista_imagenes

def checanum(a):
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

def find_nth_overlapping(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+1)
        n -= 1
    return start
    
def correcturl(text):
    url=llaves.URL_SEARCH
    urlfinal=setpage(text)
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

def setpage(text):
    if "page:" in text:
        if " page: " in text:
            texto=text[text.find("page: ")+6:]
        else: texto=text[text.find("page:")+5:]
        if ":" in text[:text.find("page:")]:
            return llaves.TAGPAGE+texto
        return llaves.SEARCHPAGE+texto
    return ""

def getimages(urlpagina,more,i):
    url = urlpagina+'/'+str(i)+'.jpg' #Se ingresa a la direccion url de cada imagen de hentai
    page = requests.get(url) #Se almacena el contenido de la pagina en una variable
    if page.status_code!=200:
        url = urlpagina+'/'+str(i)+'.png' #Se ingresa a la direccion url de cada imagen de hentai
        page = requests.get(url) #Se almacena el contenido de la pagina en una variable
        if page.status_code!=200:
            url = urlpagina+'/'+str(i)+'.gif' #Se ingresa a la direccion url de cada imagen de hentai
            page = requests.get(url) #Se almacena el contenido de la pagina en una variable
            if page.status_code!=200:
                more=False
    return page,more

def geturlpagina(urlpagina):
    if "cover.jpg" in urlpagina:
        urlpagina=urlpagina[urlpagina.find("cover.jpg",2)-34:urlpagina.find("cover.jpg",2)]
    else:
        if "cover.png" in urlpagina:
            urlpagina=urlpagina[urlpagina.find("cover.png",2)-34:urlpagina.find("cover.png",2)]
        else: urlpagina=urlpagina[urlpagina.find("cover.gif",2)-34:urlpagina.find("cover.gif",2)]
    return urlpagina[urlpagina.find("https",0):len(urlpagina)-1]

def enHilo(usuarios,inthread,id):
    i=0
    numUsuario=95
    for usuario in usuarios:
        if usuario==id:
            if inthread[i]==False:
                numUsuario=i
                return numUsuario,False
        i=i+1
    return numUsuario,True

def verificarContenido(cantidad,urlpagina,lista_imagenes,lista_codigos):
    j=0
    while j<cantidad:
        buffer=""
        index=int(find_nth_overlapping(urlpagina,"thumb",j*2+1))
        buffer=urlpagina[index-34:index-1]+"/cover"
        url = buffer+'.jpg' #Se ingresa a la direccion url de cada imagen de hentai
        if "png" in urlpagina[index:index+20]:
            url = buffer+'.png' #Se ingresa a la direccion url de cada imagen de hentai
        if "gif" in urlpagina[index:index+20]:
            url = buffer+'.gif' #Se ingresa a la direccion url de cada imagen de hentai
        if "\n" in url:
            if len(lista_imagenes)!=0:
                return lista_imagenes, lista_codigos
            return "No H in search",None
        index=int(find_nth_overlapping(urlpagina,"class=\"cover\"",j+1))
        codigo=urlpagina[index-9:index-3]
        papa=True
        while papa:
            if "/" in codigo:
                codigo=codigo[codigo.find("/")+1:]
            else: papa=False
        lista_codigos.append(codigo)
        url=url[url.find("https"):]
        page = requests.get(url) #Se almacena el contenido de la pagina en una variable
        if page.status_code!=200:
            url = buffer+'/.gif' #Se ingresa a la direccion url de cada imagen de hentai
            page = requests.get(url) #Se almacena el contenido de la pagina en una variable
        guardarImagen(lista_imagenes,page)
        j=j+1