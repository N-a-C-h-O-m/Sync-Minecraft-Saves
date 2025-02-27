# This module provides functions to authenticate with Google Drive and perform file operations.
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
import os
import log

# Define OAuth 2.0 scope for Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']
TOKEN = 'token.json'
CREDENTIALS = 'credentials.json'

'''------------FUNCION AUTENTICACION------------'''
# Authenticate and get credentials
def authenticate():
    creds = None

    # Load existing credentials if available
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)

    # If credentials are invalid, refresh or obtain new ones
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
        creds = flow.run_local_server(port=0)

        # Save credentials for future use
        with open(TOKEN, "w") as token:
            token.write(creds.to_json())

    return creds


'''------------FUNCIONES LISTAR ARCHIVOS Y CARPETAS------------'''
# Function to list files in Google Drive
def list_files(service):
    query = "trashed = false"
    results = service.files().list(q=query ,fields="files(id, name)").execute()
    files = results.get("files", [])

    if not files:
        log.write_to_log("No se encontraron archivos en Google Drive.")
    else:
        log.write_to_log("Archivos en Drive:")
        for file in files:
            log.write_to_log(f"Nombre: {file['name']} | ID: {file['id']}")


# Function to list folders in Google Drive
def list_folders(service):
    query = "mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])

    if not folders:
        log.write_to_log("No se encontraron carpetas en Google Drive.")
    else:
        log.write_to_log("Carpetas en Drive:")
        for folder in folders:
            log.write_to_log(f"Nombre: {folder['name']} | ID: {folder['id']}")


'''------------FUNCIONES BUSCAR ARCHIVO Y CARPETA------------'''
# Function to search for a file in Google Drive
def search_file(service, file_name):
    query = f"name = '{file_name}' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])

    if not files:
        log.write_to_log(f"No se encontró el archivo: {file_name}")
    else:
        for file in files:
            log.write_to_log(f"Archivo encontrado: {file['name']} | ID: {file['id']}")

# Function to search for a folder in Google Drive
def search_folder(service, folder_name):
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])

    if not folders:
        log.write_to_log(f"No se encontró la carpeta: {folder_name}")
    else:
        for folder in folders:
            log.write_to_log(f"Carpeta encontrada: {folder['name']} | ID: {folder['id']}")


'''------------FUNCIONES SUBIR ARCHIVO Y CARPETA------------'''
# Function to upload a file to Google Drive
def upload_file(service, file_path, file_name, folder_id=None):
    file_metadata = {"name": file_name}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    log.write_to_log(f'File uploaded successfully! File ID: {file.get("id")}')
    return file.get("id")


# Function to upload a folder recursively to Google Drive
def upload_folder(service, folder_path, folder_name, parent_folder_id=None):
    # Step 1: Create the root folder in Google Drive
    root_folder_id = create_drive_folder(service, folder_name, parent_folder_id)
    
    # Step 2: Map local directories to Google Drive folders
    folder_id_map = {folder_path: root_folder_id}

    for root, dirs, files in os.walk(folder_path):
        # Step 3: Create subfolders in Google Drive
        for directory in dirs:
            local_folder_path = os.path.join(root, directory)
            parent_id = folder_id_map[root]  # Parent is the Drive folder corresponding to 'root'
            folder_id_map[local_folder_path] = create_drive_folder(service, directory, parent_id)
        
        # Step 4: Upload files to the correct Drive folder
        for file in files:
            file_path = os.path.join(root, file)
            parent_id = folder_id_map[root]  # Upload into the corresponding Drive folder
            upload_file(service, file_path, file, parent_id)

    return root_folder_id

# Function to create a folder in Google Drive
def create_drive_folder(service, folder_name, parent_folder_id=None):
    """Creates a folder in Google Drive and returns its ID."""
    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_folder_id] if parent_folder_id else []
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    log.write_to_log(f"Created folder: {folder_name} (ID: {folder['id']})")
    return folder["id"]


'''------------FUNCIONES DESCARGAR ARCHIVO Y CARPETA------------'''
# Function to download a file from Google Drive
def download_file(service, file_id, save_path):
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    
    done = False
    while not done:
        _, done = downloader.next_chunk()
    
    with open(save_path, 'wb') as f:
        f.write(file.getvalue())

    log.write_to_log(f'File downloaded successfully! Saved as: {save_path}')


# Function to download a folder recursively from Google Drive
def download_folder(service, folder_id, save_path):
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    files = results.get("files", [])

    if not files:
        log.write_to_log("No se encontraron archivos en la carpeta.")
    else:
        for file in files:
            if file["mimeType"] == "application/vnd.google-apps.folder":
                # Recursively download subfolders
                subfolder_path = os.path.join(save_path, file["name"])
                os.makedirs(subfolder_path, exist_ok=True)
                download_folder(service, file["id"], subfolder_path)
            else:
                # Download file
                save_file_path = os.path.join(save_path, file["name"])
                download_file(service, file["id"], save_file_path)


'''------------FUNCIONES EDITAR ARCHIVOS Y CARPETAS------------'''
def  update_file(service, file_id, new_file):
    media = MediaFileUpload(new_file, resumable=True)
    updated_file = service.files().update(fileId=file_id, media_body=media).execute()

    log.write_to_log(f'File updated successfully! File ID: {updated_file.get("id")}')

def remove_folder(service, folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id, mimeType)").execute()
    files = results.get("files", [])

    for file in files:
        if file["mimeType"] == "application/vnd.google-apps.folder":
            remove_folder(service, file["id"])  # Recursively delete subfolders
        else:
            service.files().delete(fileId=file["id"]).execute()  # Delete file

    # Finally, delete the folder itself
    service.files().delete(fileId=folder_id).execute()
    log.write_to_log(f'Folder deleted successfully! Folder ID: {folder_id}')

def rename_folder(service, folder_id, new_name):
    folder_metadata = {"name": new_name}
    updated_folder = service.files().update(fileId=folder_id, body=folder_metadata).execute()

    print(f'Folder renamed successfully! New Name: {updated_folder.get("name")}')
    return updated_folder.get("id")


'''------------FUNCIONES GETID ARCHIVOS Y CARPETAS------------'''
def get_folder_id(service, folder_name):
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])
    ids = []

    if not folders:
        log.write_to_log(f"No folder found with name: {folder_name}")
        return None
    else:
        for f in folders:
            ids.append(f["id"])
        return ids

def get_file_id(service, file_name):
    query = f"name = '{file_name}' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    ids = []

    if not files:
        log.write_to_log(f"No file found with name: {file_name}")
        return None
    else:
        ids = []
        for f in files:
            ids.append(f["id"])
        return ids