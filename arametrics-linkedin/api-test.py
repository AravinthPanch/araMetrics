#!/usr/bin/env python

# Author        : Aravinth Panch
# Description   : API Tester

import requests
import pprint
import csv
import json

from config.config import *

# urn:li:fs_miniProfile:ACoAAArvscgBnXp5J2T_ipLQXmXy73eyNWs9zcE
# urn:li:member:183480776

# profileUpdatesV2
LI_REQUEST_URL = 'https://www.linkedin.com/voyager/api/identity/profileUpdatesV2?count=5&includeLongTermHistory=true&moduleKey=member-shares%3Aphone&numComments=0&numLikes=0&profileUrn=urn%3Ali%3Afsd_profile%3AACoAAArvscgBnXp5J2T_ipLQXmXy73eyNWs9zcE&q=memberShareFeed'

# socialUpdateAnalyticsHeader
LI_REQUEST_URL = 'https://www.linkedin.com/voyager/api/identity/socialUpdateAnalyticsHeader/urn:li:activity:6749841001667465216'


# LI_REQUEST_URL = 'https://www.linkedin.com/voyager/api/identity/profiles/aravinthpanch/following?count=1&entityType=INFLUENCER&q=followedEntities'
# LI_REQUEST_URL = 'https://www.linkedin.com/voyager/api/identity/profiles/me/networkinfo?shouldIncludeFollowingCount=true'
# LI_REQUEST_URL = 'https://www.linkedin.com/voyager/api/identity/profiles/ACoAAANoAaQBWD4a3F1sZL97KZ659lr_0SGzbKo/posts'
# LI_REQUEST_URL = 'https://www.linkedin.com/voyager/api/feed/social/urn:li:activity:6749841001667465216'
# LI_REQUEST_URL = 'https://www.linkedin.com/voyager/api/feed/updates/urn:li:activity:6749841001667465216'

with requests.session() as session:
    session.cookies['li_at'] = LI_ACCESS_TOKEN
    session.cookies["JSESSIONID"] = LI_CSRF_TOKEN
    session.headers = LI_REQUEST_HEADER
    session.headers["csrf-token"] = session.cookies["JSESSIONID"].strip('"')
    response = session.get(LI_REQUEST_URL).json()
    print(json.dumps(response))
