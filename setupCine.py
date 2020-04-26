import libtorrent as lt
import time
from colorama import init, Fore, Back, Style
from pyfiglet import Figlet
import requests
from utilsText import clearStartAndEnd, generateCode
import sys
import os
import shlex, subprocess
import pymysql
from datetime import datetime
import shutil
from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials


# sudo apt-get install python3-libtorrent
# pip3 install requests
# pip3 install colorama
# pip3 install pyfiglet
# pip3 install gspread
# pip3 install oauth2client
# pip3 install PyOpenSSL

URL = "http://www.omdbapi.com/"


def banner():
    custom_fig = Figlet(font='big')
    banner = custom_fig.renderText('CINE GOTTO DOWNLOAD !!!')
    print( Style.BRIGHT + Fore.WHITE  + banner)

init()



def registerData():
    codeCinema = generateCode()
    
    print(Style.BRIGHT + Fore.GREEN  + "Link magnet torrent ")
    linkTorrent = clearStartAndEnd(str(input(Style.NORMAL + Fore.GREEN + ">  ")))

    print(Style.BRIGHT + Fore.GREEN  + "Nombre ")
    nameCinema = clearStartAndEnd(str(input(Style.NORMAL + Fore.GREEN + ">  ")))

    print(Style.BRIGHT + Fore.GREEN  + "Año ")
    yearCinema = clearStartAndEnd(str(input(Style.NORMAL + Fore.GREEN + ">  ")))

    print(Style.BRIGHT + Fore.GREEN  + "Descripción ")
    descriptionCinema = clearStartAndEnd(str(input(Style.NORMAL + Fore.GREEN  + ">  ")))

    print(Style.BRIGHT + Fore.GREEN  + "Categoria para varios ")
    typesCinemaMore = clearStartAndEnd(str(input(Style.NORMAL + Fore.GREEN + ">  ")))
    
    print(Style.BRIGHT + Fore.GREEN  + "Categoria - tomar el primero ")
    listPelis = "ACCION\nANIME\nAVENTURAS\nCIENCIA-FICCION\nCLASICAS\nCOMEDIA\nDEPORTES\nDOCUMENTALES\nDRAMA\nROMANCE\nTERROR"
    print(listPelis)
    typeCinema = clearStartAndEnd(str(input(Style.NORMAL + Fore.GREEN + ">  ")))


    statusSearch, resultSearch = searchCinema(nameCinema)

    releaseCinema = None
    directorCinema = None
    actorsCinema = None
    countryCinema = None
    pathImgCinema = None

    if(statusSearch == 'True'):
        print(Style.BRIGHT + Fore.GREEN  + "Lanzamiento ")
        releaseCinema = resultSearch["Released"]
        print(Style.NORMAL + Fore.GREEN  + ">  " + releaseCinema)

        print(Style.BRIGHT + Fore.GREEN  + "Director ")        
        directorCinema = resultSearch["Director"]
        print(Style.NORMAL + Fore.GREEN  + ">  " + directorCinema)

        print(Style.BRIGHT + Fore.GREEN  + "Actores ")        
        actorsCinema = resultSearch["Actors"]
        print(Style.NORMAL + Fore.GREEN  + ">  " + actorsCinema   )

        print(Style.BRIGHT + Fore.GREEN  + "Pais ")       
        countryCinema = resultSearch["Country"]
        print(Style.NORMAL + Fore.GREEN  + ">  " + countryCinema   )

        print(Style.BRIGHT + Fore.GREEN  + "URL portada img ")          
        pathImgCinema = resultSearch["Poster"]  
        print(Style.NORMAL + Fore.GREEN  + ">  " + pathImgCinema   )
   
    else:
        print(Style.BRIGHT + Fore.GREEN  + "URL portada img ") 
        pathImgCinema = str(input(Style.NORMAL + Fore.GREEN + ">  "))

    print(Style.BRIGHT + Fore.YELLOW + "Continuar (yes) o Cancelar (no)")
    statusConfirm = str(input(Style.NORMAL + Fore.YELLOW + ">  "))
    if(statusConfirm == "yes"):
        # INICIAR DESCARGA DE PELICULA
        print(Style.BRIGHT + Fore.GREEN + "INICIANDO DESCARGA")
        downloadCinema(linkTorrent)
        print()

        print(Style.BRIGHT + Fore.GREEN  + "Nombre de OneDrive 1 ") 
        accountOneDrive1 = str(input(Style.NORMAL + Fore.GREEN + ">  "))

        print(Style.BRIGHT + Fore.GREEN  + "Nombre de OneDrive 2 ") 
        accountOneDrive2 = str(input(Style.NORMAL + Fore.GREEN + ">  "))

        print(Style.BRIGHT + Fore.GREEN  + "Nombre de MEGA ") 
        accountMega = str(input(Style.NORMAL + Fore.GREEN + ">  "))
        if(accountOneDrive1):
            print()
            uploadCinema(accountOneDrive1,typeCinema)
        if(accountOneDrive2):
            print()
            uploadCinema(accountOneDrive2,typeCinema)
        if(accountMega):
            print()
            uploadCinema(accountMega,typeCinema)
                   
        print()
        print(Style.BRIGHT + Fore.GREEN  + "Link de acceso Onedrive ")
        linkAccessOnedrive = clearStartAndEnd(str(input(Style.NORMAL + Fore.GREEN  + ">  ")))
        shortCutOneDrive = shortCut(linkAccessOnedrive)

        print(Style.BRIGHT + Fore.GREEN  + "Link de acceso Mega ")
        linkAccessMega = clearStartAndEnd(str(input(Style.NORMAL + Fore.GREEN  + ">  ")))
        shortAccessMega = shortCut(linkAccessMega)

        listData = (codeCinema, linkTorrent, nameCinema, yearCinema, descriptionCinema, typesCinemaMore,typeCinema, releaseCinema, directorCinema, actorsCinema, countryCinema, pathImgCinema, datetime.now(), linkAccessOnedrive, linkAccessMega, shortCutOneDrive,shortAccessMega , 0)
        listData2 = (codeCinema, linkTorrent, nameCinema, yearCinema, descriptionCinema, typesCinemaMore,typeCinema, releaseCinema, directorCinema, actorsCinema, countryCinema, pathImgCinema, datetime.now().strftime("%d-%b-%Y %H:%M:%S.%f"), linkAccessOnedrive, linkAccessMega, shortCutOneDrive,shortAccessMega , 0)
        saveDataCinema(listData)
        saveDataExcelDrive(listData2)

        shutil.rmtree('./torrent/')
        os.mkdir("torrent")
    else:
        sys.exit()
    # VERIFICAR QUE TODO ESTE CORRECT
    # DESCARGAR LA PELICULA Y SUBIR A ONEDRIVEPELIS , ONEDRIVEPELIS2, MEGA
    # PEGAR URL DE ACCESO AL VIDEO
    # ACORTAR URL CON DOS ACORTADORES DE PUBLICIDAD Y POR ULTIMO PASAR POR BITLY



def shortCut(urlDestionation):
    urlDestionation = urlDestionation.strip()
    URL = "http://ouo.io/api/key?s={}".format(urlDestionation)
    values = requests.get(URL).text	
    return values


def saveDataCinema(listData):
    try:
        conexion = pymysql.connect(host="x" , 
                                        user="x", 
                                        password="x", 
                                        db="x")
        try:
            with conexion.cursor() as cursor:
                consulta = "INSERT INTO cine_gotto(codeCinema, linkTorrent, nameCinema, yearCinema, descriptionCinema, typesCinema, typeCinema, releaseCinema, directorCinema, actorsCinema, countryCinema, pathImgCinema, dateCreated, linkAccessOnedrive, linkAccessMega, linkAccessShortOnedrive, linkAccessShortMega, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                #Podemos llamar muchas veces a .execute con datos distintos
                cursor.execute(consulta, listData)
            conexion.commit()
        finally:
            conexion.close()
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
    
def saveDataExcelDrive(listData):
    scope = ['x','x']
    credencial = ServiceAccountCredentials.from_json_keyfile_name('./x.json',scope)
    gc = authorize(credencial)
    wks = gc.open('file_name').sheet1
    # 17
    wks.append_row(listData)


def searchCinema(title):    
    API_KEY = "x"
    payload = {'t': title, 'plot': 'full', 'r': 'json', 'apikey': API_KEY}
    values = requests.get(URL, params=payload).json()
    return values["Response"], values


def downloadCinema(linkManget):
    

    # CREDITOS => https://gist.github.com/samukasmk/940ca5d5abd9019e8b1af77c819e4ca9
    folder = "/torrent"
    pathFIle = os.getcwd() + folder
    ses = lt.session()
    ses.listen_on(6881, 6891)
    params = {
        'save_path': pathFIle,
        'storage_mode': lt.storage_mode_t(2),
        'paused': False,
        'auto_managed': True,
        'duplicate_is_error': True}
    link = linkManget
    handle = lt.add_magnet_uri(ses, link, params)
    ses.start_dht()

    print ('downloading metadata...')
    while (not handle.has_metadata()):
        time.sleep(1)
    print ('got metadata, starting torrent download...')
    while (handle.status().state != lt.torrent_status.seeding):
        s = handle.status()
        state_str = ['queued', 'checking', 'downloading metadata', \
                'downloading', 'finished', 'seeding', 'allocating']
        print ('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
                (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                s.num_peers, state_str[s.state]))
        time.sleep(5)

    

def uploadCinema(accountStorage, typeCinema):
    print("INICIANDO SUBIDA CON  LA CUENTA: {}".format(accountStorage))
    typeCinema = typeCinema.upper()
    command = "rclone copy -P   --checkers 1 --transfers 1 --tpslimit 1 --user-agent 'ISV|rclone|rclone/v1.42' ./torrent {}:{}".format(accountStorage,typeCinema)
    command = shlex.split(command)
    subprocess.call(command)
    # os.system(command)



if __name__ == "__main__":
    banner()
    print(Fore.YELLOW+"Bienvenido a CINE GOTTO !!!")
    registerData()


