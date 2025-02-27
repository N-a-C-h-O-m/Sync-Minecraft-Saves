from drive import *
from googleapiclient.discovery import build
from log import *
import filecmp

import os

SAVEFILES = "" # Directorio donde guardaras la partida
CURRENT_SAVE = "current_save"
OLD_SAVE = "old_save"
RUNNING_MSG = "Server ejecutandose"
STOP_MSG = "Server parado"

def remove_folder(folder_path):
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                remove_folder(item_path)
        os.rmdir(folder_path)

def download_save(service):
    ids = get_folder_id(service, CURRENT_SAVE)
    if ids is None:
        write_to_log(f"Carpeta {CURRENT_SAVE} no encontrada")

    # I just assume it only exists one folder not the best
    remove_folder(SAVEFILES)
    download_folder(service, ids[0], SAVEFILES)


def upload_save(service):
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
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)
    while True:
        os.system('cls')  # cls (Windows), clear (Linux)
        print("====================== Menu ======================")
        print("1. Iniciar partida")
        print("2. Crear Backup")
        print("q. Salir")
        choice = input("Elige una opción: ")
        
        match choice:
            case '1':
                # Abrir log y ver si hay alguien jugando y última partida guardada
                '''
                Si log_drive =  log_local subir log indicando jugando y empezar
                Si log_drive != log_local y hay alguien jugando indicar por pantalla
                Si log_drive != log_local y no hay alguien jugando descargar partida actualizada
                '''
                download_log(service)
                if not filecmp.cmp("log", SEVER_LOG, shallow=False):
                    with open(SEVER_LOG, 'r') as f:
                        last_line = f.readlines()[-1]
                    msg = extract_message(last_line)
                    if msg == RUNNING_MSG:
                        print("\nALGUIEN ESTA JUGANDO")

                        choice = input("\nPresiona Enter para seguir")
                        if choice != 'm':
                            continue
                    
                    else:
                        download_save(service)

                os.remove(LOCAL_LOG)
                os.rename(SEVER_LOG, LOCAL_LOG)
                write_to_log(RUNNING_MSG)
                upload_log(service)
                print("\nPuedes empezar a jugar")
                while True:
                    choice = input("\nPulsa x cuando acabes ")
                    if choice == 'x':
                        break
                
                upload_save(service)
                write_to_log(STOP_MSG)
                upload_log(service)

            case '2':
                backup_name = f"backup({PC_ID})[{time.ctime(time.time())}]"
                backup_folder_id = get_folder_id(service, "backups")[0]
                upload_folder(service, SAVEFILES, backup_name, backup_folder_id)
                print("\nBackup subida con éxito")
            case 'q':
                break
        
        input("\nPresiona Enter para seguir")

if __name__ == "__main__":
    main()