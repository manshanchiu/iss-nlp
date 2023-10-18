# Now, let's generate some text
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# openai.api_key = ""



# response = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who won the world series in 2020?"}
#     ]
# )

# message = response
# print("OpenAI's output':\n")
# print(message)

def load_gheet_data(link):
    try:
        scope = ['https://www.googleapis.com/auth/spreadsheets']
        creds = ServiceAccountCredentials.from_json_keyfile_name('./gapi.json', scope)

        # authorize access to the Google Sheet using the credentials
        client = gspread.authorize(creds)

        # open the Google Sheet by its URL or title
        # sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1BiNltufbq1F4iW5SKrtP_QaQ3wxPYPhsfGPBlyvBR7g/edit?usp=sharing').sheet1
        sheet = client.open_by_url(link)
        # or
        # sheet = client.open('your_sheet_title').sheet1

        # read data from the Google Sheet
        # data = sheet.get_all_values()
        return sheet
    except:
        print("Failed to get gheet")
        raise Exception('Failed to get gheet')
    
gsheet_data = load_gheet_data("https://docs.google.com/spreadsheets/d/14GehTs7xrby0dfcrmLsyfnvh55uPivPvdlO1m83dD2s")
print(gsheet_data)