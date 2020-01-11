import os
import datetime
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class CCDocsHandler:

    def __init__(self, folderID):
        self.SCOPES = \
            [
                'https://www.googleapis.com/auth/drive.file'
            ]
        self.folder_ID = folderID
        # self.folder_ID = '1zFtn4H3DsM3V-az09tJVR_YqFyMAV4q1'
        self.doc_ID = None

        self.drive_service = None
        self.docs_service = None

        self.initializeGoogleDriveDocs()
        self.makeNewDoc()
        print('Started the Google Drive/Docs handler...')


    def setFolderID(self, newfolderID):
        self.folder_ID = newfolderID

    def listQuestions(self, author, new_question):
        str(new_question)
        str(author)
        formatted_question = author + ': ' + new_question.strip('!q ') + '\n'
        self.writeToDoc(formatted_question)

    def writeToDoc(self, question):
        print('Writing question')
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1
                    },
                    'text': question
                }
            }
        ]
        result = self.docs_service.documents().batchUpdate(
            documentId=self.doc_ID, body={'requests': requests}).execute()
        print('Jobs done.')

    def makeNewDoc(self):

        current_date = datetime.datetime.now()
        file_metadata = {
            'name': 'Conservationcast questions from: ' +
                    str(current_date.month) + '/' +
                    str(current_date.day) + '/' +
                    str(current_date.year) + ' at: ' +
                    str(current_date.strftime("%H:%M:%S")),
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [self.folder_ID]
        }
        file = self.drive_service.files().create(body=file_metadata,
                                                 fields='id').execute()
        self.doc_ID = file.get('id')
        print('Folder ID: %s' % file.get('id'))

    # Use this one when setting up - save the folder-id from the output in the FOLDER_ID variable
    def makeNewFolder(self):
        file_metadata = {
            'name': 'Conservationcast question bot test folder',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.drive_service.files().create(body=file_metadata,
                                                 fields='id').execute()
        print('Folder ID: %s' % file.get('id'))

    def chooseFolder(self, chosen_folder_ID):
        str(chosen_folder_ID)
        self.folder_ID = chosen_folder_ID
        print('Folder ID set to: ' + chosen_folder_ID)

    def initializeGoogleDriveDocs(self):
        creds = self.getCredentials()
        self.setDriveService(creds)
        self.setDocsService(creds)

    def setDriveService(self, creds):
        self.drive_service = build('drive', 'v3', credentials=creds)

    def setDocsService(self, creds):
        self.docs_service = build('docs', 'v1', credentials=creds)

    def getCredentials(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    './credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds
