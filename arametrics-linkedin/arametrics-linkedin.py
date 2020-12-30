#!/usr/bin/env python

# Author        : Aravinth Panch
# Description   : Request LinkedIn's API to retrieve JSON data of the given URL

import requests
import pprint

from config.config import *

with requests.session() as s:
    s.cookies['li_at'] = LI_ACCESS_TOKEN
    s.cookies["JSESSIONID"] = LI_CSRF_TOKEN
    s.headers = LI_REQUEST_HEADER
    s.headers["csrf-token"] = s.cookies["JSESSIONID"].strip('"')
    response = s.get(LI_REQUEST_URL)
    response_dict = response.json()
    pprint.pprint(response_dict)
