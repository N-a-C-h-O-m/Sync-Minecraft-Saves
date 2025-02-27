import time
from drive import download_file, update_file

PC_ID = 1
LOCAL_LOG = "log"
CLOUD_LOG_ID = ""

def write_to_log(message):
    with open(LOCAL_LOG, "a") as f:
        f.write(f'PC({PC_ID})[{time.ctime(time.time())}]: {message}\n')

def download_log(service):
    download_file(service, CLOUD_LOG_ID, "server_log")

def upload_log(service):
    update_file(service, CLOUD_LOG_ID, LOCAL_LOG)