# query github using apis
from gettext import install
import sys, requests
sys.path.append("././")

import json5 as json

from typing import List
from app.models.installation import Installation
from app.models.jwt_query import JWTQuery

def query_installations(query: JWTQuery) -> List[Installation]:
    result: List[Installation] = []
    try:
        headers = query.headers
        url = query.url

        page = 1
        per_page = 100
        while(True):
            urlNew = url + "?per_page=%s&page=%s" % (per_page, page)
            response = requests.get(urlNew, headers=headers)
            if response.status_code != 200:
                raise Exception("error with func auth: code: %s, message: %s" % (response.status_code, json.loads(response.text)["message"]))
            installations = response.json()
            result.extend([Installation(id=installation["id"], app_id=installation["app_id"]) for installation in installations])
            if len(installations) < per_page:
                break
            else:
                page += 1
    except Exception as e:
        print("error with func query_installations: %s" % (repr(e)))
    finally:
        return result



def query_access_token(query: JWTQuery) -> str:
    result: str = None
    try:
        response = requests.post(query.url, headers=query.headers)
        if response.status_code != 201:
            raise Exception("error with func auth: code: %s, message: %s" % (response.status_code, json.loads(response.text)["message"]))
        result = response.json()["token"]
    except Exception as e:
        print("error with func query_access_token: %s" % (repr(e)))
    finally:
        return result