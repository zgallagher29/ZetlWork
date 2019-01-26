from __future__ import print_function
import io
from apiclient.http import MediaIoBaseDownload

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive.metadata'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

files = DRIVE.files().list().execute().get('files', [])

print(files[1]['id'])
file_id = files[1]['id']


# ideas: read the file into dataframe and then maybe match some rows with common words and put them into note card?
from apiclient import errors
from apiclient import http
# ...

def print_file_metadata(service, file_id):
  """Print a file's metadata.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to print metadata for.
  """
  try:
    file = service.files().get(fileId=file_id).execute()

    print ('Title: %s' % file['title'])
    print ('MIME type: %s' % file['mimeType'])
  except ():
    print ('An error occurred: %s' % error)


print_file_metadata(DRIVE,file_id)
Uses the Python client library.

from apiclient import errors
# ...

def print_about(service):
  """Print information about the user along with the Drive API settings.

  Args:
    service: Drive API service instance.
  """
  try:
    about = service.about().get().execute()

    print 'Current user name: %s' % about['name']
    print 'Root folder ID: %s' % about['rootFolderId']
    print 'Total quota (bytes): %s' % about['quotaBytesTotal']
    print 'Used quota (bytes): %s' % about['quotaBytesUsed']
  except errors.HttpError, error:
    print 'An error occurred: %s' % error