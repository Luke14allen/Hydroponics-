import time
from datetime import datetime, timezone
from Google import Create_Service
import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from flask import Flask, request
import uuid
import platform
import os

app = Flask(__name__)

CLIENT_SECRET_FILE = 'secret_file.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

#dictionary to track check times for each folder
last_check_times = {}

def list_new_files_in_folder(service, folder_id, last_check_time):
    query = f"'{folder_id}' in parents and trashed = false and (createdTime > '{last_check_time.isoformat()}' or modifiedTime > '{last_check_time.isoformat()}')"
    results = service.files().list(q=query, fields="files(id, name, createdTime)").execute()
    return results.get('files', [])

#used to set and get Folder ids
def setFolderId(id):
    response = service.files().list(
        q=f"'{id}' in parents",
        fields = "nextPageToken, files(id, name)"
    ).execute()
    return response.get("files", [])

def download_file(service, file_id, file_name, folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        path = os.path.join(folder_path, file_name)
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fh.seek(0)

        with open(path, 'wb') as f:
            f.write(fh.read())
        print(f"File '{file_name}' downloaded successfully.")
    except HttpError as error:
        print(f"An error occurred while downloading '{file_name}': {error}")

@app.route('/webhook', methods=['POST'])
def webhook():

    print("Webhook triggered! Checking for new files...")
    
    for name, id in folderIds.items():
        last_check_time = last_check_times.get(id, datetime.now(timezone.utc))

        new_files = list_new_files_in_folder(service, id, last_check_time)
    
        if new_files:
            print(f"\nFound {len(new_files)} new file(s):")
            for file in new_files:
                print(f"Downloading: {file['name']} (ID: {file['id']})")
                if name == 'sensor_data':
                    download_file(service, file['id'], file['name'], 'data')
                elif name == 'images':
                    download_file(service, file['id'], file['name'], 'images')
        else:
            print("No new files found.")
        
        last_check_times[id] = datetime.now(timezone.utc)
    return "OK", 200

def setup_webhook(folder_id, webhook_url):
    try:
        uniqueid = str(uuid.uuid4())
        body = {
            'id': uniqueid,
            'type': 'web_hook',
            'address': webhook_url
        }
        service.files().watch(fileId=folder_id, body=body).execute()
        print("Webhook set up successfully!")
    except HttpError as error:
        print(f"An error occurred setting up the webhook: {error}")

if __name__ == "__main__":
    ngrok_url = input("Enter your ngrok HTTPS URL: ")
    webhook_url = f"{ngrok_url}/webhook"
    parentid = None
    folderIds = {}
    filepath = ["data", "images"]
    
    
    result = (service.files()
           .list(fields = "nextPageToken, files(id, name)")
           .execute())
    files = result.get("files", [])

    for file in files:
        if(file['name'] == "DevNet-Test"):
            parentid = file['id']
    
    if(parentid):
        subfolders = setFolderId(parentid)

    for folder in subfolders:
        if folder['name'] == 'images' or folder['name'] == 'sensor_data':
            folderIds[folder['name']] = folder['id']
    
    for path in filepath:
        if not os.path.exists(path):
            os.makedirs(path)
            
    items = os.listdir(path)
    download = [f for f in items if os.path.isfile(os.path.join(path, f))]
    if not download:
        for id in folderIds.values():
                    files = setFolderId(id)
                    for file in files:
                        if os.path.splitext(file['name'])[1] == ".csv":
                            download_file(service, file['id'], file['name'], 'data')
                        else:
                            download_file(service, file['id'], file['name'], 'images')
                    
    for id in folderIds.values():
        last_check_times[id] = datetime.now(timezone.utc)
    
    for id in folderIds.values():
        setup_webhook(id, webhook_url)
    
    print("Starting Flask server...")
    app.run(port=5000)
