import os
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def authenticate():
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_info(info=None, scopes=SCOPES)
    if not creds or creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

      print("Saving credentials...",creds)

      if creds:
        with open("token.json", "w") as token:
          token.write(creds.to_json())

      else:
        print("Failed to authenticate.")
        return creds
        







def list_files_in_folder(service, folder_id, last_check_time):
    query = f"'{folder_id}' in parents and trashed=false and modifiedTime > '{last_check_time}'"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
    return results.get("files", [])

def download_file(service, file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    file.seek(0)
    with open(file_name, "wb") as f:
        f.write(file.read())

def process_data(file_name):
    print(f"Processing file: {file_name}")
    
    # Determine the file type (e.g., csv, json, txt) based on the file extension
    file_extension = file_name.split('.')[-1].lower()
    
    try:
        if file_extension == 'csv':
            # Process CSV file
            import pandas as pd
            df = pd.read_csv(file_name)
            
            # Example operations:
            # 1. Remove any rows with missing values
            df = df.dropna()
            
            # 2. Convert a date column to datetime
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            
            # 3. Perform some calculations
            if 'value' in df.columns:
                df['squared_value'] = df['value'] ** 2
            
            # 4. Save the processed data
            processed_file_name = f"processed_{file_name}"
            df.to_csv(processed_file_name, index=False)
            print(f"Processed data saved to {processed_file_name}")
            
        
            # Save the processed data
            processed_file_name = f"processed_{file_name}"
            with open(processed_file_name, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Processed data saved to {processed_file_name}")
            
        elif file_extension == 'txt':
            # Process text file
            with open(file_name, 'r') as file:
                content = file.read()
            
            # Example: Convert text to uppercase
            processed_content = content.upper()
            
            # Save the processed data
            processed_file_name = f"processed_{file_name}"
            with open(processed_file_name, 'w') as file:
                file.write(processed_content)
            print(f"Processed data saved to {processed_file_name}")
            
        else:
            print(f"Unsupported file type: {file_extension}")
    
    except Exception as e:
        print(f"Error processing {file_name}: {str(e)}")
    
    print(f"Finished processing {file_name}")

def main():
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)
    
    folder_id = "https://drive.google.com/drive/folders/1pMX_mGXn0GKd5QZ3SCXajqPXlt1XLXu9?usp=drive_link"
    last_check_time = "1970-01-01T00:00:00"  # Start from the beginning of time
    
    while True:
        try:
            print("Checking for new files...")
            new_files = list_files_in_folder(service, folder_id, last_check_time)
            
            for file in new_files:
                print(f"New file found: {file['name']}")
                download_file(service, file['id'], file['name'])
                process_data(file['name'])
            
            if new_files:
                last_check_time = time.strftime("%Y-%m-%dT%H:%M:%S")
            
            # Wait for some time before checking again (5 minutes)
            time.sleep(300)
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            break

if __name__ == "__main__":
    main()
