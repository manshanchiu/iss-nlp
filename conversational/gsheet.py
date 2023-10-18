import gspread
from oauth2client.service_account import ServiceAccountCredentials

# define the scope and credentials for accessing the Google Sheet
scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('./gapi.json', scope)

# authorize access to the Google Sheet using the credentials
client = gspread.authorize(creds)

# open the Google Sheet by its URL or title
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/14GehTs7xrby0dfcrmLsyfnvh55uPivPvdlO1m83dD2s').sheet1
# or
# sheet = client.open('your_sheet_title').sheet1

# read data from the Google Sheet
data = sheet.get_all_values()

# print the data
print(data[0])
print(data[1])