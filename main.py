from drive import *

import os

LOCAL_LOG = "log.txt"
SAVEFILES = "" # Directorio donde guardaras la partida

def download_save():
    pass

def upload_save():
    pass

def download_log():
    pass

def upload_log():
    pass

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