from drive import *
from googleapiclient.discovery import build
from log import *

import os

SAVEFILES = "" # Directorio donde guardaras la partida
BACKUPS_ID = ""
SAVES_ID = ""
CURRENT_SAVE = "current_save"
OLD_SAVE = "old_save"


def remove_folder(folder_path):
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                remove_folder(item_path)
        os.rmdir(folder_path)

def download_save():
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    ids = get_folder_id(service, CURRENT_SAVE)
    if ids is None:
        write_to_log(f"Carpeta {CURRENT_SAVE} no encontrada")

    # I just assume it only exists one folder not the best
    remove_folder(SAVEFILES)
    download_folder(service, ids[0], SAVEFILES)


def upload_save():
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    ids = get_folder_id(service, CURRENT_SAVE)
    if ids is None:
        write_to_log(f"Carpeta {CURRENT_SAVE} no encontrada")
    else:
        for i in ids:
            rename_folder(service, i, OLD_SAVE)

    ids = get_folder_id(service, OLD_SAVE)
    if ids is None:
        write_to_log(f"Carpeta {OLD_SAVE} no encontrada")
    else:
        for i in ids:
            remove_folder(service, i)

    upload_folder(service, SAVEFILES, CURRENT_SAVE)


def main():
    while True:
        os.system('cls')  # cls (Windows), clear (Linux)
        print("====================== Menu ======================")
        print("1. Iniciar partida")
        print("2. Crear Backup")
        print("3. Cargar backup")
        print("q. Salir")
        choice = input("Elige una opción: ")
        
        match choice:
            case 1:
                # Abrir log y ver si hay alguien jugando y última partida guardada
                '''
                Si log_drive =  log_local subir log indicando jugando y empezar
                Si log_drive != log_local y hay alguien jugando indicar por pantalla
                Si log_drive != log_local y no hay alguien jugando descargar partida actualizada
                '''
                # Si no subir log informando
                # Descargar partida si es necesario
                # Indicar ok
                # Esperar a que acabe la partida
                # Subir partida y actualizar log
                pass
            case 2:
                # Subir partida como backup(fecha y hora)
                pass
            case 3:
                # Mostrar lista con todas las backups disponibles
                # Sustituir guardado nube y local por backup, INDICANDO BORRADO DE DATOS
                pass
            case 'q':
                break
        
        input("\nPresiona Enter para seguir")

if __name__ == "__main__":
    main()