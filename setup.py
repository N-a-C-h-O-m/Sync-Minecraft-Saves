import log
from googleapiclient.discovery import build
from drive import authenticate, create_drive_folder, upload_file

creds = authenticate()
service = build("drive", "v3", credentials=creds)

log.write_to_log("Log creado.")
create_drive_folder(service, "backups")
upload_file(service, log.LOCAL_LOG, "log")

'''
Ejecutar una vez en un solo equipo.
CUuando ejecutes este scrip se creara el log y se subira a drive y te mostrara la id de log 
Es el valor que tienes que dar a CLOUD_LOG_ID
'''