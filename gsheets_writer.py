import json
import os
import csv
import httplib2

from pprint import pprint
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

# Write results to Google Sheets
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Job Listing Crawler'

def get_credentials():
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir, CREDENTIALS_FILE)

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CREDENTIALS_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else:
			credentials = tools.run(flow, store)

	return credentials

def update_sheet():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
					'version=v4')
	service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
	spreadsheet_id = "1hLuinub18OTaCb0Q54_7RXUjv0CMbH-GBGJeQ1fRp-E"

	batch_update_request_body = {
		'valueInputOption': "USER_ENTERED",
		'data': {
			'range': 'Sheet1',
			'majorDimension': "ROWS",
			'values': []
		}
	}

	with open('jobs.csv') as jobs_data_file:
		jobsreader = csv.reader(jobs_data_file, delimiter=',')
		for line in jobsreader:
			jobs_data_to_keep = [line[0], line[-1]]
			batch_update_request_body['data']['values'].append(jobs_data_to_keep)

	request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=batch_update_request_body)
	response = request.execute()

	pprint(response)

def main():
	update_sheet()