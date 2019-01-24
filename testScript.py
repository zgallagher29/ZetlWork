from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1gcHzsXx6Vmhg5lxTeDKFFQL6WZveI3AvAr_dBW43FJI'
SAMPLE_RANGE_NAME = 'A2:H85'

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

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        dict = {}
        courseSec = ''
        secondCourse = ''
        doubleClass = False
        Syllabus = ''
        for row in values:
            print(row)
            if (row[4] != '' and int(row[4]) < 10 and len(row[4]) > 1):
                courseSec = str(row[3]) +"-" + str(row[4])
            elif (row[4] != '' and int(row[4]) > 100 and int(row[4]) < 400):
                courseSec = str(row[3]) +"-" + str(row[4])
            elif (row[4] != '' and int(row[4]) < 10 and len(row[4]) <= 1):
                courseSec = str(row[3]) +"-00" + str(row[4])
            else:
                courseSec = str(row[3])
            Syllabus = row[5]
            instructor = row[1]
            semester = row[2]
            if (row[6] == 'Yes'):
                if(len(row) == 8 and row[7] == 'Yes'):
                    if('388' in courseSec):
                        dict.update({(courseSec,semester,instructor):Syllabus})
                        secondCourse = courseSec
                        secondCourse = "462" + secondCourse[3:]
                        dict.update({(secondCourse,semester, instructor): Syllabus})
                    else:
                        dict.update({(courseSec,semester,instructor):Syllabus})
                        secondCourse = str(int(row[3]) + 100)
                        dict.update({(secondCourse,semester, instructor): Syllabus})

                if(doubleClass):
                    dict.update({(courseSec,semester,instructor):Syllabus})
                    dict.update({(secondCourse,semester, instructor): Syllabus})
                    doubleClass = False
                else:
                    dict.update({(courseSec,semester,instructor):Syllabus})
        generateAllSyllabi(dict)
        generateClassesByProfessor(dict)
        generateSemesterSyllabi(dict)

def generateSemesterSyllabi(dict):
    template = '''   "COMP {0}", "{1}", "{2}", "`PDF <{3}>`_"\n'''
    keys = dict.keys()
    keys = sorted(keys)
    for j in keys:
        header ='''
********************************
{4} Syllabi
********************************
.. csv-table::
   :header: "{0}", "{1}", "{2}", "{3}"
   :widths: 20, 10, 20, 40
    \n'''
        file = open(str(j[1]).replace(' ', '_').lower()+"_syllabi.rst", "w")
        file.write(header.format("Class", "Professor", "Semester", "Syllabi", j[1]))
        for i in keys:
            temp = dict.get(i)
            print(i)
            if(i[1] == j[1]):
                file.write(template.format(i[0], i[2], i[1], temp))
        file.close()

def generateClassesByProfessor(dict):
    template = '''   "COMP {0}", "{1}", "{2}", "{3}"\n'''
    keys = dict.keys()
    file2 = open('classes_by_professors.rst', 'w')
    header2 ='''
********************************
Classes By Professor Information
********************************
.. csv-table::
   :header: "{0}", "{1}", "{2}", "{3}"
   :widths: 20, 10, 20, 40
\n'''
    file2.write(header2.format("Professor", "Class", "Semester", "Syllabus"))
    keys = sorted(keys, key=lambda tup: tup[2].lower())
    for i in keys:
        temp = dict.get(i)
        print(i)
        file2.write(template.format(i[2], i[0], i[1], temp))
    file2.close()

def generateAllSyllabi(dict):
    header ='''
********************
Syllabus Information
********************
.. csv-table::
   :header: "{0}", "{1}", "{2}", "{3}"
   :widths: 10, 20, 20, 40
\n'''
    template = '''   "Comp {0}", "{1}", "{2}", "{3}"\n'''
    header.format("Course", "Professor", "Semester", "Syllabus")
    file = open("./all_syllabi.rst","w")
    file.write(header.format("Course", "Professor", "Semester", "Syllabus"))
    keys = dict.keys()
    keys = sorted(keys)
    for i in keys:
        temp = dict.get(i)
        print(i)
        file.write(template.format(i[0], i[2], i[1], temp))
    file.close()



if __name__ == '__main__':
    main()
