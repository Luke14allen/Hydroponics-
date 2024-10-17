import time
from datetime import datetime, timezone
from Google import Create_Service
import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from flask import Flask, request

app = Flask(__name__)

CLIENT_SECRET_FILE = 'secret_file.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# Replace 'your_images_folder_id' with the actual ID of your images folder
last_check_time = datetime.now(timezone.utc)

def list_new_files_in_folder(service, folder_id, last_check_time):
    query = f"'{folder_id}' in parents and trashed = false and createdTime > '{last_check_time.isoformat()}'"
    results = service.files().list(q=query, fields="files(id, name, createdTime)").execute()
    return results.get('files', [])

#used to set and get Folder ids
def setFolderId(id):
    response = service.files().list(
        q=f"'{id}' in parents",
        fields = "nextPageToken, files(id, name)"
    ).execute()
    return response.get("files", [])


def download_file(service, file_id, file_name):
    try:
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fh.seek(0)

        with open(file_name, 'wb') as f:
            f.write(fh.read())
        print(f"File '{file_name}' downloaded successfully.")
    except HttpError as error:
        print(f"An error occurred while downloading '{file_name}': {error}")

@app.route('/webhook', methods=['POST'])
def webhook():
    global last_check_time
    print("Webhook triggered! Checking for new files...")
    
    new_files = list_new_files_in_folder(service, images_folder_id, last_check_time)
    
    if new_files:
        print(f"\nFound {len(new_files)} new file(s):")
        for file in new_files:
            print(f"Downloading: {file['name']} (ID: {file['id']})")
            download_file(service, file['id'], file['name'])
    else:
        print("No new files found.")
    
    last_check_time = datetime.now(timezone.utc)
    return "OK", 200

def setup_webhook(folder_id, webhook_url):
    try:
        body = {
            'id': 'my-webhook',
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
    images_folder_id = None
    data_folder_id = None

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
        if(folder['name'] == 'images'):
            images_folder_id = folder['id']
        elif(folder['name'] == 'sensor_data'):
            data_folder_id = folder['id']

    setup_webhook(images_folder_id, webhook_url)
    
    print("Starting Flask server...")
    app.run(port=5000)
