from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive']

# The ID and range of a sample spreadsheet.
#06288052658033293223
SAMPLE_SPREADSHEET_ID = '1gcHzsXx6Vmhg5lxTeDKFFQL6WZveI3AvAr_dBW43FJI'
SAMPLE_RANGE_NAME = 'A2:H84'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/jweezy/Downloads/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    drive = build('drive', 'v2', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    permissions = drive.permissions()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        pageIDS = []
        for row in values:
            pageIDS.append(row[5].split('/')[3].split('=')[1])
        request = {
            "role": "reader",
            "type": "anyone",
            "withLink": True
        }
        #permission = service.permissions().get(
        #fileId=file_id, permissionId="anyoneWithLink".execute()

        #for i in pageIDS:
        permissions.insert(fileId="1w_Ipa_xeVjI8tsbsyCQG4bgGT2VN2RykTPWPX1_u_JE", body=request)


main()
