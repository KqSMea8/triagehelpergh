from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def get_googleCred():
	# If modifying these scopes, delete the file token.pickle.
	SCOPES = ['https://www.googleapis.com/auth/documents.readonly', 'https://www.googleapis.com/auth/spreadsheets']
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
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server()
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)
	return creds

def read_googleDoc(creds, DOCUMENT_ID):
	service = build('docs', 'v1', credentials=creds)
	# Retrieve the documents contents from the Docs service.
	document = service.documents().get(documentId=DOCUMENT_ID).execute()
	body = document.get('body')['content']
	return body


def read_googleSheet(creds, SPREADSHEET_ID, RANGE_NAME):
	# The ID and range of a sample spreadsheet.
	service = build('sheets', 'v4', credentials=creds)
	# Call the Sheets API
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME).execute()
	values = result.get('values', [])
	return values

def append_googleSheet(data,creds, SPREADSHEET_ID, SAMPLE_RANGE_NAME):
	# The ID and range of a sample spreadsheet.
	service = build('sheets', 'v4', credentials=creds)
	# Call the Sheets API
	sheet = service.spreadsheets()

	sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, body=data, valueInputOption='USER_ENTERED').execute()

def update_googleSheet(data, creds, SPREADSHEET_ID):
	# The ID and range of a sample spreadsheet.
	service = build('sheets', 'v4', credentials=creds)
	# Call the Sheets API
	sheet = service.spreadsheets()
	sheet.values().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=data).execute()

def sort_by_column(creds, SPREADSHEET_ID, sheet_id, sortColumn, sortOrder, sortRange):

	startRowIndex, endRowIndex, startColumnIndex, endColumnIndex = sortRange
	requests=[
	{
	  "sortRange": {
	    "range": {
	      "sheetId": sheet_id,
	      "startRowIndex": startRowIndex,
	      "endRowIndex": endRowIndex,
	      "startColumnIndex": startColumnIndex,
	      "endColumnIndex": endColumnIndex
	    },
	    "sortSpecs": [
	      {
	        "dimensionIndex": sortColumn,
	        "sortOrder": sortOrder
	      },
	    ]
	  }
	}
	]

	body = {
		'requests': requests
	}

	service = build('sheets', 'v4', credentials=creds)
	# Call the Sheets API
	sheet = service.spreadsheets()
	sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()

