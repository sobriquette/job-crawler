import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Write results to Google Sheets
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scopes=SCOPE)
file = gspread.authorize(credentials)
sheet = file.open("Job Listings").sheet1
cell_count = 2

with open('jobs.csv') as jobs_data:	
	for line in jobs_data:
		data = line.split(',')
		if 'Engineer' in data[0]:
			sheet.update_acell('A{}'.format(cell_count), data[0])
			sheet.update_acell('B{}'.format(cell_count), data[-1])
			cell_count += 1
