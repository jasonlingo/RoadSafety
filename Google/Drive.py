#!/usr/bin/python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import httplib2
import webbrowser
import operator
import datetime
from apiclient import errors
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from config import CLIENT_ID, CLIENT_SECRET


def create_public_folder(service, folder_name):
  """create a public folder on Google Drive

  Args:
    service: the Google drive service 
    folder_name: the name of the folder that is going to be created
  Returns:
    information of the created folder
  """

  body = {
    'title': folder_name,
    'mimeType': 'application/vnd.google-apps.folder'
  }

  file = service.files().insert(body=body).execute()

  permission = {
    'value': '',
    'type': 'anyone',
    'role': 'reader'
  }

  service.permissions().insert(fileId=file['id'], body=permission).execute()

  return file


def insert_file(service, title, description, parent_id, mime_type, filename):
  """Insert new file.

  Args:
    service: Drive API service instance.
    title: Title of the file to insert, including the extension.
    description: Description of the file to insert.
    parent_id: Parent folder's ID.
    mime_type: MIME type of the file to insert.
    filename: Filename of the file to insert.
  Returns:
    Inserted file metadata if successful, None otherwise.
  """

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
    file = service.files().insert(
        body=body,
        media_body=media_body).execute()

    # Uncomment the following line to print the File ID
    # print 'File ID: %s' % file['id']

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


def GDriveUpload(photoList, folder_name):
    """create a public director and upload photo
    
    Args:
      photoList: a list of photos to be uploaded
    Returns:
      a list of public link to the uploaded photos
    """
    # Check https://developers.google.com/drive/scopes for all available scopes
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

    # Redirect URI for installed apps
    REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,redirect_uri=REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    print 'Go to the following link in your browser: ' + authorize_url
    webbrowser.open_new(authorize_url)
    code = raw_input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)

    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = credentials.authorize(http)

    drive_service = build('drive', 'v2', http=http)

    # create a public folder
    folder = create_public_folder(drive_service, folder_name+"-"+datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
    folder_id = folder['id']

    # Insert files
    links = {}
    for photo in photoList:     
        file = insert_file(drive_service, photo.split("/")[-1], "video frame of road", folder_id, 'image/jpeg', photo)
        print photo + " uploaded!"
        #linkList[photo] = file['alternateLink']
        templink = file['webContentLink'].strip().split("&")[0]
        links[photo] = templink
    return links
