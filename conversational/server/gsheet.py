import gspread
from oauth2client.service_account import ServiceAccountCredentials

class Gheet:
    def __init__(self, link):
        self.link = link
    def load_sheet(self):
        try:
            scope = ['https://www.googleapis.com/auth/spreadsheets']
            creds = ServiceAccountCredentials.from_json_keyfile_name('./gapi.json', scope)

            # authorize access to the Google Sheet using the credentials
            client = gspread.authorize(creds)

            # open the Google Sheet by its URL or title
            # sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1BiNltufbq1F4iW5SKrtP_QaQ3wxPYPhsfGPBlyvBR7g/edit?usp=sharing').sheet1
            sheet = client.open_by_url(self.link)
            # or
            # sheet = client.open('reviews_for_classification').sheet1
            sheet = sheet.sheet1
            # read data from the Google Sheet
            data = sheet.get_all_values()
            # return sheet
            return data
        except:
            print("Failed to get gheet")
            raise Exception('Failed to get gheet')
    def to_dict(self, data):
        # convert data to a dictionary
        keys = data[0]
        keys = [x.lower() for x in keys]
        values = data[1:]
        list_of_dicts = [dict(zip(keys, values)) for values in values]
        return list_of_dicts