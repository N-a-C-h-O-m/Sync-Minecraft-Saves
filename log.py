import time
from drive import authenticate, upload_file, download_file
from googleapiclient.discovery import build

PC_ID = 1
LOCAL_LOG = "log"
CLOUD_LOG_ID = ""

def write_to_log(message):
    with open(LOCAL_LOG, "a") as f:
        f.write(f'PC({PC_ID})[{time.ctime(time.time())}]: {message}\n')

def download_log():
    creds = authenticate()
    session = build("drive", "v3", credentials=creds)

    download_file(session, CLOUD_LOG_ID, "server_log")

def upload_log():
    creds = authenticate()
    session = build("drive", "v3", credentials=creds)

    upload_file(session, LOCAL_LOG, "log")