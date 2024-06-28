import json

import requests


def get_json_by_url(url:str):
    res=requests.get(url)
    return json.loads(res.content.decode('utf-8'))