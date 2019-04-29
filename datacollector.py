import time
import random
import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
url = "http://IPADDRESSHERE/api/current?apikey=KEY"

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('YOUR CREDENTIALS FILE HERE', scope)

gc = gspread.authorize(credentials)

sheet = gc.open_by_key("YOUR SPREAD SHEET ID HERE")
sh = sheet.sheet1
reauthCounter = 0
refreshInterval = 5
while True:
        time.sleep(refreshInterval)
        reauthCounter += 1
        if reauthCounter >= (60 * 60) / refreshInterval:
                gc.login()
                reauthCounter = 0
        response = requests.get(url)
        if (response.ok):
                jData = json.loads(response.content)
                current = jData
                if current != 0.0:
                        sh.append_row([time.time(),current])
        else:
                response.raise_for_status()
