#!/usr/bin/python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import httplib2
import webbrowser
import datetime
from apiclient import errors
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from config import CLIENT_ID, CLIENT_SECRET

def GDriveUpload(photoList, folder_name):
    """
    Create a public director and upload photos.
    
    Args:
      (list) photoList: photos to be uploaded
    Returns:
      (dictionary) a dictionary of uploaded photos and their public link
    """
    # Check https://developers.google.com/drive/scopes for all available scopes
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

    # Redirect URI for installed apps
    REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,redirect_uri=REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    print 'Go to the following link in your browser: ' + authorize_url
    # Open the web to get an authorization code
    webbrowser.open_new(authorize_url)
    # User inputs the authorization code
    code = raw_input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)

    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    # Build a Google Drive service
    drive_service = build('drive', 'v2', http=http)

    # Create a public folder on Google Drive
    folder = create_public_folder(drive_service, folder_name + "-" + datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
    # Get the folder from the replied data
    folder_id = folder['id']

    # Insert files
    links = {}
    for photo in photoList:     
        file = insert_file(drive_service, photo.split("/")[-1], "video frame of road", folder_id, 'image/jpeg', photo)
        print photo + " uploaded!"
        # Get the public web link of the uploaded photo
        templink = file['webContentLink'].strip().split("&")[0]
        links[photo] = templink
    return links


def create_public_folder(service, folder_name):
    """
    Create a public folder on Google Drive

    Args:
      service: the Google drive service 
      (String) folder_name: the name of the folder that is going to be created
    Returns:
      (dictionary) information of the created folder
    """
    # Parameters for uploading photos
    body = {
      'title': folder_name,
      'mimeType': 'application/vnd.google-apps.folder'
    }
    
    # Insert the photo
    file = service.files().insert(body=body).execute()

    # Parameters for setting photo privacy
    permission = {
      'value': '',
      'type': 'anyone',
      'role': 'reader'
    }
    
    # Set photo privacy
    service.permissions().insert(fileId=file['id'], body=permission).execute()
    return file


def insert_file(service, title, description, parent_id, mime_type, filename):
    """
    Insert new file.

    Args:
      service: Drive API service instance.
      (String) title: Title of the file to insert, including the extension.
      (String) description: Description of the file to insert.
      (String) parent_id: Parent folder's ID.
      (String) mime_type: MIME type of the file to insert.
      (String) filename: Filename of the file to insert.
    Returns:
      (dictionary) Inserted file metadata if successful, None otherwise.
    """
    # Parameters for uploading photos
    media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
    body = {
      'title': title,
      'description': description,
      'mimeType': mime_type
    }
    # Set the parent folder.
    if parent_id:
        body['parents'] = [{'id': parent_id}]

    try:
        # Insert a photo
        file = service.files().insert(
            body=body,
            media_body=media_body).execute()
        return file
    except errors.HttpError, error:
        print 'An error occured: %s' % error
        return None


def retrieve_all_files(service):
  """Retrieve a list of File resources.

  Args:
    service: Drive API service instance.
  Returns:
    List of File resources.
  """
  result = []
  page_token = None
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      files = service.files().list(**param).execute()

      result.extend(files['items'])
      page_token = files.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      break
  return result    
