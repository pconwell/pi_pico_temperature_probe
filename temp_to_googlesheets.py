import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import serial
import re
from datetime import datetime


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREEADSHEET_ID = "1IkLTiT4nJygvy1z8A3qt64Liemnv4ty0Zyc3vbx20AY"
VALUE_INPUT_OPTION = "USER_ENTERED"
# VALUE_INPUT_OPTION = "RAW"
RANGE_ID = "Sheet1"

ser = serial.Serial('/dev/ttyACM0', 9600)
# line = re.split(r'[:;,\s]\s*', ser.readline().decode("utf-8".rstrip()))

def get_data():
    line = re.split(r'[:;,\s]\s*', ser.readline().decode("utf-8".rstrip()))

#    print(line, type(line[1]), type(line[3]))
    if line[0] == "Temperature":
#        print("a")
        return line

    else:
#        print("b")
        line = get_data()
        return line


def get_credentials(cred_file):
    if os.path.exists(cred_file):
        with open(cred_file, 'rb') as token:
            creds = pickle.load(token)
            print("Credentials Found!")
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            print("No credentials found!\nGenerating Credentials...")

    # if creds.expired and creds.refresh_token:
    #     creds.refresh(Request())
    #     print("Credentials Expired! \nRefreshing Credentials...")

    return creds

line = get_data()
#print(line)


# print(datetime.now(), line[1], line[3])

# credentials = GoogleCredentials.get_application_default()
service = build('sheets', 'v4', credentials=get_credentials('/home/pi/ac_temp/token.pickle'))

# list = [["Api", "B", "C", "D"]]
# list = [[str(datetime.now()), str(line[1]), str(line[3])]]
list = [[str(datetime.now()), line[1], line[3]]]


print(list)

data = {
  "majorDimension": "ROWS",
  "values": list
}
spreadsheetId = SPREEADSHEET_ID
range = RANGE_ID
service.spreadsheets().values().append(
  spreadsheetId=spreadsheetId,
  range=range,
  body=data,
  valueInputOption=VALUE_INPUT_OPTION
).execute()
