import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()

WORLDCUP_API_EMAIL = os.environ.get("WORLDCUP_API_EMAIL")
WORLDCUP_API_PASSWORD = os.environ.get("WORLDCUP_API_PASSWORD")
WORLDCUP_API_URL = "http://api.cup2022.ir/api/v1"

def get_flag(country):
    with open('data/flags.json', 'r') as f:
        flags = json.load(f)
        return flags[country]

def wc_api_login():
    url = WORLDCUP_API_URL + '/user/login'
    data = {'email': WORLDCUP_API_EMAIL, 'password': WORLDCUP_API_PASSWORD}

    # use requests to post the data
    response = requests.post(url, json=data)
    jwt = json.loads(response.text)['data']['token']

    return jwt

def wc_api_get_match_by_date(jwt, date):
    url = WORLDCUP_API_URL + '/match'

    headers = {
        'Authorization': 'Bearer ' + jwt,
        'Content-Type': 'application/json'
    }

    # use requests to post the data
    response = requests.get(url, headers=headers)

    data = json.loads(response.text)['data']

    # filter data with key 'local_date' that contains '11/21/2022'
    data = list(filter(lambda x: date in x['local_date'], data))

    return data