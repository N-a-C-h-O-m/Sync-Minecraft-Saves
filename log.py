import time
import drive

PC_ID = 1
LOCAL_LOG = "log"
SEVER_LOG = "server_log"

def write_to_log(message):
    with open(LOCAL_LOG, "a") as f:
        f.write(f'PC({PC_ID})[{time.ctime(time.time())}]: {message}\n')

def extract_message(logline):
    return logline.split(']: ')[1]

def download_log(service):
    log_id = drive.get_file_id(service, "log")[0];
    drive.download_file(service, log_id, SEVER_LOG)

def upload_log(service):
    log_id = drive.get_file_id(service, "log")[0];
    drive.update_file(service, log_id, LOCAL_LOG)